---
categories:
- 优质工具
date: 2023-04-26 00:52:39.337742
id: scapy
tags:
- 优质工具
title: 【优质工具】Scapy 发包工具
url: posts/scapy
---

Python 的 [scapy](https://scapy.net/) 库是一个非常优秀的发包工具，可以灵活构造各种报文。

```python
import socket
import struct
from scapy.all import *
from scapy.layers.inet import *
from scapy.layers.inet6 import *

RS = '120.55.68.91'
TIMEOUT = 0.5
```

<!-- more -->

## IPv4 ICMP 报文

```python
pkt = IP(dst=RS)/ICMP()
pkt.show()
print(hexdump(pkt))
sr1(pkt, timeout=TIMEOUT)
```

```
###[ IP ]### 
  version   = 4
  ihl       = None
  tos       = 0x0
  len       = None
  id        = 1
  flags     = 
  frag      = 0
  ttl       = 64
  proto     = icmp
  chksum    = None
  src       = 192.168.1.112
  dst       = 120.55.68.91
  \options   \
###[ ICMP ]### 
     type      = echo-request
     code      = 0
     chksum    = None
     id        = 0x0
     seq       = 0x0
     unused    = ''

0000  45 00 00 1C 00 01 00 00 40 01 FC 35 C0 A8 01 70  E.......@..5...p
0010  78 37 44 5B 08 00 F7 FF 00 00 00 00              x7D[........
None
Begin emission:
Finished sending 1 packets.

Received 2 packets, got 1 answers, remaining 0 packets
```

## IPv4 UDP 报文

```python
pkt = IP(dst=RS)/UDP(sport=3000, dport=82)
pkt.show()
print(hexdump(pkt))
sr1(pkt, timeout=TIMEOUT)
```

```
###[ IP ]### 
  version   = 4
  ihl       = None
  tos       = 0x0
  len       = None
  id        = 1
  flags     = 
  frag      = 0
  ttl       = 64
  proto     = udp
  chksum    = None
  src       = 192.168.1.112
  dst       = 120.55.68.91
  \options   \
###[ UDP ]### 
     sport     = 3000
     dport     = 82
     len       = None
     chksum    = None

0000  45 00 00 1C 00 01 00 00 40 11 FC 25 C0 A8 01 70  E.......@..%...p
0010  78 37 44 5B 0B B8 00 52 00 08 75 29              x7D[...R..u)
None
Begin emission:
Finished sending 1 packets.

Received 9 packets, got 1 answers, remaining 0 packets
```

## 携带 Option 的 IPv4 UDP 报文

```python
opt = IPOption(option=0x1f, length=8, value=0)
pkt = IP(dst=RS, options=opt)/UDP(sport=3000, dport=82)
pkt.show()
print(hexdump(pkt))
sr1(pkt, timeout=TIMEOUT)
```

```
###[ IP ]### 
  version   = 4
  ihl       = None
  tos       = 0x0
  len       = None
  id        = 1
  flags     = 
  frag      = 0
  ttl       = 64
  proto     = udp
  chksum    = None
  src       = 192.168.1.112
  dst       = 120.55.68.91
  \options   \
   |###[ IP Option ]### 
   |  copy_flag = 0
   |  optclass  = control
   |  option    = 31
   |  length    = 8
   |  value     = 0
###[ UDP ]### 
     sport     = 3000
     dport     = 82
     len       = None
     chksum    = None

0000  46 00 00 20 00 01 00 00 40 11 DC 19 C0 A8 01 70  F.. ....@......p
0010  78 37 44 5B 1F 08 00 00 0B B8 00 52 00 08 75 29  x7D[.......R..u)
None
Begin emission:
Finished sending 1 packets.

Received 7 packets, got 0 answers, remaining 1 packets
```

## 携带 IPv6 Destination Extension Header 的 UDP 报文

```python
opt = HBHOptUnknown(otype=0x1f, optlen=6, optdata=0)
pkt = IPv6(dst=RSV6)/IPv6ExtHdrDestOpt(options=opt)/UDP(sport=3000, dport=82)
pkt.show2()
print(hexdump(pkt))
sr1(pkt, timeout=TIMEOUT)
```

```
###[ IPv6 ]### 
  version   = 6
  tc        = 0
  fl        = 0
  plen      = 16
  nh        = Destination Option Header
  hlim      = 64
  src       = ::
  dst       = fe02::2
###[ IPv6 Extension Header - Destination Options Header ]### 
     nh        = UDP
     len       = 0
     autopad   = On
     \options   \
      |###[ Scapy6 Unknown Option ]### 
      |  otype     = 31 [00: skip, 0: Don't change en-route]
      |  optlen    = 6
      |  optdata   = '\x01\x02\x00\x00'
###[ UDP ]### 
        sport     = 3000
        dport     = 82
        len       = 8
        chksum    = 0xf5cf
```
