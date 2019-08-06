from SAHGlobalVariables import SAHGlobalVariables

class ZcoreCalculator():	
	def calculateZscore(self, row, patientIDLabel, variableConcept):
		patientID = str(row[patientIDLabel])
		result = None

		if "2000000210" in variableConcept: 
			result = self.__calculateZCoreTMTA(patientID, row['MeasureNumber'])
			if result:
				row['Variable'] 		= "TMT-A Z-score"
				row['VariableConcept'] 	= "2000000211"
				row['MeasureNumber'] 	= result
		#if "2000000212" in variableConcept: 
		#	row['Variable'] 		= "TMT-B Z-score"
		#	row['VariableConcept'] 	= "2000000213"
		#	row['Measure'] 			= row['MeasureNumber'] = 
		#if "2000000009" in variableConcept: 
		#	row['Variable'] 		= "Animals Fluency 1 min Z-score"
		#	row['VariableConcept'] 	= "2000000008"
		#	row['Measure'] 			= row['MeasureNumber'] = 
		#if "2000000045" in variableConcept:
		#	row['Variable'] 		= "CERAD Figures Z-score"
		#	row['VariableConcept'] 	= "2000000046"
		#	row['Measure'] 			= row['MeasureNumber'] = 
		#if "2000000047" in variableConcept:
		#	row['Variable'] 		= "CERAD WL delayed Z-score"
		#	row['VariableConcept'] 	= "2000000048"
		#	row['Measure'] 			= row['MeasureNumber'] = 
		#if "2000000049" in variableConcept: 
		#	row['Variable'] 		= "CERAD WL immediate Z-score"
		#	row['VariableConcept'] 	= "2000000050"
		#	row['Measure'] 			= row['MeasureNumber'] = 
		#if "2000000206" in variableConcept: 
		#	row['Variable'] 		= "Story Delayed Z-score"
		#	row['VariableConcept'] 	= "2000000207"
		#	row['Measure'] 			= row['MeasureNumber'] = 
		#if "2000000208" in variableConcept: 
		#	row['Variable'] 		= "Story Immediate Z-score"
		#	row['VariableConcept'] 	= "2000000209"
		#	row['Measure'] 			= row['MeasureNumber'] = 

		#Waiting for confirmation
		#if "2000000xxx" in variableConcept: #CERAD Figures Delayed
		#	row['Variable'] 		= "CERAD Figures Delayed Z-score"
		#	row['VariableConcept'] 	= ""
		#	row['Measure'] 			= row['MeasureNumber'] = 
		#if "2000000xxx" in variableConcept: #CERAD WL Recognition
		#	row['Variable'] 		= "CERAD WL Recognition Z-score"
		#	row['VariableConcept'] 	= ""
		#	row['Measure'] 			= row['MeasureNumber'] = 

		if result != None:
			row['Measure'] 			= "Calculated automatically"
		return [] #zcore entry

	def __calculateZCoreTMTA(self, patientID, measure):
		try:
			gender = SAHGlobalVariables.gender[patientID] #Male:8507, Female:8532
			eduy = SAHGlobalVariables.yearsOfEducation[patientID]
			age = SAHGlobalVariables.age[patientID]
			if gender == 8532 and eduy < 13 and age > 50.99:
				return (44.4-measure)/13.7
			if gender == 8532 and eduy < 13 and age > 69.99:
				return (48.1-measure)/15.3
			if gender == 8532 and eduy < 13 and age > 79.99:
				return (53.6-measure)/20.4
			if gender == 8532 and eduy > 12 and age > 50:
				return (39.7-measure)/11
			if gender == 8532 and eduy > 12 and age > 69.99:
				return (51-measure)/22.3
			if gender == 8532 and eduy > 12 and age > 79.99:
				return (61-measure)/20.4
			if gender == 8507 and eduy < 13 and age > 50:
				return (44.6-measure)/13.7
			if gender == 8507 and eduy < 13 and age > 69.99:
				return (50.1-measure)/16.2
			if gender == 8507 and eduy < 13 and age > 79.99:
				return (62-measure)/22.1
			if gender == 8507 and eduy > 12 and age > 50:
				return (43.8-measure)/17.2
			if gender == 8507 and eduy > 12 and age > 69.99:
				return (45.8-measure)/15.1
			if gender == 8507 and eduy > 12 and age > 79.99:
				return (59.6-measure)/12.2
		except:
			return None