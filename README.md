# Topic Detection and Sentiment Analysis

This project is a web application that combines real-time topic detection and sentiment analysis to analyze news headlines. It scrapes headlines from predefined or custom news websites, classifies their sentiment (e.g., POSITIVE or NEGATIVE), and identifies the 
relevant topic (e.g., Health, Politics, Sports). The results are visualized in an interactive dashboard.

## Getting Started
### Prerequisites

Python 3.8 or above installed on your system.

pip for installing dependencies.

### Setup Instructions
**Clone the Repository**

```
git clone https://github.com/krushikagujarati/Topic-Detection-and-Sentiment-Analysis.git
cd Topic-Detection-and-Sentiment-Analysis
```
**Install Dependencies Navigate to the flask-backend directory and install the dependencies:**

```
cd flask-backend
pip install -r requirements.txt
```

### Running the Application
**Start the Flask Backend Navigate to the flask-backend folder and run the backend server:**

```
python app.py
```
The backend will start running at http://127.0.0.1:5000.

**Run the Streamlit Dashboard In the root directory, run the Streamlit dashboard:**
```
streamlit run dashboard.py
```
The dashboard will open in your default web browser at http://localhost:8501
