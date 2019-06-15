from FileManager import FileManager 
from Migrator import Migrator
from MigratorArgs import MigratorArgs

def main(adHoc=None):
    argsParsed = MigratorArgs.help()
    args = MigratorArgs(argsParsed)

    fm = FileManager(args)
    etl = Migrator(cohort         = fm.getCohort(), 
                   columnsMapping = fm.getColumnsMappingByDomain, 
                   contentMapping = fm.getContentMapping())
    if (adHoc):
        etl.setAdHocMethods(adHoc)
    results = etl.migrate()
    
    dbConfig = args.getDBConfigs()
    fm.writeResults(results, dbConfig)
    
if __name__ == "__main__":
    main()
