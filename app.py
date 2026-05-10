import streamlit as st
from google import genai
import json
import os

from dotenv import load_dotenv

from rag import retrieve_context

# Load environment variables

load_dotenv()

# Configure Gemini client

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# Streamlit UI

st.title("Enterprise Smart Assistant")

st.write(
    "AI-powered workplace assistant for employees and visitors."
)

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

    # POLICY / RAG SEARCH

    else:

        context = retrieve_context(query)

        prompt = f"""
        You are an enterprise office assistant.

        Answer professionally using the provided context.

        Context:
        {context}

        Question:
        {query}
        """

        try:

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

            st.write(response.text)

        except Exception as e:

            st.error(
                "Gemini API temporarily unavailable."
            )

            st.write(
                """
                Fallback Response:

                - Visitor access requires employee approval.
                - Meeting rooms can be booked 24 hours in advance.
                - Restricted floors require admin access.
                """
            )

            st.caption(f"Error: {e}")