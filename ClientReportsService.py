import Constants
import os
import datetime

def generate_clients():
    clients = []
    file = open("Clients", 'r')
    for line in file.readlines():
        content = line.strip().split(", ")
        clients.append({'name' : content[0], 'email' : content[1]})
    file.close()
    return clients

def generate_new_reports(clients, date):
    for client in clients:
        report_name = f"report_{client.get('name')}_{date.strftime('%d-%m-%Y')}.txt"
        path = os.path.join(os.getcwd(), "Reports", report_name)
        file = open(path, "w")
        file.write(f"Report written for {client.get('name')} on {date.strftime('%d-%m-%Y')}")
        file.close()


# OBSOLETE IMPLEMENTATION
# Initially reports where generated all at one, based on the clients and a list of dates in Constants
# It makes more sens to generate new reports every day in scheduler
dates = Constants.dates
def generate_initial_reports(clients, dates):
    # delete old reports
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), "Reports")):
        for file in files:
            os.remove(os.path.join(root, file))

    # generate the new ones
    for client in clients:
        for date in dates:
            report_name = f"report_{client.get('name')}_{date.strftime('%d-%m-%Y')}.txt"
            path = os.path.join(os.getcwd(), "Reports", report_name)
            file = open(path, "w")
            file.write(f"Report written for {client.get('name')} on {date.strftime('%d-%m-%Y')}")
            file.close()

def initialize_data():
    clients = generate_clients()
    generate_initial_reports(clients, dates)
    return clients, dates
