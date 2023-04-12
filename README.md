# PFSS
Power Facility Soh Streaming  (2023.03.31~)

## 개요
빅데이터 기술에 대한 이론을 공부하고 만약 전력설비의 데이터를 실시간으로 받아서 soh 상태를 시각적으로 확인하면 손쉽게 이상 징후를 파악할 수 있지 않을까라는 생각에 시작하게 되었습니다.

## 데이터 파이프라인(초안)
![draft](https://user-images.githubusercontent.com/97713997/229030147-74484849-311f-459c-bb73-ce670a166a52.PNG)

#### 데이터
ai허브에 있는 전력 설비 에너지 패턴 및 고장 분석 센서 데이터를 이용하고자 했습니다.
<br>
이 데이터는 설비별 1분 간격의 센서 데이터를 json 파일로 저장되어 있습니다.
<br>
데이터 파이프라인에서 데이터는 설비별 센서로부터 n초 마다 데이터를 받고 있다고 가정하였습니다.
<br>
설비별 센서로부터 n초 마다 받기 위해서 비동기 프로그래밍으로 센서마다 데이터를 원격 서버에 전송하도록 하였습니다.
<br>
이 때 비동기 프로그래밍에 사용한 것은 python의 asyncio 라이브러리입니다.
#### 분산환경
aws ec2를 이용하여 1개의 master와 3개의 worker들로 구성하였습니다.
#### 메세지 브로커
#### 스트림 처리
#### 스트림 처리 DB
#### 실시간 뷰
#### 배치 처리 DB
#### 배치 처리
#### 데이터 마트
#### 배치 뷰
