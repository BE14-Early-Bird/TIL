#!/usr/bin/env python3

import os
import re
from collections import defaultdict

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
    month_data = defaultdict(lambda: defaultdict(dict))  # month -> day -> member -> filepath

    for member_folder in MEMBERS.keys():
        if not os.path.isdir(member_folder):
            continue

        for filename in os.listdir(member_folder):
            match = re.match(r"(\d{4})-(\d{2})-(\d{2})\.md$", filename)
            if match:
                year, month, day = match.groups()
                month_int = int(month)
                day_int = int(day)
                filepath = f"{member_folder}/{filename}"
                month_data[month_int][day_int][member_folder] = filepath

    return month_data

def generate_table(month_data):
    content = ""
    for month in sorted(month_data.keys()):
        content += f"<details>\n  <summary><b>📅 {month}월</b></summary>\n\n"
        content += "| 날짜 | " + " | ".join(MEMBERS.values()) + " |\n"
        content += "|-----" + "|-----" * len(MEMBERS) + "|\n"

        for day in sorted(month_data[month].keys()):
            row = f"| {day}일 "
            for member_folder in MEMBERS.keys():
                if member_folder in month_data[month][day]:
                    path = month_data[month][day][member_folder]
                    link = f"[링크]({REPO_URL}{path})"
                    row += f"| {link} "
                else:
                    row += "|      "
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
