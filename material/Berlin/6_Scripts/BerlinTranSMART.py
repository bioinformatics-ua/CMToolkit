import sys
#GREAT SHIT
sys.path.insert(0, '../../../src/Migrator')
sys.path.insert(0, '../../../src/Tables')
sys.path.insert(0, '../../../src/Utils')
sys.path.insert(0, '../../../src/Vocabularies')
sys.path.insert(0, '../../../src/TranSMART')

import TranSMARTMap

class Harmonizer(object):
	def set_2000000013(self, value):
		if value == "2/2" or value == "2/3" or value == "3/3":
			return "Non-carrier"
		if value == "3/4" or value == "2/4":
			return "Heterozygote"
		if value == "4/4":
			return "Homozygote"
		return value

	#Maybe this can be removed
	def set_2000000434(self, value):
		if value == "n.b.":
			return ""
		return value

TranSMARTMap.main(adHoc=Harmonizer)
