from TranSMARTArgs import TranSMARTArgs
from sqlalchemy import create_engine

class TranSMARTMap():
	#Demographic mappings
	DemographicSex 			= 2000000609
	DemographicRace 		= 2000000603
	DemographicEthnic 		= 2000000555
	DemographicBirthYear 	= 2000000503
	#DemographicCounty 		= 2000000065
	#DemographicAge 		= 2000000488

	#Person query index
	PersonPersonIdIndex       		= 0
	PersonGenderNameIndex       	= 2
	PersonRaceNameIndex       		= 4
	PersonEthnicNameIndex       	= 6
	PersonBirthYearIndex       		= 7

	#Observation query index
	ObservationPersonIdIndex       		= 1
	ObservationObsvationConceptIdIndex	= 2
	ObservationValuesAsNumberIndex		= 6
	ObservationValuesAsStringIndex		= 7
	ObservationValuesAsConceptIdIndex	= 8
	ObservationValuesAsConceptNameIndex	= 9

	def __init__(self, args):
		self.args 						= args
		self.engine						= create_engine(args.db["datatype"]+"://"+args.db["user"]+":"+args.db["password"]+"@"+args.db["server"]+":"+args.db["port"]+"/"+args.db["database"])
		self.observationsDict 			= set([TranSMARTMap.DemographicSex, TranSMARTMap.DemographicRace, TranSMARTMap.DemographicEthnic, TranSMARTMap.DemographicBirthYear])

	def createCSV(self):
		structure = self.__createStructure()
		tmStructure = self.__buildStructureForTM(structure)
		harmonizedStructure = self.__harmonizeStructureForRM(tmStructure)
		self.observationsDict = sorted(list(self.observationsDict))
		self.__writeCSV(harmonizedStructure)
		print(self.args.transmartcohortfile + " created")

	def __createStructure(self):
		newStructure = self.__loadObservations()
		newStructure = self.__loadPatientData(newStructure)
		return newStructure
	
	def __loadObservations(self):
		observationSet = self.engine.execute("\
			SELECT observation_id, person_id, observation_concept_id, concept.concept_name, observation_date, \
       			observation_type_concept_id, value_as_number, value_as_string, value_as_concept_id, valueConcept.concept_name \
  			FROM "+self.args.db["schema"]+".observation \
  			INNER JOIN "+self.args.db["schema"]+".concept as concept on "+self.args.db["schema"]+".observation.observation_concept_id=concept.concept_id \
  			LEFT JOIN "+self.args.db["schema"]+".concept as valueConcept  on "+self.args.db["schema"]+".observation.value_as_concept_id=valueConcept.concept_id;")  
		newStructure = {}
		for row in observationSet:  
			person_id = row[TranSMARTMap.ObservationPersonIdIndex]
			observation_concept_id = row[TranSMARTMap.ObservationObsvationConceptIdIndex]

			if person_id in newStructure:
				newStructure[person_id][observation_concept_id] = self.__getObservation(row)
			else:
				newStructure[person_id] = {}
				newStructure[person_id][observation_concept_id] = self.__getObservation(row)
			self.__fulfillObsDict(observation_concept_id)
		return newStructure

	def __loadPatientData(self, newStructure):
		personSet = self.engine.execute("\
			SELECT person_id, gender_concept_id, genderConcept.concept_name as gender_concept_name,\
       			race_concept_id, raceConcept.concept_name as race_concept_name,\
			    ethnicity_concept_id, ethnicityConcept.concept_name as race_concept_name,\
			    year_of_birth, month_of_birth, day_of_birth, birth_datetime, death_datetime\
			FROM "+self.args.db["schema"]+".person\
			LEFT JOIN "+self.args.db["schema"]+".concept as genderConcept on "+self.args.db["schema"]+".person.gender_concept_id = genderConcept.concept_id\
			LEFT JOIN "+self.args.db["schema"]+".concept as raceConcept on "+self.args.db["schema"]+".person.race_concept_id = genderConcept.concept_id\
			LEFT JOIN "+self.args.db["schema"]+".concept as ethnicityConcept on "+self.args.db["schema"]+".person.ethnicity_concept_id = ethnicityConcept.concept_id;")
		for row in personSet:  
			person_id = row[TranSMARTMap.PersonPersonIdIndex]
			if person_id not in newStructure:
				newStructure[person_id] = {}
			newStructure[person_id][TranSMARTMap.DemographicSex] 		= self.__convertNoneToEmptyString(row[TranSMARTMap.PersonGenderNameIndex])
			newStructure[person_id][TranSMARTMap.DemographicRace] 		= self.__convertNoneToEmptyString(row[TranSMARTMap.PersonRaceNameIndex])
			newStructure[person_id][TranSMARTMap.DemographicEthnic] 	= self.__convertNoneToEmptyString(row[TranSMARTMap.PersonEthnicNameIndex])
			newStructure[person_id][TranSMARTMap.DemographicBirthYear] 	= self.__convertNoneToEmptyString(row[TranSMARTMap.PersonBirthYearIndex])
		return newStructure

	def __convertNoneToEmptyString(self, value):
		if value:
			return value
		return ""

	def __getObservation(self, row):
		#value_as_number, value_as_string, value_as_concept_id, valueConcept.concept_name \
		#		6				7					8						9
		if row[TranSMARTMap.ObservationValuesAsConceptNameIndex] != None:
			return row[TranSMARTMap.ObservationValuesAsConceptNameIndex]
		if row[TranSMARTMap.ObservationValuesAsNumberIndex] != None:
			return row[TranSMARTMap.ObservationValuesAsNumberIndex]
		return row[TranSMARTMap.ObservationValuesAsStringIndex]

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
		foutput = open('{}{}'.format(self.args.transmartdstdir, self.args.transmartcohortfile), "w")
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
		foutput = open('{}{}'.format(self.args.transmartdstdir, "colunmn_map.txt"), "w")
		foutput.write("Filename\tCategory_Code (tranSMART)\tColumn\tDataLabel\tdata_label_src\tControlVocab_cd\tData_type\n")
		foutput.write(self.args.transmartcohortfile + "\t\t1\tSUBJ_ID\t\t\t\n")
		
		protegeOutput = {}
		with open(self.args.protegeoutput) as fp:
			for line in fp:
				row = line.strip().split("\t")
				if int(row[2]) in self.observationsDict:
					protegeOutput[int(row[2])] = row
		for line in sorted(protegeOutput):
			row = protegeOutput[line]
			#['Weight (kg)', 'Clinical_Information+Vital_Signs', '2000000462']
			foutput.write(self.args.transmartcohortfile + "\t" + row[1] + "\t" + \
				str(self.observationsDict.index(int(row[2]))+2) + "\t" + row[0] + "\t\t\t\n")
		fp.close()
		foutput.close()
		self.__createDefaultFiles()
		print("TranSMART load files created")

	def __createDefaultFiles(self):
		foutput = open('{}{}'.format(self.args.transmartdstdir, "clinical.params"), "w")
		foutput.write("COLUMN_MAP_FILE=column_map.txt\nRECORD_EXCLUSION_FILE=x")
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
				harmonizedStructure[row][2000000462] = int(float(tmStructure[row][2000000462].replace(',',''))) if tmStructure[row][2000000462] != '' else ''

		return harmonizedStructure

def main():
	argsParsed = MigratorArgs.help()
	args = MigratorArgs(argsParsed)
	tm = TranSMARTMap(args = args)
	tm.createCSV()
	tm.createTMMap()

main()
