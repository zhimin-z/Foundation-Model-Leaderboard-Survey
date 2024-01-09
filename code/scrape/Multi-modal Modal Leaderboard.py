import requests
import pandas as pd

path_leaderboard = 'data/Multi-modal Modal Leaderboard'

url = 'https://opencompass.openxlab.space/utils/MMLB.json'
response = requests.get(url)
json_data = response.json()

df = pd.DataFrame(json_data).transpose()
df.reset_index(inplace=True)
df.rename(columns={'index': 'Model'}, inplace=True)
df.to_json(f'{path_leaderboard}/shw.json', orient='records', indent=4)