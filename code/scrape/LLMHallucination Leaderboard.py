import json
import os

from collections import defaultdict

path_leaderboard = 'data/LLMHallucination Leaderboard'
path_data = f'{path_leaderboard}/hf.json'

if __name__ == "__main__":
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    output_files = defaultdict(list)
    with open(path_data, 'r') as file:
        data = json.load(file)
        for evaluator, models in data.items():
            extractor, checker = evaluator.split('###')
            for model_name, datasets in models.items():
                for dataset_name, scores in datasets.items():
                    file_key = f"hf-{extractor}-{checker}-{dataset_name}.json"
                    if file_key not in output_files:
                        output_files[file_key] = []
                    scores['Model'] = model_name
                    output_files[file_key].append(scores)
        for file_key, models_data in output_files.items():
            file_name = f'{path_leaderboard}/{file_key}'
            with open(file_name, 'w') as file:
                json.dump(models_data, file, indent=2)
    os.remove(path_data)
