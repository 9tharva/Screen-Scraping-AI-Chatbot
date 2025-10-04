# AI Chat Auto-Responder Bot
This is a sophisticated Python script that automates replies in a chat application. It uses screen scraping to read the latest conversation, sends the context to an AI to generate a human-like response, and then automatically pastes the reply back into the chat.

The bot is designed to be highly intelligent, with a specific persona ("Atharva Chandratre") and the ability to understand and reply in the same language as the conversation, including transliterated Hindi ("Hinglish") and Marathi ("Manglish").

## Key Features
Automated Screen Scraping: Uses pyautogui to select and copy chat history directly from the screen.

Intelligent AI Persona: Leverages the OpenAI API via OpenRouter to generate responses that are in character, casual, and context-aware.

Dynamic Language Detection: Automatically detects if a conversation is in English, Hindi, or Marathi (even when typed with English letters) and instructs the AI to reply in the same style.

Context-Aware Replies: The AI is specifically prompted to reply to the most recent messages, ensuring timely and relevant responses.

Secure API Key Management: Uses a .env file to keep your API key safe and out of version control.

Fully Automated Workflow: The entire process from reading the chat to sending the reply is automated with a single script execution.

## Setup and Usage
Follow these steps to get the bot running on your machine.

1. Prerequisites
   Python 3.x installed.
   An API key from OpenRouter.ai.

2. Installation
   First, clone this repository to your local machine or download the files.

3. Install Dependencies
   Navigate to the project directory in your terminal and install the required Python libraries
   using the requirements.txt file.
   It's recommended to use the py launcher on Windows to avoid PATH issues
   py -m pip install -r requirements.txt

4. Configure Your API Key
   You will find a file named .env in the project folder.
   Open it and replace the placeholder key with your actual OpenRouter API key.
   OPENROUTER_API_KEY="sk-or-v1-your-actual-api-key-here"

5. (CRUCIAL) Configure Screen Coordinates
   Open the ai_auto_responder.py script.
   You must update the coordinate variables at the top of the file to match the positions on
   your screen. Use a screen coordinate tool to find the correct (X, Y) values for your specific
   application and screen resolution.

   Screen coordinates for automation - UPDATE THESE
   PASTE_AND_ENTER_X, PASTE_AND_ENTER_Y = 801, 1091
   ICON_X, ICON_Y = 635, 1166
   DRAG_START_X, DRAG_START_Y = 670, 180
   DRAG_END_X, DRAG_END_Y = 1875, 1036
   DESELECT_X, DESELECT_Y = 667, 201

7. Run the Bot
   Open the target chat application and make sure it's visible.
   Run the script from your terminal:
   python ai_auto_responder.py
   You will have 3 seconds to switch to the chat window before the automation begins.

## How It Works
Scrape: The script uses pyautogui to simulate mouse clicks and drags, selecting the visible chat history and copying it to the clipboard.

Analyze: The copied text is analyzed to detect the dominant language.

Generate: The chat history and a dynamically generated system prompt (with persona and language instructions) are sent to the AI via the OpenRouter API.

Paste & Send: The AI's generated response is copied to the clipboard, and the script pastes it into the chat input field and presses Enter.

Note: This script relies on fixed screen coordinates. If you resize your chat window, change your screen resolution, or use a different monitor, you will need to update the coordinates in the script.
