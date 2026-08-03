import json
from datetime import datetime, timedelta, timezone

def generate_schedule():
    # rotation.json 파일 읽기
    with open('rotation.json', 'r', encoding='utf-8') as f:
        rotation = json.load(f)

    # 오늘 첫 보스 시간인 2026-08-04 07:30:00 KST (= 2026-08-03 22:30:00 UTC)를 기준점으로 설정
    base_time = datetime(2026, 8, 3, 22, 30, 0, tzinfo=timezone.utc)
    
    schedule_list = []
    current_time = base_time
    interval = timedelta(hours=3, minutes=30)
    
    # 하루 동안 생성되는 월드 보스 개수(약 7개)만큼 생성
    for i in range(7):
        rot_item = rotation[i % len(rotation)]
        timestamp = int(current_time.timestamp())
        start_time_str = current_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        
        # rotation.json의 boss와 zones 데이터를 그대로 매핑
        item = {
            "id": timestamp,
            "timestamp": timestamp,
            "boss": rot_item["boss"],
            "type": "world_boss",
            "startTime": start_time_str,
            "zone": rot_item["zones"]
        }
        schedule_list.append(item)
        current_time += interval

    # 생성된 일정을 worldboss.json에 저장
    with open('worldboss.json', 'w', encoding='utf-8') as f:
        json.dump(schedule_list, f, ensure_ascii=False, indent=2)

    print("worldboss.json 생성 완료!")

if __name__ == "__main__":
    generate_schedule()
