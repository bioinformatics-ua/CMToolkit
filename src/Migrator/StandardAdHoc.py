from Singleton import Singleton
from ZcoreCalculator import ZcoreCalculator
from SAHGlobalVariables import SAHGlobalVariables
from datetime import date
import datetime

class StandardAdHoc(object, metaclass=Singleton):
	def __init__(self):
		self.patientIDLabel = None
		self.zcoreCalculator = ZcoreCalculator()
		
		#Temporary variables calculated based on other variables
		self.ageMeasurement = [] 
	
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

			zcore = self.zcoreCalculator.calculateZscore(row, self.patientIDLabel, variableConcept)
			outputDataDict += [zcore]
		
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

	#########################
	#	Processing stage 	#
	#########################
	def __processRow(self, row, patientID, variableConcept):
		if "2000000480" in variableConcept:
			return self.__dealWithDateOfBloodCollection(row, patientID)
		return self.__cleaner(row, variableConcept, patientID)

	def __dealWithDateOfBloodCollection(self, row, patientID):
		return self.__dealWithDatesDifferencesInDays(row, patientID)

	def __dealWithDatesDifferencesInDays(self, row, patientID):
		try:
			delta = self.__compareDates(SAHGlobalVariables.dateOfDiagnosis[patientID], row["Measure"], '%d-%M-%Y')
			if delta:
				row["MeasureNumber"] = round(delta.days/365, 5)
				row["MeasureString"] = None
				return row
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
		return row

	#############################################
	#	Final stage 							#
	#											#
	# This stage runs one time for each file 	#
	#############################################
	def __addNewMeasurements(self):
		newMeasurements = []
		newMeasurements += self.__addMeasurement(self.ageMeasurement)
		#missingRows += self.__process...
		#....
		return newMeasurements

	def __addMeasurement(self, listOfMeasurements):
		results = []
		if len(listOfMeasurements) > 0:
			results = listOfMeasurements.copy()
			listOfMeasurements.clear()
		return results