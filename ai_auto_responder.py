import pyautogui
import pyperclip
import time
from openai import OpenAI
import os
from dotenv import load_dotenv

# --- Load Environment Variables ---
# This line loads the variables from your .env file (e.g., your API key)
load_dotenv()

# --- Configuration ---
# API and Persona Setup
# The script now securely gets the API key from the .env file
api_key = os.getenv("OPENROUTER_API_KEY")

# Check if the API key was loaded successfully
if not api_key:
    print("ERROR: OPENROUTER_API_KEY not found.")
    print("Please create a file named .env and add your key like this:")
    print('OPENROUTER_API_KEY="sk-or-v1-..."')
    exit()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# Screen coordinates for automation
PASTE_AND_ENTER_X, PASTE_AND_ENTER_Y = 801, 1091
ICON_X, ICON_Y = 635, 1166
DRAG_START_X, DRAG_START_Y = 670, 180
DRAG_END_X, DRAG_END_Y = 1875, 1036
DESELECT_X, DESELECT_Y = 667, 201


def detect_dominant_language(text):
    """
    Upgraded function to guess the dominant language of the chat,
    now supporting transliterated Hindi (Hinglish) and Marathi (Manglish).
    """
    text_lower = text.lower()
    words = text_lower.split()

    # Word lists now include both Devanagari and Roman script (transliterated) words
    marathi_words = {'आहे', 'आणि', 'मला', 'काय', 'कसा', 'झालं', 'हो', 'नाही', 'ahe', 'ani', 'mala', 'kay', 'kasa', 'jhala', 'kela', 'bagh', 're', 'baba'}
    hindi_words = {'है', 'और', 'मुझे', 'क्या', ' कैसे', 'हुआ', 'हाँ', 'नहीं', 'hai', 'aur', 'mujhe', 'kya', 'kaise', 'hua', 'kiya', 'toh', 'yaar', 'bhai'}

    marathi_score = sum(1 for word in words if word in marathi_words)
    hindi_score = sum(1 for word in words if word in hindi_words)

    if marathi_score > hindi_score:
        return "marathi"
    elif hindi_score > marathi_score:
        return "hindi"
    else:
        # Fallback for when scores are tied or the words aren't in the list
        if any('kela' in w or 'ahes' in w for w in words):
            return "marathi"
        if any('kiya' in w or 'hai' in w for w in words):
            return "hindi"
        return "mixed"


# 1. Give user time to switch windows before automation starts
print("Script will start in 3 seconds... Switch to your target window.")
time.sleep(3)
print("Running automation...")

# 2. Scrape the chat history from the screen using pyautogui
try:
    pyautogui.click(ICON_X, ICON_Y)
    time.sleep(1.5) # Increased wait for UI to respond, enhancing stability

    # --- More reliable drag method ---
    # This sequence is often more robust than a single dragTo() command.
    pyautogui.moveTo(DRAG_START_X, DRAG_START_Y, duration=0.2) # Move to start position
    pyautogui.mouseDown(button='left') # Press and hold the mouse button
    pyautogui.moveTo(DRAG_END_X, DRAG_END_Y, duration=1.5) # Drag to the end position
    pyautogui.mouseUp(button='left') # Release the mouse button to complete the selection

    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5) # Allow time for clipboard to update

    chat_history = pyperclip.paste()
    pyautogui.click(DESELECT_X, DESELECT_Y)

    if not chat_history:
        print("Clipboard is empty. No text was copied. Exiting.")
        exit()
    
    print("\n--- Chat History Copied Successfully ---")
    print(chat_history)
    print("--------------------------------------")

except Exception as e:
    print(f"\nAn error occurred during screen scraping: {e}")
    exit()


# 3. Process the history and get a natural AI response
try:
    # Detect the language to create a dynamic prompt
    dominant_language = detect_dominant_language(chat_history)
    print(f"Detected dominant language: {dominant_language.capitalize()}")

    # Dynamically set the language instruction for the AI
    if dominant_language == "marathi":
        language_instruction = "The chat is primarily in Marathi (typed in English script). Your reply MUST be in casual Marathi, with some English/Hindi words mixed in, just like a native speaker from Maharashtra."
    elif dominant_language == "hindi":
        language_instruction = "The chat is primarily in Hindi (typed in English script). Your reply MUST be in casual Hindi, with some English words mixed in."
    else: # 'mixed'
        language_instruction = "The chat is a mix of languages. Your reply should also be a natural mix of Hindi, Marathi, and English."

    # The main system prompt that defines the persona and task
    system_prompt = f"""
    You are embodying the persona of Atharva Chandratre.
    
    **Persona Details:**
    - From: Maharashtra, India
    - Profession: Expert Coder
    - Languages: Fluent in English, Hindi, and Marathi. You naturally mix these languages.
    - Tone: Casual, friendly, and authentic. You are NOT a formal AI assistant.
    
    **Your Task:**
    Analyze the provided chat history. Your response MUST be the very next message Atharva would send.
    
    **--- CRITICAL RULES ---**
    1.  **Focus on Recency:** The chat history may span several days. Your reply MUST be relevant to the most recent messages at the end of the log (e.g., messages under a "Today" marker). Ignore older parts of the conversation.
    2.  **Be a Logical Continuation:** Do not ask redundant questions that were just answered in the previous message.
    3.  **Obey Language Instructions:** {language_instruction}
    
    **Example of a good, timely response:**
    - Recent Chat History: ... (older messages) ... [Today] Person A says, "Papa phone gharich visarli ahe"
    - A GOOD response from you: "Arey, parat ka? Thik ahe, call karu nako mag."
    - A BAD response (ignoring recency): "How was your maths paper?"
    
    Now, provide Atharva's next reply based on the user's provided chat history.
    """
    
    print("Sending request to AI...")
    completion = client.chat.completions.create(
      model="openai/gpt-3.5-turbo",
      messages=[
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": chat_history}
      ]
    )

    response = completion.choices[0].message.content
    pyperclip.copy(response) # Copy the AI's authentic response to the clipboard
    
    print("\n--- AI Response Generated ---")
    print(response)
    print("-----------------------------")

except Exception as e:
    print(f"\nAn error occurred during the API call: {e}")
    exit()

# 4. Paste the AI's response back into the application
try:
    print("Pasting the AI's response and sending...")
    pyautogui.click(PASTE_AND_ENTER_X, PASTE_AND_ENTER_Y)
    time.sleep(0.5)

    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)

    pyautogui.press('enter')
    print("\nScript finished successfully.")

except Exception as e:
    print(f"\nAn error occurred while pasting the response: {e}")