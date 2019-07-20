import json
import telebot 

class svinotaBot(telebot.TeleBot):
	# @self.message_handler(content_types = [text])
	def repeatAllMessages(self,message):
		self.send_message(message.chat_id, message.text)

def getConfig():
	with open ("config.cfg", "r") as cfg:
		config = json.load(cfg)
		return config["token"]

def main ():
	bot = None
	try:
		token = getConfig()
		bot = svinotaBot(token)
	except Exception as e: return 
	bot.polling(none_stop = True)

if __name__ == "__main__":
	main()