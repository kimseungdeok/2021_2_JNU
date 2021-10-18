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


