from SAHGlobalVariables import SAHGlobalVariables

NO 		= 2000000239
YES 	= 2000000238

class AbnormalCalculator():	
	def __init__(self, cutOffs):
		self.cutOffs = cutOffs

	def calculate(self, rowData, patientIDLabel, variableConcept):
		row = dict(rowData)
		patientID = str(row[patientIDLabel])
		res = None

		'''
		-> amyloid beta 1-42
		-> total tau
		-> phosphory tau 
		'''
		if "2000000070" in variableConcept and "2000000297" in self.cutOffs:
			res = self.__compareWithCutOff(row['MeasureNumber'], self.cutOffs["2000000297"])
			row['Variable'] 		= "Amyloid Beta 1-42 Abnormal"
			row['VariableConcept'] 	= "2000000071"
		
		#HA CUT OFF QUE É > E OUTROS QUE É <


		if "2000000075" in variableConcept and "2000000298" in self.cutOffs:
			res = self.__compareWithCutOff(row['MeasureNumber'], self.cutOffs["2000000298"])
			row['Variable'] 		= "Total Tau Abnormal"
			row['VariableConcept'] 	= "2000000076"
		if "2000000070" in variableConcept and "2000000463" in self.cutOffs:
			res = self.__compareWithCutOff(row['MeasureNumber'], self.cutOffs["2000000463"])
			row['Variable'] 		= "Amyloid Beta 1-42 Abnormal"
			row['VariableConcept'] 	= "2000000463"
		#Sintax: if variable code in variableConcept and cutOff code in self.cutOffs
		#if "2000000xxx" in variableConcept and "2000000yyy" in self.cutOffs:
		#	res = self.__compareWithCutOff(row['MeasureNumber'], self.cutOffs["2000000xxx"])
		#	row['Variable'] 		= "XXXXXX"
		#	row['VariableConcept'] 	= "2000000zzz"

		if res != None:
			row['Measure'] 			= "Calculated automatically"
			row['MeasureConcept'] 	= res
			return row
		return [] 

	def __compareWithCutOff(self, baseNumber, cutOffValue):
		print("Calma que falta acabar uma coisinha nos CUT OFFS")
		if baseNumber < cutOffValue:
			return YES
		return NO
