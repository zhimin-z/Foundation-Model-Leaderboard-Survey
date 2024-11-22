<div align="center">
    <h1>On the Workflows and Smells of Leaderboard Operations:<br>An Exploratory Study of Foundation Model Leaderboards</h1>
</div>

<p align="center">
    <a href="https://arxiv.org/abs/2407.04065"><img src="https://img.shields.io/badge/📃-Arxiv-b31b1b?style=for-the-badge"></a>
</a>

Watch the following video teaser to learn about our motivation, methodology, and key findings!
#### Video: [Canva](https://www.canva.com)
#### Image: [GPT-4o](https://chat.openai.com)
#### Music: [Suno](https://suno.com)

https://github.com/user-attachments/assets/031a2f93-6f95-4b67-993f-808864abbfaa

## Overview
Our paper investigates various foundation model (FM) leaderboards across multiple platforms, focusing on their operational workflows ("**LBOps**"), and common pitfalls ("**leaderboard smells**"). We also curate an awesome list of FM leaderboards, check [here](https://github.com/SAILResearch/awesome-foundation-model-leaderboards).

## Contents
1. **requirements.txt**: Lists all the necessary libraries required to run the script. Use this file to install dependencies with a package manager like pip.

2. **README.md**: Provides comprehensive documentation for the replication package, including setup instructions and usage guidelines.

3. **code/main.ipynb**: The main Jupyter notebook containing the core script of our study, including data processing, analysis, and visualization steps.

4. **data/Dependents_Lookup.sh**: Bash script used for mining GitHub repositories. It automates the process of retrieving repository information.

5. **data/GitHub.json**: Stores metadata about the GitHub repositories mined during our study, including relevant details for analysis.

6. **data/HuggingFace.json**: Contains the URLs of all the mined Hugging Face spaces, facilitating further exploration and analysis of foundation models.

7. **data/PapersWithCode.json**: Stores URLs of the mined leaderboards from Papers with Code, supporting our study on benchmarking efforts.

8. **result/Foundation Model Leaderboards.xlsx**: Spreadsheet containing all the labels and relevant information extracted for the foundation model leaderboards analyzed in our research.

9. **result/Leaderboard-Distribution.pdf**: Visual representation of the distribution of leaderboards across various platforms, summarizing the findings of our study.

## Citation
If you find this repository useful, please consider giving us a star :star: and citation:
```
@article{zhao2024workflows,
  title={On the Workflows and Smells of Leaderboard Operations (LBOps): An Exploratory Study of Foundation Model Leaderboards},
  author={Zhao, Zhimin and Bangash, Abdul Ali and C{\^o}go, Filipe Roseiro and Adams, Bram and Hassan, Ahmed E},
  journal={arXiv preprint arXiv:2407.04065},
  year={2024}
}
```

## Contact
If you have any questions or collaborate, feel free to [raise an issue](https://github.com/zhimin-z/Foundation-Model-Leaderboard-Survey/issues/new).
