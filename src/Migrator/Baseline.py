from FileManager import FileManager 
from Migrator import Migrator
from MigratorArgs import MigratorArgs
from CSVTransformer import CSVTransformer
from Harmonizer import Harmonizer
from Logger import Logger

def loadArgs():
    argsParsed = MigratorArgs.help()
    return MigratorArgs(argsParsed)

def main(adHoc=None):
    args = loadArgs()
    log = Logger(args)

    if not args.transformcsv and not args.migrate and not args.harmonize:
        print("Nothing to do, please select the execution mode")
        MigratorArgs.help(show=True)
    
    fm = FileManager(args)

    if args.transformcsv:
        csvTransformer = CSVTransformer(headers     = args.headers, 
                                        measures    = args.measures, 
                                        cohortdir   = args.cohortdir, 
                                        cohortdest  = args.cohortdest, 
                                        cohortsep   = args.cohortsep)
        csvTransformer.transform()
        log.info("Csv transformation completed!", verbose=True)

    if args.harmonize:
        harmonizer = Harmonizer(cohortOrigin = args.cohortdest, 
                                cohortDest   = args.harmonizedest, 
                                mapping      = args.contentmapping,
                                cohortSep    = args.cohortsep)
        if (adHoc):
            harmonizer.setAdHocClass(adHoc)
        harmonizer.harmonize()
        log.info("Csv harmonization completed!", verbose=True)

    if args.migrate:
        etl = Migrator(cohortDir        = args.cohortdest,
                       person           = args.patientcsv,
                       observations     = args.obsdir)
        if (adHoc):
            etl.setAdHocClass(adHoc)
        etl.migrate("person")
        etl.migrate("observation")

        results = etl.getMigrationResults()
        dbConfig = args.getDBConfigs()
        fm.writeResults(results, dbConfig)
        log.info("Migration completed!", verbose=True)
        
if __name__ == "__main__":
    main()
#todo
#visit e observation period