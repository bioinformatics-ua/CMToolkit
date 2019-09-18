from SAHGlobalVariables import SAHGlobalVariables

NO 		= 2000000239
YES 	= 2000000238

Relation = {
	"2000000070":{"cutOff"	:"2000000297", "cutOffName"		:"Amyloid Beta 1-42 Cut-off",
				  "abnormal":"2000000071", "abnormalName"	:"Amyloid Beta 1-42 Abnormal"},
	"2000000073":{"cutOff"	:"2000000463", "cutOffName"		:"Phosphorylated Tau Cut-off", 
				  "abnormal":"2000000074", "abnormalName"	:"Phosphorylated Tau Abnormal"},
	"2000000075":{"cutOff"	:"2000000298", "cutOffName"		:"Total Tau Cut-off", 
				  "abnormal":"2000000076", "abnormalName"	:"Total Tau Abnormal"}
}

class CutOffCalculator():	
	def __init__(self, cutOffs):
		'''
		cutOffs = "cutOffId":{"value":xxxx, "operator": "<" or >"}
		or
		cutOffs = "cutOffId":{"conditionalMethod": method()}
		'''
		self.cutOffs = cutOffs

	def calculate(self, rowData, variableConcept):
		if variableConcept in Relation:
			if Relation[variableConcept]["cutOff"] in self.cutOffs:
				if "conditionalMethod" in self.cutOffs[Relation[variableConcept]["cutOff"]]:
					#This is a method
					operator, value = self.cutOffs[Relation[variableConcept]["cutOff"]]["conditionalMethod"](dict(rowData))
					if value == None:
						return []
				else:
					operator = self.cutOffs[Relation[variableConcept]["cutOff"]]["operator"]
					value = self.cutOffs[Relation[variableConcept]["cutOff"]]["value"]
				cutOffResult = self.__cutOffBuilder(dict(rowData), variableConcept, operator, value)
				abdnormalResult = self.__abnormalBuilder(dict(rowData), variableConcept, operator, value)
				return [cutOffResult, abdnormalResult]
		return [] 

	def __cutOffBuilder(self, row, variableConcept, operator, value):
		row['Variable'] 		= Relation[variableConcept]["cutOffName"]
		row['VariableConcept'] 	= Relation[variableConcept]["cutOff"]
		row['Measure'] 			= "Calculated automatically"
		row['MeasureNumber'] 	= None
		row['MeasureString'] 	= operator + str(value)
		return row

	def __abnormalBuilder(self, row, variableConcept, operator, cutOffValue):
		value = row['Measure']
		row['Variable'] 		= Relation[variableConcept]["abnormalName"]
		row['VariableConcept'] 	= Relation[variableConcept]["abnormal"]
		row['Measure'] 			= "Calculated automatically"
		row['MeasureNumber'] 	= None
		if operator == ">":
			row['MeasureConcept'] = YES if float(value) > float(cutOffValue) else NO
		elif operator == "<":
			row['MeasureConcept'] = YES if float(value) < float(cutOffValue) else NO
		else:
			print("Abnormal calculator error:", operator, "operator not recognized! Variable:", Relation[variableConcept]["abnormalName"])
			return []
		return row
