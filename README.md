# PFSS
Power Facility Soh Streaming  (2023.04~2023.05)

## 개요
빅데이터 기술에 대한 이론을 공부하고 만약 전력설비의 데이터를 실시간으로 받아서 soh 상태를 시각적으로 확인하면 손쉽게 이상 징후를 파악할 수 있지 않을까라는 생각에 시작하게 되었습니다.
<br>
이때 생각한 데이터 파이프라인 아키텍처로 람다 아키텍처를 떠올렸고, 그 중 스트리밍 처리부분을 구현하고자 했습니다.

## 데이터 파이프라인
![image](https://github.com/mooncw/PFSS/assets/97713997/383b3ae8-9665-46b1-a78b-b6695fe0dbdd)

#### 데이터
ai허브에 있는 전력 설비 에너지 패턴 및 고장 분석 센서 데이터를 이용하고자 했습니다.
<br>
이 데이터는 설비별 1분 간격의 센서 데이터를 json 파일로 저장되어 있습니다.
<br>
데이터 파이프라인에서 데이터는 센서들로부터 n초 마다 데이터를 받고 있다고 가정하였습니다.
<br>
설비별 센서로부터 n초 마다 받기 위해서 비동기 프로그래밍으로 센서마다 데이터를 Kafka 서버에 전송하도록 했습니다.
<br>
이 때 비동기 프로그래밍에 사용한 것은 python의 asyncio 라이브러리입니다.
#### 분산환경
aws ec2를 이용하여 1개의 master 서버와 3개의 worker 서버들로 구성했습니다.
<br>
각 서버는 cpu 2코어, ram 8G, 볼륨 50G로 구성했습니다. (m5a.large)
<br>
각 서버는 authorized_keys를 이용해 서로 통신하도록 했습니다.
<br>
필요한 경우 port를 개방하여 외부 서버가 접근할 수 있도록 했습니다.
#### 메세지 브로커
Kafka를 사용하였고 tar를 다운로드하고 3개의 worker 서버들에 설치하여 3개의 클러스터로 구성했습니다.
<br>
Kafka에 2개의 토픽 'heat'와 'heat_pf'가 존재합니다.
'heat'는 가상의 센서가 프로듀서이고 Spark가 컨슈머입니다.
<br>
'heat_pf'는 spark가 프로듀서이고 Influxdb가 컨슈머입니다. 
<br>
Kafka를 중앙화함으로써 확장성을 가지도록 했습니다.
<br>
Kafka에서의 데이터의 보존 기간은 24시간으로 설정했습니다.
<br>
24시간으로 설정한 이유는 센서데이터는 DW로 보내지고, 이 후에 배치처리가 구현이 된다면 최대 24시간 마다의 배치처리를 할 것이라 예상이 되기에 24시간이상 가지고 있을 필요가 없다고 판단하였기 때문입니다.
#### 스트림 처리
Spark를 사용하였고 분산환경에 맞게 구성했습니다.
<br>
spark structured streaming 구조 즉, Spark Session을 사용했습니다.
<br>
효율적인 작업을 위해 클러스터 매니저는 YARN을 사용했습니다.
<br>
스트림 처리 과정은 2개의 쿼리를 사용합니다.
<br>
하나는 Kafka에서 받은 데이터를 HDFS DW로 보내는 쿼리입니다.
<br>
다른 하나는 Kafka에서 받은 데이터를 변환한 새로운 DataFrame을 다시 Kafka에 보내는 쿼리입니다.
<br>
여기서 변환 과정은 Kafka에서 받은 데이터를 DataFrame으로 가져와서 원하는 형태의 DataFrame으로 변환하고,
<br>
간단하게 만든 ml모델을 이용해 label을 predict하고 그 값과 함께 새로운 DataFrame을 만듭니다.
#### 스트림 처리 DB
시계열 데이터 db에 적합하고 전통적인 influxdb를 사용했습니다.
<br>
보존 기간은 Kafka에서와 같은 이유로 24시간으로 설정했습니다.
#### 실시간 뷰
grafana 사용했습니다.
<br>
대시보드는 5초마다 갱신되고 5개 센서의 pf 값과 pf 상태를 시각화하도록 구성했습니다.
<br>
<br>
![그라파나1](https://user-images.githubusercontent.com/97713997/236662390-c805eef6-a1d3-4099-a813-9a2fd5d78b45.png)
#### 데이터 웨어하우스
Spark warehouse로 hdfs를 사용했습니다.

## 파일설명
DataToDashboard.ipynb : 데이터를 대시보드에 보내기 위해 데이터가 Kafka에서 InfluxDB로 이동하는 코드
KtoStoK.ipynb : pyspark로 Kafka에 데이터를 받아 스트림 처리를 하고 다시 Kafka로 보내는 코드
dataTypeExample.md : 가상의 센서 데이터 예시
draft-datapipeline.md : 람다 아키텍처 파이프라인(그림)
kafka_pro2.py : 가상의 센서 데이터를 Kafka로 보내는 코드

## 개선사항
