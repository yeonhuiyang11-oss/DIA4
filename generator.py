import json
from datetime import datetime, timedelta, timezone

def generate_schedule():
    with open('rotation.json', 'r', encoding='utf-8') as f:
        rotation = json.load(f)

    # 2026-08-01 14:30:00 UTC 기준점
    base_time = datetime(2026, 8, 1, 14, 30, 0, tzinfo=timezone.utc)
    
    schedule_list = []
    current_time = base_time
    interval = timedelta(hours=3, minutes=30)
    
    for i in range(100):
        rot_item = rotation[i % len(rotation)]
        timestamp = int(current_time.timestamp())
        start_time_str = current_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        
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

    with open('worldboss.json', 'w', encoding='utf-8') as f:
        json.dump(schedule_list, f, ensure_ascii=False, indent=2)

    print("worldboss.json 생성 완료!")

if __name__ == "__main__":
    generate_schedule()
