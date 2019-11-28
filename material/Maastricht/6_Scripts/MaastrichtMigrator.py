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
		self.patientWithStroopV10 = []
		self.stroops = []
		self.CST0X = {}
		self.SRTImmediate = {}
		self.SRTDelayed = {}
		self.otherCerebrovascularDisorders = {}
		self.otherCardiovascularDisorders = {}
		self.otherSomaticDisorders = {}
		'''
		cutOffs = "cutOffId":{"value":xxxx, "operator": "<" or >"}
		or
		cutOffs = "cutOffId":{"conditionalMethod": method()}
		'''
		self.cutOff = {
			"2000000168":{"value":2, "operator": ">"},	#MTA Bilateral
			"2000000121":{"value":7, "operator": ">"},	#HDS
			"2000000297":{"value":551, "operator": "<"},#Amyloid beta 1-42
			"2000000463":{"value":52, "operator": ">"},	#p-tau
			"2000000298":{"value":375, "operator": ">"}	#t-tau
			}


	###################################################
	#	Public methods in the harmonization stage	  #
	###################################################
	def harmonizer(self, rawData):
		row = self.__dealWithDate(rawData)
		if len(row) == 0:
			return []

		variableConcept = str(row["VariableConcept"])
		toRemove = ["2000000609"]
		for variable in toRemove:
			if variable in variableConcept:
				return []
		
		if "2000000540" in variableConcept:
			return self.__dealWithDiagnosisDate(row)
		if "2000000488" in variableConcept:
			return self.__dealWithAge(row)

		if "2000000323" in variableConcept:
			return self.__dealWithAlcohol(row)
		if "2000000013" in variableConcept:
			return self.__dealWithApoE(row)
		if "2000000435" in variableConcept:
			return self.__dealWithSmoke(row)
		if "2000000618" in variableConcept:
			return self.__dealWithStroopVersion(row)

		if "2000000276" in variableConcept or 	\
		   "2000000278" in variableConcept or 	\
		   "2000000280" in variableConcept:		#STR1 STR2 STR3
		   return self.__dealWithStroops(row)

		if "2000000708" in variableConcept:
			return self.__dealWithCST0X(row)

		if "2000000613" in variableConcept:
			return self.__dealWithSRTImmediate(row)
		if "2000000094" in variableConcept:
			return self.__dealWithSRTDelayed(row)

		if "2000000639" in variableConcept:
			return self.__dealWithOtherCerebrovascularDisorders(row)
		if "2000000637" in variableConcept:
			return self.__dealWithOtherCardiovascularDisorders(row)
		if "2000000412" in variableConcept:
			return self.__dealWithOtherSomaticDisorders(row)
			

		if "2000000642" in variableConcept:
			print("check this")
			return []

		#1 - Yes and 0 or 2 - No. Not all used, just to save work i added all of the comorbidities
		listOfNumericVariablesToConvertToYesOrNo = ["2000000640", "2000000326", "2000000357", "2000000390", "2000000643",
			"2000000383", "2000000337", "2000000441","2000000341",  "2000000360", "2000000367",  "2000000400", "2000000381", "2000000382", 
			"2000000396", "2000000402", "2000000403", "2000000438", "2000000363", "2000000384", "2000000385", "2000000405", "2000000378", 
			"2000000408", "2000000416", "2000000434", "2000000334", "2000000379", "2000000415", "2000000331", "2000000469", "2000000470", 
			"2000000410", "2000000343", "2000000432", "2000000433"
			]
		for variable in listOfNumericVariablesToConvertToYesOrNo:
			if variable in variableConcept:
				return self.__covertNumericVariablesToYesOrNo(row, yes='1', no=['0', '2'])

		#Last cleaning	
		listOfNumericVariablesToClean = ["2000000617", "2000000625", "2000000215", "2000000216", "2000000138",
			"2000000323", "2000000582"]
		for variable in listOfNumericVariablesToClean:
			if variable in variableConcept:
				return self.__cleanTrashInNumericVariables(row)
		return row	

	def addMissingRows(self):
		missingRows = []
		missingRows += self.__processStroops()
		missingRows += self.__processCST0X()
		missingRows += self.__processSRTImmediate()
		missingRows += self.__processSRTDelayed()
		missingRows += self.__processOtherCerebrovascularDisorders()
		missingRows += self.__processOtherCardiovascularDisorders()
		missingRows += self.__processOtherSomaticDisorders()
		#missingRows += self.__process...
		#....
		return missingRows

	###############
	#	Private	  #
	###############
	def __dealWithDate(self, rawData):
		import datetime
		row = dict(rawData)
		row['testdag'] = str(row['testdag']) + "-" + str(row['testmnd']) + "-" + str(row['testjr'])
		row['Gebdag'] = str(row['Gebdag']) + "-" + str(row['Gebmnd']) + "-" + str(row['Gebjr'])
		try:
			date = datetime.datetime.strptime(row['testdag'], '%d-%m-%Y')
		except ValueError:
			self.logger.error(errorType	= INVALID_DATE, 
						 	  patientID = row["PIN"], 
						 	  variable 	= "testdag/testmnd/testjr", 
						 	  measure 	= row['testdag'],
						 	  msg 		= "One of this three variables has a invalid value leading to a invalid date!")
			return []
		try:
			date = datetime.datetime.strptime(row['Gebdag'], '%d-%m-%Y')
		except ValueError:
			self.logger.error(errorType	= INVALID_DATE, 
						 	  patientID = row["PIN"], 
						 	  variable 	= "Gebdag/Gebmnd/Gebjr", 
						 	  measure 	= row['Gebdag'],
						 	  msg 		= "One of this three variables has a invalid value leading to a invalid date!")
			return []
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
			row["MeasureConcept"] = 2000000239#No
		else:
			self.logger.warn(warnType	= WRONG_VALUE, 
						 	patientID 	= row["PIN"], 
						 	variable 	= row["Variable"], 
						 	measure 	= row["Measure"],
						 	msg 		= "The variable was not one of the expected!")
			return []
		return row

	def __dealWithSmoke(self, row):
		row["MeasureNumber"] = None
		if row["Measure"] == '1':
			row["MeasureConcept"] = 2000000239#No
		elif row["Measure"] == '2':
			print("fix past concept missing in CONCEPT.CSV")
			row["MeasureString"] = "Past"
			#row["MeasureConcept"] = todo
		elif row["Measure"] == '3':
			row["MeasureConcept"] = 2000000238#YES
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

	def __dealWithStroopVersion(self, row):
		if row["Measure"] == '10':
			self.patientWithStroopV10.append(row["PIN"])
			return row
		return []

	def __dealWithStroops(self, row):
		self.stroops.append(row)
		return []

	def __dealWithCST0X(self, row):
		if row["MeasureNumber"] != None:
			if row["PIN"] not in self.CST0X:
				self.CST0X[row["PIN"]] = {}
			if row["testdag"] not in self.CST0X[row["PIN"]]:
				self.CST0X[row["PIN"]][row["testdag"]] = []
			self.CST0X[row["PIN"]][row["testdag"]].append(row)
		if row["MeasureString"] != None: 
			self.logger.warn(warnType	= WRONG_VALUE, 
						 	patientID 	= row["PIN"], 
						 	variable 	= row["Variable"], 
						 	measure 	= row["Measure"],
						 	msg 		= "The variable was not one of the expected!")
		return []

	def __dealWithSRTImmediate(self, row):
		if row["MeasureNumber"] != None:
			if row["PIN"] not in self.SRTImmediate:
				self.SRTImmediate[row["PIN"]] = {}
			if row["testdag"] not in self.SRTImmediate[row["PIN"]]:
				self.SRTImmediate[row["PIN"]][row["testdag"]] = []
			self.SRTImmediate[row["PIN"]][row["testdag"]].append(row)
		return []

	def __dealWithSRTDelayed(self, row):
		if row["MeasureNumber"] != None:
			if row["PIN"] not in self.SRTDelayed:
				self.SRTDelayed[row["PIN"]] = {}
			if row["testdag"] not in self.SRTDelayed[row["PIN"]]:
				self.SRTDelayed[row["PIN"]][row["testdag"]] = []
			self.SRTDelayed[row["PIN"]][row["testdag"]].append(row)
		return []

	def __dealWithOtherCerebrovascularDisorders(self, row):
		if row["Variable"] == "CEVD3":#CEVD3 	If something is mentioned Other Cerebrovascular Disorders should be yes
			row["MeasureConcept"] = 2000000238#YES
			row["MeasureNumber"] = None
			row["MeasureString"] = None
			
		if row["Variable"] == "CEREDIAGYN":
			row = self.__covertNumericVariablesToYesOrNo(row, yes='1', no=['0', '2'])

		if len(row) != 0:
			self.otherCerebrovascularDisorders[row["PIN"]] = row
		return []

	def __dealWithOtherCardiovascularDisorders(self, row):
		if row["Variable"] == "CAVD7":#CAVD7 	if there is text in CAVD7, Other Cardiovascular Disorders should be Yes
			row["MeasureConcept"] = 2000000238#YES
			row["MeasureNumber"] = None
			row["MeasureString"] = None
			
		if row["Variable"] == "CARDIOVASCYN":
			row = self.__covertNumericVariablesToYesOrNo(row, yes='1', no=['0', '2'])
			
		if len(row) != 0:
			self.otherCardiovascularDisorders[row["PIN"]] = row
		return []

	def __dealWithOtherSomaticDisorders(self, row):
		if row["Variable"] == "SOMD4":#SOMD4 	If there is text in this variable Somatic Disorders=Yes
			row["MeasureConcept"] = 2000000238#YES
			row["MeasureNumber"] = None
			row["MeasureString"] = None
			
		if row["Variable"] == "SOMYN":
			row = self.__covertNumericVariablesToYesOrNo(row, yes='1', no=['0', '2'])
			
		if len(row) != 0:
			self.otherSomaticDisorders[row["PIN"]] = row
		return []

	def __processStroops(self):
		results = []
		for row in self.stroops:
			if row["PIN"] in self.patientWithStroopV10:
				results.append(row)
		return results

	def __processCST0X(self):
		results = []
		for patient in self.CST0X:
			visits = self.CST0X[patient]
			for date in visits:
				count = 0
				sumCST = 0
				originalVariables = ""
				originalMeasures = ""
				for row in visits[date]:
					sumCST += row["MeasureNumber"]
					count += 1
					originalVariables += str(row["Variable"]) + ", "
					originalMeasures += str(row["MeasureNumber"]) + ", "
				lastRow = visits[date][-1]
				lastRow["MeasureNumber"] = sumCST/count
				lastRow["Measure"] = originalMeasures[:-2]
				lastRow["Variable"] = originalVariables[:-2]
				results.append(lastRow)
		return results

	def __processSRTImmediate(self):
		results = []
		for patient in self.SRTImmediate:
			visits = self.SRTImmediate[patient]
			for date in visits:
				sumCST = 0
				originalVariables = ""
				originalMeasures = ""
				for row in visits[date]:
					sumCST += row["MeasureNumber"]
					originalVariables += str(row["Variable"]) + "+"
					originalMeasures += str(row["MeasureNumber"]) + "+"
				lastRow = visits[date][-1]
				lastRow["MeasureNumber"] = sumCST
				lastRow["Measure"] = originalMeasures[:-1]
				lastRow["Variable"] = originalVariables[:-1]
				results.append(lastRow)
		return results

	def __processSRTDelayed(self):
		results = []
		for patient in self.SRTDelayed:
			visits = self.SRTDelayed[patient]
			for date in visits:
				sumCST = 0
				originalVariables = ""
				originalMeasures = ""
				for row in visits[date]:
					sumCST += row["MeasureNumber"]
					originalVariables += str(row["Variable"]) + "+"
					originalMeasures += str(row["MeasureNumber"]) + "+"
				lastRow = visits[date][-1]
				lastRow["MeasureNumber"] = sumCST
				lastRow["Measure"] = originalMeasures[:-1]
				lastRow["Variable"] = originalVariables[:-1]
				results.append(lastRow)
		return results

	def __processOtherCerebrovascularDisorders(self):
		results = []
		for patientID in self.otherCerebrovascularDisorders:
			results.append(self.otherCerebrovascularDisorders[patientID]) 
		return results

	def __processOtherCardiovascularDisorders(self):
		results = []
		for patientID in self.otherCardiovascularDisorders:
			results.append(self.otherCardiovascularDisorders[patientID]) 
		return results

	def __processOtherSomaticDisorders(self):
		results = []
		for patientID in self.otherSomaticDisorders:
			results.append(self.otherSomaticDisorders[patientID]) 
		return results

	def __covertNumericVariablesToYesOrNo(self, row, yes, no):
		row["MeasureNumber"] = None
		row["MeasureString"] = None
		if row["Measure"] in no:
			row["MeasureConcept"] = 2000000239#No
		elif row["Measure"] in yes:
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

	def set_person_day_of_birth(self, value):
		return value.str.split('-').str[0]


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
