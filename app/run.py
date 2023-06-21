import telebot
import os
from modules import chat_model, TTS, whisper_api, log_handler
from requests.exceptions import ReadTimeout
import sys
import io
import time
from config import TELEBOT_API_KEY, HF_API_KEY, BOT_SYSTEM_INSTRUCTION, SYSTEM_REFRESH, BARK_SMALL_MODELS, SPEAKER

# TTS Init
au_model = TTS('app/assets/audio/', BARK_SMALL_MODELS)
print('TTS initialized successfully 👍')

# chat_model Init
chat = chat_model(HF_API_KEY)

# Telegram Bot Init
bot = telebot.TeleBot(TELEBOT_API_KEY)

# Log declaration
log = log_handler('app\log\log.txt')

@bot.message_handler(content_types=['text', 'document'])
def handle_text(message):
    chat_id = message.chat.id
    if chat.number == 0:
        if message.text != '/start':
            response = chat.query_bot(f'{message.text}', BOT_SYSTEM_INSTRUCTION, SYSTEM_REFRESH)
            bot.send_message(chat_id, response, timeout=None)
            # Add a new text message the './log/log.txt' file
            log.log_write(f'Date:{message.date} Chat_id: {chat_id} User: {message.text} Bot: {response}')
        else:
            bot.send_message(chat_id, 'Hello!', timeout=None)
            # Add a new text message the './log/log.txt' file
            log.log_write(f'Date:{message.date} Chat_id: {chat_id} User: {message.text} Bot: Hello!')
    else:
        if message.text == '/exit' or message.text == 'exit' or message.text == 'Exit':
            bot.send_message(chat_id, 'Bye!', timeout=None)
            log.log_write(f'Date:{message.date} User: {message.text} Bot: Closed correctly. ')
            log.fn_block()
            return
        elif message.text == '/reset' or message.text == 'reset' or message.text == 'Reset':
            bot.send_message(chat_id, 'Chat reset successfully.', timeout=None)
            log.log_write(f'Date:{message.date} User: {message.text} Bot: Chat reset successfully. ')
            chat.context = ''
            log.fn_block()
            return
        else:
            # Pass the ID of the last message
            response = chat.query_bot(f'{message.text}', BOT_SYSTEM_INSTRUCTION, SYSTEM_REFRESH)
            bot.send_message(chat_id, response, timeout=None)
            # Add a new text message to the './log/log.txt' file
            log.log_write(f'Date:{message.date} Chat_id: {chat_id} User: {message.text} Bot: {response} ')
            return

def send_audio(text, chat_id):
    try:
        au_model.to_audio(text, SPEAKER)
        bot.send_voice(chat_id, open('./assets/audio/tts.ogg', "rb"))
        os.remove("./assets/audio/tts.ogg")
        return
    except Exception as err:
        print('Error in send_audio function:\n'+str(err))
        log.log_write('Something went wrong with send_audio:\n'+str(err))
        bot.send_message(chat_id, text) 
        return

@bot.message_handler(content_types=['voice', 'audio'])
def handle_voice(message):
    whisper = whisper_api(HF_API_KEY)
    try:
        chat_id = message.chat.id
        if chat.number == 0:
            if message.text != '/start':
                # Get information about the audio file
                file_info = bot.get_file(message.voice.file_id)
                file_path = file_info.file_path
                # Download the audio file
                downloaded_file = bot.download_file(file_path)
                # Save the audio file
                audio_file_path = 'app/assets/audio/audio.ogg'
                with open(audio_file_path, 'wb') as f:
                    f.write(downloaded_file)

                text = whisper.transcribe(audio_file_path)
                time.sleep(5)
                os.remove(audio_file_path)
                response = chat.query_bot(text, BOT_SYSTEM_INSTRUCTION, SYSTEM_REFRESH)
                send_audio(response, message.chat.id)
                bot.send_message(chat_id, response, timeout=None)
                log.log_write(f'Date:{message.date} User: {message.text} Bot: {text}')
                return
            else:
                bot.send_message(chat_id, 'Hello!', timeout=None)
                # Add a new text message with its respective ID to the './log/log.txt' file
                write = f'Date:{message.date} Chat_id: {chat_id} User: {message.text} Bot: Hello!'
                log.log_write(write)
        else:
            # Get information about the audio file
            file_info = bot.get_file(message.voice.file_id)
            file_path = file_info.file_path
            # Download the audio file
            downloaded_file = bot.download_file(file_path)
            # Save the audio file
            audio_file_path = 'app/assets/audio/audio.ogg'
            with open(audio_file_path, 'wb') as f:
                f.write(downloaded_file)

            text = whisper.transcribe(audio_file_path)
            time.sleep(5)
            os.remove(audio_file_path)
            response = chat.query_bot(text, BOT_SYSTEM_INSTRUCTION, SYSTEM_REFRESH)
            send_audio(response, message.chat.id)
            bot.send_message(chat_id, response, timeout=None)
            log.log_write(f'Date:{message.date} User: {message.text} Bot: {text}')
            return
    except Exception as err:
        print('Error in handle_voice:\n'+str(err))
        log.fn_by_err(str(err))
        log.log_write('Error in handle_voice:\n'+str(err))
        
if __name__ == "__main__":
    try:
        while True:
            try:
                bot.polling(timeout=30)
            except ReadTimeout:
                print("A timeout occurred. Trying again...")
    except Exception as err:
        print('Error in bot.polling:\n' + str(err))
        log.fn_by_err(str(err))
