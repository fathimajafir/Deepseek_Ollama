import streamlit as st
import requests

# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000/chat"

# Streamlit app
def main():
    st.title("Construction Domain Chatbot 🏗️")
    st.write("Ask me anything about construction, including CSI numbers, materials, costs, and more!")

    # User input
    user_input = st.text_input("You:", placeholder="Type your question here...")

    if st.button("Send"):
        if user_input.strip() == "":
            st.warning("Please enter a question.")
        else:
            # Call FastAPI backend
            try:
                response = requests.post(
                    FASTAPI_URL,
                    json={"user_input": user_input}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.write(f"**Bot:** {data['bot_response']}")
                    st.write(f"**Reflection:** {data['reflection']}")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Run the Streamlit app
if __name__ == "__main__":
    main()