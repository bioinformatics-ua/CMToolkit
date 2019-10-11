import sys
#GREAT SHIT
sys.path.insert(0, '../../../src/Migrator')
sys.path.insert(0, '../../../src/Tables')
sys.path.insert(0, '../../../src/Utils')
sys.path.insert(0, '../../../src/Vocabularies')
sys.path.insert(0, '../../../src/TranSMART')

import TranSMARTMap

class Harmonizer(object):
	##Patient ID
	def patient_id(self, value):
		return value.split(".")[0]

	
	##Change fields
	def set_2000000013(self, value):
		if value == "2/2" or value == "2/3" or value == "3/3":
			return "Non-carrier"
		if value == "3/4" or value == "2/4":
			return "Heterozygote"
		if value == "4/4":
			return "Homozygote"
		return value

	'''
	def set_2000000642(self, value):
		return ""

	def set_2000000617(self, value):
		if isinstance(value, float):
			return value
		if "-" in value:
			return ""
		return value

	def set_2000000625(self, value):
		if isinstance(value, float):
			return value
		if "-" in value:
			return ""
		return value

	def set_2000000215(self, value):
		if isinstance(value, float):
			return value
		if "-" in value:
			return ""
		return value

	def set_2000000216(self, value):
		if isinstance(value, float):
			return value
		if "-" in value:
			return ""
		return value

	def set_2000000435(self, value):
		if isinstance(value, float):
			return value
		return ""	

	def set_2000000637(self, value):
		if isinstance(value, float):
			return value
		return ""
	def set_2000000639(self, value):
		if isinstance(value, float):
			return value
		return ""
	def set_2000000640(self, value):
		if isinstance(value, float):
			return value
		return ""
	def set_2000000643(self, value):
		if isinstance(value, float):
			return value
		return ""
	def set_2000000323(self, value):
		if isinstance(value, float):
			return value
		return ""
	def set_2000000582(self, value):
		if isinstance(value, float):
			return value
		return ""
	def set_2000000215(self, value):
		if isinstance(value, float):
			return value
		return ""
	def set_2000000216(self, value):
		if isinstance(value, float):
			return value
		return ""
	def set_2000000138(self, value):
		if isinstance(value, float):
			return value
		return ""
	'''
		


	##Add fields
	def add_2000000620(self):#Study name
		return "Maastricht"

	def add_2000000571(self):#Study name
		return "No"


TranSMARTMap.main(adHoc=Harmonizer)
