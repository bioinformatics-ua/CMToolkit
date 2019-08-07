from SAHGlobalVariables import SAHGlobalVariables

class CutOffCalculator():	
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
			res = "<"+str(self.cutOffs["2000000297"])
			row['Variable'] 		= "Amyloid Beta 1-42 Cut-off"
			row['VariableConcept'] 	= "2000000297"
		#Sintax: if variable code in variableConcept and cutOff code in self.cutOffs
		#if "2000000xxx" in variableConcept and "2000000yyy" in self.cutOffs:
		#	res = "<"+str(self.cutOffs["2000000yyy"])
		#	row['Variable'] 		= "XXXXXX"
		#	row['VariableConcept'] 	= "2000000yyy"

		if res != None:
			row['Measure'] 			= "Calculated automatically"
			row['MeasureString'] 	= res
			return row
		return [] 