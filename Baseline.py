import argparse
from FileManager import FileManager 
from Migrator import Migrator

def help():
    parser = argparse.ArgumentParser(description='Cohort mapper')
    parser.add_argument('-i', '--input-cohort', dest='input', \
                        type=str, default="cohort/", \
                        help='The input can be a cohort CSV file or a dir with all CSV files (default: cohort/)')

    parser.add_argument('-c', '--columns-mapping', dest='columns', \
                        type=str, default="USAGIcolumns.csv", \
                        help='The USAGI output file in CSV format with the column mapping (default: USAGIcolumns.csv)')
    parser.add_argument('-m', '--measurements-mapping', dest='measures', \
                        type=str, default="", \
                        help='The USAGI output file in CSV format with the cohort content harmonized')

    parser.add_argument('-b', '--separator', dest='sep', \
                        type=str, default='\t', \
                        help='The separator used in the CSV file (default: tab -> \\t)')

    parser.add_argument('-r', '--results', dest='results', \
                        type=str, default="results/", \
                        help='The path to write the CSV tables with the cohort migrated to OMOP CDM v5 (default: "results/")')
    parser.add_argument('-s', '--settings', dest='settings', \
                        type=str, default="settings.ini", \
                        help='The system settings file (default: settings.ini)')
    return parser.parse_args()

def main(adHoc=None):
    args = help()
    fm = FileManager(args)
    configuration = fm.getSystemSettings() #important for db data insertion

    etl = Migrator(cohort         = fm.getCohort(), 
                   columnsMapping = fm.getColumnsMappingByDomain, 
                   contentMapping = fm.getContentMapping())
    if (adHoc):
        etl.setAdHocMethods(adHoc)
    results = etl.migrate()

    fm.writeResults(results, configuration)

if __name__ == "__main__":
    main()
