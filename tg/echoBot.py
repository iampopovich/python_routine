#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import sqlite3
import telebot
from telebot import types

def getConfig():
	currentDir = os.path.dirname(os.path.realpath(__file__))
	with open ("%s/config.cfg" %currentDir, "r") as cfg:
		config = json.load(cfg)
		return config["token"]

token = getConfig()
global bot 
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start", "help", "test"])
def send_welcome(message):  
	markup = types.ReplyKeyboardMarkup(row_width=2)
	itembtn1 = types.KeyboardButton("Откачать весь музон")
	markup.add(itembtn1)
	bot.reply_to(message, "Choose one letter:", reply_markup=markup)

@bot.message_handler(commands=["load_music"])
def loadAllMusic(message):
	print ("Пойти нахуй")

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
	bot.send_message(message.chat.id, message.text)
	text = parseSignal(message.text)
	print(text)
	print(message.chat.id)

@bot.message_handler(content_types=["audio"])
def showChannelId(message):
	print(message.chat.id)

@bot.channel_post_handler(content_types = ["text"])
def printMessageFromChannel(message):
	print(message.text)

def checkDatabaseConnection():
	pass

def appendUser():
	pass
	
def parseSignal(messageText):
	serializedMessage = {}
	for item in messageText.split("\n"):
		keyIndex = item.split("-")[0]
		value= item.split("-")[-1]
		serializedMessage[keyIndex] = value
	return serializedMessage
	pass

def sendOrder():
	pass

def main ():
	# currentDir = getcwd()

	checkDatabaseConnection()
	bot.polling(none_stop = True)

if __name__ == "__main__":
	main()