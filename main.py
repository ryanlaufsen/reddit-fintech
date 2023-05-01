import pandas as pd
import os
import glob
import importlib
datawriter = importlib.import_module('utilities.datawriter')

# Configure directory names for data download, semi-processed files, and final results
config_dirs = {
    'data': 'data',
    'processed': 'processed',
    'results': 'results'
}

# Create directories
for dir in config_dirs:
    if not os.path.exists(dir):
        os.makedirs(dir)
        print(f'Created /{dir} directory.')

# Pause / resume controls. Parameters can be edited depending on hardware capabilities
f = f'{config_dirs["data"]}/daily_discussion_moves.csv'
start_index = 0
chunk_size = 100

for i in range(start_index, len(pd.read_csv(f)), chunk_size):
    df_part = datawriter.write(i, chunk_size, f)
    if not df_part.empty:
        df_part.to_csv(f'{config_dirs["processed"]}/processed_{i}_{i + chunk_size}.csv')
        print(f'Processed and saved rows {i} to {i + chunk_size}.'
              f'({len(df_part)} {"tickers" if len(df_part) > 1 else "ticker"} found.)'
              )

df = datawriter.consolidate(glob.glob(f'{config_dirs["processed"]}/*.csv'))
