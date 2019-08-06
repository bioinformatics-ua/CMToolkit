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

	###################################################
	#	Public methods in the harmonization stage	  #
	###################################################
	def harmonizer(self, row):
		variableConcept = str(row["VariableConcept"])
		if "2000000049" in variableConcept:
			return self.__readCeradWLRounds(row)
		if "2000000468" in variableConcept:
			return self.__dealWithFamilyHistoryDementia(row)
		if "2000000434" in variableConcept:
			return self.__dealWithSleepDisordersClinicalInformation(row)
		if "2000000609" in variableConcept:
			return self.__dealWithGender(row)
		return row	

	def addMissingRows(self):
		missingRows = []
		missingRows += self.__processCeradWLRounds()
		#missingRows += self.__process...
		#....
		return missingRows

	###############
	#	Private	  #
	###############
	def __readCeradWLRounds(self, row):
		self.ceradWLRounds += [row]
		row['VariableConcept'] = None
		return row

	def __dealWithFamilyHistoryDementia(self, row):
		#convert 0 = no or 1 = yes
		row["MeasureNumber"] = None
		if row["Measure"] == '0':
			row["MeasureConcept"] = 2000000239
		if row["Measure"] == '1':
			row["MeasureConcept"] = 2000000238
		return row

	def __dealWithSleepDisordersClinicalInformation(self, row):
		if row["Measure"] == "n.b.":
			row["MeasureString"] = None
		return row

	def __dealWithGender(self, row):
		#convert {1:8507, 0:8532}
		row["MeasureNumber"] = None
		if row["Measure"] == '0':
			row["MeasureConcept"] = 8532
		if row["Measure"] == '1':
			row["MeasureConcept"] = 8507
		return row

	def __processCeradWLRounds(self):
		results = []
		if len(self.ceradWLRounds) > 0:
			#key will be (patient, date)
			measureDict = {}
			sumOfMeasuresDict = {} 
			for entry in self.ceradWLRounds:
				if (entry["Patient ID"], entry["Date of neuropsychological testing"]) in sumOfMeasuresDict:
					sumOfMeasuresDict[(entry["Patient ID"], entry["Date of neuropsychological testing"])] += int(entry["Measure"])
					measureDict[(entry["Patient ID"], entry["Date of neuropsychological testing"])] += "," + str(entry["Measure"])
				else:
					sumOfMeasuresDict[(entry["Patient ID"], entry["Date of neuropsychological testing"])] = int(entry["Measure"])
					measureDict[(entry["Patient ID"], entry["Date of neuropsychological testing"])] = str(entry["Measure"])
			for entry in sumOfMeasuresDict:
				results += [{
					'Patient ID':entry[0],
					'Date of neuropsychological testing':entry[1],
					'Variable': '[Cerad WL round 1, Cerad WL round 2, Cerad WL round 3]', 
					'Measure': measureDict[entry],
					'MeasureNumber': sumOfMeasuresDict[entry], 
					'VariableConcept': '2000000049', 
					'MeasureConcept': None
				}]
		self.ceradWLRounds = []
		return results
		
	#######################################
	#	Harmonizer during the migration	  #
	#######################################
	def filter_person(self, cohort):
		cohort = cohort[pd.notnull(cohort['Sex'])]
		return cohort.reset_index(drop=True)

	#Person
	def set_person_gender_concept_id(self, value):
		gender_map = {1:8507, 0:8532}
		return value.map(gender_map)

	#Observation
	def set_observation_observation_type_concept_id(self, value):
		return pd.Series("2000000260", index=Observation.ObservationIDSet)

Baseline.main(Harmonizer)
