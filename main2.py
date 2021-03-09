# import libraries
import pandas as pd

df = pd.read_json('contacts.json')
row_data = []

def function2(df, col):
    print("running function")
    data = df.sort_values([col])
    data = data[data[col] != '']
    empty_data = data[data[col] == '']
    data.reset_index(inplace=True)

    i = 0
    j = i+1

    link = [i]
    ticket_trace = [int(data.loc[i, 'Id'])]
    contacts = int(data.loc[i, 'Contacts'])

    while j < len(data):
        row_data.append([])
        print(row_data[i-1])

        if data.loc[i, col] == data.loc[j, col]:
            link.append(j)  # stores index of data
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
                row_data[i] = [int(data.loc[i, 'Id']), ret_str]
            i = j
            link = [i]
            ticket_trace = [int(data.loc[i, 'Id'])]
            contacts = int(data.loc[i, 'Contacts'])

        j += 1

    final = data.merge(empty_data)
    return final

df = function2(df, 'Email')
# df = df.sort_values(["Id"])

final = pd.DataFrame(row_data, columns=['ticket_id', 'ticket_trace/contact'])
final.to_csv('final2.csv')



