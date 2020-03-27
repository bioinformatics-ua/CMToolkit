from Singleton import Singleton
from ZcoreCalculator import ZcoreCalculator
from CutOffCalculator import CutOffCalculator
from SAHGlobalVariables import SAHGlobalVariables
from MigratorArgs import MigratorArgs
from Logger import *
from datetime import date
import datetime

NO 		= 2000000239
YES 	= 2000000238

class StandardAdHoc(object, metaclass=Singleton):
	def __init__(self, cutOffs):
		self.logger				= Logger()
		self.formatDate			= MigratorArgs().formatdate
		self.patientIDLabel 	= None
		self.zcoreCalculator 	= ZcoreCalculator()
		self.cutOffsCalculator	= None
		if cutOffs != None:
			self.cutOffsCalculator	= CutOffCalculator(cutOffs)
		
		#Base variables
		self.bodyLength = {}
		self.weight 	= {}

		#Temporary variables calculated based on other variables
		self.ageMeasurement  	= [] 
		self.bodyMass		 	= []
		self.comorbidities	 	= {}
		self.comorbidityYes	 	= []
		self.apoE			 	= []

		#Variables to create the Priority <domain> (Attention, Executive Functioning, Language, Immediate and Delayed Memory)
		self.priorityDomains 	= {}
		self.memorySourceList 	= []	  
		self.priorityDomainsIDs = { #IDs sorted by priority
			"Attention":{ #Priority Attention Type
				"source":["2000000210", "2000000276", "2000000278", "2000000424"],
				"targetValue":"2000000180", "targetType":"2000000282", "zscore":"2000000181"
				}, 	
			"Executive":{ #Priority Executive Type
				"source":["2000000212", "2000000280"],		
				"targetValue":"2000000182", "targetType":"2000000283", "zscore":"2000000183"
				},					 	
			"Language":	{ #Priority Language Type
				"source":["2000000009",       "2000000144", "2000000146", "2000000011"    ], 
				"targetValue":"2000000184", "targetType":"2000000284", "zscore":"2000000185"
				},					 	
			"MemoryDelayed":	{ #Priority Memory Type
				"source":self.memorySourceList, 
				"targetValue":"2000000186", "targetType":"2000000285", "zscore":"2000000187"
				},						 	
			"MemoryImmediate":	{ #Priority Memory Type
				"source":self.memorySourceList, 
				"targetValue":"2000000188", "zscore":"2000000189"
				},					 	
			"Visuoconstruction":	{ #Priority Visuoconstruction Type
				"source":["2000000054", "2000000045", "2000000062"     ], 
				"targetValue":"2000000419", "targetType":"2000000657", "zscore":"2000000420"
				},	
			#...
			}
		self.conceptNames = {#This dictionary was created to simplify the method for Pirority domain, consider refactor this
			"2000000210":"Trail Making Test A",
			"2000000276":"Stroop 1",
			"2000000278":"Stroop 2",
			"2000000424":"Symbol Digit Substitution Task",

			"2000000212":"Trail Making Test B", 
			"2000000280":"Stroop 3",

			"2000000009":"Animal Fluency 1 min", 
			#"Category Fluency 1 min"
			"2000000144":"Letter Fluency 1 min", 
			"2000000146":"Letter Fluency 2 min", 
			"2000000011":"Animal Fluency 2 min", 
			#"Boston Naming Test (15/30/60 items)"
			#"Any picture naming test"
			
			#Priority List of primary memory tests:
			#1=RAVLT
			#2=CERAD
			#3=Grober-Buschke FCSRT
			#4=Story recall test
			#5=Logical memory
			#6=Hopkins
			#7=VAT
			#8=Story recall Brescia
			#9=Recall Rey figure
			#10=MMSE
			#11=ADAS-Cog
			#12=10 word list
			#13=immediate recall 10 word list

			#Priority list Visuoconstruction:
			"2000000054":"Rey complex Figure copy",
			"2000000045":"Copy of CERAD Figures",
			"2000000062":"Clock Drawing",
			#4. Any other copying task- Qual
		}

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
			self.__dealWithAge(row, patientID)
		if "2000000609" in variableConcept:
			self.__loadGender(row, patientID)
		if "2000000388" in variableConcept:
			self.__loadBodyLength(row, patientID)
		if "2000000462" in variableConcept:
			self.__loadWeight(row, patientID)
		if "2000000013" in variableConcept:
			self.__loadExtraApoE(row, patientID)

		for domain in self.priorityDomainsIDs:
			for variable in self.priorityDomainsIDs[domain]["source"]:
				if variable in variableConcept:
					self.__loadPriorityDomains(row, variableConcept)

		#Comorbidities to calculate yes
		allComorbidities = {
			"2000000637":{
				"name":"Cardiovascular Disorders",
				"concepts":["2000000326", "2000000341", "2000000357", "2000000360", "2000000367", "2000000390", "2000000400"]
			},
			"2000000638":{
				"name":"Cardiovascular Risk Factors",
				"concepts":["2000000381", "2000000382", "2000000383", "2000000396", "2000000402"]
			},
			"2000000639":{
				"name":"Cerebrovascular Disorders",
				"concepts":["2000000337", "2000000403", "2000000438", "2000000441"]
			},
			"2000000640":{
				"name":"Endocrine Disorders",
				"concepts":["2000000363", "2000000384", "2000000385", "2000000405"]
			},
			"2000000641":{
				"name":"Neurological Disorders",
				"concepts":["2000000378", "2000000408", "2000000416", "2000000434"]
			},
			"2000000473":{
				"name":"Other Cardiac Diseases",
				"concepts":["2000000334", "2000000379", "2000000415"]
			},
			"2000000642":{
				"name":"Psychiatric Disorders",
				"concepts":["2000000331", "2000000469", "2000000470", "2000000410"]
			},
			"2000000643":{
				"name":"Somatic Disorders",
				"concepts":["2000000343", "2000000432", "2000000433", "2000000412"]
			}
		}
		for comorbidity in allComorbidities:
			for variable in allComorbidities[comorbidity]["concepts"]:
				if variable in variableConcept:
					return self.__addComorbiditiesSubClass(row, patientID, allComorbidities[comorbidity]["name"], comorbidity)

	def __dealWithAge(self, row, patientID):#refactor this
		if(row['Measure'].isdigit()):
			self.ageMeasurement.append(row)
			SAHGlobalVariables.age[patientID] = int(row['Measure'])
		else:
			self.__loadBirthdayDate(row, patientID)

	def __loadDateOfDiagnosis(self, row, patientID):
		if row['Measure'] != "":
			SAHGlobalVariables.dateOfDiagnosis[patientID] = row['Measure']
		if len(SAHGlobalVariables.birthdayDate) > 0:
			if patientID in SAHGlobalVariables.birthdayDate:
				self.__calculateAge(row, patientID)

	def __loadYearsOfEducation(self, row, patientID):
		if row['Measure'] != "":
			SAHGlobalVariables.yearsOfEducation[patientID] = int(float(row['Measure']))
	
	def __loadBirthdayDate(self, row, patientID):
		if row['Measure'] != "":
			SAHGlobalVariables.birthdayDate[patientID] = row['Measure']
		if len(SAHGlobalVariables.dateOfDiagnosis) > 0:
			if patientID in SAHGlobalVariables.dateOfDiagnosis:
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

	def __loadExtraApoE(self, row, patientID):
		if row['MeasureString'] == row['MeasureString']:#Verify if is NaN
			measures = row['MeasureString'].split("/")
			if len(measures) == 2:
				self.apoE += [
					self.__mergeDictionaries(row, {
						self.patientIDLabel:patientID,
						'Variable': row['Variable'],
						'Measure': row['Measure'],
						'VariableConcept': '2000000320', #ApoE Allele 1
						'MeasureConcept': None,
						'MeasureNumber': None,
						'MeasureString': measures[0]
						}), 
					self.__mergeDictionaries(row, {
						self.patientIDLabel:patientID,
						'Variable': row['Variable'],
						'Measure': row['Measure'],
						'VariableConcept': '2000000321', #ApoE Allele 2
						'MeasureConcept': None,
						'MeasureNumber': None,
						'MeasureString': measures[1]
						}),
					self.__mergeDictionaries(row, {
						self.patientIDLabel:patientID,
						'Variable': row['Variable'],
						'Measure': row['Measure'],
						'VariableConcept': '2000000014', #ApoE4 Carrier
						'MeasureConcept': YES if measures[0] == "4" or measures[1] == "4" else NO,
						'MeasureNumber': None,
						'MeasureString': None
						})]
			else:
				self.logger.warn(warnType	= WRONG_VALUE, 
								 patientID 	= patientID, 
								 variable 	= row['Variable'], 
								 measure 	= row['Measure'],
								 msg 		= "This method was not able to split the measure by /")
		else:
			self.logger.warn(warnType	= MISSING_VALUE, 
							 patientID 	= patientID, 
							 variable 	= row['Variable'], 
							 measure 	= row['Measure'],
							 msg 		= "This method was not able to split the measure by / because the measure is NaN")
	
	def __loadPriorityDomains(self, row, variableConcept):
		if variableConcept not in self.priorityDomains:
			self.priorityDomains[variableConcept] = []
		self.priorityDomains[variableConcept].append(row)

	def __addComorbiditiesSubClass(self, row, patientID, variable, conceptID):
		if row["MeasureConcept"] == YES:
			if variable not in self.comorbidities:
				self.comorbidities[variable] = []
			if len(list(filter(lambda line: line[self.patientIDLabel] == patientID, self.comorbidities[variable]))) == 0:
				self.comorbidities[variable] += [self.__mergeDictionaries(row, {
					self.patientIDLabel:patientID,
					'Variable': "Ontology rule " + variable, 
					'Measure': "",
					'MeasureNumber': None, 
					'VariableConcept': conceptID,
					'MeasureConcept': YES
				})]
				self.__addComorbidity(row, patientID)

	def __addComorbidity(self, row, patientID):
		if len(list(filter(lambda line: line[self.patientIDLabel] == patientID, self.comorbidityYes))) == 0:
			self.comorbidityYes += [self.__mergeDictionaries(row, {
				self.patientIDLabel:patientID,
				'Variable': 'Ontology rule (Comorbidity - Yes)', 
				'Measure': "",
				'MeasureNumber': None, 
				'VariableConcept': "2000000525",
				'MeasureConcept': YES
			})]

	def __calculateAge(self, row, patientID):
		try:
			delta = self.__compareDates(SAHGlobalVariables.dateOfDiagnosis[patientID], SAHGlobalVariables.birthdayDate[patientID])
			if delta:
				age = int(delta.days/365)
				SAHGlobalVariables.age[patientID] = age
				self.ageMeasurement += [self.__mergeDictionaries(row, {
					self.patientIDLabel:patientID,
					'Age':age,
					'Variable': 'Calculated age', 
					'Measure': "",
					'MeasureNumber': age, 
					'VariableConcept': '2000000488', 
					'MeasureConcept': None
				})]
		except:
			var = "Calculated age"
			msg = "Age not calculated due to missing variable."
			if patientID not in SAHGlobalVariables.dateOfDiagnosis:
				var = "Date of Diagnosis"
			elif patientID not in SAHGlobalVariables.birthdayDate:
				var = "Birthday Date"
			else:
				msg = "Age calculation fail maybe due to the date format."
			self.logger.warn(warnType	= MISSING_VALUE, 
							 patientID 	= patientID, 
							 variable 	= var, 
							 msg 		= msg)

	def __calculateBodyMassIndex(self, row, patientID):
		try:
			bmi = self.weight[patientID]/((self.bodyLength[patientID]/100)*(self.bodyLength[patientID]/100))
			if bmi > 30:
				value = YES
			else:
				value = NO
			self.bodyMass += [self.__mergeDictionaries(row, {
				self.patientIDLabel:patientID,
				'Body Mass Index':bmi,
				'Variable': 'Calculated bmi', 
				'Measure': "",
				'MeasureNumber': bmi, 
				'VariableConcept': '2000000339', 
				'MeasureConcept': None
			}), self.__mergeDictionaries(row, {
				self.patientIDLabel:patientID,
				'Variable': 'Calculated obesity', 
				'Measure': "",
				'MeasureNumber': None, 
				'VariableConcept': '2000000396', 
				'MeasureConcept': value
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
			"2000000170":{"min":0, "max":4},
			"2000000171":{"min":0, "max":4},
			"2000000168":{"min":0, "max":8},
			"2000000121":{"min":0, "max":52},
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
		else:
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
			delta = self.__compareDates(SAHGlobalVariables.dateOfDiagnosis[patientID], row["Measure"])
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

	def __compareDates(self, initalDate, finalDate):
		try:
			d0 = datetime.datetime.strptime(initalDate, self.formatDate)
			d1 = datetime.datetime.strptime(finalDate, self.formatDate)
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
		for comorbidity in self.comorbidities:
			newMeasurements += self.__addMeasurement(self.comorbidities[comorbidity])
		newMeasurements += self.__addMeasurement(self.comorbidityYes)
		newMeasurements += self.__addMeasurement(self.apoE)
		#Priority Domains
		newMeasurements += self.__addPriorityDomains()
		#newMeasurements += self.__addMeasurement...
		#....
		return newMeasurements

	def __addMeasurement(self, listOfMeasurements):
		results = []
		if len(listOfMeasurements) > 0:
			results = listOfMeasurements.copy()
			listOfMeasurements.clear()
		return results

	def __addPriorityDomains(self):
		results = []
		for domain in self.priorityDomainsIDs:
			tmpResults = []
			for conceptID in self.priorityDomainsIDs[domain]["source"]:
				if conceptID in self.priorityDomains:
					for row in self.priorityDomains[conceptID]:
						if conceptID in row['VariableConcept']:
							#Entry with value
							newRow = row.copy()
							newRow['VariableConcept'] = self.priorityDomainsIDs[domain]["targetValue"]
							tmpResults.append(newRow)

							#Entry with type
							if "targetType" in self.priorityDomainsIDs[domain]:
								newRow = row.copy()
								newRow['VariableConcept'] = self.priorityDomainsIDs[domain]["targetType"]
								newRow['Measure'] = self.conceptNames[conceptID]
								newRow['MeasureConcept'] = None
								newRow['MeasureNumber'] = None
								newRow['MeasureString'] = self.conceptNames[conceptID]
								tmpResults.append(newRow)

							#Entry with Z-Score
							zcore = self.zcoreCalculator.calculate(row, self.patientIDLabel, conceptID)
							if isinstance(zcore, list):
								for entry in zcore:
									entry['VariableConcept'] = self.priorityDomainsIDs[domain]["zscore"]
									tmpResults.append(entry)
							else:
								zcore['VariableConcept'] = self.priorityDomainsIDs[domain]["zscore"]
								tmpResults.append(zcore)

				if len(tmpResults) > 0:
					results += tmpResults
					break
		#What is missing:
		#ZcoreCalculator.allCalculatedZScores
		#Priority list Attention tests:
		# "2000000210" 1. Trail Making Test A
		# "2000000276" 2. Stroop 1
		# "2000000278" 3. Stroop 2
		# "2000000424" 4. Symbol Digit Substitution Task

		#Priority list Executive functioning:
		# "2000000212" 1. Trail Making Test B
		# "2000000280" 2. Stroop 3

		#Priority list language tests:
		# "2000000009" 1. Animal Fluency 1 min
		# ?????????? 2. Category Fluency 1 min - Não existe
		# "2000000144" 3. Letter Fluency 1 min
		# "2000000146" 4. Any type of fluency 2 min
		# "2000000011" 
		# ?????????? 5. Boston Naming Test (15/30/60 items) - Quais?
		# ?????????? 6. Any picture naming test - DO 80 Picture Naming?

		#Priority List of primary memory tests:
		#1=RAVLT
		#2=CERAD
		#3=Grober-Buschke FCSRT
		#4=Story recall test
		#5=Logical memory
		#6=Hopkins
		#7=VAT
		#8=Story recall Brescia
		#9=Recall Rey figure
		#10=MMSE
		#11=ADAS-Cog
		#12=10 word list
		#13=immediate recall 10 word list

		#Priority list Visuoconstruction:
		#1. Rey complex Figure copy
		#2. Copy of CERAD Figures
		#3. Clock Drawing
		#4. Any other copying task
		return results