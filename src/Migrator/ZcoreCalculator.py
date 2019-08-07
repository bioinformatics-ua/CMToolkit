from SAHGlobalVariables import SAHGlobalVariables

MALE 	= 8507
FEMALE 	= 8532

class ZcoreCalculator():
	def calculate(self, rowData, patientIDLabel, variableConcept):
		row = dict(rowData)
		patientID = str(row[patientIDLabel])
		res = None

		if "2000000210" in variableConcept: 
			res = self.__calculateZCoreTMTA(patientID, row['MeasureNumber'])
			row['Variable'] 		= "TMT-A Z-score"
			row['VariableConcept'] 	= "2000000211"
		if "2000000212" in variableConcept:  
			res = self.__calculateZCoreTMTB(patientID, row['MeasureNumber'])
			row['Variable'] 		= "TMT-B Z-score"
			row['VariableConcept'] 	= "2000000213"
		if "2000000009" in variableConcept: 
			res = self.__calculateZCoreAnimalsFluency1Min(patientID, row['MeasureNumber'])
			row['Variable'] 		= "Animals Fluency 1 min Z-score"
			row['VariableConcept'] 	= "2000000008"
		if "2000000045" in variableConcept:
			res = self.__calculateZCoreCERADFigures(patientID, row['MeasureNumber'])
			row['Variable'] 		= "CERAD Figures Z-score"
			row['VariableConcept'] 	= "2000000046"
		#if "2000000047" in variableConcept:
		#	res = self.__calculateZCoreXXXXXX(patientID, row['MeasureNumber'])
		#	row['Variable'] 		= "CERAD WL delayed Z-score"
		#	row['VariableConcept'] 	= "2000000048"
		#if "2000000049" in variableConcept: 
		#	res = self.__calculateZCoreXXXXXX(patientID, row['MeasureNumber'])
		#	row['Variable'] 		= "CERAD WL immediate Z-score"
		#	row['VariableConcept'] 	= "2000000050"
		#if "2000000206" in variableConcept: 
		#	res = self.__calculateZCoreXXXXXX(patientID, row['MeasureNumber'])
		#	row['Variable'] 		= "Story Delayed Z-score"
		#	row['VariableConcept'] 	= "2000000207"
		#if "2000000208" in variableConcept: 
		#	res = self.__calculateZCoreXXXXXX(patientID, row['MeasureNumber'])
		#	row['Variable'] 		= "Story Immediate Z-score"
		#	row['VariableConcept'] 	= "2000000209"

		#Waiting for confirmation
		#if "2000000xxx" in variableConcept:
		#	res = self.__calculateZCoreXXXXXX(patientID, row['MeasureNumber'])
		#	row['Variable'] 		= "CERAD Figures Delayed Z-score"
		#	row['VariableConcept'] 	= ""
		#if "2000000xxx" in variableConcept: 
		#	res = self.__calculateZCoreXXXXXX(patientID, row['MeasureNumber'])
		#	row['Variable'] 		= "CERAD WL Recognition Z-score"
		#	row['VariableConcept'] 	= ""

		if res != None:
			row['Measure'] 			= "Calculated automatically"
			row['MeasureNumber'] 	= res
			return row
		return [] #zcore entry

	def __getInitialVariables(self, patientID):
		try:
			gender = SAHGlobalVariables.gender[patientID] #Male:8507, Female:8532
			eduy = SAHGlobalVariables.yearsOfEducation[patientID]
			age = SAHGlobalVariables.age[patientID]
			return gender, eduy, age
		except:
			return None, None, None

	def __calculateZCoreTMTA(self, patientID, measure):
		gender, eduy, age = self.__getInitialVariables(patientID)
		if gender == FEMALE and eduy < 13 and age > 50.99:
			return (44.4-measure)/13.7
		if gender == FEMALE and eduy < 13 and age > 69.99:
			return (48.1-measure)/15.3
		if gender == FEMALE and eduy < 13 and age > 79.99:
			return (53.6-measure)/20.4
		if gender == FEMALE and eduy > 12 and age > 50:
			return (39.7-measure)/11
		if gender == FEMALE and eduy > 12 and age > 69.99:
			return (51-measure)/22.3
		if gender == FEMALE and eduy > 12 and age > 79.99:
			return (61-measure)/20.4
		if gender == MALE and eduy < 13 and age > 50:
			return (44.6-measure)/13.7
		if gender == MALE and eduy < 13 and age > 69.99:
			return (50.1-measure)/16.2
		if gender == MALE and eduy < 13 and age > 79.99:
			return (62-measure)/22.1
		if gender == MALE and eduy > 12 and age > 50:
			return (43.8-measure)/17.2
		if gender == MALE and eduy > 12 and age > 69.99:
			return (45.8-measure)/15.1
		if gender == MALE and eduy > 12 and age > 79.99:
			return (59.6-measure)/12.2
		return None
		
	def __calculateZCoreTMTB(self, patientID, measure):
		gender, eduy, age = self.__getInitialVariables(patientID)
		if gender == FEMALE and eduy < 13 and age > 50.99:
			return (106.6-measure)/37.9
		if gender == FEMALE and eduy < 13 and age > 69.99:
			return (138.3-measure)/58.9
		if gender == FEMALE and eduy < 13 and age > 79.99:
			return (141.6-measure)/42.5
		if gender == FEMALE and eduy > 12 and age > 50:
			return (95.1-measure)/35.9
		if gender == FEMALE and eduy > 12 and age > 69.99:
			return (107.6-measure)/40
		if gender == FEMALE and eduy > 12 and age > 79.99:
			return (145-measure)/42.5
		if gender == MALE and eduy < 13 and age > 50:
			return (117.8-measure)/50.9
		if gender == MALE and eduy < 13 and age > 69.99:
			return (141-measure)/65.6
		if gender == MALE and eduy < 13 and age > 79.99:
			return (190.7-measure)/69.9
		if gender == MALE and eduy > 12 and age > 50:
			return (96.9-measure)/34.2
		if gender == MALE and eduy > 12 and age > 69.99:
			return (104.7-measure)/31.7
		if gender == MALE and eduy > 12 and age > 79.99:
			return (124.6-measure)/34.2
		return None

	def __calculateZCoreAnimalsFluency1Min(self, patientID, measure):
		gender, eduy, age = self.__getInitialVariables(patientID)
		if eduy == None or age == None:
			return None
		elif eduy < 7:
			edulow=1
			eduhigh=0
		elif eduy > 6: 
			edulow=0
			eduhigh=0
		elif eduy > 12: 
			eduhigh=1
			edulow=0
		return (measure-(30.24+(-0.124*age)+(-11.42*edulow)+(5.861*eduhigh)+0.135*(age*edulow)-0.0404*(age*eduhigh)))/5.604

	def __calculateZCoreCERADFigures(self, patientID, measure):
		gender, eduy, age = self.__getInitialVariables(patientID)
		if gender == FEMALE and eduy < 13 and age > 50.99:
			return (measure - 10.1)/0.9
		if gender == FEMALE and eduy < 13 and age > 69.99:
			return (measure - 10)/1
		if gender == FEMALE and eduy < 13 and age > 79.99:
			return (measure - 9.5)/1.2
		if gender == FEMALE and eduy > 12 and age > 50:
			return (measure - 10.5)/0.7
		if gender == FEMALE and eduy > 12 and age > 69.99:
			return (measure - 10.5)/0.7
		if gender == FEMALE and eduy > 12 and age > 79.99:
			return (measure - 10.4)/0.5
		if gender == MALE and eduy < 13 and age > 50:
			return (measure - 10.4)/0.8
		if gender == MALE and eduy < 13 and age > 69.99:
			return (measure - 10.4)/0.8
		if gender == MALE and eduy < 13 and age > 79.99:
			return (measure - 9.8)/1.2
		if gender == MALE and eduy > 12 and age > 50:
			return (measure - 10.6)/0.6
		if gender == MALE and eduy > 12 and age > 69.99:
			return (measure - 10.6)/0.6
		if gender == MALE and eduy > 12 and age > 79.99:
			return (measure - 10.5)/0.8
		return None
