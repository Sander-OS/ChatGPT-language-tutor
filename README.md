# ChatGPT Language Tutor

Welcome to ChatGPT Language Tutor! This application leverages OpenAI's GPT-3.5-turbo model to create an interactive language learning experience. Practice any supported language with ChatGPT in a playful and engaging way using naturally spoken language, following specific language learning rules.

## Requirements
Ensure you have the following Python libraries installed:

```bash
pip install flet openai googletrans playsound gtts SpeechRecognition python-dotenv
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/Sander-OS/ChatGPT-Language-Tutor.git
cd ChatGPT-Language-Tutor
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
```

3. Install the required libraries:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project folder and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key
```

## Execution

Run the application using the following command:

```bash
python ChatGPT-language-tutor.py
```


## Additional Topics

- **Language Learning Rules**: Follow the specified rules for an effective language learning experience.
- **Translation**: The application uses Google Translate to translate messages.
- **Text-to-Speech**: Enjoy spoken responses using gTTS. Uncomment the Google Cloud Text-to-Speech code if desired.
- **Microphone Interaction**: Engage in spoken conversations by toggling the microphone button.
- **User Interface**: Explore the features of the interactive user interface built with Flet.

## How to Use

1. Start a conversation as the Italian language tutor named Luigi.
2. Follow the provided rules for an effective language learning experience.
3. Communicate with the program in Italian, and it will respond accordingly.
4. The program supports voice input through the microphone button.
5. Enjoy a playful and engaging language learning journey!

Feel free to contribute, report issues, or suggest improvements. Happy language learning!
