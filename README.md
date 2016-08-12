## Project McNulty
#### Team 4 ([@naoyak](https://github.com/naoyak), [@cwvanharen](https://github.com/cwvanharen), [@WDUpdegraff](https://github.com/WDUpdegraff), [@wccosby](https://github.com/wccosby))

### LoanBot: A Lending Club Robo-Advisor

LoanBot is an app for prospective investors on [Lending Club](https://www.lendingclub.com/), a P2P consumer lending platform. Enter the amount of money you have available to lend, your risk appetite level, and the type of loan you want to fund, and LoanBot will find loans for you to fund!

#### Tools used
- `scikit-learn`
- Flask
- D3
- Amazon EC2
- SQLite

#### Deployment instructions
- Obtain preprocessed `loans.db` SQLite file and place inside `loanBot/data` directory
- Create conda environment: `conda env create -f environment.yml`
- Activate env: `source activate loan-pred`
- Run app: `python app.py`
- Navigate to `0.0.0.0:9000`
