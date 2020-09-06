import NXOpen
import re

class NXJournal:

	def __init__(self):
		self.session  = NXOpen.Session.GetSession()
		self.work_part = self.session.Parts.Work
		self.lw = self.session.ListingWindow


	def check_item_order(self, note, text):
		try:
			associative_text = self.work_part.Annotations.CreateAssociativeText()
			first_item_in_line = []
			check_item_order_pass = True
			for line in text:
				first_item_in_line.append(
					associative_text.GetEvaluatedText(note, line)
					)
			fn = [item for item in first_item_in_line if isinstance(item, int)]
			if len(first_item_in_line) > 2:
				for item in first_item_in_line[1:]:
					if item < first_item_in_line[item.index - 1]:
						check_item_order = False
						break
					else:
						pass
			return check_item_order_pass
		except Exception as ex:
			return("check_item_order failed with {}".format(ex))

	def check_spec_marks(self):
		try:
			pmi_cusotm_symbols = self.work_part.Annotations.CustomSymbols
			pmi_balloon_notes = self.work_part.Annotations.BalloonNotes
			associative_text = self.work_part.Annotations.CreateAssociativeText()
			list_stgm = []
			dict_stgm = {}
			dict_markups = {}
			checkSpecMarksPass = True
			for item in pmi_cusotm_symbols:
				if "triangle" in str(item.SymbolName).lower():
					list_stgm.append(item)
				else:
					continue

			for item in pmi_balloon_notes:
				data = item.GetSymbolData()
				data_text = ["".join(item.GetText()) for item in data.GetTextData()]
					dict_stgm[item.JournalIdentifier] = data_text
					lw.WriteLine("{}".format(dict_stgm))
				lw.WriteLine("{}".format(" -- ".join([
					item.JournalIdentifier,
					item.SymbolName,
					data_text
					])))

			for note in noteCollection:
				cd = self.work_part.Annotations.CreateComponentData(note)
				for textComponent in cd.GetTextComponents():

			for line in text:
				ptr = r"\d{1,}"
				if "клеймить" in line.lower:
					numLine = ""
					for ch in line:
						if re.match( ptr, ch ):
							numLine += ch
						else:
							break
					dict_markups[numLine] = "клеймение"
				elif "маркировать" in line.lower:
					numLine = ""
					for ch in line:
						if re.match( ptr, ch):
							numLine += ch
						else:
							break
					dict_markups[numLine] = "маркировка"

			return dict_markups
		except Exception as ex:
			return("check_spec_marks failed with {}".format(ex))

def main() :
	app = NXJournal()
	app.lw.Open()
	app.check_spec_marks()

if __name__ == "__main__":
	main()
