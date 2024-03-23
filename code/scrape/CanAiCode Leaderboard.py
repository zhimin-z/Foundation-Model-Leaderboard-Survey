import pandas as pd
import os

path_leaderboard = 'data/CanAiCode Leaderboard'
# check https://huggingface.co/spaces/mike-ravkine/can-ai-code-results/discussions/2
original_filename = 'can-ai-code-results.csv'


def process_name(text):
    text = text.lower()
    text = text.replace('-', '_')
    return text


if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    df = pd.read_csv(f'{path_leaderboard}/{original_filename}')
    for (interview, task), group in df.groupby(['Interview', 'Task']):
        interview = process_name(interview)
        task = process_name(task)
        group.rename(columns={'name': 'Model'}, inplace=True)
        group.to_json(f'{path_leaderboard}/hf-{interview}-{task}.json', orient='records', indent=4)
    
    os.remove(f'{path_leaderboard}/{original_filename}')