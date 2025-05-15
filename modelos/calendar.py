from typing import Dict, List
from datetime import datetime, date, timedelta

TODAYS_DATE = date(date.today().year, date.today().month, date.today().day)
NEXT_HOUR = (datetime.now() + timedelta(hours=2)).hour
LAST_DATE_OF_THE_YEAR = date(date.today().year, 12, 31)

class Calendar:
    def __init__(self, start_date: date = TODAYS_DATE, end_date: date = LAST_DATE_OF_THE_YEAR):
        self.calendar = {}
        dates = self.__get_all_date_strings_current_year(start_date, end_date)
        self.__map_dates_to_calendar(dates)

    def __get_all_date_strings_current_year(self, start_date: date, end_date: date) -> List[str]:
        delta = timedelta(days=1)
        
        date_hour_slots = []
        while start_date <= end_date:
            for hour in range(NEXT_HOUR, 17):  # From 8:00 to 16:00
                date_hour_str = f"{start_date.strftime('%Y-%m-%d')} {hour:02d}:00"
                date_hour_slots.append(date_hour_str)
            start_date += delta
        return date_hour_slots

    def __map_dates_to_calendar(self, dates: List) -> Dict:
        for date in dates:
            self.calendar[date] = True

    def __str__(self):
        return f"{self.calendar}"
    
    def show_available_slots(self):
        print("Available slots:")
        for date, available in self.calendar.items():
            if available:
                print(date)

calendar = Calendar()
print(calendar)
#calendar.show_available_slots()
