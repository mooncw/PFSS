# PFSS
Power Facility Soh Streaming  (2023.03.31~)

## 개요
빅데이터 기술에 대한 이론을 공부하고 만약 전력설비의 데이터를 실시간으로 받아서 soh 상태를 시각적으로 확인하면 손쉽게 이상 징후를 파악할 수 있지 않을까라는 생각에 시작하게 되었습니다.

## 데이터파이프라인(초안)
![draft](https://user-images.githubusercontent.com/97713997/229030147-74484849-311f-459c-bb73-ce670a166a52.PNG)

1. 데이터 -> ai허브에 있는 전력 설비 에너지 패턴 및 고장 분석 센서 데이터를 이용하고자 했습니다.

이 데이터는 설비별 1분 간격의 센서 데이터를 json 파일로 저장되어 있습니다. 
2. 메세지 브로커
3. 스트림 처리
4. 스트림 처리 DB
5. 실시간 뷰
6. 배치 처리 DB
7. 배치 처리
8. 데이터 마트
9. 배치 뷰
