import json
from datetime import datetime, timedelta, timezone

# 영문 보스 이름을 한글로 변환하는 딕셔너리
BOSS_KR = {
    "Ashava": "아샤바",
    "Avarice": "아바리스",
    "Wandering Death": "떠도는 죽음",
    "Azmodan": "아즈모단"
}

def translate_boss(name):
    return BOSS_KR.get(name, name)

def generate_schedule():
    # rotation.json 파일 읽기
    with open('rotation.json', 'r', encoding='utf-8') as f:
        rotation = json.load(f)

    # rotation 데이터 안전 체크
    if not rotation:
        print("rotation.json 데이터가 없습니다.")
        return

    # 헬타이드 기준점:
    # 2026년 8월 6일 19:00:00 KST
    # = 2026년 8월 6일 10:00:00 UTC
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

    # 앞으로 8개 일정 생성
    for i in range(8):
        rot_index = (start_index + i) % len(rotation)
        rot_item = rotation[rot_index]

        timestamp = int(current_time.timestamp())
        start_time_str = current_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        # 같은 시간 여러 보스 처리 및 한글 변환 적용
        zones = rot_item.get("zones", [])
        boss_names_kr = []

        for z in zones:
            b_name = z.get("boss")
            if b_name:
                b_name_kr = translate_boss(b_name)
                if b_name_kr not in boss_names_kr:
                    boss_names_kr.append(b_name_kr)

        if len(boss_names_kr) > 1:
            combined_boss = ",".join(boss_names_kr)
        elif len(boss_names_kr) == 1:
            combined_boss = boss_names_kr[0]
        else:
            fallback_name = rot_item.get("boss", "Unknown")
            combined_boss = translate_boss(fallback_name)

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

    # ★ 안전장치:
    # 항상 시간순 정렬해서 EXE가 첫 번째 미래 보스를 정확히 읽게 함
    schedule_list.sort(key=lambda x: x["timestamp"])

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
