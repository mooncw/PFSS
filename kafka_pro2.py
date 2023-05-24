from kafka import KafkaProducer
import os
import json
import asyncio
import time

# Kafka 브로커의 주소와 포트 설정
bootstrap_servers = 'spark-worker-01:9092,spark-worker-02:9092,spark-worker-03:9092'

# KafkaProducer 객체 생성
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode())

# nums 가져오기
def get_nums():
    files = os.listdir("C:/Users/mcw/pfss/pro")

    nums = []

    for file in files:
        num = file.split('_')[3].replace('.json','')
        nums += [num]
    return nums

# json 데이터 가져오기
def get_json_data(num):
    address = f"C:/Users/mcw/pfss/new/new_heat_soh_pf_{num}.json"

    with open(address, 'r') as f:

        json_data = json.load(f)
        return json_data

# n초 간격으로 json 데이터 전송
async def send_json_data(num, n):
    json_data = get_json_data(num)

    for i in json_data:
        i['timestamp'] = time.time()
        # print(i)
        producer.send('heat', i)
        await asyncio.sleep(n)

# nums 예시
nums = ['100', '101', '113', '114', '115']
# nums = get_nums()[:10]

# 비동기 json 데이터 전송하기
async def process_async():
    await asyncio.wait([
        send_json_data(num, 5) for num in nums
    ])

if __name__ == '__main__':
    asyncio.run(process_async())

# KafkaProducer 종료
    producer.close()