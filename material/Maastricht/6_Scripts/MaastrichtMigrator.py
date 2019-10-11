import sys
#GREAT SHIT
sys.path.insert(0, '../../../src/Migrator')
sys.path.insert(0, '../../../src/Tables')
sys.path.insert(0, '../../../src/Utils')
sys.path.insert(0, '../../../src/Vocabularies')

import Baseline
import pandas as pd
import datetime
from Observation import Observation
from Logger import *
from datetime import date

class Harmonizer(object):
	def __init__(self):
		self.logger = Logger()
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
			"2000000168":{"value":2, "operator": ">"},
			"2000000121":{"value":7, "operator": ">"},
			}


	###################################################
	#	Public methods in the harmonization stage	  #
	###################################################
	def harmonizer(self, rawData):
		row = self.__dealWithDate(rawData)
		variableConcept = str(row["VariableConcept"])
		if "2000000540" in variableConcept:
			return self.__dealWithDiagnosisDate(row)
		if "2000000488" in variableConcept:
			return self.__dealWithAge(row)

		if "2000000323" in variableConcept:
			return self.__dealWithAlcohol(row)
		if "2000000013" in variableConcept:
			return self.__dealWithApoE(row)

		if "2000000642" in variableConcept:
			#print(row)
			return ""

		#1 - Yes or 0 - No conversion 
		#listOfNumericVariablesToConvertToYesOrNo = []
		#for variable in listOfNumericVariablesToConvertToYesOrNo:
		#	if variable in variableConcept:
		#		return self.__covertNumericVariablesToYesOrNo(row, yes='1', no='0')

		#1 - Yes or 2 - No conversion Not all used, just to save work i added all of the comorbidities
		listOfNumericVariablesToConvertToYesOrNo = ["2000000640", "2000000326", "2000000357", "2000000390", "2000000639", "2000000643",
			"2000000383", "2000000337", "2000000441","2000000341",  "2000000360", "2000000367",  "2000000400", "2000000381", "2000000382", 
			"2000000396", "2000000402", "2000000403", "2000000438", "2000000363", "2000000384", "2000000385", "2000000405", "2000000378", 
			"2000000408", "2000000416", "2000000434", "2000000334", "2000000379", "2000000415", "2000000331", "2000000469", "2000000470", 
			"2000000410", "2000000343", "2000000432", "2000000433", "2000000412"]
		for variable in listOfNumericVariablesToConvertToYesOrNo:
			if variable in variableConcept:
				return self.__covertNumericVariablesToYesOrNo(row, yes='1', no='2')

		#Last cleaning	
		listOfNumericVariablesToClean = ["2000000617", "2000000625", "2000000215", "2000000216", "2000000138",
			"2000000435", "2000000637", "2000000323", "2000000582"]
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

	def __dealWithDiagnosisDate(self, row):
		row["Measure"] = row["testdag"]
		row['MeasureNumber'] = None
		return row

	def __dealWithAge(self, row):
		row["Measure"] = row["testdag"]
		row['MeasureNumber'] = None
		return row

	def __dealWithAlcohol(self, row):
		row["MeasureNumber"] = None
		if row["Measure"] == '0':
			row["MeasureConcept"] = 2000000239#No
		elif row["Measure"] == '1':
			row["MeasureConcept"] = 2000000238#YES
		elif row["Measure"] == '2':
			print("FIX FIX FIX PAST")
			row["MeasureString"] = "Past"#Add concept
		else:
			self.logger.warn(warnType	= WRONG_VALUE, 
						 	patientID 	= row["PIN"], 
						 	variable 	= row["Variable"], 
						 	measure 	= row["Measure"],
						 	msg 		= "The variable was not one of the expected!")
			return []
		return row

	def __dealWithApoE(self, row):
		value = row['Measure'].split("E")
		if len(value) == 3:
			row['MeasureString'] = "{}/{}".format(value[1],value[2])
			return row
		self.logger.warn(warnType	= WRONG_VALUE, 
						 patientID 	= row["PIN"], 
						 variable 	= row["Variable"], 
						 measure 	= row["Measure"],
						 msg 		= "The variable was not one of the expected! For this variable in this cohort we are expecting the following format 'E<value>E<value>'.")
		return[]
	
	def __covertNumericVariablesToYesOrNo(self, row, yes, no):
		row["MeasureNumber"] = None
		if row["Measure"] == no:
			row["MeasureConcept"] = 2000000239#No
		elif row["Measure"] == yes:
			row["MeasureConcept"] = 2000000238#YES
		else:
			self.logger.warn(warnType	= WRONG_VALUE, 
							 patientID 	= row["PIN"], 
							 variable 	= row["Variable"], 
							 measure 	= row["Measure"],
							 msg 		= "The variable was not one of the expected! For this variable, the '{}' means 'No' and the '{}' means 'Yes'.".format(no, yes))
			return[]
		return row

	def __cleanTrashInNumericVariables(self, row):
		if row["Measure"].isdigit():
			return row
		self.logger.warn(warnType	= WRONG_VALUE, 
						 patientID 	= row["PIN"], 
						 variable 	= row["Variable"], 
						 measure 	= row["Measure"],
						 msg 		= "The variable was not one of the expected! For this variable, is expected a numeric value.")
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
