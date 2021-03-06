# import libraries
import pandas as pd

# import dataset
df = pd.read_json('contacts.json')
email = df.sort_values(by=["Email"])
phone = df.sort_values(by=["Phone"])
orderId = df.sort_values(by=["Order ID"])
contacts = df.sort_values(by=["Contacts"])

email_tab = [[]]
phone_tab = [[]]
orderId_tab = [[]]
contacts_tab = [[]]

for i in email.iterrows():
    if i['Id']




