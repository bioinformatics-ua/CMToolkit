from Singleton import Singleton
from ZcoreCalculator import ZcoreCalculator
from CutOffCalculator import CutOffCalculator
from SAHGlobalVariables import SAHGlobalVariables
from Logger import *
from datetime import date
import datetime

NO 		= 2000000239
YES 	= 2000000238

class StandardAdHoc(object, metaclass=Singleton):
	def __init__(self, cutOffs):
		self.logger				= Logger()
		self.patientIDLabel 	= None
		self.zcoreCalculator 	= ZcoreCalculator()
		self.cutOffsCalculator	= None
		if cutOffs != None:
			self.cutOffsCalculator	= CutOffCalculator(cutOffs)
		
		#Base variables
		self.bodyLength = {}
		self.weight 	= {}

		#Temporary variables calculated based on other variables
		self.ageMeasurement 			= [] 
		self.bodyMass					= []
		self.cardiovascularDisordersYes	= []
		self.comorbidityYes				= []

	def definePatientIDLabel(self, patientIDLabel):
		self.patientIDLabel = patientIDLabel

	def processLoadingStage(self, dataDict):
		for row in dataDict:
			variableConcept = str(row["VariableConcept"])
			self.__loadingStage(row, str(row[self.patientIDLabel]), variableConcept)

	def processCalculationAndAppendingStage(self, dataDict):
		outputDataDict = []
		for row in dataDict:
			variableConcept = str(row["VariableConcept"])
			if (self.__validateMeasureContent(row, str(row[self.patientIDLabel]), variableConcept)):
				data = self.__processRow(row, str(row[self.patientIDLabel]), variableConcept)
				if isinstance(data, list):
					outputDataDict += data
				else:
					outputDataDict += [data]

				zcore = self.zcoreCalculator.calculate(row, self.patientIDLabel, variableConcept)
				if isinstance(zcore, list):
					outputDataDict += zcore
				else:
					outputDataDict += [zcore]

				if self.cutOffsCalculator != None:
					cutOff = self.cutOffsCalculator.calculate(row, variableConcept)
					outputDataDict += cutOff

		outputDataDict += self.__addNewMeasurements()

		return outputDataDict

	#####################
	#	Loading stage 	#
	#####################
	def __loadingStage(self, row, patientID, variableConcept):
		if "2000000540" in variableConcept:
			self.__loadDateOfDiagnosis(row, patientID)
		if "2000000554" in variableConcept:
			self.__loadYearsOfEducation(row, patientID)
		if "2000000488" in variableConcept:
			self.__loadBirthdayDate(row, patientID)
		if "2000000609" in variableConcept:
			self.__loadGender(row, patientID)
		if "2000000388" in variableConcept:
			self.__loadBodyLength(row, patientID)
		if "2000000462" in variableConcept:
			self.__loadWeight(row, patientID)

		#Cardiovascular Disorders (Yes)
		listOfCardiovascularDisorders = ["2000000326", "2000000341", "2000000357", "2000000360", 
			"2000000367", "2000000390", "2000000400"]
		for variable in listOfCardiovascularDisorders:
			if variable in variableConcept:
				return self.__addCardiovascularDisorders(row, patientID)


	def __loadDateOfDiagnosis(self, row, patientID):
		if row['Measure'] != "":
			SAHGlobalVariables.dateOfDiagnosis[patientID] = row['Measure']
		if len(SAHGlobalVariables.birthdayDate) > 0:
			self.__calculateAge(row, patientID)

	def __loadYearsOfEducation(self, row, patientID):
		if row['Measure'] != "":
			SAHGlobalVariables.yearsOfEducation[patientID] = int(row['Measure'])
	
	def __loadBirthdayDate(self, row, patientID):
		if row['Measure'] != "":
			SAHGlobalVariables.birthdayDate[patientID] = row['Measure']
		if len(SAHGlobalVariables.dateOfDiagnosis) > 0:
			self.__calculateAge(row, patientID)

	def __loadGender(self, row, patientID):
		if row['MeasureConcept'] != "":
			SAHGlobalVariables.gender[patientID] = row['MeasureConcept']	

	def __loadBodyLength(self, row, patientID):
		if row['Measure'] != "":
			self.bodyLength[patientID] = row['MeasureNumber']
		if len(self.weight) > 0:
			self.__calculateBodyMassIndex(row, patientID)

	def __loadWeight(self, row, patientID):
		if row['Measure'] != "":
			self.weight[patientID] = row['MeasureNumber']
		if len(self.bodyLength) > 0:
			self.__calculateBodyMassIndex(row, patientID)

	def __addCardiovascularDisorders(self, row, patientID):
		if row["MeasureConcept"] == YES:
			if len(list(filter(lambda line: line[self.patientIDLabel] == patientID, self.cardiovascularDisordersYes))) == 0:
				self.cardiovascularDisordersYes += [self.__mergeDictionaries(row, {
					self.patientIDLabel:patientID,
					#add observation date to do
					'Variable': 'Ontology rule (Cardiovascular Disorders - Yes)', 
					'Measure': "",
					'MeasureNumber': None, 
					'VariableConcept': "2000000637",
					'MeasureConcept': YES
				})]
				self.__addComorbidity(row, patientID)

	def __addComorbidity(self, row, patientID):
		if len(list(filter(lambda line: line[self.patientIDLabel] == patientID, self.comorbidityYes))) == 0:
			self.comorbidityYes += [self.__mergeDictionaries(row, {
				self.patientIDLabel:patientID,
				#add observation date to do
				'Variable': 'Ontology rule (Comorbidity - Yes)', 
				'Measure': "",
				'MeasureNumber': None, 
				'VariableConcept': "2000000526",
				'MeasureConcept': YES
			})]

	def __calculateAge(self, row, patientID):
		try:
			delta = self.__compareDates(SAHGlobalVariables.dateOfDiagnosis[patientID], SAHGlobalVariables.birthdayDate[patientID], '%d-%M-%Y')
			if delta:
				age = int(delta.days/365)
				SAHGlobalVariables.age[patientID] = age
				self.ageMeasurement += [self.__mergeDictionaries(row, {
					self.patientIDLabel:patientID,
					#add observation date to do
					'Age':age,
					'Variable': 'Calculated age', 
					'Measure': "",
					'MeasureNumber': age, 
					'VariableConcept': '2000000488', 
					'MeasureConcept': None
				})]
		except:
			pass

	def __calculateBodyMassIndex(self, row, patientID):
		try:
			bmi = self.weight[patientID]/((self.bodyLength[patientID]/100)*(self.bodyLength[patientID]/100))
			self.bodyMass += [self.__mergeDictionaries(row, {
				self.patientIDLabel:patientID,
				'Body Mass Index':bmi,
				'Variable': 'Calculated bmi', 
				'Measure': "",
				'MeasureNumber': bmi, 
				'VariableConcept': '2000000339', 
				'MeasureConcept': None
			})]
		except Exception as ex:
			var = "Body Mass Index"
			if patientID not in self.weight:
				var = "Weight"
			elif patientID not in self.bodyLength:
				var = "Length"
			self.logger.warn(warnType	= MISSING_VALUE, 
							 patientID 	= patientID, 
							 variable 	= var, 
							 msg 		= "Body Mass Index not calculated due to missing variable")

	def __mergeDictionaries(self, row, newData):
		for key in row:
			if key not in newData:
				newData[key] = row[key]
		return newData
	#########################
	#	Validation stage 	#
	#########################
	def __validateMeasureContent(self, row, patientID, variableConcept):
		''' Validate measures. This is a work in process. 
		Default is True because we considered everything valid until something wrong happen.'''
		
		#other validation by variableConcept
		#if "xxxxxxxxxx" in variableConcept:
		#	self.__xxx(row, ...)

		listOfRanges = {
			"2000000173":{"min":0, "max":144},
			}
		for variable in listOfRanges:
			if variable in variableConcept:
				return self.__isVariableInNumericRange(variableConcept=variableConcept, 
													   patientID=patientID,
													   measure=row["Measure"], 
													   minimum=listOfRanges[variable]["min"], 
													   maximum=listOfRanges[variable]["max"])
		return True

	def __isVariableInNumericRange(self, variableConcept, patientID, measure, minimum, maximum):
		if measure.isdigit():
			if minimum <= float(measure) <= maximum:
				return True
			self.logger.warn(warnType	= OUT_OF_RANGE, 
							 patientID 	= patientID, 
							 variable 	= variableConcept, 
							 measure 	= measure,
							 msg 		= "The range of values defined for this variable are {}-{}".format(minimum, maximum))
		self.logger.warn(warnType	= WRONG_TYPE, 
						 patientID 	= patientID, 
						 variable 	= variableConcept, 
						 measure 	= measure)
		return False

	#########################
	#	Processing stage 	#
	#########################
	def __processRow(self, row, patientID, variableConcept):
		if "2000000480" in variableConcept:
			return self.__dealWithDatesDifferencesInDays(row, patientID)
		if "2000000479" in variableConcept:
			return self.__dealWithDatesDifferencesInDays(row, patientID)
		if "2000000482" in variableConcept:
			return self.__dealWithDatesDifferencesInDays(row, patientID)
		if "2000000477" in variableConcept:
			return self.__dealWithDatesDifferencesInDays(row, patientID)
		return self.__cleaner(row, variableConcept, patientID)

	def __dealWithDatesDifferencesInDays(self, row, patientID):
		try:
			delta = self.__compareDates(SAHGlobalVariables.dateOfDiagnosis[patientID], row["Measure"], '%d-%M-%Y')
			if delta:
				if round(delta.days/365, 5) > -15 and round(delta.days/365, 5) < 15:
					row["MeasureNumber"] = round(delta.days/365, 5)
					row["MeasureString"] = None
					return row
				else:
					self.logger.warn(warnType	= INVALID_DATE, 
									 patientID 	= patientID, 
									 variable 	= row["Variable"], 
									 measure 	= round(delta.days/365, 5),
									 msg 		= "The difference of dates is too big (more than 15 years)")
		except Exception as e:
			var = row["Variable"]
			if patientID not in SAHGlobalVariables.dateOfDiagnosis:
				var = "Date Of Diagnosis"
			self.logger.warn(warnType	= MISSING_VALUE, 
							 patientID 	= patientID, 
							 variable 	= var, 
							 msg 		= "Missing date to calculate the difference of dates")
		return []

	def __compareDates(self, initalDate, finalDate, formatDate):
		try:
			d0 = datetime.datetime.strptime(initalDate, formatDate)
			d1 = datetime.datetime.strptime(finalDate, formatDate)
			return (d0 - d1)
		except:
			return None

	def __cleaner(self, row, variableConcept, patientID):
		if "2000000488" in variableConcept:
			return []
		if "2000000540" in variableConcept:
			return []
		return row

	#############################################
	#	Final stage 							#
	#											#
	# This stage runs one time for each file 	#
	#############################################
	def __addNewMeasurements(self):
		newMeasurements = []
		newMeasurements += self.__addMeasurement(self.ageMeasurement)
		newMeasurements += self.__addMeasurement(self.bodyMass)
		newMeasurements += self.__addMeasurement(self.cardiovascularDisordersYes)
		newMeasurements += self.__addMeasurement(self.comorbidityYes)
		#newMeasurements += self.__addMeasurement...
		#....
		return newMeasurements

	def __addMeasurement(self, listOfMeasurements):
		results = []
		if len(listOfMeasurements) > 0:
			results = listOfMeasurements.copy()
			listOfMeasurements.clear()
		return results