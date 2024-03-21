import pandas as pd
import os

path_leaderboard = 'data/CanAiCode Leaderboard'

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)