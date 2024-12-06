import streamlit as st
import requests
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns

# Backend URLs
SCRAPE_URL = "http://127.0.0.1:5000/scrape-headlines"
PROCESS_URL = "http://127.0.0.1:5000/process-headlines"

st.title("Topic Detection and Sentiment Analysis")
st.sidebar.title("Input URL")

# Predefined URLs for convenience
predefined_urls = {
    "BBC News": "https://www.bbc.com/news",
    "NBC News": "https://www.nbcnews.com/",
    "ABC News": "https://abcnews.go.com/"
}

# Dropdown for predefined URLs
selected_url = st.sidebar.selectbox("Select a News Website", ["Custom URL"] + list(predefined_urls.keys()))

# Input box for custom URL
if selected_url == "Custom URL":
    url = st.sidebar.text_input("Enter the news website URL (e.g., https://www.example.com):")
else:
    url = predefined_urls[selected_url]

batch_size = st.sidebar.slider("Batch Size", min_value=1, max_value=5, value=2)

# Placeholder for results and progress bar
results_placeholder = st.empty()
chart_placeholder = st.empty()
progress_bar = st.progress(0)

# Fetch and process headlines in batches
def fetch_and_process_batches(url, batch_size):
    all_results = []  # Store all results
    start_index = 0

    while True:
        # Fetch batch of headlines
        response = requests.post(SCRAPE_URL, json={"url": url, "start_index": start_index, "batch_size": batch_size})
        if response.status_code != 200:
            st.warning("No more headlines to process or an error occurred.")
            break

        batch_headlines = response.json().get("headlines", [])
        if not batch_headlines:
            st.warning("No more headlines found.")
            break

        # Process batch
        process_response = requests.post(PROCESS_URL, json={"headlines": batch_headlines})
        if process_response.status_code != 200:
            st.error("Error processing headlines.")
            break

        batch_results = process_response.json()
        all_results.extend(batch_results)

        # Update UI with new data
        df = pd.DataFrame(all_results)
        results_placeholder.write(df[['headline', 'sentiment', 'confidence', 'topic']])
        update_chart(df, chart_placeholder)

        # Increment start index and update progress bar
        start_index += batch_size
        progress = min(start_index / (start_index + batch_size), 1.0)  # Simulated progress
        progress_bar.progress(progress)

        time.sleep(2)  # Simulate real-time effect

    progress_bar.progress(1.0)  # Mark progress as complete
    return all_results

# Update chart dynamically
def update_chart(df, placeholder):
    if df.empty:
        placeholder.write("No data to display.")
        return

    topic_sentiment = df.groupby(['topic', 'sentiment']).size().reset_index(name='count')
    plt.figure(figsize=(10, 6))
    sns.barplot(data=topic_sentiment, x="topic", y="count", hue="sentiment")
    plt.title("Sentiment Distribution by Topic")
    plt.xlabel("Topic")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    placeholder.pyplot(plt)

# Button to start scraping and analyzing
if st.sidebar.button("Scrape and Analyze"):
    if not url:
        st.error("Please provide a valid URL!")
    else:
        with st.spinner("Scraping and analyzing headlines in batches..."):
            fetch_and_process_batches(url, batch_size)
