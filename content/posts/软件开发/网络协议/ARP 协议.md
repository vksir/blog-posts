---
categories:
- 软件开发
date: 2023-03-04 03:29:19.482388
draft: false
id: arp
tags:
- 网络协议
- 软件开发
title: ARP 协议
url: posts/arp
---

## ARP 格式

![image-20230304013902868](https://static.vksir.zone/img/image-20230304013902868.png)

```c
struct arphdr
  {
    unsigned short int ar_hrd;		/* Format of hardware address.  */
    unsigned short int ar_pro;		/* Format of protocol address.  */
    unsigned char ar_hln;		/* Length of hardware address.  */
    unsigned char ar_pln;		/* Length of protocol address.  */
    unsigned short int ar_op;		/* ARP opcode (command).  */
  };

struct	ether_arp {
	struct	arphdr ea_hdr;		/* fixed-size header */
	uint8_t arp_sha[ETH_ALEN];	/* sender hardware address */
	uint8_t arp_spa[4];		/* sender protocol address */
	uint8_t arp_tha[ETH_ALEN];	/* target hardware address */
	uint8_t arp_tpa[4];		/* target protocol address */
};
```

<!-- more -->

## Ethernet II 格式

![image-20230304014125049](https://static.vksir.zone/img/image-20230304014125049.png)

```c
typedef unsigned short __u16;
typedef __u16 __bitwise __be16;

struct ethhdr {
   unsigned char  h_dest[ETH_ALEN];  /* destination eth addr    */
   unsigned char  h_source[ETH_ALEN];    /* source ether addr   */
   __be16    h_proto;      /* packet type ID field    */
} __attribute__((packed));
```

## C 收发 ARP 报文

### 发

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <linux/if_ether.h>
#include <netinet/if_ether.h>
#include <linux/if_packet.h>
#include <net/if.h>
#include <string.h>
#include <net/if_arp.h>
#include <arpa/inet.h>
#include <unistd.h>


int main() {
    // Create raw socket
    int socket_fd = socket(AF_PACKET, SOCK_RAW, 0);
    if (socket_fd < 0) {
        perror("create socket failed");
        exit(1);
    }

    // Bind interface and get local mac
    struct sockaddr_ll local;
    local.sll_family = AF_PACKET;
    local.sll_ifindex = (int) if_nametoindex("eth0");
    socklen_t local_len = sizeof local;
    if (bind(socket_fd, (struct sockaddr *) &local, local_len) < 0) {
        perror("bind dev failed");
        exit(1);
    }
    getsockname(socket_fd, (struct sockaddr *) &local, &local_len);

    // Create packet
    unsigned char buf[256];
    struct ethhdr *eh = (struct ethhdr *) buf;
    struct ether_arp *arp = (struct ether_arp *) (eh + 1);
    size_t size = (unsigned char *) (struct ether_arp *) (arp + 1) - buf;

    // Ethernet II header
    memset(eh->h_dest, 255, ETH_ALEN);
    memcpy(eh->h_source, local.sll_addr, ETH_ALEN);
    eh->h_proto = htons(ETH_P_ARP);

    // Arp header
    arp->ea_hdr.ar_hrd = htons(ARPHRD_ETHER);
    arp->ea_hdr.ar_pro = htons(ETH_P_IP);
    arp->ea_hdr.ar_hln = ETH_ALEN;
    arp->ea_hdr.ar_pln = 4;
    arp->ea_hdr.ar_op = htons(ARPOP_REQUEST);

    // Sender addr
    memcpy(arp->arp_sha, local.sll_addr, ETH_ALEN);
    struct in_addr src_ip;
    inet_aton("172.22.211.129", &src_ip);
    memcpy(arp->arp_spa, &src_ip.s_addr, 4);

    // Target addr
    memset(arp->arp_tha, 255, ETH_ALEN);
    struct in_addr dst_ip;
    inet_aton("172.22.208.1", &dst_ip);
    memcpy(arp->arp_tpa, &dst_ip.s_addr, 4);

    while (1) {
        if (send(socket_fd, buf, size, 0) < 0) {
            perror("send arp failed");
            exit(1);
        }
        printf("send arp success\n");
        sleep(1);
    }
}
```

存在 `char *` 和 `struct` 的相互转化，因结构体个变量地址连续且排列顺序固定，所以可以这么做。——如此编程精巧但易出错，只能说不愧是 C！

### 收

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <linux/if_ether.h>
#include <netinet/if_ether.h>
#include <net/if_arp.h>
#include <arpa/inet.h>


void print_mac(unsigned char *mac) {
    for (int i = 0; i < ETH_ALEN - 1; ++i) {
        printf("%02X:", mac[i]);
    }
    printf("%02X", mac[ETH_ALEN - 1]);
}

int main() {
    // Create raw socket
    int socket_fd = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ARP));
    if (socket_fd < 0) {
        perror("create socket failed");
        exit(1);
    }

    unsigned char buf[4096];
    while (1) {
        if (recv(socket_fd, &buf, sizeof buf, 0) < 0) {
            perror("recv arp failed");
            exit(1);
        }
        struct ethhdr *eh = (struct ethhdr *) buf;
        struct ether_arp *arp = (struct ether_arp *) (eh + 1);
        printf(arp->ea_hdr.ar_op == htons(ARPOP_REQUEST) ? "Request" : "Reply");
        printf(" from %s [", inet_ntoa(*(struct in_addr *) arp->arp_spa));
        print_mac(arp->arp_sha);
        printf("] to %s [", inet_ntoa(*(struct in_addr *) arp->arp_tpa));
        print_mac(arp->arp_tha);
        printf("]\n");
    }
}
```

## Python 实现收发 ARP 报文

### 发

```python
import socket
import struct
import time

s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, 0)
s.bind(('eth0', socket.SOCK_RAW))
local_mac = s.getsockname()[4]

dst_mac_addr = b'\xff\xff\xff\xff\xff\xff'
src_mac_addr = local_mac
ethernet_type = 0x806
ethernet_header = struct.pack('!6s6sH', dst_mac_addr, src_mac_addr, ethernet_type)

hardware_type = 1
protocol_type = 0x800
hardware_addr_len = 6
protocol_addr_len = 4
op = 1
sender_hardware_addr = local_mac
sender_protocol_addr = socket.inet_aton('172.22.211.129')
target_hardware_addr = b'\xff\xff\xff\xff\xff\xff'
target_protocol_addr = socket.inet_aton('172.22.208.1')
arp_header = struct.pack('!HHBBH6s4s6s4s', hardware_type, protocol_type, hardware_addr_len, protocol_addr_len, op,
                         sender_hardware_addr, sender_protocol_addr, target_hardware_addr, target_protocol_addr)

packet = ethernet_header + arp_header
while True:
    if s.send(packet) < 0:
        print('send arp failed')
        exit(1)
    print('send arp success')
    time.sleep(1)
```

Python 在 `struct.pack` 时附带转换网络字节序的功能，因而无需对原始变量进行 `htons` 处理。

虽然 Python 写出来的代码更简洁，但单阅读上讲，并不会比 C 代码易读，因 `struct.pack` 太黑盒。

### 收

```python
import socket
import struct


def format_mac(mac_chars):
    mac_str_lst = []
    for c in mac_chars:
        mac_str_lst.append('%02X' % int(c))
    return ':'.join(mac_str_lst)


s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x806))
while True:
    recv = s.recv(4096)
    res = struct.unpack('HHBBH6s4s6s4s', recv[14:42])
    op = 'Request' if res[4] == socket.htons(1) else 'Reply'
    src_mac = format_mac(res[-4])
    src_ip = socket.inet_ntoa(res[-3])
    dst_mac = format_mac(res[-2])
    dst_ip = socket.inet_ntoa(res[-1])
    print(f'{op} from {src_ip} [{src_mac}] to {dst_ip} [{dst_mac}]')
```

---

参考文档：

- [Address Resolution Protocol - Wikipedia](https://en.wikipedia.org/wiki/Address_Resolution_Protocol)
- [Ethernet frame - Wikipedia](https://en.wikipedia.org/wiki/Ethernet_frame)
