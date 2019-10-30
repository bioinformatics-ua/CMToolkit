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
			"2000000297":{"conditionalMethod": self.__calculateCutOffValues}, #Amyloid Beta 1-42 Cut-off
			"2000000298":{"conditionalMethod": self.__calculateCutOffValues}, #Total Tau Cut-off
			"2000000463":{"conditionalMethod": self.__calculateCutOffValues}  #Phosphorylated Tau Cut-off
			}

	def __calculateCutOffValues(self, row):
		'''
			CSF date before 03.12.2014:
				Cutoffs not available
			CSF date between 03.12.2014 and 31.12.2016:
				Cutoff: amyloid <600, cutoff t-tau >300, cutoff p-tau >60
			CSF date between 31.12.2016 and 28.11.2018:
				Cutoff amyloid <1000, cutoff t-tau >400, cutoff p-tau >62
			CSF date after 28.11.2018:
				Cutoff amyloid <680, cutoff t-tau >400, cutoff p-tau >62.
		'''
		try:
			date = datetime.datetime.strptime(row['Date of puncture (Liquor)'], '%d-%M-%Y')
		except:
			print("No date defined for the cutOffs, which is necessary in this cohort:\t", row)
			return None, None

		if date < datetime.datetime(2014, 12, 3):
			return None, None
		elif date < datetime.datetime(2016, 12, 31):
			if "2000000070" in row["VariableConcept"]:
				return "<", 600
			if "2000000073" in row["VariableConcept"]:
				return ">", 60
			if "2000000075" in row["VariableConcept"]:
				return ">", 300
		elif date < datetime.datetime(2018, 11, 28):
			if "2000000070" in row["VariableConcept"]:
				return "<", 1000
			if "2000000073" in row["VariableConcept"]:
				return ">", 62
			if "2000000075" in row["VariableConcept"]:
				return ">", 400
		else:
			if "2000000070" in row["VariableConcept"]:
				return "<", 680
			if "2000000073" in row["VariableConcept"]:
				return ">", 62
			if "2000000075" in row["VariableConcept"]:
				return ">", 400
		return None, None


	###################################################
	#	Public methods in the harmonization stage	  #
	###################################################
	def harmonizer(self, row):
		variableConcept = str(row["VariableConcept"])
		if "2000000049" in variableConcept:
			return self.__readCeradWLRounds(row)
		if "2000000051" in variableConcept:
			return self.__readCeradWLRecognition(row)
		if "2000000551" in variableConcept:
			return self.__readDiagnosisAndEtiology(row)
		if "2000000013" in variableConcept:
			self.__readApoE(row)

		if "2000000468" in variableConcept:
			return self.__dealWithFamilyHistoryDementia(row)
		if "2000000434" in variableConcept:
			return self.__dealWithSleepDisordersClinicalInformation(row)
		if "2000000609" in variableConcept:
			return self.__dealWithGender(row)
		if "2000000293" in variableConcept:
			return self.__dealWithCSFAssay(row)

		#Deal with the errors in the cohort
		if "2000000462" in variableConcept:
			return self.__dealWithWeight(row)
		if "2000000388" in variableConcept:
			return self.__dealWithHeight(row)
		if "2000000421" in variableConcept:
			return self.__dealWithPulseRate(row)
		if "2000000358" in variableConcept:
			return self.__dealWithCholesterol(row)
		if "2000000532" in variableConcept:
			return self.__dealWithCSFMeasure(row)
		if "2000000068" in variableConcept:
			return self.__dealWithAmyloidBeta138(row)

		return row	

	def addMissingRows(self):
		missingRows = []
		missingRows += self.__processCeradWLRounds()
		missingRows += self.__processCeralWLRecognition()
		missingRows += self.__processDiagnosisAndEtiology()
		#missingRows += self.__processApoE()
		#missingRows += self.__process...
		#....
		return missingRows

	###############
	#	Private	  #
	###############
	def __readCeradWLRounds(self, row):
		self.ceradWLRounds += [row]
		return []

	def __readCeradWLRecognition(self, row):
		self.ceradWLRecognition += [row]
		return []

	def __readApoE(self, row):
		self.apoE += [row]

	def __readDiagnosisAndEtiology(self, row):
		if row["Variable"] == "Diagnosis":
			self.diagnosis[row["Patient ID"]] = row
		if row["Variable"] == "Etiology":
			self.etiology[row["Patient ID"]] = row
		return []

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

	def __dealWithCSFAssay(self, row):
		'''
		CSF date before 03.12.2014:
			Assay: Innotest
		CSF date between 03.12.2014 and 31.12.2016:
			Assay: MSD
		CSF date after 31.12.2016:
			Assay: Luminex
		'''
		try:
			date = datetime.datetime.strptime(row['Date of puncture (Liquor)'], '%d-%M-%Y')
		except:
			print("No date defined in CSF Assay:\t", row)
			return []
		if date < datetime.datetime(2014, 12, 3):
			row["MeasureString"] = "Innotest"
		elif date < datetime.datetime(2016, 12, 31):
			row["MeasureString"] = "MSD"
		else:
			row["MeasureString"] = "Luminex"
		row["MeasureNumber"] = None
		return row

	def __dealWithWeight(self, row):
		if row["Measure"].isdigit():
			if float(row["Measure"]) < 0 or float(row["Measure"]) > 150:# remove invalid weights
				return []
			return row
		return []

	def __dealWithHeight(self, row):
		if row["Measure"].isdigit():
			if float(row["Measure"]) < 100 or float(row["Measure"]) > 230:# remove invalid heights
				return []
			return row
		return []

	def __dealWithPulseRate(self, row):
		if row["Measure"].isdigit():
			return row
		return []

	def __dealWithCholesterol(self, row):
		if row["Measure"].isdigit():
			return row
		return []

	def __dealWithCSFMeasure(self, row):
		if row["Measure"].isdigit():
			return row
		return []

	def __dealWithAmyloidBeta138(self, row):
		if row["Measure"].isdigit():
			return row
		return []

	def __processCeradWLRounds(self):
		results = []
		if len(self.ceradWLRounds) > 0:
			#key will be (patient, date)
			measureDict = {}
			sumOfMeasuresDict = {} 
			for entry in self.ceradWLRounds:
				if (entry["Patient ID"], entry["Date of neuropsychological testing"]) in sumOfMeasuresDict:
					sumOfMeasuresDict[(entry["Patient ID"], entry["Date of neuropsychological testing"])] += int(float(entry["Measure"]))
					measureDict[(entry["Patient ID"], entry["Date of neuropsychological testing"])] += "," + str(entry["Measure"])
				else:
					sumOfMeasuresDict[(entry["Patient ID"], entry["Date of neuropsychological testing"])] = int(float(entry["Measure"]))
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
		
	def __processCeralWLRecognition(self):
		results = []
		if len(self.ceradWLRecognition) > 0:
			#key will be (patient, date)
			measureDict = {}
			sumOfMeasuresDict = {} 
			for entry in self.ceradWLRecognition:
				if (entry["Patient ID"], entry["Date of neuropsychological testing"]) in sumOfMeasuresDict:
					sumOfMeasuresDict[(entry["Patient ID"], entry["Date of neuropsychological testing"])] += int(float(entry["Measure"]))
					measureDict[(entry["Patient ID"], entry["Date of neuropsychological testing"])] += "," + str(entry["Measure"])
				else:
					sumOfMeasuresDict[(entry["Patient ID"], entry["Date of neuropsychological testing"])] = int(float(entry["Measure"]))
					measureDict[(entry["Patient ID"], entry["Date of neuropsychological testing"])] = str(entry["Measure"])
			for entry in sumOfMeasuresDict:
				results += [{
					'Patient ID':entry[0],
					'Date of neuropsychological testing':entry[1],
					'Variable': '[Cerad WL recognition no, Cerad WL recognition yes]', 
					'Measure': measureDict[entry],
					'MeasureNumber': (sumOfMeasuresDict[entry] - 10), 
					'VariableConcept': '2000000051', 
					'MeasureConcept': None
				}]
		self.ceradWLRecognition = []
		return results

	def __processDiagnosisAndEtiology(self):
		''' Isabelle email (3/9/2019)		 
			If the column “Diagnosis” in the Berlin dataset =10, Diagnosis on transmart should be “MCI”, 
				independent of the collum “Etiology” in the Berlin dataset. This applies to n=60 patients
			If “Diagnosis” is 1, Diagnosis on transmart should be “SCI”. This applies to n=25 patients. 
			If Diagnosis is 81 or 8, Diagnosis on transmart should be “Depression”. This applies to n=81 patients
			If Diagnosis is 2 or 3, Diagnosis should be “Other" 
			If Diagnosis is 5,6 or 7 we need the category “Etiology” to define the type of dementia. 
				If (Diagnosis =>5 and <8) and Etiology=1 Diagnosis =AD
				If (Diagnosis =>5 and <8) and Etiology=2 Diagnosis =Mixed dementia
				If (Diagnosis =>5 and <8) and Etiology=3 Diagnosis =VAD
				If (Diagnosis =>5 and <8) and Etiology=5 Diagnosis =FTD
				If (Diagnosis =>5 and <8) and Etiology=8 Diagnosis =Other Dementia
		'''
		results = []
		for patient in self.diagnosis:
			row = self.diagnosis[patient]
			concept = None
			if str(row['Measure']) == "10":
				concept = "2000000254" #MCI
			elif str(row['Measure']) == "1":
				concept = "2000000256" #SCI
			elif str(row['Measure']) == "81" or str(row['Measure']) == "8":
				concept = "2000000470" #Depression
			elif str(row['Measure']) == "2" or str(row['Measure']) == "3":
				concept = "2000000700" #Other
			elif str(row['Measure']) == "5" or str(row['Measure']) == "6" or str(row['Measure']) == "7":
				if patient in self.etiology:
					if str(self.etiology[patient]['Measure']) == "1":
						concept = "2000000255" #AD
					elif str(self.etiology[patient]['Measure']) == "2":
						concept = "2000000701" #Mixed dementia
					elif str(self.etiology[patient]['Measure']) == "3":
						concept = "2000000685" #VAD
					elif str(self.etiology[patient]['Measure']) == "5":
						concept = "2000000665" #FTD
					elif str(self.etiology[patient]['Measure']) == "8":
						concept = "2000000699" #Other Dementia

			results += [{
				'Patient ID': patient,
				'Number of Visit': row['Number of Visit'],
				'Date of Diagnosis': row['Date of Diagnosis'],
				'Variable': row['Variable'],
				'Measure': row['Measure'],
				'VariableConcept': '2000000551',
				'MeasureConcept': concept,
				'MeasureNumber': None,
				'MeasureString': None
				}]
		self.diagnosis = {}
		return results

	def __processApoE(self):
		print("Check and remove this shit, because now we have a standard ad hoc method for this")
		results = []
		if len(self.apoE) > 0:
			for row in self.apoE:
				measures = row['Measure'].split("/")
				if len(measures) == 2:
					results += [{
						'Patient ID': row['Patient ID'],
						'Date of puncture (Liquor)': row['Date of puncture (Liquor)'],
						'Variable': row['Variable'],
						'Measure': row['Measure'],
						'VariableConcept': '2000000320', #ApoE Allele 1
						'MeasureConcept': None,
						'MeasureNumber': None,
						'MeasureString': measures[0]
						},{
						'Patient ID': row['Patient ID'],
						'Date of puncture (Liquor)': row['Date of puncture (Liquor)'],
						'Variable': row['Variable'],
						'Measure': row['Measure'],
						'VariableConcept': '2000000321', #ApoE Allele 2
						'MeasureConcept': None,
						'MeasureNumber': None,
						'MeasureString': measures[1]
						},{
						'Patient ID': row['Patient ID'],
						'Date of puncture (Liquor)': row['Date of puncture (Liquor)'],
						'Variable': row['Variable'],
						'Measure': row['Measure'],
						'VariableConcept': '2000000014', #ApoE4 Carrier
						'MeasureConcept': None,
						'MeasureNumber': None,
						'MeasureString': "Yes" if measures[0] == "4" or measures[1] == "4" else "No"
						}]
		self.apoE = []
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

	def set_person_year_of_birth(self, value):
		return pd.DatetimeIndex(value).year

	def set_person_month_of_birth(self, value):
		return pd.DatetimeIndex(value).month

	def set_person_day_of_birth(self, value):
		return pd.DatetimeIndex(value).day
	#Observation
	#def set_observation_observation_type_concept_id(self, value):
	#	return pd.Series("2000000260", index=Observation.ObservationIDSet)

Baseline.main(Harmonizer)
