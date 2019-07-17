from MigratorArgs import MigratorArgs
from sqlalchemy import create_engine

class TranSMARTMap():
	def __init__(self, args):
		self.args 						= args
		self.engine						= create_engine(args.db["datatype"]+"://"+args.db["user"]+":"+args.db["password"]+"@"+args.db["server"]+":"+args.db["port"]+"/"+args.db["database"])
		self.observationsDict 			= {} 
		self.baseIdForObservationsDict 	= 1

	def createCSV(self):
		structure = self.__createStructure()
		tmStructure = self.__buildStructureForTM(structure)
		self.__writeCSV(tmStructure)
		print(self.args.transmartcohortfile + " created")

	def __createStructure(self):
		result_set = self.engine.execute("\
			SELECT observation_id, person_id, observation_concept_id, concept.concept_name, observation_date, \
       			observation_type_concept_id, value_as_number, value_as_string, value_as_concept_id, valueConcept.concept_name \
  			FROM omopcdm.observation \
  			INNER JOIN omopcdm.concept as concept on omopcdm.observation.observation_concept_id=concept.concept_id \
  			LEFT JOIN omopcdm.concept as valueConcept  on omopcdm.observation.value_as_concept_id=valueConcept.concept_id;")  
		newStructure = {}
		for row in result_set:  
			person_id = row[1]
			observation_concept_id = row[2]

			if person_id in newStructure:
				newStructure[person_id][observation_concept_id] = self.__getObservation(row)
			else:
				newStructure[person_id] = {}
				newStructure[person_id][observation_concept_id] = self.__getObservation(row)
			self.__fulfillObsDict(observation_concept_id)
		return newStructure

	def __getObservation(self, row):
		#value_as_number, value_as_string, value_as_concept_id, valueConcept.concept_name \
		#		6				7					8						9
		if row[9] != None:
			return row[9]
		if row[6] != None:
			return row[6]
		return row[7]

	def __fulfillObsDict(self, observation_concept_id):
		if observation_concept_id not in self.observationsDict:
			self.baseIdForObservationsDict += 1
			self.observationsDict[observation_concept_id] = self.baseIdForObservationsDict

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

		for row in sorted(tmStructure):
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
		with open(self.args.protegeoutput) as fp:
			for line in fp:
				row = line.strip().split("\t")
				if int(row[2]) in self.observationsDict:
					#['Weight (kg)', 'Clinical_Information+Vital_Signs', '2000000462']
					foutput.write(self.args.transmartcohortfile + "\t" + row[1] + "\t" + \
						str(self.observationsDict[int(row[2])]) + "\t" + row[0] + "\t\t\t\n")
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

def main():
	argsParsed = MigratorArgs.help()
	args = MigratorArgs(argsParsed)
	tm = TranSMARTMap(args = args)
	tm.createCSV()
	tm.createTMMap()

main()
