#!/usr/bin/env python3

import os
import re
import calendar

from collections import defaultdict
from datetime import datetime
from calendar import monthcalendar, SUNDAY

# 멤버 설정 (폴더명 -> 표시할 이름)
MEMBERS = {
    "JMS": "민선",
    "JSW": "시원",
    "KKJ": "기종",
    "KSH": "석희",
    "KSM": "성민",
    "MSK": "민수"
}

REPO_URL = "https://github.com/BE14-Early-Bird/TIL/blob/main/"

# README 상단 고정 내용
HEADER = """# TIL

### 📂 폴더 구조
```bash
└─ 📁 이니셜
    └─ 📄 년-월-일.md
```

### ⭐ conventions
- 처음 작성일때 : [이니셜] 날짜_생성
- 내용 추가일 때 : [이니셜] 날짜_수정

### 📜 templates
서식은 수정가능하나 아래 내용은 필수로 추가되어야 합니다.

```md
# ☀️ 오늘 한 일

# 🚩 내일 할 일
```

----

"""

def parse_files():
    month_data = defaultdict(lambda: defaultdict(dict))

    for member_folder in MEMBERS.keys():
        if not os.path.isdir(member_folder):
            continue

        for filename in os.listdir(member_folder):
            match = re.match(r"(\d{4})-(\d{2})-(\d{2})\.md$", filename)
            if match:
                year, month, day = map(int, match.groups())
                filepath = f"{member_folder}/{filename}"
                month_data[month][day][member_folder] = filepath

    return month_data


def get_week_map(year: int, month: int) -> dict[int, int]:
    calendar.setfirstweekday(calendar.SUNDAY)
    calendar_weeks = calendar.monthcalendar(year, month)
    week_map = {}
    for week_idx, week in enumerate(calendar_weeks, start=1):
        for day in week:
            if day != 0:
                week_map[day] = week_idx
    return week_map

def get_weekday(year: int, month: int, day: int) -> str:
    date = datetime(year, month, day)
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    return weekdays[date.weekday()]

def get_week_map_with_range(year: int, month: int):
    """
    주차별 정보 생성:
    - day → week_num
    - week_num → (start_day, end_day)
    """
    calendar.setfirstweekday(SUNDAY)  # 일요일 시작 보장
    weeks = monthcalendar(year, month)
    
    day_to_week = {}
    week_range = {}  # week_num → (start_day, end_day)
    
    for idx, week in enumerate(weeks, start=1):
        days_in_week = [day for day in week if day != 0]
        if not days_in_week:
            continue
        start_day, end_day = days_in_week[0], days_in_week[-1]
        week_range[idx] = (start_day, end_day)
        for day in days_in_week:
            day_to_week[day] = idx
            
    return day_to_week, week_range

def generate_table(month_data):
    content = ""
    today = datetime.today()
    current_year, current_month, current_day = today.year, today.month, today.day

    for month in sorted(month_data.keys()):
        content += f"### 📅 {month}월\n\n"

        day_to_week, week_range = get_week_map_with_range(2025, month)

        current_week = None
        if current_year == 2025 and current_month == month:
            current_week = day_to_week.get(current_day)

        weeks = defaultdict(list)
        for day in sorted(month_data[month].keys()):
            week_num = day_to_week.get(day, 0)
            weeks[week_num].append(day)

        for week_num in sorted(weeks.keys()):
            start_day, end_day = week_range.get(week_num, (0, 0))
            emoji = " ⭐" if week_num == current_week else ""
            summary = f"<summary><b>{week_num}주차 ({start_day}일~{end_day}일){emoji}</b></summary>"
            content += f"<details>\n  {summary}\n\n"

            content += "| 날짜 | " + " | ".join(MEMBERS.values()) + " |\n"
            content += "|-------------" + "|:---:" * len(MEMBERS) + "|\n"

            for day in weeks[week_num]:
                weekday = get_weekday(2025, month, day)
                row = f"| **{day}일 ({weekday})** "
                for member_folder in MEMBERS.keys():
                    if member_folder in month_data[month][day]:
                        path = month_data[month][day][member_folder]
                        link = f"[📄]({REPO_URL}{path})"
                        row += f"| {link} "
                    else:
                        row += "|     "
                row += "|\n"
                content += row

            content += "\n</details>\n\n"

    return content

def main():
    data = parse_files()
    table = generate_table(data)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(HEADER)
        f.write(table)

if __name__ == "__main__":
    main()
