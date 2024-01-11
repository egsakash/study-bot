import os
import telebot
import threading
import json
import html
from api_ai import generate , genmcq
import random
from bot_utils import *

BOT_TOKEN = os.environ['BOT_TOK']

bot = telebot.TeleBot(BOT_TOKEN)

config = load_config()

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    first_name = html.escape(message.from_user.username) if message.chat.type == 'group' and message.from_user.username else 'User'
    if not_allowed(message):
    	bot.reply_to(message, get_message_template('not_allowed').format(first_name=first_name),parse_mode='HTML')
    	return

    welcome_message = (get_message_template('welcome_message').format(first_name=first_name))

    bot.send_message(chat_id, welcome_message,parse_mode='HTML')


@bot.message_handler(commands=['info'])
def handle_info(message):
    chat_id = message.chat.id if message.chat.id is not None else 'Not Available'
    user_id = message.from_user.id if message.from_user and message.from_user.id is not None else "Unknown"
    username = html.escape(message.from_user.username) if message.from_user and message.from_user.username is not None else "Not Available"
    first_name = html.escape(message.from_user.username) if message.chat.type == 'group' and message.from_user.username else 'User' if message.from_user and message.from_user.first_name is not None else "Not Available"
    last_name = html.escape(message.from_user.last_name) if message.from_user and message.from_user.last_name is not None else "Not Available"

    user_info = (
        f"Chat ID : `{chat_id}`\n"
        f"User ID: `{user_id}`\n"
        f"Username: `{username}`\n"
        f"First Name: `{first_name}`\n"
        f"Last Name: `{last_name}`\n"
    )

    bot.reply_to(message, user_info,parse_mode='MarkdownV2')

@bot.message_handler(commands=['answer'])
def handle_answer(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if not_allowed(message):
    	bot.reply_to(message, get_message_template('not_allowed').format(first_name=html.escape(message.from_user.username) if message.chat.type == 'group' and message.from_user.username else 'User'),parse_mode='HTML')
    	return

    try:
        question = message.text.split(' ', 1)[1]
    except IndexError:
        bot.reply_to(message, get_message_template('no_question').format(first_name=html.escape(message.from_user.username) if message.chat.type == 'group' and message.from_user.username else 'User'),parse_mode='HTML')
        return

    # Call your local API library to get the answer
    try:
        answer = generate(question)
    except Exception as e:
        print(e)
        bot.reply_to(message, get_message_template('server_down').format(first_name=html.escape(message.from_user.username) if message.chat.type == 'group' and message.from_user.username else 'User'),parse_mode='HTML')
        return

    # Format the response using a template
    template = get_message_template("answer_template")
    formatted_message = template.format(
        user=html.escape(message.from_user.username) if message.chat.type == 'group' and message.from_user.username else 'User',
        question=html.escape(question),
        answer=html.escape(answer)
    )

    bot.reply_to(message, formatted_message, parse_mode='HTML' , disable_web_page_preview=True)



bot.polling(none_stop=True)