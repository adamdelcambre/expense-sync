import pickle
import os


authfile = os.path.join(os.path.dirname(__file__), 'auth.pkl')
with open(authfile, 'r') as auth:
    AUTH = pickle.load(auth)


CONCUR = {
    'KEY': 'N4zuZJA8pNUZudJA9KY3jZ',
    'SECRET': '39qBPKQfNzJMe9MFNDhcQWypLHPBWjUS',
    'AUTH_URL': "https://www.concursolutions.com/net2/oauth2/accesstoken.ashx",
    'REPORTS_URL': "https://www.concursolutions.com/api/expense/expensereport/v2.0/Reports/",
    'REPORT_URL': "https://www.concursolutions.com/api/expense/expensereport/v2.0/report/",
    'USER_URL': "https://www.concursolutions.com/api/user/v1.0/user",
    'REVOKE_URL': 'https://www.concursolutions.com/net2/oauth2/revoketoken.ashx',
    'LIST_URL': 'https://www.concursolutions.com/api/expense/list/v1.0/',
    'PROJECT_ID': 'gWk3uaR6loEqhEfAooPQJ$phoz9xSnZyBvSw',
    'VALUES': {
        'Status': {
            'In Progress': 1,
            'Awaiting Approval' : 2,
            'Approved for Payment' : 3,
            'Rejected' : 4,
            'Paid' : 5,
            'Transferred to Quickbooks': 6
        },
        'ExpenseCategory' : {
            'Mileage':2, #Personal Car Mileage
            'Entertainment':3, #Entertainment - Client, #Entertainment - Staff, #Lunch, #Snacks/Beverages, 
            'Phone':29685283, #Mobile/Cellular Phone
            'Transportation':29685284, #Public Transport, #Taxi
            'Hotel':29685285, #Hotel
            'Meals':29685286, #Breakfast, #Business Meals (Attendees), #Dinner
            'Per Diem':29685287,
            'Other':29685288, #Gifts - Clients, Gifts - Staff, etc
            'Airfare':29685820, #Airfare, #Airline fees,
            'Car Rental':29685821,#Car Rental
            'Parking':29685822, #Parking
        }, 

        'alias': {
            'Personal Car Mileage': 'Mileage',
            'Entertainment - Client': 'Entertainment',
            'Entertainment - Staff': 'Entertainment',
            'Mobile/Cellular Phone' : 'Phone',
            'Public Transport': 'Transportation',
            'Taxi': 'Transportation',
            'Personal Car Mileage': 'Transportation',
            'Fuel': 'Transportation',
            'Hotel': 'Hotel',
            'Breakfast': 'Meals',
            'Business Meals': 'Meals',
            'Dinner': 'Meals',
            'Lunch': 'Meals',
            'Business Meals (Attendees)': 'Meals',
            'Snacks/Beverages': 'Meals',
            'Per Diem': 'Per Diem',
            'Other': 'Other',
            'Agency Booking Fees': 'Other',
            'Internet/Online Fees': 'Other',
            'Office Equipment/Hardware': 'Other',
            'Gifts - Clients': 'Other',
            'Gifts - Staff': 'Other',
            'Miscellaneous': 'Other',
            'Seminar/Course Fees': 'Other',
            'Postage': 'Other',
            'Airfare': 'Airfare',
            'Airline Fees': 'Airfare',
            'Car Rental': 'Car Rental',
            'Parking': 'Parking',
        },

        'WorkType': {
            'No Charge':123,
            'Internal Project':123,
            'Internal Training':123,
            'Billable Services':123,
            'Helpdesk':123,
            'Staffing':123,
            'Runmobile':123,
            'Interdept':123,
        },

        'PaymentType': {#X
            'Employee Paid':5,
            'Company Paid':9,
        }
    }
}

#GLCode 13685
SOAP_URL = 'https://webservices1.autotask.net/atservices/1.5/atws.asmx'

WSDL_URL = "https://webservices1.autotask.net/atservices/1.5/atws.wsdl"

PROXIES = {
    "http" : "https://webservices3.autotask.net/atservices/1.5/atws.wsdl"
}
