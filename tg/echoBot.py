#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import sqlite3
import telebot
from telebot import types
from telebot import apihelper

def getConfig():
	currentDir = os.path.dirname(os.path.realpath(__file__))
	with open ("%s/config.cfg" %currentDir, "r") as cfg:
		config = json.load(cfg)
		return config

config = getConfig()
bot = telebot.TeleBot(config["token"])
apihelper.proxy = config["proxy"]

# @bot.message_handler(commands=["start", "help", "test"])
# def send_welcome(message):  
# 	markup = types.ReplyKeyboardMarkup(row_width=3)
# 	itembtn1 = types.KeyboardButton("1")
# 	itembtn2 = types.KeyboardButton("2")
# 	itembtn3 = types.KeyboardButton("3")
# 	markup.add(itembtn1,itembtn2,itembtn3)
# 	bot.reply_to(message, "Choose one letter:", reply_markup=markup)

@bot.channel_post_handler(content_types = ["text"])
def printMessageFromChannel(message):
	# bot.send_message(message.chat.id, "response: {}".format(message.chat.id))
	text = parseSignal(message.text)
	response = "\n".join(map(str,[message.chat.id, str(text)]))
	bot.send_message(config["botID"], "response: {}".format(response))

@bot.message_handler(commands = ["getBotID"])
def printBotId(message):
	bot.send_message(message.chat.id, message.chat.id)

def checkDatabaseConnection():
	pass

def registerUser():
	pass
	
def parseSignal(messageText):
	serializedMessage = {}
	for item in messageText.split("\n"):
		keyIndex = item.split("-")[0]
		value= item.split("-")[-1]
		serializedMessage[keyIndex] = value
	return serializedMessage

def sendOrder():
	pass

def main ():
	checkDatabaseConnection()
	bot.polling(none_stop = True)

if __name__ == "__main__":
	main()