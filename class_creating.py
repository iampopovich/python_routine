import random
import time

class trooh:
	def __init__(self):
		self.age = None
		self.phrases = ["nu i...","taks taks", "nado potestit'...",
		"ladno zabeite...", "ya za bezopasnost'!"]
		self.skills = ["python"]
		self.actions = ["teret ekran ob stol", "bejat v kameru khraneniya",
		"otbirat cheki", "pryatat bankivskuy kartu"]
		
	def speak(self, whatToSay = None):
		print(whatToSay)
		if random.randint(0, 1) == 1:
			time.sleep(random.randint(5,15))
			border = self.phrases.__len__()
			print(self.phrases[random.randint(0,border-1)])
		return None
		
	def programming(self, language):
		if language in self.skills: return "taks taks taks...nu interesno"
		else: return "nado potestit'"
		
	def action(self):
		border = self.actions.__len__()
		return self.actions[random.randint(0, border - 1)]
		
def main():
	shurch = trooh()
	shurch.action()
	shurch.programming("java")
	for i in range (10):
		shurch.speak("est tezis...")

if __name__ == "__main__":
	main()