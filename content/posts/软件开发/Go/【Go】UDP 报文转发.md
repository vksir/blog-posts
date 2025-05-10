---
categories:
- 软件开发
date: 2022-07-10 23:15:16.760081
id: go-udp-redirect
tags:
- go
- 软件开发
title: 【Go】UDP 报文转发
url: posts/go-udp-redirect
---

【背景】

- 如 Wireguard 等工作在三层的 VPN，不会主动转发 UDP 广播报文，但能转发指定 IP 的 UDP 报文。

- 现有一程序，仅在 PC 主网卡（192.168.1.106）上发送从 14001 端口到 14001 端口的 UDP 广播报文。这种报文一是不会使用虚拟网卡（10.0.0.3）发送，二是就算使用虚拟网卡发送，该种虚拟网卡（Wireguard）也无法发送 UDP 广播报文。
- 想将报文捕获，使用虚拟网卡（10.0.0.3）指定目的 IP （10.0.0.2）进行转发。

【语言】Go

<!-- more -->

---

## 开发

主要用到 Google 的三个库：

- github.com/google/gopacket
- github.com/google/gopacket/layers
- github.com/google/gopacket/pcap

进行捕获和解析报文。其中，捕获报文在 Windows 上使用 ncap（Wireshark 底层也使用这个），在 Linux 上使用 libpcap（tcpdump 底层使用这个）。

代码不多，如下：

```go
package main

import (
	"context"
	"errors"
	"flag"
	"fmt"
	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
	"github.com/google/gopacket/pcap"
	"log"
	"net"
	"os"
	"os/signal"
	"strings"
)

var packetChan chan *Packet

type UDP struct {
	SrcIP   net.IP
	DstIP   net.IP
	SrcPort int
	DstPort int
	Content []byte
}

func (u *UDP) Send() error {
	laddr := &net.UDPAddr{IP: u.SrcIP, Port: u.SrcPort}
	raddr := &net.UDPAddr{IP: u.DstIP, Port: u.DstPort}

	if conn, err := net.DialUDP("udp", laddr, raddr); err != nil {
		return err
	} else {
		defer conn.Close()
		if _, err := conn.Write(u.Content); err != nil {
			return err
		} else {
			return nil
		}
	}
}

type Packet struct {
	Ethernet layers.Ethernet
	IP4      layers.IPv4
	TCP      layers.TCP
	UDP      layers.UDP
	Payload  gopacket.Payload

	Decoded []gopacket.LayerType
}

// NewPacket 解析报文
func NewPacket(packetData []byte) (*Packet, error) {
	var p Packet
	parser := gopacket.NewDecodingLayerParser(layers.LayerTypeEthernet, &p.Ethernet, &p.IP4, &p.TCP, &p.UDP, &p.Payload)
	if err := parser.DecodeLayers(packetData, &p.Decoded); err != nil {
		return nil, err
	} else {
		return &p, nil
	}
}

// String 显示报文信息
// 用于打印。
func (p *Packet) String() string {
	var info []string
	for _, layerType := range p.Decoded {
		switch layerType {
		case layers.LayerTypeEthernet:
			info = append(info,
				p.Ethernet.SrcMAC.String()+" > "+p.Ethernet.DstMAC.String(),
				"Ethernet Type: "+p.Ethernet.EthernetType.String(),
			)
		case layers.LayerTypeIPv4:
			info = append(info,
				p.IP4.SrcIP.String()+" > "+p.IP4.DstIP.String(),
				"Protocol: "+p.IP4.Protocol.String(),
			)
		case layers.LayerTypeTCP:
			info = append(info,
				p.TCP.SrcPort.String()+" > "+p.TCP.DstPort.String(),
			)
		case layers.LayerTypeUDP:
			info = append(info,
				p.UDP.SrcPort.String()+" > "+p.UDP.DstPort.String(),
			)
		case gopacket.LayerTypePayload:
			info = append(info,
				"Content: "+string(p.Payload.LayerContents()),
			)
		}
	}
	return strings.Join(info, " | ")
}

// findDevByIp 通过设备 IP 查找设备
// 在 Linux 中，设备名很容易获取，如 “eth0”； 但在 Windows 中则较难, 因而有此函数。
func findDevByIp(ip net.IP) (*pcap.Interface, error) {
	devices, err := pcap.FindAllDevs()
	if err != nil {
		return nil, err
	}
	for _, device := range devices {
		for _, address := range device.Addresses {
			if address.IP.Equal(ip) {
				return &device, nil
			}
		}
	}
	return nil, errors.New("find device failed by ip")
}

// capture 捕获报文，解析并放入 chan
func capture(dev *pcap.Interface, filter string) {
	if h, err := pcap.OpenLive(dev.Name, 4096, true, -1); err != nil {
		log.Panicln(err)
	} else if err := h.SetBPFFilter(filter); err != nil {
		log.Panicln(err)
	} else {
		defer h.Close()
		for {
			if packetData, _, err := h.ReadPacketData(); err != nil {
				log.Panicln(err)
			} else if p, err := NewPacket(packetData); err != nil {
				log.Panicln(err)
			} else {
				fmt.Println(p.String())
				packetChan <- p
			}
		}
	}
}

// redirect 转发报文
// 指定源 IP 和目的 IP，端口不变。
func redirect(ctx context.Context, srcIP, dstIP net.IP) {
	for {
		select {
		case <-ctx.Done():
			return
		case p := <-packetChan:
			u := UDP{
				SrcIP:   srcIP,
				DstIP:   dstIP,
				SrcPort: int(p.UDP.SrcPort),
				DstPort: int(p.UDP.DstPort),
				Content: p.Payload.LayerContents(),
			}
			if err := u.Send(); err != nil {
				log.Printf("send p failed: %+v", u)
			}
		}
	}
}

func Run(ctx context.Context, devIp, filter, srcIp, dstIp string) {
	dev, err := findDevByIp(net.ParseIP(devIp))
	if err != nil {
		log.Panicf("find device by ip failed: ip=%s, err=%s", devIp, err)
	}

	packetChan = make(chan *Packet, 64)
	go capture(dev, filter)
	redirect(ctx, net.ParseIP(srcIp), net.ParseIP(dstIp))
}

func main() {
	var (
		devIP  = flag.String("d", "192.168.1.106", "Device IP.")
		filter = flag.String("f", "port 14001", "BPF filter expression.")
		srcIP  = flag.String("src-ip", "10.0.1.3", "Redirect src IP.")
		dstIP  = flag.String("dst-ip", "10.0.1.2", "Redirect dst IP.")
	)
	flag.Parse()

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()
	Run(ctx, *devIP, *filter, *srcIP, *dstIP)
}
```

编译后使用命令如下：

```
nettool -d 192.168.1.106 -f "port 14001" -src-ip 10.0.0.3 -dst-ip 10.0.0.2
```

## 验证

### 使用 Python 模拟发送 UDP 广播报文

```python
import socket
from time import sleep


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        print('begin sending broadcast')
        sock.sendto(b'hello world', ("255.255.255.255", 14001))
        print('end sending broadcast')
        sleep(1)
    sock.close()


if __name__ == '__main__':
    main()
```

### 开启 Wireguard

本端虚拟网卡：

```shell
ipconfig /all
```

![image-20220710230447035](https://static.vksir.zone/img/image-20220710230447035.png)

对端虚拟网卡：

```shell
ip a
```

![image-20220710230532707](https://static.vksir.zone/img/image-20220710230532707.png)

### 对端 tcpdump 抓包

```shell
tcpdump -i mine -nne port 14001
```

### 本端启动 UDP 报文转发

查看本端主网卡（即 UDP 报文发出的网卡）：

```shell
ipconfig /all
```

![image-20220710231005215](https://static.vksir.zone/img/image-20220710231005215.png)

该网卡 IP 为 192.168.1.106，报文转发命令如下：

```
nettool -d 192.168.1.106 -f "port 14001" -src-ip 10.0.0.3 -dst-ip 10.0.0.2
```

### 查看对端抓包结果

![image-20220710231228351](https://static.vksir.zone/img/image-20220710231228351.png)

成功转发报文！
