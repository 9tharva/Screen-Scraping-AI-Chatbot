from openai import OpenAI
import os
from dotenv import load_dotenv

# Your API key is correct for OpenRouter
api_key = os.getenv("OPENROUTER_API_KEY")

# --- API Client Setup ---
# FIX 1: Add the base_url to point the client to OpenRouter's servers.
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# Your chat history and command
command = '''
[9:18 PM, 10/3/2025] atharva_chandratre: J what place it could be?? and what train it could be??
Timing is kinda morning ig
And platform 6
[9:20 PM, 10/3/2025] J: exactly cant be sure lools like nashik tbh
[9:32 PM, 10/3/2025] atharva_chandratre: But nashik ko konsi train 6 pe rukti hai
[12:48 PM, 10/4/2025] J: Idea nahi re
Pune chi astey ani baki mumbai wagre asta normal sakali
'''

try:
    # --- API Call ---
    completion = client.chat.completions.create(
      # FIX 2: Use the full model name required by OpenRouter.
      model="openai/gpt-3.5-turbo",
      messages=[
          {"role": "system", "content": "You are a person named Atharva who speaks hindi as well as english. He is from India and is a coder. You analyze chat history and respond like Atharva"},
          {"role": "user", "content": command}
      ]
    )

    print(completion.choices[0].message.content)

except Exception as e:
    print(f"An error occurred: {e}")