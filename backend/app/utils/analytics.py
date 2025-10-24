from datetime import datetime
from typing import List


def month_range(start: str, end: str) -> List[str]:
    start_date = datetime.strptime(start, "%Y-%m")
    end_date = datetime.strptime(end, "%Y-%m")
    months: List[str] = []
    cursor = start_date
    while cursor <= end_date:
        months.append(cursor.strftime("%Y-%m"))
        if cursor.month == 12:
            cursor = cursor.replace(year=cursor.year + 1, month=1)
        else:
            cursor = cursor.replace(month=cursor.month + 1)
    return months
