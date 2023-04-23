import poe
import os
from dotenv import load_dotenv
import json
import pandas as pd

# load_dotenv()

# client = poe.Client(os.environ['POE_TOKEN'])

# message = """IBM fucked me"""

# def get_ticker(message):
#     for chunk in client.send_message('nasdaqxnyse', message):
#         pass

#     try:  
#         res = json.loads(chunk['text'])
#         return res['identified_ticker']
#     except:
#         return ''

# print(get_ticker(message))

df = pd.read_csv('data/daily_discussion_moves.csv')
print(df)


    
