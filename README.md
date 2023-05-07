# PFSS
Power Facility Soh Streaming  (2023.03.31~2023.05.03)

## 개요
빅데이터 기술에 대한 이론을 공부하고 만약 전력설비의 데이터를 실시간으로 받아서 soh 상태를 시각적으로 확인하면 손쉽게 이상 징후를 파악할 수 있지 않을까라는 생각에 시작하게 되었습니다.
<br>
이때 생각한 데이터 파이프라인 아키텍처로 람다 아키텍처를 떠올렸고, 일단 스트리밍 처리부분을 구현하고자 했습니다.

## 데이터 파이프라인(초안)
![draft](https://user-images.githubusercontent.com/97713997/229030147-74484849-311f-459c-bb73-ce670a166a52.PNG)

#### 데이터
ai허브에 있는 전력 설비 에너지 패턴 및 고장 분석 센서 데이터를 이용하고자 했습니다.
<br>
이 데이터는 설비별 1분 간격의 센서 데이터를 json 파일로 저장되어 있습니다.
<br>
데이터 파이프라인에서 데이터는 설비별 센서로부터 n초 마다 데이터를 받고 있다고 가정하였니다.
<br>
설비별 센서로부터 n초 마다 받기 위해서 비동기 프로그래밍으로 센서마다 데이터를 Kafka 서버에 전송하도록 했습니다.
<br>
이 때 비동기 프로그래밍에 사용한 것은 python의 asyncio 라이브러리입니다.
<br>
여기서 통신은 socket 통신입니다.
#### 분산환경
aws ec2를 이용하여 1개의 master 서버와 3개의 worker 서버들로 구성했습니다.
<br>
각 서버는 cpu 2코어, ram 8G, 볼 50G로 구성했습니다. (m5a.large)
<br>
각 서버는 authorized_keys를 이용해 서로 통신하도록 했습니다.
<br>
필요한 경우 port를 개방하여 외부 서버가 접근할 수 있도록 했습니다.
#### 메세지 브로커
Kafka를 사용하였고 tar를 다운로드하고 3개의 worker 서버들에 설치하여 3개의 클러스터로 구성했습니다.
<br>
먼저 python으로 구현한 가상의 센서들에서 Kafka로 데이터를 보내면 Kafka에서 Spark로 데이터를 보내고 Spark에서 스트림 처리를 하고난 후 데이터를 다시 Kafka로 보내도록 구성했습니다.
<br>
확장성을 위해 이런 구성을 했습니다.
<br>
Kafka에서의 데이터의 보존 기간은 24시간으로 설정했습니다.
<br>
24시간으로 설정한 이유는 센서데이터는 DW로 보내지고, 이 후에 구 예정이였던 최대 24시간마다의 배치처리를 생각하고있었기에 24시간이상 가지고 있을 필요가 없다고 판단하였기 때문입니다.
#### 스트림 처리
Spark를 사용하였고 분산환경에 맞게 구성했습니다.
<br>
spark structured streaming 구조를 사용하였습니다.
<br>
스트림 처리 과정은 Kafka에서 받은 데이터를 DataFrame로 가져와서 원하는 형태의 DataFrame으로 변환하고,
<br>
간단하게 만든 ml모델을 이용해 label을 predict하고 그 값과 함께 새로운 DataFrame을 만들어서 다시 Kafka로 데이터를 보냅니다.
<br>
여기서 모델이 predict하는 쿼리와 Kafka로 보내는 쿼리가 있습니다.
#### 스트림 처리 DB
시계열 데이터 db에 적합하고 전통적인 influxdb를 사용했습니다.
<br>
보존 기간은 Kafka에서와 같은 이유로 24시간으로 설정했습니다.
#### 실시간 뷰
grafana 사용했습니다.
<br>
대시보드는 5초마다 갱신되고 각 센서의 pf 값과 pf 상태를 시각화하도록 구성했습니다.
<br>
<br>
![그라파나1](https://user-images.githubusercontent.com/97713997/236662390-c805eef6-a1d3-4099-a813-9a2fd5d78b45.png)
#### 배치 처리 DB(DW)
저장하기 쉬운 spark warehouse로 hdfs 사용했습니다.
<br>
이 후에 배치 처리를 구현한다면 Hbase를 사용할 예정입니다.
#### 배치 처리
미구현
<br>
이 후에 배치 처리를 구현한다면 Hadoop을 사용할 예정입니다.
#### 데이터 마트
미구현
#### 배치 뷰
미구현
#### 워크플로
미구현
