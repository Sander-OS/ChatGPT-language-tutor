import flet as ft
from threading import Thread
import os
import re
import openai
import tempfile
from sys import exit as term
import speech_recognition as recognition
from pathlib import Path as path
from gtts import gTTS
from googletrans import Translator
from playsound import playsound
import concurrent.futures
#from google.cloud import texttospeech

# Load environment variables
from dotenv import load_dotenv
project_folder = os.path.expanduser('.') 
load_dotenv(os.path.join(project_folder, '.env'))

#Speech recognition & Translation init
speech  = recognition.Recognizer()
translator = Translator()
name = "Luigi"
content = ""
source_lang = []
target_lang = []

# Remove special characters from text
def no_emoji(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+", re.UNICODE)
    return re.sub(emoj, '', data)

#Return translated message
def translate(message, lang: str):
    lang = "nl" if lang == "" else lang
    
    #Translate and Print ChatGPT response
    message = no_emoji(message)
    native = ""
    try:
        native = translator.translate(message, dest=lang, src='auto').text
    except:
        native = "Error"
    detected = translator.detect(message)
    print(f"{detected}: {native}")
    return native

#Return text to speech
def tts(text, lang_code):
    # Uncomment one of the following lines based on the desired TTS provider

    # Using gTTS (uncomment this line if you want to use gTTS)
    tts = gTTS(text=text, lang=lang_code, slow=False, tld='nl')
    mp3 = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    mp3 = mp3.name
    try:
        os.remove(mp3)
    except:
        pass
    tts.save(mp3)
    playsound(mp3)
    try:
        os.remove(mp3)
    except:
        pass

    # Using Google Cloud Text-to-Speech (uncomment this line if you want to use Google Cloud Text-to-Speech)
    # client = texttospeech.TextToSpeechClient()
    # synthesis_input = texttospeech.SynthesisInput(text=text)
    # voice = texttospeech.VoiceSelectionParams(
    #     language_code=lang_code,
    #     name=f"en-{lang_code}-standard-b",
    #     ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    # )
    # audio_config = texttospeech.AudioConfig(
    #     audio_encoding=texttospeech.AudioEncoding.LINEAR16
    # )
    # response = client.synthesize_speech(
    #     input=synthesis_input, voice=voice, audio_config=audio_config
    # )
    # playsound(BytesIO(response.audio_content))


#Code to print messages in the message log
class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type
class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment="start"
        self.controls=[
                ft.CircleAvatar(
                    content=ft.Text(self.get_initials(message.user_name)),
                    color=ft.colors.WHITE,
                    bgcolor=self.get_avatar_color(message.user_name),
                ),
                ft.Column(
                    [
                        ft.Text(message.user_name, weight="bold"),
                        ft.Text(message.text, selectable=True),
                    ],
                    tight=True,
                    spacing=5,
                ),
            ]

    def get_initials(self, user_name: str):
        return user_name[:1].capitalize()

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]

#ChatApp talks with ChatGPT
class ChatApp:
    def __init__(self):
        # Setting the API key to use the OpenAI API
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.messages = [
            {"role": "system", "content": f'''
            Lets play a game! Act as my italian language tutor {name}.
            I want you to start a conversation with me on a basic level italian.
            Ask me the level of italian i am speaking based on the standard levels A1, A2, B1, B2 etc.
            Start with teaching me some essential words to communicate based on my level.
            I want you to speak to me in italian mainly.
            I may ask something in my native language to clarify. I may ask you to respond in my native language.
            Include a variety of language learning techniques such as guessing games and filling in the blanks.
            Make it playfull and fun and reward me with emoji so i keep engaged in the conversation.
            Start with a simple greeting. Then ask my name. Then ask my native language and use my native language.
            Respond in my native language when necessary.
            Then continue the conversation
            
            REMEMBER THESE RULES AT ALL TIMES:
            1. NEVER USE LISTS - Only practice single words and continue to the next word when I respond correctly.
            2. NEVER MIX TWO LANGUAGES IN A RESPONSE
            3. JUST PRACTICE PER SINGLE WORD OR SENTENCE.
            4. NEVER USE ___ characters 
            5. NEVER USE summing up words in lists
            6. ALWAYS RESPOND WITH SHORT SENTENCES
            7. USE ONLY A SINGLE LANGUAGE IN A RESPONSE
            8. CORRECT MY SENTENCES WHEN YOU DO NOT UNDERSTAND BY REPEATING WHAT I SAID OR ASK ME IN MY NATIVE LANGUAGE
            '''},
        ]
        self.native = []

    def chat(self, message):
        self.messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6
        )
        self.messages.append({"role": "assistant", "content": response["choices"][0]["message"].content})
        return response["choices"][0]["message"]



#Chat INIT
ChatGPT = ChatApp()
first_response = ChatGPT.chat("").content
print("Start sentence: ", first_response)

def main(page: ft.Page):
    t = ft.Text()

    def toggle_microphone(e):
        e.control.selected = not e.control.selected
        e.control.update()
        while e.control.selected:
            with recognition.Microphone() as source:
                try:
                    speech.energy_threshold = 4000
                    print("Listening..")
                    new_message.value = "Listening.."
                    page.update()
                    e.control.selected = True
                    audio = speech.listen(source)

                    text_dest = speech.recognize_google(audio, language=target_lang.value, with_confidence=True)
                    text_src = speech.recognize_google(audio, language=source_lang.value, with_confidence=True)
                    text = text_dest[0] if text_dest[1] > text_src[1] else text_src[0]
                    print(text)
                    new_message.value = text
                    page.update()
                    e.control.selected = False
                    e.control.update()
                    send_message_click(e)
                    break
                except recognition.UnknownValueError:
                    print("Speech Recognition could not understand audio.")
                    break
                except recognition.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                    break
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    break

    def send_message_click(e):
        # Check if the message is not empty
        if new_message.value != "":
            # Get the user's message
            user_message = new_message.value

            # Translate the user's message to the source language
            translated_message = translate(user_message, source_lang.value[:2])
            print(translated_message)

            # Display the user's message on the chat history screen and clear input fields
            page.pubsub.send_all(Message("Me", f"{user_message}\n{translated_message}", message_type="chat_message"))
            new_message.value = ""
            new_message.focus()
            page.update()

            # Generate a response from ChatGPT
            response = ChatGPT.chat(user_message).content

            # Uncomment the following line if you want to translate the GPT response
            translated_response = translate(response, source_lang.value[:2])
            # translated_response = ""

            # Detect the language of the GPT response & Display the GPT response on the screen
            detected_language = translator.detect(response)
            page.pubsub.send_all(Message(name, f"{response}\n{translated_response}", message_type="chat_message"))
            
            # Convert the GPT response to speech and toggle the microphone
            tts(response, detected_language.lang[:2])
            
            # Print the detected language for debugging purposes
            print("Detected language:", detected_language)

            # Toggle the microphone only if it's off
            if microphone_button.selected == False:
                toggle_microphone(e)

            # Update the page
            page.update()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
        chat.controls.append(m)
        page.update()
    
    page.pubsub.subscribe(on_message)

    # Chat messages
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    lang_list = [
            ft.dropdown.Option("en-EN"),
            ft.dropdown.Option("de-DE"),
            ft.dropdown.Option("nl-NL"),
            ft.dropdown.Option("it-IT"),
            ft.dropdown.Option("bs")
        ]
    
    source_lang = ft.Dropdown(value="nl-NL", width=100, options=lang_list, border_radius=40)
    target_lang = ft.Dropdown(value="it-IT", width=100, options=lang_list, border_radius=40)

    # A new message entry form
    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=False,
        expand=True,
        on_submit=send_message_click,
        bgcolor={"selected": ft.colors.GREY_300, "": ft.colors.GREY_200}
    )
 
    def Switch_lang(e):
        langSwitch.label = target_lang.value if langSwitch.value == True else source_lang.value
        print(langSwitch.label)
        page.update()

    microphone_button = ft.IconButton(
        icon=ft.icons.MIC_OFF_ROUNDED,
        selected_icon=ft.icons.MIC_ROUNDED,
        on_click=toggle_microphone,
        selected=False,
        style=ft.ButtonStyle(
            color={"selected": ft.colors.RED, "": ft.colors.GREY}, 
            shape=ft.CircleBorder(), 
            padding=20,
            bgcolor={"selected": ft.colors.GREY_300, "": ft.colors.GREY_200}
            ),
        icon_size = 40  
    )
    
    langSwitch = ft.Switch(
        label=target_lang.value, 
        value=True, 
        label_position=ft.LabelPosition.RIGHT, 
        on_change=Switch_lang
        )

    native = "" # translate(first_response, source_lang.value)  #.native(first_response)
    page.pubsub.send_all(Message(name, f"{first_response}\n{native}", message_type="chat_message"))
    page.update()

    page.add(
        ft.Row(
            [
                source_lang,
                target_lang,
            ]
        ),
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                ),
            ]
        ),
        ft.Row(
            [
                microphone_button,
                langSwitch,
            ], alignment = ft.MainAxisAlignment.CENTER
        ),
    )

ft.app(target=main)