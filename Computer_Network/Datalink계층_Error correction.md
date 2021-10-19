# Error correction
## ARQ 방식
### 오류 제어(Error Control)
- 불리계층의 오류(BER) 문제를 해결하여 error free(=> BER=0)를 보장(BER=0이면 오류 제어 기능은 필요 없음)
- 오류 검출과 오류 정정 과정으로 수행
- 오류 검출과 CRC(Cyclic Redundancy Check) : 프레임 단위로 이루어지고 프레임 트레일러의 CRC 필드를 사용
>- 순환부호(cylic code)의 생성 다항식을 사용하여 CRC 데이터 생성
- 오류 정정과 재전송(retransmission) : 프레임 오류가 검출되면 전송부에 재전송 요청하여 오류 정정
>- 물리계층의 오류정정 부호(채널 부호)를 FEC(Forward Error Correction)이라 부른다. -> retransmission와 Forward는 서로 반대
### 오류 정정을 위한 재전송 방식
- 정지-대기 ARQ 방식
- go-back-N ARQ 방식
- selective repeat ARQ 방식
#### 정지-대기 ARQ 방식
1. stop : 전송단은 Data frame을 전송하고 Frame 전송을 멈추고
2. 전송 buffer : 재선송 경우를 위해 전송한 frame을 buffer에 저장하고
3. timer : ACK 또는 NAK frame을 수신할 때까지 timer를 동작시키고
4. ACK 수신 : 다음 Data frame을 전송
5. 다음의 경우 이전 Data frame을 재전송
>1. 수신단으로부터 NAK 수신
>2. timer의 time-out(RTT/RTD) 동안 수신단으로부터 ACK frame을 수신하지 못할 경우

