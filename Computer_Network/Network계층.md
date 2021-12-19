# 네트워크 계층
## 패킷 교환 네트워크(packet switching network)
- 사용자 호스트와 서버 간 종단-대-종단(end-to-end)으로 발신과 착신 IP주소를 사용하여 패킷을 전달
- 종단-대-종단
- 패킷 전달
## 내트워크 계층 기능
- 어드레싱(addressing) : IPv4, IPv6 프로토콜
- 패키징(packaging) : 패킷(packet)
- 라우팅(routing) : 라우터에서 라우팅 알고리즘
- 패킷의 분할 및 조립 : MTU 크기에 맞추어 패킷을 분할하고 조립
## 네트워크 계층 프로토콜
### IPv4 프로토콜
- ARP(Address Resolution Protocol, 주소 해석 프로토콜) : 호스트와 서버의 IP 주소에 대한 데이터링크 계층의 MAC 주소를 찾기 위해 사용 
- ICMP(Internet Control Message Protocol) : IP 패킷의 전달 과정에서 오류나 상태를 리포트하고 진단을 위해 사용
- IGMP(Intetnet Group Management Protocol) : IP 멀티캐스트 그룹을 관리하기 위해 사용
### IPv6 프로토콜
- ICMPv6(Internet Control Message Protocol version 6) : ICMP의 version 6
- NDP(Neighbor Discovery Protocol) : 로컬 네트워크 내 이웃 노드들의 탐색 등을 수행하는 프로토콜
- MLD(Multicast Listener Discovery) : 멀티캐스트 리스너 그룹을 관리하는 프로토콜
### 인터넷 프로토콜(IP, Internet Protocol)
- 인터넷을 통해 사용자 호스트와 서버간 발신, 착신 IP 주소에 따라 데이터그램 혹은 패킷을 전달하는 통신 프로토콜(최근에는 패킷보다는 데이터그램을 더 많이 사용)
- 인터넷으로 데이터그램을 전달하기 위해 호스트와 서버의 주소지정, 패킷의 분할 및 조립, 라우팅 기능을 수행
