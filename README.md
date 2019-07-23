### CMT - The Cohort Migrator Toolkit

The CMT - The Cohort Migrator Toolkit is a python based application design to migrate CSV cohorts into the OMOP CDM schema. The of having the cohorts harmonized in this schema is the interoperability of the data by allowing the exportation of several cohorts into a new system reusing the same script. In this repository we have scripts to migrate the following formats:
- CSV to OMOP CDM
- OMOP CDM to TranSMART batch

To run a new cohort, please read the following documentation <here> or just run the make commands to reproduce the already migrate cohorts. In the file material/<cohort>/6_Scripts/settings.ini there are available all the settings to execute all the sets for the cohort in question. In a new environment, maybe some changes will be needed in this file, perhaps related to the database configuration.

Note: To migrate a the existent cohorts it is necessary to copy the CSVs files to the folder 0_CSVs because for security reasons the row data is stored in a different repository.

Berlin cohort:
- make Berlin-Migrate
- make Berlin-TranSMART