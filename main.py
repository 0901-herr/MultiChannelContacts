# import libraries
import pandas as pd

df = pd.read_json('contacts.json')

def function1(df,column):
    column='Email'
    data=df.sort_values(by=[column])
    empty=data[data[column]=='']
    data=data[data[column]!='']
    data.reset_index(inplace=True)
    for row,col in data.iterrows():
        if len(str(data.loc[row,'Id']))<8:
            lst=[row]
            string=str(data.loc[row,'Id'])
            contact=int(data.loc[row,'Contacts'])
            while data.loc[row,column]==data.loc[row+1,column] :
                string=string+'-'+str(data.loc[row+1,'Id'])
                lst.append(row+1)
                contact+=int(data.loc[row+1,'Contacts'])
                row+=1
            for i in lst:
                data.loc[i,'Id']=string
                data.loc[i,'Contacts']=contact
    final=data.merge(empty)
    return final

df=function1(df,'Email')
df=function1(df,'OrderId')
df=function1(df,'Phone')

df=df[['Id','Contacts']]

