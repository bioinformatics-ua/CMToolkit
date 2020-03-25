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
			row['VariableConcept'] 	= "2000000010"
		if "2000000045" in variableConcept:
			res = self.__calculateZCoreCERADFigures(patientID, row['MeasureNumber'])
			row['Variable'] 		= "CERAD Figures Z-score"
			row['VariableConcept'] 	= "2000000046"

		if "2000000015" in variableConcept:
			res = self.__calculateZCoreAVLTDelayed(patientID, row['MeasureNumber'])
			row['Variable'] 		= "AVLT Delayed Z-score"
			row['VariableConcept'] 	= "2000000016"
		if "2000000017" in variableConcept:
			res = self.__calculateZCoreAVLTImmediate(patientID, row['MeasureNumber'])
			row['Variable'] 		= "AVLT Immediate Z-score"
			row['VariableConcept'] 	= "2000000018"

		if "2000000276" in variableConcept:
			res = self.__calculateZCoreStroopPart1(patientID, row['MeasureNumber'])
			row['Variable'] 		= "Stroop Part 1 Z-score"
			row['VariableConcept'] 	= "2000000277"
		if "2000000278" in variableConcept:
			res = self.__calculateZCoreStroopPart2(patientID, row['MeasureNumber'])
			row['Variable'] 		= "Stroop Part 2 Z-score"
			row['VariableConcept'] 	= "2000000279"
		if "2000000280" in variableConcept:
			res = self.__calculateZCoreStroopPart3(patientID, row['MeasureNumber'])
			row['Variable'] 		= "Stroop Part 3 Z-score"
			row['VariableConcept'] 	= "2000000281"
		if "2000000424" in variableConcept:
			res = self.__calculateZCoreSDST(patientID, row['MeasureNumber'])
			row['Variable'] 		= "SDST Z-score"
			row['VariableConcept'] 	= "2000000425"


		#TO DO
		#if "2000000047" in variableConcept:
		#	res = self.__calculateZCoreXXXXXX(patientID, row['MeasureNumber'])
		#	row['Variable'] 		= "CERAD WL delayed Z-score"
		#	row['VariableConcept'] 	= "2000000048"
		#if "2000000049" in variableConcept: 
		#	res = self.__calculateZCoreXXXXXX(patientID, row['MeasureNumber'])
		#	row['Variable'] 		= "CERAD WL immediate Z-score"
		#	row['VariableConcept'] 	= "2000000050"

		#Asked to Isabelle
		#if "2000000206" in variableConcept: 
		#	res = self.__calculateZCoreXXXXXX(patientID, row['MeasureNumber'])
		#	row['Variable'] 		= "Story Delayed Z-score"
		#	row['VariableConcept'] 	= "2000000207"
		#if "2000000208" in variableConcept: 
		#	res = self.__calculateZCoreXXXXXX(patientID, row['MeasureNumber'])
		#	row['Variable'] 		= "Story Immediate Z-score"
		#	row['VariableConcept'] 	= "2000000209"


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
		print("Confirm edulow and eduhigh")
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

	def __calculateZCoreAVLTDelayed(self, patientID, measure):
		gender, eduy, age = self.__getInitialVariables(patientID)
		if eduy == None or age == None or (gender != MALE and gender != FEMALE):
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
		sex = 1 if gender == MALE else 0
		print("Confirm edulow and eduhigh")
		return (measure - (10.924 + (-0.073 * (age - 50)) + (-0.0009 * (age - 50)**2) + (-1.197 * sex) + (-0.844 * edulow) + (0.424 * eduhigh)))/2.496

	def __calculateZCoreAVLTImmediate(self, patientID, measure):
		gender, eduy, age = self.__getInitialVariables(patientID)
		if eduy == None or age == None or (gender != MALE and gender != FEMALE):
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
		sex = 1 if gender == MALE else 0
		print("Confirm edulow and eduhigh")
		return (measure - (49.672 + (-0.247 * (age - 50)) + (-0.0033 * (age - 50)**2) + (-4.227 * gender) + (-3.055 * edulow) + (2.496 * eduhigh)))/7.826

	def __calculateZCoreStroopPart1(self, patientID, measure):
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
		print("Confirm edulow and eduhigh")
		return ((1/measure)-(0.01566 + 0.000315*age + -0.00112*edulow + 0.001465*eduhigh + (-0.0000032 * age * age)))/0.0034

	def __calculateZCoreStroopPart2(self, patientID, measure):
		print("Asked to Isabelle")
		return None

	def __calculateZCoreStroopPart3(self, patientID, measure):
		gender, eduy, age = self.__getInitialVariables(patientID)
		if eduy == None or age == None or (gender != MALE and gender != FEMALE):
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
		sex = 1 if gender == MALE else 0
		print("Confirm edulow and eduhigh")
		return ((1/measure)-(0.001926 + 0.000348*age + 0.0002244*sex + -0.0006982*edulow + 0.001015*eduhigh + -0.000003522*age**2))/0.002

	def __calculateZCoreSDST(self, patientID, measure):
		gender, eduy, age = self.__getInitialVariables(patientID)
		if age == None:
			return None
		if age > 51 and measure > -1:
			return -3
		if age > 51 and measure > 3:
			return -2.7
		if age > 51 and measure > 4:
			return -2.3
		if age > 51 and measure > 6:
			return -2
		if age > 51 and measure > 7:
			return -1.7
		if age > 51 and measure > 8:
			return -1.3
		if age > 51 and measure > 12:
			return -1
		if age > 51 and measure > 16:
			return -0.7
		if age > 51 and measure > 21:
			return -0.3
		if age > 51 and measure > 25:
			return 0
		if age > 51 and measure > 28:
			return 0.3
		if age > 51 and measure > 32:
			return 0.7
		if age > 51 and measure > 35:
			return 1
		if age > 51 and measure > 38:
			return 1.3
		if age > 51 and measure > 41:
			return 1.7
		if age > 51 and measure > 42:
			return 2
		if age > 51 and measure > 46:
			return 2.3
		if age > 51 and measure > 54:
			return 2.7
		if age > 51 and measure > 56:
			return 3
		if age > 69 and measure > -1:
			return -3
		if age > 69 and measure > 2:
			return -2.7
		if age > 69 and measure > 3:
			return -2.3
		if age > 69 and measure > 6:
			return 2
		if age > 69 and measure > 7:
			return -1.7
		if age > 69 and measure > 8:
			return -1.30
		if age > 69 and measure > 9:
			return -1
		if age > 69 and measure > 11:
			return -0.7
		if age > 69 and measure > 14:
			return -0.3
		if age > 69 and measure > 18:
			return 0
		if age > 69 and measure > 20:
			return 0.3
		if age > 69 and measure > 24:
			return 0.7
		if age > 69 and measure > 27:
			return 1
		if age > 69 and measure > 30:
			return 1.3
		if age > 69 and measure > 35:
			return 1.7
		if age > 69 and measure > 41:
			return 2
		if age > 69 and measure > 46:
			return 2.3
		if age > 69 and measure > 48:
			return 2.7
		if age > 69 and measure > 51:
			return 3
		if age > 75 and measure > -1:
			return -3
		if age > 75 and measure > 0:
			return -2.7
		if age > 75 and measure == 1:
			return -2.3
		if age > 75 and measure > 1:
			return -2
		if age > 75 and measure > 2:
			return -1.7
		if age > 75 and measure > 4:
			return -1.3
		if age > 75 and measure > 6:
			return -1
		if age > 75 and measure > 8:
			return -0.7
		if age > 75 and measure > 11:
			return -0.3
		if age > 75 and measure > 15:
			return 0
		if age > 75 and measure > 18:
			return 0.3
		if age > 75 and measure > 20:
			return 0.7
		if age > 75 and measure > 24:
			return 1
		if age > 75 and measure > 28:
			return 1.3
		if age > 75 and measure > 32:
			return 1.7
		if age > 75 and measure > 41:
			return 2
		if age > 75 and measure > 45:
			return 2.3
		if age > 75 and measure > 47:
			return 2.7
		if age > 75 and measure > 50:
			return 3
