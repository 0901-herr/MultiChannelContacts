# import libraries
import pandas as pd

df = pd.read_json('contacts.json')
row_data = []
ticket_data = []
contact_data = []

for i in range(0, 500000):
    row_data.append([])
    ticket_data.append([])
    contact_data.append(0)

def function2(df, col):
    print("running function")
    data = df.sort_values([col])
    data = data[data[col] != '']
    data.reset_index(inplace=True, drop=True)

    i = 0
    j = i+1

    link = [i]  # for data
    id = int(data.loc[i, 'Id'])
    ticket_trace = [id] # global row data (id)
    contacts = int(data.loc[i, 'Contacts'])  # global row data (id)

    while j < len(data):
        if data.loc[i, col] == data.loc[j, col]:
            link.append(j)  # stores index of data
            if int(data.loc[j, 'Id']) not in ticket_trace:
                ticket_trace.append(int(data.loc[j, 'Id'])) # stores id
                contacts += int(data.loc[j, 'Contacts'])
        else:
            ticket_trace.sort()
            ret_str = ""

            for i in ticket_trace:
                if i != ticket_trace[0]:
                    ret_str += "-" + str(i)
                elif i == ticket_trace[0] and len(ticket_trace) < 2:
                    ret_str = str(i)
                else:
                    ret_str += str(i)
            ret_str = ret_str + ", " + str(contacts)

            for i in link:
                id = int(data.loc[i, 'Id'])
                ticket_data[id] = ticket_trace
                contact_data[id] = contacts
                row_data[id] = [int(data.loc[i, 'Id']), ret_str]
                # print(row_data[i])

            i = j
            link = [i]
            id = int(data.loc[i, 'Id'])
            ticket_trace = ticket_data[id]
            contacts = int(data.loc[i, 'Contacts'])

            if id not in ticket_trace:
                ticket_trace.append(id)
                # print(ticket_trace)
                contacts = contact_data[id] + int(data.loc[i, 'Contacts'])

        j += 1

print("one")
function2(df, 'Email')

print("two")
function2(df, 'Phone')

print("three")
function2(df, 'OrderId')
# df = df.sort_values(["Id"])

row_data.sort()
# s = pd.Series(row_data)

final = pd.DataFrame(row_data[1:], columns=['ticket_id', 'ticket_trace/contact'])
final['ticket_id'] = pd.to_numeric(final['ticket_id'], downcast='integer')

print(final.head())
print(final.tail())

final.to_csv('final3.csv')






