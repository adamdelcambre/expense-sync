import pickle

with open('auth.pkl', 'r') as auth:
    AUTH = pickle.load(auth)


CONCUR = {
    'KEY': 'N4zuZJA8pNUZudJA9KY3jZ',
    'SECRET': '39qBPKQfNzJMe9MFNDhcQWypLHPBWjUS',
    'AUTH_URL': "https://www.concursolutions.com/net2/oauth2/accesstoken.ashx",
    'REPORTS_URL': "https://www.concursolutions.com/api/expense/expensereport/v2.0/Reports/",
    'REPORT_URL': "https://www.concursolutions.com/api/expense/expensereport/v2.0/report/",
    'USER_URL': "https://www.concursolutions.com/api/user/v1.0/user",
    'REVOKE_URL': 'https://www.concursolutions.com/net2/oauth2/revoketoken.ashx',
    'LIST_URL': 'https://www.concursolutions.com/api/v3.0/common/listitems',
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
            'Mileage':('Personal Car Mileage'),
            'Entertainment': ('Entertainment - Client', 'Entertainment - Staff',),
            'Phone' : ('Mobile/Cellular Phone'),
            'Transportation': ('Public Transport', 'Taxi', 'Personal Car Mileage', 'Fuel'),#YES
            'Hotel': ('Hotel'),#YES
            'Meals': ('Breakfast', 'Business Meals', 'Dinner', 'Lunch', 'Snacks/Beverages',),
            'Per Diem': ('Per Diem'),
            'Other': ('Other', 'Gifts - Clients', 'Gifts - Staff', 'Miscellaneous', 'Postage'),
            'Airfare': ('Airfare', 'Airline Fees'),#YES
            'Car Rental': ('Car Rental'),#YES
            'Parking': ('Parking'),#YES
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
