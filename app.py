import streamlit as st
from google import genai
import json
import os

from dotenv import load_dotenv

from rag import retrieve_context

# Load environment variables

load_dotenv()

# Load Gemini model

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# Streamlit UI

st.title("Enterprise Smart Assistant")

query = st.text_input(
    "Ask something about office"
)

if query:

    # ROOM SEARCH

    if "room" in query.lower():

        with open("rooms.json") as f:
            rooms = json.load(f)

        found = False

        for room in rooms:

            if room["room"].lower() in query.lower():

                st.success(
                    f"""
                    Room {room['room']}
                    is on Floor {room['floor']}
                    in {room['wing']}
                    """
                )

                found = True

        if not found:
            st.warning("Room not found.")

    # RAG SEARCH

    else:

        context = retrieve_context(query)

        prompt = f"""
        You are an enterprise office assistant.

        Answer professionally.

        Context:
        {context}

        Question:
        {query}
        """

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        st.write(response.text)