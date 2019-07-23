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
		if value == 3/3:
			return 33
		if value == 2/3 or value == 0.666666666666667:
			return 23
		if value == 3/4:
			return 34
		if value == 2/4:
			return 24
		if value == 4/4:
			return 44
		return value

	def set_2000000434(self, value):
		if value == "n.b.":
			return ""
		return value


def generateWordMap():
	return ["2000000013\t33\tNon-carrier",
			"2000000013\t34\tHeterozygote",
			"2000000013\t44\tHomozygote",
			"2000000013\t23\tNon-carrier",
			"2000000013\t24\tHeterozygote"]

TranSMARTMap.main(adHoc=Harmonizer, wordMaps=generateWordMap())
