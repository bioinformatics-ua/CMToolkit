import sys
#GREAT SHIT
sys.path.insert(0, '../../../src/Migrator')
sys.path.insert(0, '../../../src/Tables')
sys.path.insert(0, '../../../src/Utils')
sys.path.insert(0, '../../../src/Vocabularies')

import Baseline
from Observation import Observation
import pandas as pd
from datetime import date
import datetime

class Harmonizer(object):
	def __init__(self):
		#Variables calculated based on other variables
		self.ceradWLRounds = []
		self.ceradWLRecognition = []
		self.apoE = []
		self.diagnosis = {}
		self.etiology = {}
		self.adHocCutOff = {}
		'''
		cutOffs = "cutOffId":{"value":xxxx, "operator": "<" or >"}
		or
		cutOffs = "cutOffId":{"conditionalMethod": method()}
		'''
		self.cutOff = {
			}


	###################################################
	#	Public methods in the harmonization stage	  #
	###################################################
	def harmonizer(self, rawData):
		row = self.__dealWithDate(rawData)
		variableConcept = str(row["VariableConcept"])
		#if "2000000049" in variableConcept:
		#	return self.__readCeradWLRounds(row)
		if "2000000323" in variableConcept:
			return self.__dealWithAlcohol(row)

		if "2000000013" in variableConcept:
			self.__dealWithApoE(row)
			#if value == "2/2" or value == "2/3" or value == "3/3":
			#	return "Non-carrier"
			#if value == "3/4" or value == "2/4":
			#	return "Heterozygote"
			#if value == "4/4":
			#	return "Homozygote"
			return row

		if "2000000642" in variableConcept:
			print(row)
			return ""

		#Yes or No conversion
		listOfNumericVariablesToConvertToYesOrNo = ["2000000326", "2000000357", "2000000390"]
		for variable in listOfNumericVariablesToConvertToYesOrNo:
			if variable in variableConcept:
				return self.__covertNumericVariablesToYesOrNo(row)

		#Last cleaning	
		listOfNumericVariablesToClean = ["2000000617", "2000000625", "2000000215", "2000000216", "2000000138",
			"2000000435", "2000000637", "2000000639", "2000000640", "2000000643", "2000000323", "2000000582", 
			"2000000215", "2000000216"]
		for variable in listOfNumericVariablesToClean:
			if variable in variableConcept:
				return self.__cleanTrashInNumericVariables(row)
		return row	

	def addMissingRows(self):
		missingRows = []
		#missingRows += self.__process...
		#....
		return missingRows

	###############
	#	Private	  #
	###############
	def __dealWithDate(self, rawData):
		row = dict(rawData)
		row['testdag'] = str(row['testdag']) + "-" + str(row['testmnd']) + "-" + str(row['testjr'])
		#row['Gebdag'] = str(row['Gebdag']) + "-" + str(row['Gebmnd']) + "-" + str(row['Gebjr'])
		return row

	def __dealWithAlcohol(self, row):
		row["MeasureNumber"] = None
		if row["Measure"] == '0':
			row["MeasureConcept"] = 2000000239#No
		if row["Measure"] == '1':
			row["MeasureConcept"] = 2000000238#YES
		if row["Measure"] == '2':
			print("FIX FIX FIX PAST")
			row["MeasureString"] = "Past"#YES
		return row

	def __dealWithApoE(self, row):
		#if value == "2/2" or value == "2/3" or value == "3/3":
		#	return "Non-carrier"
		#if value == "3/4" or value == "2/4":
		#	return "Heterozygote"
		#if value == "4/4":
		#	return "Homozygote"
		print("todo")
		return row
	
	def __covertNumericVariablesToYesOrNo(self, row):
		row["MeasureNumber"] = None
		if row["Measure"] == '0':
			row["MeasureConcept"] = 2000000239#No
		elif row["Measure"] == '1':
			row["MeasureConcept"] = 2000000238#YES
		else:
			print("[WRONG TYPE] The variable was not one of the expected", row["Measure"])
			return[]
		return row

	def __cleanTrashInNumericVariables(self, row):
		if isinstance(row["Measure"], float):
			return row
		return ""
		
	#######################################
	#	Harmonizer during the migration	  #
	#######################################
	def filter_person(self, cohort):
		cohort = cohort[pd.notnull(cohort['Sex'])]
		return cohort.reset_index(drop=True)

	#Person
	def set_person_gender_concept_id(self, value):
		gender_map = {"M":8507, "V":8532}
		return value.map(gender_map)

	#def set_person_birth_datetime(self, value):
	#	#todo
	#	return value

	#	if "person_year_of_birth" in variableConcept:
	#	print(value)
	#	raise
	#	return value

#The Usagi files for this cohort were built using a different input
def prepareUsagiFiles(args):
	mappingFiles = [args.settings["cohort_mappings"]["columnsmapping_original"]]
	mappingFiles += [args.settings["cohort_mappings"]["contentmapping_original"]]
	for file in mappingFiles:
		location = "/".join(file.split("/")[:-1])
		fileName = file.split("/")[-1].split(".")[0] + "_processed.csv"
		fw = open("{}/{}".format(location, fileName), "w")
		firstLine = True
		with open(file) as fp:
			for line in fp:
				row = line.split(",")
				if firstLine:
					fw.write(row[0]+","+row[1]+",translate,"+",".join(row[2:]))
					firstLine = False
				else:
					fw.write("AD Switchbox Maastricht Original data file.csv,"+",".join(row)) 
		fp.close() 
		fw.close()
	
prepareUsagiFiles(Baseline.loadArgs())
Baseline.main(Harmonizer)
