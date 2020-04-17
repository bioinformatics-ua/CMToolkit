# CMT - Cohort Migrator Toolkit

The CMT - Cohort Migrator Toolkit is a python-based application designed to migrate and harmonize clinical cohorts from CSV format into the OHDSI OMOP CDM schema. This procedure increases the interoperability of the data by allowing the exportation of several cohorts into a new system reusing the same scripts. In this repository we have scripts to migrate the following formats:
- CSV to OMOP CDM
- OMOP CDM to TranSMART batch

### Installation
This toolkit has some dependencies defined in the requirements.pip file and it is required to have a relational database management system installed (for instance, PostgreSQL) to run the pipeline from CSV into TranSMART batch. During the concept mappings, it was used the Usagi and WhiteRabbit tools (available at OHDSI repository).

### Harmonize new cohort
The pipeline was divided into several septs that will create directories during the process, but in the initial step, it is required to create manually some directories. In the end, the harmonization process will have the following directory for each cohort:

```bash
/CohortTools/material/Berlin$ ll
./
../
0_CSVs/
1_WhiteRabbit_processing/
2_Pre-Processing_Usagi/
3_Mappings/
4_Content_Organized/
5_Content_Harmonized/
6_Scripts/
7_Results/
```

The 0_CSVs directory contains all the CSV files composing the cohort, ignoring other formats. The 1_WhiteRabbit_processing contains the outputs from the WhiteRabbit tool, this step is manual and performed externally to these scripts. The directory 2_Pre-Processing_Usagi contains the CSV files that will be used as input in the Usagi tool to perform the concept mappings, and the 3_Mappings contains the outputs of those mappings (CSV Usagi export format). The directory 4_Content_Organized contains two txt files indicating which variables are considered headers and which ones are considered measures. In this directory will be created CSV files of the cohort in a different structure, during the script execution. The 5_Content_Harmonized directory contains similar CSVs to the ones in the previous directory, but with concepts and measures already harmonized. The 6_Scripts contains the python code to call the standard scripts and to develop customized methods for a specific cohort. Finally, the results will be created in the directory 7_Results.

#### Details about the directory 6_Scripts
In this directory, it is necessary to create the python scripts for both migration procedures. Regarding the pipeline from the CSV to the OMOP CDM, it is necessary a python script that imports the Baseline class and passes as argument the Harmonizer class. See the following example:

```python
import Baseline
...
class Harmonizer(object):
    def __init__(self):
        ....
        
    #For processing each row of the CSV files
    def harmonizer(self, row):
        variableConcept = str(row["VariableConcept"])
        if "2000000049" in variableConcept:
            return self.__readCeradWLRounds(row)
        ....
        
    #For adding new rows based on conditions
    def addMissingRows(self):
        missingRows = []
        #missingRows += self.__process...
        ....
        
Baseline.main(Harmonizer)
```

For the OMOP CDM to TranSMART Batch, it is necessary a similar script and the data in a relational database management system because some queries are performed for gathering data. See the following python example:

```python
import TranSMARTMap

class Harmonizer(object):
    #For changing fields stored in an different format in the OMOP CDM
    def set_2000000013(self, value):
        if value == "2/2" or value == "2/3" or value == "3/3":
            return "Non-carrier"
        if value == "3/4" or value == "2/4":
            return "Heterozygote"
        if value == "4/4":
            return "Homozygote"
        return ""#value

    #For adding new fields that do not exist in the OMOP CDM data
    def add_2000000620(self):#Study name
        return "Berlin"
        
TranSMARTMap.main(adHoc=Harmonizer)
```

Finally, it is necessary to define the settings in the ini file. This file contains the variables for the pipeline execution, such as database definitions, paths for the files necessary in the process and data formats. The following example contains the variables used for the Berlin cohort.

```ini
[database]
datatype=postgresql
server=localhost
database=berlin
schema=omopcdm
port=5433
user=bmd
password=12345

[cohort_info]
cohortdir=../0_CSVs/
cohortsep=\t

patientcsv=../5_Content_Harmonized/TH_20190510 EMIF Patient Data.csv
obsdir=../5_Content_Harmonized/
results=../7_Results/
vocabulariesdir=../../../UsagiConceptMapping/Vocabularies/
log=execution.log
cohortname=Berlin
formatdate=%%d-%%M-%%Y


[cohort_mappings]
columnsmapping=../3_Mappings/UsagiExportColumnMapping_v2.csv
contentmapping=../3_Mappings/UsagiExportContentMapping_v6.csv
usagisep=,

[cohort_transformation]
headers=../4_Content_Organized/headers.txt
measures=../4_Content_Organized/measures.txt
cohortdest=../4_Content_Organized/

[cohort_harmonization]
cohortharmonizeddest=../5_Content_Harmonized/

[transmart]
cohortoutputfile=Transmart.tsv
cohortname=Berlin
transmartdstdir=../7_Results/TranSMART/
protegeoutput=../../../protege_output.txt
visitindependentoutput=../../../visit_independent_output.txt

[patient_ids]
;I replaced the spaces by underscores
20190510_EMIF_Patient_Data.csv="Patient ID"
20190510_EMIF_Blood_and_CSF.csv="Patient ID"
20190510_EMIF_Diagnosis.csv="Patient ID"
20190510_EMIF_Neuropsychology.csv="Patient ID"
20190510_EMIF_Sleep.csv="Patient ID"
```

### Execute pipeline for migrated cohorts
There is a make file in the project root to simplify the execution of the system in the cohorts already migrated. Note: The original data is not available in the repository, therefore, it is necessary to copy the CSV files for the 0_CSVs directory.

Berlin cohort:
- make Berlin-Migrate
- make Berlin-TranSMART

Maastricht cohort:
- make Maastricht-Migrate
- make Maastricht-TranSMART