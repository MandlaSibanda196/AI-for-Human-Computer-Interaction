import os
import streamlit as st
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Load environment variables from .env file
load_dotenv()

# Load from environment
endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
key = os.getenv("AZURE_LANGUAGE_KEY")

# Initialize Azure client
credential = AzureKeyCredential(key)
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

# App UI
st.title("Sentiment-Aware Echo Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input prompt
if prompt := st.chat_input("Say something..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        sentiment_result = text_analytics_client.analyze_sentiment([prompt])[0]
        sentiment = sentiment_result.sentiment
        confidence = sentiment_result.confidence_scores

        response = (
            f"Echo: {prompt}\n\n"
            f"🧠 Sentiment: **{sentiment.capitalize()}** "
            f"(Positive: {confidence.positive:.2f}, Neutral: {confidence.neutral:.2f}, Negative: {confidence.negative:.2f})"
        )
    except Exception as e:
        response = f"Echo: {prompt}\n\n⚠️ Failed to analyze sentiment: {e}"

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
