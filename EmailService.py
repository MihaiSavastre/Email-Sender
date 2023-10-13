import datetime
import logging
import os
import smtplib
from email.message import EmailMessage

# local modules
import Constants

logging.basicConfig(filename="report_emails.log", encoding='utf-8', level=logging.DEBUG)


def server_setup():
    smtp = smtplib.SMTP_SSL(Constants.email_server)
    # smtp.set_debuglevel(1)
    smtp.ehlo()
    smtp.login(Constants.sender_email, Constants.password)
    return smtp


# I'm storing recipients as dictionaries, though in a real life scenario they would be
# stored in a database and their information could be retrieved through an object
# with the necessary fields. This implementation is for the sake of simplicity
def create_email(receiver, date):
    em = EmailMessage()
    em['From'] = Constants.sender_email
    em['To'] = receiver.get('email')
    em['Subject'] = "Your daily report from OurCompany"
    date = date.strftime("%d-%m-%Y")
    message = f"""
            Good morning, {receiver.get('name')}!
            Here you'll find attached our report for today, {date}.
            Have a great rest of the day!
            
            At your service,
            OurCompany
            """
    em.set_content(message)

    # now for the attachment
    report = ""
    # find the correct report, using the name scheme
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), "Reports")):
        for file in files:
            if receiver.get('name') in file and date in file:
                report = os.path.join(root, file)
    if report == "":
        raise FileNotFoundError("No report exists")
    with open(report, 'rb') as attachment:
        content = attachment.read()
        # there does seem to be some issue with the attachment on the receiving end.
        # Seems to not be properly recognized by neither Gmail nor Windows
        em.add_attachment(content, maintype='application', subtype='pdf', filename='Daily Report')
    return em


def send_reports(clients, date):
    smtp = server_setup()
    for client in clients:
        try:
            email = create_email(client, date)
            receiver_address = client.get("email")
            # smtp.sendmail(Constants.sender_email, receiver_address, email.as_string())
            smtp.send_message(email, Constants.sender_email, receiver_address)
            logging.info(f"Report sent to {client.get('name')} at address {client.get('email')}"
                         f" for day {date} at {datetime.datetime.now().strftime('%H:%M:%S')}")
        except FileNotFoundError:
            logging.error(f"Report doesn't exist for client {client.get('name')}, email {client.get('email')}"
                          f" for day {date} at {datetime.datetime.now().strftime('%H:%M:%S')}")


# Testing template for sending an email to a person that may not have a report generated
# send_reports([{"name":"", "email":""}], datetime.date.today())