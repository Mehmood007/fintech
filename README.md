# Fintech

## Description

**Welcome to the Fintech Bank Online Banking App - your secure and convenient gateway to managing your finances anytime, anywhere. Our application offers a comprehensive suite of features designed to simplify your banking experience and keep your financial activities at your fingertips.**  


## Features

- Manage Accounts
- Admin Panel


### Technologies Used

| HTML | CSS | Python | Django | PostgreSQL |
|------|-----|--------|--------|------------|
| <img src="https://upload.wikimedia.org/wikipedia/commons/6/61/HTML5_logo_and_wordmark.svg" width="50"> | <img src="https://upload.wikimedia.org/wikipedia/commons/d/d5/CSS3_logo_and_wordmark.svg" width="50"> | <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width="50"> | <img src="https://upload.wikimedia.org/wikipedia/commons/7/75/Django_logo.svg" width="50"> | <img src="https://wiki.postgresql.org/images/3/30/PostgreSQL_logo.3colors.120x120.png" width="50"> |



## Setup Locally
- **First clone repo locally**  
  **Run below command in terminal**  
  `git clone https://github.com/Mehmood007/fintech.git`


- **Install Dependencies**  
  - First make sure virtual environment is activated  
  - Make sure you have postgres installed on system and running  
`pip install -r requirements.txt`

- **Setup .env**  
  - Create `.env` file inside project  
  - Look into `.env-sample` and fill `.env` accordingly  


- **Run Migrations in app directory**  
  - Make sure you have created db in postgres  
  `python manage.py makemigrations`  
  `python manage.py migrate`


- **Run Server**  
  `python manage.py runserver`

