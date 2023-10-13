import datetime
import schedule
import time

import EmailService
import ClientReportsService


# Generally, daily_task should only be run for the current day, but allowing the parameter
# allows for more testing avenues
def daily_task(date=datetime.date.today()):
    clients = ClientReportsService.generate_clients()
    ClientReportsService.generate_new_reports(clients, date)
    EmailService.send_reports(clients, date)


def scheduler():
    schedule.every().day.at("12:30", "Europe/Berlin").do(daily_task)
    while True:
        schedule.run_pending()
        time.sleep(10)

daily_task(datetime.date(2024, 5, 19))
