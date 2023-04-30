import pandas as pd
import os
import importlib
datawriter = importlib.import_module('datawriter')

if not os.path.exists('data'):
    os.makedirs('data')
    print('Created /data directory.')

if not os.path.exists('for_regression'):
    os.makedirs('for_regression')
    print('Created /for_regression directory.')

f = 'data/daily_discussion_moves.csv'
starting_index = 0
chunk_size = 100

for i in range(starting_index, len(pd.read_csv(f)), chunk_size):
    datawriter.write(i, chunk_size)
