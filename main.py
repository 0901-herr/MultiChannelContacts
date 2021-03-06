# import libraries
import pandas as pd

# import dataset
df = pd.read_json('contacts.json')
df = df.sort_values(by=['Email'])
