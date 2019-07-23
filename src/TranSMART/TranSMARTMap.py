from TranSMARTArgs import TranSMARTArgs
from sqlalchemy import create_engine
from TranSMARTConstants import TranSMARTConstants
import pathlib

class TranSMARTMap():
	def __init__(self, args):
		self.adHocHarmonization = None
		self.args 				= args
		self.engine				= create_engine(args.db["datatype"]+"://"+args.db["user"]+":"+args.db["password"]+"@"+args.db["server"]+":"+args.db["port"]+"/"+args.db["database"])
		self.observationsDict 	= set([TranSMARTConstants.DemographicSex, TranSMARTConstants.DemographicRace, TranSMARTConstants.DemographicEthnic, TranSMARTConstants.DemographicBirthYear])
		self.visitIndependent	= self.__readVisitIndependent()

	def __readVisitIndependent(self):
		visitIndependent = []
		with open(self.args.vioutput) as fp:
			for line in fp:
				visitIndependent += [line.split("\t")[0]]
		return visitIndependent

	def setAdHocMethods(self, adHocMethod):
		self.adHocHarmonization = adHocMethod()

	def createCSV(self):
		structure = self.__createStructure()
		tmStructure = self.__buildStructureForTM(structure)
		harmonizedStructure = self.__harmonizeStructureForRM(tmStructure)
		self.observationsDict = sorted(list(self.observationsDict))
		self.__writeCSV(harmonizedStructure)
		print(self.args.cohortoutputfile + " created")

	def __createStructure(self):
		newStructure = self.__loadObservations()
		newStructure = self.__loadPatientData(newStructure)
		return newStructure
	
	def __loadObservations(self):
		observationSet = self.engine.execute(TranSMARTConstants.observationQuery(self.args.db["schema"]))  
		newStructure = {}
		for row in observationSet:  
			person_id = row[TranSMARTConstants.ObservationPersonIdIndex]
			observation_concept_id = row[TranSMARTConstants.ObservationObsvationConceptIdIndex]

			if person_id in newStructure:
				newStructure[person_id][observation_concept_id] = self.__getObservation(row)
			else:
				newStructure[person_id] = {}
				newStructure[person_id][observation_concept_id] = self.__getObservation(row)
			self.__fulfillObsDict(observation_concept_id)
		return newStructure

	def __loadPatientData(self, newStructure):
		personSet = self.engine.execute(TranSMARTConstants.personQuery(self.args.db["schema"]))
		for row in personSet:  
			person_id = row[TranSMARTConstants.PersonPersonIdIndex]
			if person_id not in newStructure:
				newStructure[person_id] = {}
			newStructure[person_id][TranSMARTConstants.DemographicSex] 		= self.__convertNoneToEmptyString(row[TranSMARTConstants.PersonGenderNameIndex])
			newStructure[person_id][TranSMARTConstants.DemographicRace] 	= self.__convertNoneToEmptyString(row[TranSMARTConstants.PersonRaceNameIndex])
			newStructure[person_id][TranSMARTConstants.DemographicEthnic] 	= self.__convertNoneToEmptyString(row[TranSMARTConstants.PersonEthnicNameIndex])
			newStructure[person_id][TranSMARTConstants.DemographicBirthYear]= self.__convertNoneToEmptyString(row[TranSMARTConstants.PersonBirthYearIndex])
		return newStructure

	def __convertNoneToEmptyString(self, value):
		if value:
			return value
		return ""

	def __getObservation(self, row):
		if row[TranSMARTConstants.ObservationValuesAsConceptNameIndex] != None:
			return row[TranSMARTConstants.ObservationValuesAsConceptNameIndex]
		if row[TranSMARTConstants.ObservationValuesAsNumberIndex] != None:
			return row[TranSMARTConstants.ObservationValuesAsNumberIndex]
		return row[TranSMARTConstants.ObservationValuesAsStringIndex]

	def __fulfillObsDict(self, observation_concept_id):
		if observation_concept_id not in self.observationsDict:
			self.observationsDict.add(observation_concept_id)

	def __buildStructureForTM(self, structure):
		filledCohort = {}
		for row in structure:
			filledCohort[row] = structure[row]
			for obs in self.observationsDict:
				if obs not in filledCohort[row]:
					filledCohort[row][obs] = ""
		return filledCohort

	def __writeCSV(self, tmStructure):
		header = sorted(tmStructure[0])
		pathlib.Path(self.args.transmartdstdir).mkdir(parents=True, exist_ok=True) 
		foutput = open('{}{}'.format(self.args.transmartdstdir, self.args.cohortoutputfile), "w")
		foutput.write("Subject_ID")
		for colunmn in header:
			foutput.write("\t" + str(colunmn))
		foutput.write("\n")

		for row in sorted(tmStructure):#sort by patient id (not very important)
			rowData = sorted(tmStructure[row])
			foutput.write(str(row))
			for obsID in rowData:
				foutput.write("\t" + str(tmStructure[row][obsID]))
			foutput.write("\n")
		foutput.close()

	def createTMMap(self):
		#loadProtege_output.txt
		transmartMapping = {}
		protegeOutput = self.__loadRowsToMap()
		self.__writeColumnMap(protegeOutput)
		self.__createDefaultFiles()
		print("TranSMART load files created")

	def __loadRowsToMap(self):
		protegeOutput = {}
		with open(self.args.protegeoutput) as fp:
			for line in fp:
				row = line.strip().split("\t")
				if int(row[2]) in self.observationsDict:
					protegeOutput[int(row[2])] = row
		fp.close()
		return protegeOutput

	def __writeColumnMap(self, protegeOutput):
		foutput = open('{}{}'.format(self.args.transmartdstdir, "column_map.txt"), "w")
		foutput.write("Filename\tCategory_Code (tranSMART)\tColumn\tDataLabel\tdata_label_src\tControlVocab_cd\tData_type\n")
		foutput.write(self.args.cohortoutputfile + "\t\t1\tSUBJ_ID\t\t\t\n")
		for line in sorted(protegeOutput):
			row = protegeOutput[line] #['Weight (kg)', 'Clinical_Information+Vital_Signs', '2000000462']
			columnIndex = str(self.observationsDict.index(int(row[2]))+2)
			path = row[1]
			variableName = row[0]
			if variableName not in self.visitIndependent:
				path += "+Baseline"#Change this when I have more than one visit
			rowToWrite  = self.args.cohortoutputfile + "\t" + path + "\t" + columnIndex + "\t" + variableName + "\t\t\t\n"
			foutput.write(rowToWrite)
		foutput.close()

	def __createDefaultFiles(self):
		foutput = open('{}{}'.format(self.args.transmartdstdir, "clinical.params"), "w")
		foutput.write("COLUMN_MAP_FILE=column_map.txt\nRECORD_EXCLUSION_FILE=x\n")
		foutput.close()
		foutput = open('{}{}'.format(self.args.transmartdstdir, "study.params"), "w")
		foutput.write("STUDY_ID="+self.args.cohortname+"\n")
		foutput.write("SECURITY_REQUIRED=Y\n")
		foutput.write("TOP_NODE=\\Private Studies\\"+self.args.cohortname+"\n")
		foutput.close()

	def __harmonizeStructureForRM(self, tmStructure):
		#Write here the concepts that need to change due to the TranSMART restrictions
		#For instance the weight cannot have decimal values 78,4 must be 74
		harmonizedStructure = {}
		for row in tmStructure:
			harmonizedStructure[row] = tmStructure[row]
			if 2000000462 in tmStructure[row]: #Weight
				harmonizedStructure[row][2000000462] = int(float(tmStructure[row][2000000462])) if tmStructure[row][2000000462] != '' else ''
			#if 2000000480 in tmStructure[row]: #2000000540 in : #Date Diagnosis
			#	harmonizedStructure[row][2000000480] = 

			if(self.adHocHarmonization != None):
				harmonizedStructure[row] = self.__adHocMethods(harmonizedStructure[row])

		return harmonizedStructure

	def __adHocMethods(self, preharmonizedStructure):
		'''
		todo: document
		set_codenumber
		ex: set_2000000462
		'''
		harmonizedStructure = preharmonizedStructure
		for code in preharmonizedStructure:
			methodName = "set_" + str(code)
			if(hasattr(self.adHocHarmonization, methodName)): 
				harmonizedStructure[code] = getattr(self.adHocHarmonization, methodName)(preharmonizedStructure[code])
		return harmonizedStructure


def main(adHoc=None):
	argsParsed = TranSMARTArgs.help()
	args = TranSMARTArgs(argsParsed)
	tm = TranSMARTMap(args = args)
	if (adHoc):
		tm.setAdHocMethods(adHoc)
	tm.createCSV()
	tm.createTMMap()

if __name__ == '__main__':
	main()