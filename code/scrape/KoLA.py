import pandas as pd
import json
import os

path_leaderboard = 'data/KoLA'
original_filename = 'result.json'

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    with open(f'{path_leaderboard}/{original_filename}', 'r') as f:
        data = json.load(f)
        df = pd.DataFrame(data['result'])
        df.drop(columns=['rank'], inplace=True)
        df.rename(columns={'model': 'Model'}, inplace=True)
        df.to_json(f'{path_leaderboard}/ip.json', orient='records', indent=4)
    os.remove(f'{path_leaderboard}/{original_filename}')