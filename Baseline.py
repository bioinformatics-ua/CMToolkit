from FileManager import FileManager 
from Migrator import Migrator
from MigratorArgs import MigratorArgs
from CSVTransformer import CSVTransformer

def main(adHoc=None):
    argsParsed = MigratorArgs.help()
    args = MigratorArgs(argsParsed)
    
    if not args.transformcsv and not args.migrate:
        print("Nothing to do, please select the execution mode")
        MigratorArgs.help(show=True)

    if args.transformcsv:
        csvTransformer = CSVTransformer(headers     = args.headers, 
                                        measures    = args.measures, 
                                        cohortdir   = args.cohortdir, 
                                        cohortdest  = args.cohortdest, 
                                        cohortsep   = args.cohortsep)
        csvTransformer.transform()

    if args.migrate:
        #TO FIX
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
