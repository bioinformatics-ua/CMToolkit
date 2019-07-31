import sys
#GREAT SHIT
sys.path.insert(0, '../../../src/Migrator')
sys.path.insert(0, '../../../src/Tables')
sys.path.insert(0, '../../../src/Utils')
sys.path.insert(0, '../../../src/Vocabularies')

import Baseline
from Observation import Observation
import pandas as pd

class Harmonizer(object):
	#Just to test
	DateOfDiagnosis = {
	"10323":"31-10-2018",
"10324":"08-10-2018",
"10325":"14-02-2018",
"10325":"06-06-2018",
"10326":"19-09-2018",
"10327":"02-11-2018",
"10328":"05-11-2018",
"10329":"29-10-2018",
"10330":"30-11-2018",
"10332":"07-01-2019",
"10334":"26-06-2018",
"10335":"03-01-2019",
"10336":"06-09-2018",
"10337":"07-03-2018",
"10338":"16-11-2018",
"10339":"05-12-2018",
"10340":"05-12-2018",
"10341":"13-12-2018",
"10342":"04-01-2019",
"10343":"21-09-2018",
"10344":"20-09-2018",
"10345":"07-09-2018",
"10346":"30-11-2018",
"10347":"07-01-2019",
"10348":"20-12-2018",
"10349":"19-12-2018",
"10350":"04-01-2019",
"10351":"03-12-2018",
"10352":"29-06-2018",
"10353":"19-11-2018",
"10354":"12-11-2018",
"10355":"27-07-2018",
"10357":"17-12-2018",
"10358":"28-12-2018",
"10365":"23-01-2019",
"10367":"04-02-2019",
"10368":"28-01-2019",
"10370":"25-01-2019",
"10372":"25-01-2019",
"10373":"15-01-2019",
"10374":"06-12-2018",
"10375":"07-01-2019",
"10376":"28-01-2019",
"10377":"25-01-2019",
"10378":"29-11-2018",
"10379":"25-01-2019",
"10380":"04-12-2018",
"10381":"16-01-2019",
"10382":"15-01-2019",
"10383":"07-01-2019",
"10384":"16-01-2019",
"10385":"15-01-2018",
"10386":"25-07-2018",
"10387":"12-10-2018",
"10388":"08-10-2018",
"10389":"29-06-2018",
"10390":"08-10-2018",
"10391":"28-12-2018",
"10392":"12-11-2018",
"10393":"05-09-2018",
"10394":"30-10-2018",
"10395":"10-12-2018",
"10396":"01-10-2018",
"10397":"02-10-2018",
"10398":"18-09-2018",
"10399":"10-12-2018",
"10400":"16-11-2018",
"10401":"17-12-2018",
"10402":"28-12-2018",
"10403":"21-01-2019",
"10404":"23-01-2019",
"10405":"18-09-2018",
"10406":"24-01-2019",
"10407":"24-01-2019",
"10408":"15-11-2018",
"10409":"26-06-2018",
"10411":"22-01-2019",
"10412":"21-01-2019",
"10413":"18-01-2019",
"10414":"30-11-2018",
"10415":"22-06-2018",
"10416":"21-01-2019",
"10417":"30-11-2018",
"10418":"21-08-2018",
"10419":"21-08-2018",
"10420":"20-09-2018",
"10421":"20-09-2018",
"10422":"30-10-2018",
"10423":"06-06-2018",
"10424":"04-02-2019",
"10424":"08-04-2019",
"10425":"08-02-2019",
"10426":"08-02-2019",
"10427":"07-02-2019",
"10428":"01-02-2019",
"10429":"11-02-2019",
"10430":"11-02-2019",
"10431":"11-02-2019",
"10435":"21-02-2019",
"10436":"14-02-2019",
"10437":"18-06-2018",
"10438":"28-01-2019",
"10439":"10-01-2019",
"10440":"15-01-2019",
"10441":"08-02-2019",
"10442":"29-01-2019",
"10443":"28-01-2019",
"10444":"30-01-2019",
"10445":"28-01-2019",
"10455":"18-02-2019",
"10456":"04-02-2019",
"10457":"11-02-2019",
"10458":"21-12-2018",
"10459":"19-12-2018",
"10460":"06-12-2018",
"10461":"30-01-2019",
"10466":"15-02-2019",
"10468":"21-02-2019",
"10469":"15-02-2019",
"10472":"22-02-2019",
"10474":"15-02-2018",
"10476":"15-03-2019",
"10477":"05-04-2019",
"10481":"26-02-2019",
"10482":"26-02-2019",
"10483":"26-02-2019",
"10484":"26-02-2019",
"10485":"28-01-2019",
"10486":"04-03-2019",
"10487":"18-02-2019",
"10488":"13-02-2019",
"10489":"05-03-2019",
"10490":"05-03-2019",
"10491":"30-01-2019",
"10492":"30-01-2019",
"10499":"11-03-2019",
"10500":"25-02-2019",
"10501":"25-02-2019",
"10502":"25-02-2019",
"10503":"25-02-2019",
"10504":"26-02-2019",
"10515":"29-04-2019",
"10517":"29-03-2019",
"10518":"15-03-2019",
"10520":"15-03-2019",
"10521":"22-03-2018",
"10523":"01-04-2019",
"10524":"29-03-2019",
"10526":"13-03-2019",
"10527":"27-03-2019",
"10528":"27-03-2019",
"10542":"25-01-2019",
"10543":"25-01-2019",
"10544":"26-02-2019",
"10545":"28-01-2019",
"10546":"21-01-2019",
"10548":"28-03-2019",
"10548":"09-04-2019",
"10549":"28-03-2019",
"10550":"04-04-2019",
"10551":"04-04-2019",
"10556":"26-02-2019",
"10557":"26-02-2019",
"10558":"28-02-2019",
"10559":"28-02-2019",
"10560":"28-02-2019",
"10566":"15-04-2019",
"10578":"01-04-2019",
"10579":"02-04-2019",
"10580":"03-04-2019",
"10581":"23-04-2019",
"10582":"15-04-2019",
"10583":"23-04-2019",
"10584":"01-04-2019",
"10585":"03-04-2019",
"10586":"10-04-2019",
"10587":"27-03-2019",
"10588":"13-03-2019",
"10589":"07-03-2019",
"10590":"21-03-2019",
"10591":"20-03-2019",
"10592":"01-04-2019",
"10593":"01-04-2019",
"10594":"25-04-2019",
"10595":"25-04-2019",
"10596":"25-04-2019",
"10597":"25-04-2019",
"10598":"29-04-2019",
"10599":"19-03-2019",
"10601":"07-03-0209",
"10602":"01-04-2019",
"10603":"01-04-2019",
"10605":"26-04-2019",
"10606":"30-04-2019",
"10607":"12-04-2019",
"10608":"28-03-2019",
"10609":"29-03-2019",
"10610":"26-03-2019",
"10611":"26-03-2019",
"10612":"22-03-2019",
"10613":"22-03-2019",
"10614":"29-04-2019",
"10615":"10-04-2019",
"10616":"09-04-2019",
"10617":"25-02-2019",
"10618":"15-01-2019",
"10619":"20-03-2019",
"10620":"06-05-2019",
"10621":"08-04-2019",
"10622":"03-05-2019",
"10623":"02-04-2019",
"10624":"09-05-2019"
	}







	def __init__(self):
		#Base variables
		self.dateOfDiagnosis = {}

		#Temporary
		self.ceradWLRounds = []


	#######################################
	#	Harmonizer in the initial stage	  #
	#######################################
	def harmonizer(self, row):
		variableConcept = str(row["VariableConcept"])
		if "2000000049" in variableConcept:
			return self.__readCeradWLRounds(row)
		if "2000000468" in variableConcept:
			return self.__dealWithFamilyHistoryDementia(row)
		if "2000000434" in variableConcept:
			return self.__dealWithSleepDisordersClinicalInformation(row)
		#if "2000000540" in variableConcept:
		#	return self.__dealWithDateOfDiagnosis(row)
		if "2000000480" in variableConcept:
			return self.__dealWithDateOfBloodCollection(row)
		return row

	def __readCeradWLRounds(self, row):
		#Add no dict
		#remove mapping
		#ceradWLRounds.append
		#{'Patient ID': 10621, 'Date of neuropsychological testing': '21-03-2019', 'Variable': 'Cerad WL round 1', 'Measure': '6', 'VariableConcept': '2000000049', 'MeasureConcept': nan}
		#{'Patient ID': 10621, 'Date of neuropsychological testing': '21-03-2019', 'Variable': 'Cerad WL round 2', 'Measure': '9', 'VariableConcept': '2000000049', 'MeasureConcept': nan}
		#{'Patient ID': 10621, 'Date of neuropsychological testing': '21-03-2019', 'Variable': 'Cerad WL round 3', 'Measure': '10', 'VariableConcept': '2000000049', 'MeasureConcept': nan}
		self.ceradWLRounds += [row]
		row['VariableConcept'] = None
		return row

	def __processCeradWLRounds(self):
		results = []
		if self.ceradWLRounds:
			#key will be (patient, date)
			measureDict = {}
			sumOfMeasuresDict = {} 
			for entry in self.ceradWLRounds:
				if (entry["Patient ID"], entry["Date of neuropsychological testing"]) in sumOfMeasuresDict:
					sumOfMeasuresDict[(entry["Patient ID"], entry["Date of neuropsychological testing"])] += int(entry["Measure"])
					measureDict[(entry["Patient ID"], entry["Date of neuropsychological testing"])] += "," + str(entry["Measure"])
				else:
					sumOfMeasuresDict[(entry["Patient ID"], entry["Date of neuropsychological testing"])] = int(entry["Measure"])
					measureDict[(entry["Patient ID"], entry["Date of neuropsychological testing"])] = str(entry["Measure"])
			for entry in sumOfMeasuresDict:
				results += [{
					'Patient ID':entry[0],
					'Date of neuropsychological testing':entry[1],
					'Variable': '[Cerad WL round 1, Cerad WL round 2, Cerad WL round 3]', 
					'Measure': measureDict[entry],
					'MeasureNumber': sumOfMeasuresDict[entry], 
					'VariableConcept': '2000000049', 
					'MeasureConcept': None
				}]
		self.ceradWLRounds = []
		return results
	
	def __dealWithFamilyHistoryDementia(self, row):
		#convert 0 = no or 1 = yes
		#{'Patient ID': 10624, 'Sex': 0.0, 'Date of birth': '14-05-1940', 'Date of Admission': '02-05-2019', 
		#'Variable': 'Family history Dementia', 'Measure': 0.0, 'VariableConcept': '2000000468', 
		#'MeasureConcept': nan, 'MeasureNumber': 0.0, 'MeasureString': nan}
		row["MeasureNumber"] = None
		if row["Measure"] == 0:
			row["MeasureConcept"] = 2000000239
		if row["Measure"] == 1:
			row["MeasureConcept"] = 2000000238
		return row

	def __dealWithSleepDisordersClinicalInformation(self, row):
		#{'Patient ID': 10368, 'Date of': '28-nov-18', 'Variable': 'Epworth Sleepiness Scale (ESS)', 'Measure': 'n.b.', 'VariableConcept': '2000000434', 'MeasureConcept': nan}
		if row["Measure"] == "n.b.":
			row["MeasureString"] = None
		return row

	def __dealWithDateOfBloodCollection(self, row):
		#{'Patient ID': 10324, 'Date of puncture (Liquor)': nan, 'Variable': 'Date of blood sample', 'Measure': '28-05-2018', 'VariableConcept': '2000000480', 'MeasureConcept': nan, 'MeasureNumber': nan, 'MeasureString': '28-05-2018'}
		return self.__dealWithDatesDifferences(row, str(row["Patient ID"]))

	def __dealWithDatesDifferences(self, row, patientID):
		from datetime import date
		import datetime
		row["MeasureString"] = None
		try:
			d0 = datetime.datetime.strptime(Harmonizer.DateOfDiagnosis[patientID], '%d-%M-%Y')
		except: #Patient with date
			return row
		d1 = datetime.datetime.strptime(row["Measure"], '%d-%M-%Y')
		delta = d1 - d0
		row["MeasureNumber"] = round(delta.days/365, 2)
		return row

	def addMissingRows(self):
		missingRows = []
		missingRows += self.__processCeradWLRounds()
		#missingRows += self.__process...
		#....
		return missingRows

	#######################################
	#	Harmonizer during the migration	  #
	#######################################
	def filter_person(self, cohort):
		cohort = cohort[pd.notnull(cohort['Sex'])]
		return cohort.reset_index(drop=True)

	#Person
	def set_person_gender_concept_id(self, value):
		gender_map = {1:8507, 0:8532}
		return value.map(gender_map)

	#Observation
	def set_observation_observation_type_concept_id(self, value):
		return pd.Series("2000000260", index=Observation.ObservationIDSet)

Baseline.main(Harmonizer)
