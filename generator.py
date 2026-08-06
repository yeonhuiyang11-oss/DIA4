import json
from datetime import datetime, timedelta, timezone


def generate_schedule():
    # rotation.json 파일 읽기
    with open('rotation.json', 'r', encoding='utf-8') as f:
        rotation = json.load(f)

    # 헬타이드 기준점:
    # 2026년 8월 6일 19:00:00 KST
    # = 2026년 8월 6일 10:00:00 UTC
    # 해당 시간 월드보스: Avarice
    base_time = datetime(2026, 8, 6, 10, 0, 0, tzinfo=timezone.utc)

    # 현재 UTC 시간
    now_utc = datetime.now(timezone.utc)

    # 월드보스 간격
    interval = timedelta(hours=3, minutes=30)

    # 현재 기준 다음 월드보스 시간 찾기
    current_time = base_time

    while current_time + interval <= now_utc:
        current_time += interval

    if current_time <= now_utc:
        current_time += interval

    # 몇 번째 보스인지 계산
    time_diff = current_time - base_time
    periods_passed = int(time_diff / interval)

    start_index = periods_passed % len(rotation)

    schedule_list = []

    # 8개 일정 생성 (Avarice → Avarice → Ashava...)
    for i in range(8):
        rot_index = (start_index + i) % len(rotation)
        rot_item = rotation[rot_index]

        timestamp = int(current_time.timestamp())
        start_time_str = current_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        # 같은 시간 여러 보스 처리
        zones = rot_item.get("zones", [])

        boss_names = []

        for z in zones:
            b_name = z.get("boss")

            if b_name and b_name not in boss_names:
                boss_names.append(b_name)

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

    # worldboss.json 저장
    with open('worldboss.json', 'w', encoding='utf-8') as f:
        json.dump(
            schedule_list,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("worldboss.json 갱신 완료!")


if __name__ == "__main__":
    generate_schedule()
