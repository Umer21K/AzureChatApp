import google.generativeai as genai
from dotenv import load_dotenv
import os

def nimbus(prompt):
    try:
        load_dotenv()
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel(
            "gemini-1.5-flash", 
            system_instruction=(
                "You are a friendly, chatbot of a retro-themed chatapp called Batein."
                "Your name is Nimbus. Keep all your responses under 60 words and sometimes give subtle 2000s movie references. If someone asks then you should know the chatapp database is on Azure CosmosDB and passwords are stored on Azure Key Vault."
            )
        )

        chat = model.start_chat()
        response = chat.send_message(prompt)
        return response.text

    except Exception as e:
        pass
        # return f"Something went wrong: {e}. Please contact the devs ;("