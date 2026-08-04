import json
from datetime import datetime, timedelta, timezone

def generate_schedule():
    # rotation.json 파일 읽기
    with open('rotation.json', 'r', encoding='utf-8') as f:
        rotation = json.load(f)

    # 기준 에폭(Anchor): 2026년 8월 4일 18:00:00 KST (= 2026-08-04 09:00:00 UTC)의 Avarice 시작점
    base_time = datetime(2026, 8, 4, 9, 0, 0, tzinfo=timezone.utc)
    
    # 헬타이드 화면 첫 시간(8/4 6:00 PM)에 띄워야 하는 정확한 보스인 Avarice의 rotation.json 상 인덱스
    # 제공해주신 rotation.json 배열에서 Avarice가 처음 등장하는 정확한 위치는 6번째(인덱스 6)입니다.
    base_rotation_index = 6
    
    # 현재 UTC 시간
    now_utc = datetime.now(timezone.utc)
    
    # 기준점부터 현재까지 몇 번의 주기가 지났는지 계산
    interval = timedelta(hours=3, minutes=30)
    time_diff = now_utc - base_time
    periods_passed = int(time_diff / interval)
    
    # 현재 진행 중이거나 다가오는 보스 스케줄부터 시작하도록 current_time 조정
    current_time = base_time + (periods_passed * interval)
    start_index = (base_rotation_index + periods_passed) % len(rotation)
    
    schedule_list = []
    
    # 앞으로 다가올 일정 7개 생성
    for i in range(7):
        rot_index = (start_index + i) % len(rotation)
        rot_item = rotation[rot_index]
        
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

    # 생성된 일정을 worldboss.json에 저장
    with open('worldboss.json', 'w', encoding='utf-8') as f:
        json.dump(schedule_list, f, ensure_ascii=False, indent=2)

    print("worldboss.json 갱신 완료!")

if __name__ == "__main__":
    generate_schedule()
