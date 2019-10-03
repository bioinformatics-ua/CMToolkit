from Singleton import Singleton
from ZcoreCalculator import ZcoreCalculator
from CutOffCalculator import CutOffCalculator
from SAHGlobalVariables import SAHGlobalVariables
from datetime import date
import datetime

class StandardAdHoc(object, metaclass=Singleton):
	def __init__(self, cutOffs):
		self.patientIDLabel 	= None
		self.zcoreCalculator 	= ZcoreCalculator()
		self.cutOffsCalculator	= None
		if cutOffs != None:
			self.cutOffsCalculator	= CutOffCalculator(cutOffs)
		
		#Base variables
		self.bodyLength = {}
		self.weight = {}

		#Temporary variables calculated based on other variables
		self.ageMeasurement = [] 
		self.bodyMass		= []
	
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

	def __loadDateOfDiagnosis(self, row, patientID):
		if row['Measure'] != "":
			SAHGlobalVariables.dateOfDiagnosis[patientID] = row['Measure']
		if len(SAHGlobalVariables.birthdayDate) > 0:
			self.__calculateAge(patientID)

	def __loadYearsOfEducation(self, row, patientID):
		if row['Measure'] != "":
			SAHGlobalVariables.yearsOfEducation[patientID] = int(row['Measure'])
	
	def __loadBirthdayDate(self, row, patientID):
		if row['Measure'] != "":
			SAHGlobalVariables.birthdayDate[patientID] = row['Measure']
		if len(SAHGlobalVariables.dateOfDiagnosis) > 0:
			self.__calculateAge(patientID)

	def __loadGender(self, row, patientID):
		if row['MeasureConcept'] != "":
			SAHGlobalVariables.gender[patientID] = row['MeasureConcept']	

	def __loadBodyLength(self, row, patientID):
		if row['Measure'] != "":
			self.bodyLength[patientID] = row['MeasureNumber']
		if len(self.weight) > 0:
			self.__calculateBodyMassIndex(patientID)

	def __loadWeight(self, row, patientID):
		if row['Measure'] != "":
			self.weight[patientID] = row['MeasureNumber']
		if len(self.bodyLength) > 0:
			self.__calculateBodyMassIndex(patientID)

	def __calculateAge(self, patientID):
		try:
			delta = self.__compareDates(SAHGlobalVariables.dateOfDiagnosis[patientID], SAHGlobalVariables.birthdayDate[patientID], '%d-%M-%Y')
			if delta:
				age = int(delta.days/365)
				SAHGlobalVariables.age[patientID] = age
				self.ageMeasurement += [{
					self.patientIDLabel:patientID,
					#add observation date to do
					'Age':age,
					'Variable': 'Calculated age', 
					'Measure': "",
					'MeasureNumber': age, 
					'VariableConcept': '2000000488', 
					'MeasureConcept': None
				}]
		except:
			pass

	def __calculateBodyMassIndex(self, patientID):
		try:
			bmi = self.weight[patientID]/((self.bodyLength[patientID]/100)*(self.bodyLength[patientID]/100))
			self.bodyMass += [{
				self.patientIDLabel:patientID,
				#add observation date to do
				'Body Mass Index':bmi,
				'Variable': 'Calculated bmi', 
				'Measure': "",
				'MeasureNumber': bmi, 
				'VariableConcept': '2000000339', 
				'MeasureConcept': None
			}]
		except Exception as ex:
			print('Body Mass Index not calculated for user id:', ex)
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
					print("The difference of dates on the patient", str(patientID), "is incorrect! Value:", str(round(delta.days/365, 5)),\
						"Diagnosis date:", SAHGlobalVariables.dateOfDiagnosis[patientID], row["Measure"], "\t", row)
		except Exception as e:
			pass
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
		#missingRows += self.__addMeasurement...
		#....
		return newMeasurements

	def __addMeasurement(self, listOfMeasurements):
		results = []
		if len(listOfMeasurements) > 0:
			results = listOfMeasurements.copy()
			listOfMeasurements.clear()
		return results