import json
from datetime import datetime, timedelta, timezone

def generate_schedule():
    # rotation.json 파일 읽기
    with open('rotation.json', 'r', encoding='utf-8') as f:
        rotation = json.load(f)

    # 헬타이드 첫 기준점: 2026년 8월 4일 18:00:00 KST (= 2026-08-04 09:00:00 UTC)의 Avarice 시작점
    base_time = datetime(2026, 8, 4, 9, 0, 0, tzinfo=timezone.utc)
    
    # 현재 UTC 시간
    now_utc = datetime.now(timezone.utc)
    
    # 기준점부터 현재까지 몇 번의 주기가 지났는지 계산
    interval = timedelta(hours=3, minutes=30)
    time_diff = now_utc - base_time
    periods_passed = int(time_diff / interval)
    
    # 현재 진행 중이거나 다가오는 보스 스케줄부터 시작하도록 current_time과 시작 인덱스 조정
    current_time = base_time + (periods_passed * interval)
    start_index = periods_passed % len(rotation)
    
    schedule_list = []
    
    # 앞으로 다가올 일정 7개 생성
    for i in range(7):
        rot_index = (start_index + i) % len(rotation)
        rot_item = rotation[rot_index]
        
        timestamp = int(current_time.timestamp())
        start_time_str = current_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        
        # [핵심] zones 리스트에서 모든 보스 이름을 추출하여 겹칠 경우 합쳐주기
        zones = rot_item.get("zones", [])
        boss_names = []
        for z in zones:
            b_name = z.get("boss")
            if b_name and b_name not in boss_names:
                boss_names.append(b_name)
        
        # 보스가 2마리 이상이면 "Avarice & Azmodan" 형태로 결합, 1마리면 그대로 사용
        if len(boss_names) > 1:
            combined_boss = " & ".join(boss_names)
        elif len(boss_names) == 1:
            combined_boss = boss_names[0]
        else:
            combined_boss = rot_item.get("boss", "Unknown")
        
        item = {
            "id": timestamp,
            "timestamp": timestamp,
            "boss": combined_boss,
            "type": "world_boss",
            "startTime": start_time_str,
            "zone": zones
        }
        schedule_list.append(item)
        current_time += interval

    # 생성된 일정을 worldboss.json에 저장
    with open('worldboss.json', 'w', encoding='utf-8') as f:
        json.dump(schedule_list, f, ensure_ascii=False, indent=2)

    print("worldboss.json 갱신 완료!")

if __name__ == "__main__":
    generate_schedule()
