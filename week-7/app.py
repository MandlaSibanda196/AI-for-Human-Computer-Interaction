import os
import streamlit as st
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Load environment variables
load_dotenv()
AZURE_ENDPOINT = os.getenv("AZURE_LANGUAGE_ENDPOINT", "")
AZURE_KEY = os.getenv("AZURE_LANGUAGE_KEY", "")

# Initialize Azure client
def get_client():
    try:
        credential = AzureKeyCredential(AZURE_KEY)
        return TextAnalyticsClient(endpoint=AZURE_ENDPOINT, credential=credential)
    except Exception as e:
        st.error(f"Error initializing Azure client: {e}")
        return None

client = get_client()

# App title & layout
st.set_page_config(page_title="Sentiment-Aware Echo Bot", layout="wide")
st.title("Sentiment-Aware Echo Bot")

# Sidebar
with st.sidebar:
    st.header("About this App")
    st.write("""
        This app analyzes the **sentiment** of your input text using Azure AI Text Analytics
        and changes the **background color** based on the detected sentiment:
        - 🟩 Green = Positive
        - 🟨 Yellow = Neutral
        - 🟥 Red = Negative
    """)
    st.subheader("Instructions")
    st.write("""
        1. Type a sentence in the chat box below.
        2. Press **Enter** to send.
        3. Watch the background color update instantly!
    """)
    st.subheader("Quick Demo")
    if st.button("😊 Positive Example"):
        st.session_state["quick_demo"] = "I love sunny days!"
    if st.button("😐 Neutral Example"):
        st.session_state["quick_demo"] = "The sky is blue."
    if st.button("☹️ Negative Example"):
        st.session_state["quick_demo"] = "I hate being stuck in traffic."

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Check for quick demo trigger
if "quick_demo" in st.session_state:
    demo_prompt = st.session_state.pop("quick_demo")
    st.session_state.demo_triggered = demo_prompt
else:
    st.session_state.demo_triggered = None

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get user input or demo input
user_input = st.chat_input("Say something...")
if st.session_state.demo_triggered:
    user_input = st.session_state.demo_triggered

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    sentiment = "unknown"
    pos = neu = neg = 0.0

    if client:
        try:
            result = client.analyze_sentiment([user_input])[0]
            sentiment = result.sentiment
            pos = result.confidence_scores.positive
            neu = result.confidence_scores.neutral
            neg = result.confidence_scores.negative
        except Exception as e:
            st.warning(f"Sentiment analysis failed: {e}")

    # Choose background color based on sentiment
    bg_color = "#FFFFFF"  # default white
    if sentiment.lower() == "positive":
        bg_color = "#d4edda"  # light green
    elif sentiment.lower() == "neutral":
        bg_color = "#fff3cd"  # light yellow
    elif sentiment.lower() == "negative":
        bg_color = "#f8d7da"  # light red

    # Inject background color
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {bg_color} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    response = (
        f"Echo: {user_input}\n\n"
        f"**Sentiment:** {sentiment.capitalize()} "
        f"(Positive: {pos:.2f}, Neutral: {neu:.2f}, Negative: {neg:.2f})"
    )

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
