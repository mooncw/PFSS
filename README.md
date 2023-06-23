# PFSS
Power Facility Soh Streaming  (2023.04~2023.05)

## 개요
* 빅데이터 기술에 대한 이론을 공부하고 만약 전력설비의 데이터를 실시간으로 받아서 soh 상태를 시각적으로 확인하면 손쉽게 이상 징후를 파악할 수 있지 않을까라는 생각에 시작하게 되었습니다.
* 이때 생각한 데이터 파이프라인 아키텍처로 람다 아키텍처를 떠올렸고, 그 중 스트리밍 처리부분을 구현하고자 했습니다.

## 사용 기술 스택
<div align="left">
	<img src="https://img.shields.io/badge/python-3776AB?style=flat&logo=python&logoColor=white" />
	<img src="https://img.shields.io/badge/amazonec2-FF9900?style=flat&logo=amazonec2&logoColor=white" />
	<img src="https://img.shields.io/badge/ubuntu-E95420?style=flat&logo=ubuntu&logoColor=white" />
  <img src="https://img.shields.io/badge/jupyter-F37626?style=flat&logo=jupyter&logoColor=white" />
  <img src="https://img.shields.io/badge/apachekafka-231F20?style=flat&logo=apachekafka&logoColor=white" />
  <img src="https://img.shields.io/badge/apachespark-E25A1C?style=flat&logo=apachespark&logoColor=white" />
  <img src="https://img.shields.io/badge/apachehadoop-66CCFF?style=flat&logo=apachehadoop&logoColor=white" />
  <img src="https://img.shields.io/badge/influxdb-22ADF6?style=flat&logo=influxdb&logoColor=white" />
  <img src="https://img.shields.io/badge/grafana-F46800?style=flat&logo=grafana&logoColor=white" />
</div>

## 데이터 파이프라인
![image](https://github.com/mooncw/PFSS/assets/97713997/383b3ae8-9665-46b1-a78b-b6695fe0dbdd)

### 데이터
* ai허브에 있는 전력 설비 에너지 패턴 및 고장 분석 센서 데이터를 이용하고자 했습니다.
* 이 데이터는 설비별 1분 간격의 센서 데이터를 json 파일로 저장되어 있습니다.
* 데이터 파이프라인에서 데이터는 센서들로부터 5초 마다 데이터를 받고 있다고 가정하였습니다.
* 설비별 센서로부터 5초 마다 받기 위해서 비동기 프로그래밍으로 센서마다 데이터를 Kafka 서버에 전송하도록 했습니다.
* 이 때 비동기 프로그래밍에 사용한 것은 python의 asyncio 라이브러리입니다.

### 분산환경
* aws ec2를 이용하여 1개의 master 서버와 3개의 worker 서버들로 구성했습니다.
* 각 서버는 cpu 2코어, ram 8G, 볼륨 50G로 구성했습니다. (m5a.large)
* 각 서버는 authorized_keys를 이용해 서로 통신하도록 했습니다.
* 필요한 경우 port를 개방하여 외부 서버가 접근할 수 있도록 했습니다.

### 메세지 브로커
* Kafka를 사용하였고 3개의 worker 서버들에 설치하여 3개의 클러스터로 구성했습니다.
* Kafka에 2개의 토픽 'heat'와 'heat_pf'가 존재합니다.
* 'heat'는 가상의 센서가 프로듀서이고 Spark가 컨슈머입니다.
* 'heat_pf'는 spark가 프로듀서이고 Influxdb가 컨슈머입니다. 
* Kafka를 중앙화함으로써 확장성을 가지도록 했습니다.
* Kafka에서의 데이터의 보존 기간은 24시간으로 설정했습니다.
* 24시간으로 설정한 이유는 센서 데이터는 이 후에 DW로 보내지고 배치처리 파이프라인이 구현이 된다면 최대 24시간 마다의 배치처리를 할 것이라 예상이 되기에 24시간이상 가지고 있을 필요가 없다고 판단하였기 때문입니다.

### 스트림 처리
* Spark를 사용하였고 분산환경에 맞게 구성했습니다.
* spark structured streaming 구조 즉, Spark Session을 사용했습니다.
* 효율적인 작업을 위해 클러스터 매니저는 YARN을 사용했습니다.
* 스트림 처리 과정은 2개의 쿼리 'writeDW'와 'pf_pred_to_kafka'를 사용합니다.
* 'writeDW'는 Kafka에서 받은 데이터를 분산 스토리지인 HDFS로 보내는 쿼리입니다.
* 'pf_pred_to_kafka'는 Kafka에서 받은 데이터를 변환한 새로운 DataFrame을 다시 Kafka에 보내는 쿼리입니다.
* 여기서 변환 과정은 Kafka에서 받은 데이터를 DataFrame으로 가져와서 원하는 형태의 DataFrame으로 변환하고,
* 간단하게 만든 ml모델을 이용해 label을 predict하고 그 값과 함께 새로운 DataFrame을 만듭니다.

### 스트림 처리 DB
* 시계열 데이터 DB에 적합하고 전통적인 influxDB를 사용했습니다.
* 보존 기간은 Kafka에서와 같은 이유로 24시간으로 설정했습니다.

### 실시간 뷰
* grafana 사용했습니다.
* 대시보드는 5초마다 갱신되고 5개 센서의 pf 값과 pf 상태를 시각화하도록 구성했습니다.

<img src="https://github.com/mooncw/PFSS/assets/97713997/0d8d1317-bb10-4200-a485-3553870b9f6e" />

### 분산 스토리지
* 분산 스토리지를 구성한 이유는 이 후 Hadoop으로 배치 처리하게 될 때 Hbase를 사용한다면 필요할 것이라 생각했기 때문입니다.
* Hadoop의 hdfs를 사용했습니다.
* 아래 이미지와 같이 hdfs 위에 보통 데이터 하나씩 저장이 됩니다.

<img src="https://github.com/mooncw/PFSS/assets/97713997/1448a7f2-a145-45fa-a692-3ba4e41470eb" />

## 결과
![5sensor](https://github.com/mooncw/PFSS/assets/97713997/c294e7f9-10a3-4244-a5db-3ce23c5c066e)
<br>
* 5초에 약 3000B 크기의 데이터를 스트림 처리를 합니다.(가상 센서 1개당 약 600B)
* 가지고 있는 74개의 가상 센서를 모두 돌려본 결과 메시지 누락없이 처리는 하지만 데이터 처리에서 큰 지연이 발생합니다.

## 파일설명
**DataToDashboard.ipynb** : 데이터를 대시보드에 보내기 위해 데이터가 Kafka에서 InfluxDB로 이동하는 코드
<br>
**KtoStoK.ipynb** : pyspark로 Kafka에 데이터를 받아 스트림 처리를 하고 다시 Kafka로 보내는 코드
<br>
**dataTypeExample.md** : 가상의 센서 데이터 예시
<br>
**draft-datapipeline.md** : 람다 아키텍처 파이프라인(그림)
<br>
**kafka_pro2.py** : 가상의 센서 데이터를 Kafka로 보내는 코드

## 만족스러웠던 점
* Spark가 제 때 처리할 수 있는 정도의 데이터 양이라면 데이터가 잘 흘러간다는 점
* 데이터를 받은 ml모델이 예측한 결과를 같이 볼 수 있다는 점

## 개선사항
* 데이터가 이런 식으로 흐르게 했다라는 정도라 미흡한 부분이 많다고 생각이 됩니다.
* 제가 이 프로젝트를 진행하면서 생각하는 미흡한 부분이란 **고장 테스트**, **효율적인 분산 스토리지로의 데이터 저장**, **메타데이터 저장소**, **많은 데이터의 처리**, **늦게 도착한 데이터 처리** 등입니다.
	- **고장 테스트**는 하나의 서버를 죽여서 어떻게 되는지 보면 될 것이라 생각합니다.
	- **효율적인 분산 스토리지로의 데이터 저장**은 데이터 하나씩 저장하지 말고 여러개를 합쳐서 저장하면 좋을 것이라 생각합니다.
	- **메타데이터 저장소**는 MySQL같은 RDB 저장소를 사용하면 될 것이라 생각합니다.
	- **많은 데이터의 처리**는 간단한 방법으로 서버 스펙을 더 올리면 될 것이라 생각합니다.
	- **늦게 도착한 데이터**는 이벤트 시간이 프로세싱 시간과 5초이상 차이가 나면 버리는 코드를 직접 짜거나 워터마크를 이용하면 될 것이라 생각합니다.
