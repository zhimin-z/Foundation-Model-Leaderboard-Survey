import pandas as pd
import json
import os

path_leaderboard = 'data/KoLA/ip.json'

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    with open(path_leaderboard, 'r') as f:
        data = json.load(f)
        df = pd.DataFrame(data['result'])
        df.to_json(path_leaderboard, orient='records', indent=4)