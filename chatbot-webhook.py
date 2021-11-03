# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 18:50:10 2020

@author: Bruno
"""

from agentbot import fetch_reply
from createdb import createUser, createConversation, searchUserByFromId
import telebot
from telebot import types #add-ons connected
from flask import Flask, request
import os
import pymysql

connection = pymysql.connect(
    host = 'mysql.jacobjr.org',
    user = 'lincprog',
    password = 'linc2020prog',
    database = 'jj_chatbot'
)

cursor = connection.cursor() 

TOKEN = "1310402069:AAFl7f_xOuojg2uZPzOiku0I5N1dhu7UKm8"
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)
        
@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    # if the connection was lost, then it reconnects
    connection.ping(reconnect=True)    
    
    if searchUserByFromId(message.from_user.id, cursor) == False:
        createUser(message.from_user.first_name, message.from_user.last_name, message.from_user.id, cursor, connection)
    bot_responses = fetch_reply(message.text, message.from_user.id)
    for response in bot_responses:
        if response.text.text[0] == "":
            response.text.text[0] = "Desculpe, não entendi! :("
            bot.send_message(message.chat.id, response.text.text[0])
        else:
            bot.send_message(message.chat.id, response.text.text[0])
        createConversation(message.from_user.id, message.text, response.text.text[0], message.date, cursor, connection)
    
@bot.message_handler(commands=['help']) # help message handler
def send_welcome(message):
    # if the connection was lost, then it reconnects
    connection.ping(reconnect=True) 
    bot.reply_to(message, 'Digite "menu" para ver as opções disponíveis :)')

@bot.message_handler(content_types=['text'])
def send_reply(message):
    # if the connection was lost, then it reconnects
    connection.ping(reconnect=True) 
    bot_responses = fetch_reply(message.text, message.from_user.id)
    for response in bot_responses:
        if response.text.text[0] == "":
            response.text.text[0] = "Desculpe, não entendi! :("
            bot.send_message(message.chat.id, response.text.text[0])
        else:
            bot.send_message(message.chat.id, response.text.text[0])
        createConversation(message.from_user.id, message.text, response.text.text[0], message.date, cursor, connection)
    #bot.send_message(message.chat.id, message.text) # Para caso fosse um echo-bot

@bot.message_handler(content_types=['photo'])
def send_reply(message):
    # if the connection was lost, then it reconnects
    connection.ping(reconnect=True) 
    bot.send_message(message.chat.id, 'Gostei da foto!')


@bot.message_handler (content_types = ['contact'])
def contact (message):
    # if the connection was lost, then it reconnects
    connection.ping(reconnect=True) 
    if message.contact is not None:
        bot.send_message(message.chat.id, 'Adoraria conhecer o '+message.contact.first_name)
         
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://telegram-bot-webhook.herokuapp.com/' + TOKEN) 
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))