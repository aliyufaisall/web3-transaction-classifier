SCALABLE WEB3 FRAUD GUARD USING XGBoost

An end-to-end Web3 security system designed to detect fraudulent Ethereum transactions using XGBoost. This project solves the 'Cold Start' and data imbalance challenges inherent in blockchain security by merging live Etherscan API ingestion with historical research datasets. The pipeline is engineered for production, featuring a containerized Django interface and a modular architecture that prioritizes Recall (fraud capture) through dynamic class weighting, ensuring high-risk patterns are identified in real-time without compromising the user experience for legitimate wallets.

Key Features
Dynamic Imbalance Handling: Leverages the scale_pos_weight hyperparameter to mathematically compensate for the scarcity of fraud cases, ensuring the model prioritizes catching scammers over simply predicting the majority class.
Engineered Feature Alignment: Features like Avg min between sent tnx and total Ether sent were specifically aggregated from raw transaction diaries to match account-level behavioral profiles, providing precise scaling for the XGBoost engine.
Unbiased Generalization: Utilizes Stratified Shuffle Splitting to ensure that both training and test sets maintain an identical distribution of fraud-to-legit cases, preventing sampling bias and improving real-world reliability.
Production-Ready Portability: Fully containerized using Docker and deployed as a live Django web service, demonstrating a complete "Model-to-Product" lifecycle that is ready for instant deployment on any cloud infrastructure.
Ensemble Gradient Boosting: Harnesses the power of XGBoost, an advanced ensemble learning algorithm that builds a sequence of decision trees to capture complex, non-linear patterns in blockchain data that traditional models miss.

Technology Stack
Core Programming & ML
•	Python: The primary language used for the entire end-to-end pipeline.
•	XGBoost: The core Gradient Boosting algorithm used for high-performance classification.
•	Scikit-Learn: Used for Stratified Sampling, GridSearchCV, and model evaluation metrics.
•	Pandas: The engine for data manipulation, cleaning, and behavioral feature engineering.

Web3 & Data Ingestion
•	Etherscan API: Utilised for real-time transaction data extraction from the Ethereum blockchain.
•	Requests: Handling secure HTTP communication with external Web3 data providers.
•	Python-Dotenv: Management of sensitive environment variables and API credentials.

Web Framework & Interface
•	Django: A high-level web framework used to build the production interface and service layer.
•	Bootstrap 5: Responsive frontend framework for the dark-mode, mobile-friendly security dashboard.
•	Gunicorn: A production-grade Python WSGI HTTP Server for handling concurrent web requests.

MLOps & Deployment
•	Docker: Containerization of the entire application for consistent, platform-agnostic deployment.
•	GitHub Actions: Automated CI/CD pipeline for code validation and continuous integration.
•	Render: Cloud platform used for hosting the live containerized web application.

Data Sources
•	Live Ethereum Ingestion: High-quality transaction data for "Legitimate" accounts is extracted directly from the Etherscan V2 API, utilizing the txlist endpoint to fetch the full transaction history of verified, high-trust wallets.
•	Historical Research Data: Fraudulent examples are sourced from the Kaggle Ethereum Fraud Detection Dataset, which contains nearly 10,000 labeled accounts with ground-truth "Scam" vs. "Non-Scam" classification.

Engineered Features
To align these sources, raw transaction logs are aggregated into account-level behavioral profiles: 
•	Avg min between sent tnx: The average time (in minutes) between consecutive outbound transactions—a key indicator of bot-like "velocity".
•	Sent_tnx / Received_tnx: The total volume of normal transactions initiated and received by the account.
•	Total Ether Sent: The cumulative financial value moved by the address, normalized from Wei to Ether for consistent model scaling. 

Installation & Setup

Follow these steps to get the Web3 Fraud Guard running locally on your machine.
1. Clone the Repository
powershell
git clone https://github.com
cd web3-fraud-detection
2. Set Up Environment Variables
Create a .env file in the root directory and add your Etherscan API key:
text
ETHERSCAN_API_KEY=your_api_key_here
3. Option A: Local Installation (Manual)
If you want to run it directly on your machine, ensure you have Python 3.10+ installed:
powershell
# Create a virtual environment
python -m venv fraud_env

# Activate the environment
# On Windows:
.\fraud_env\Scripts\activate
# On Mac/Linux:
source fraud_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the server
python manage.py runserver
# 4. Option B: Docker Installation (Recommended)
If you have Docker installed, you can launch the entire system in one command without worrying about dependencies
# Build the image
docker build -t web3-fraud-guard .

# Run the container
docker run -p 8000:8000 web3-fraud-guard


