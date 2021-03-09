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
    empty_data = data[data[col] == '']
    data.reset_index(inplace=True, drop=True)

    i = 0
    j = i+1

    link = [i]
    ticket_trace = ticket_data[i]
    contacts = contact_data[i]

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
                ticket_data[i] = ticket_trace
                contact_data[i] = contact_data
                row_data[i] = [int(data.loc[i, 'Id']), ret_str]
                print(row_data[i])
            i = j
            link = [i]
            if int(data.loc[i, 'Id']) not in ticket_trace:
                ticket_trace = ticket_data[i]
                ticket_trace.append(int(data.loc[i, 'Id']))
                # print(ticket_trace)
                contacts = contact_data[i] + int(data.loc[i, 'Contacts'])
            else:
                ticket_trace = ticket_data[i]
                contacts = contact_data[i]

        j += 1

    final = data.merge(empty_data)
    return final

print("one")
df = function2(df, 'Email')
print("two")
df = function2(df, 'Phone')
print("three")
df = function2(df, 'OrderId')
df = df.sort_values(["Id"])
print(df.head())
row_data.sort()
final = pd.DataFrame(row_data, columns=['ticket_id', 'ticket_trace/contact'])
final.to_csv('final3.csv')



