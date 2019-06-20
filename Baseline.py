from FileManager import FileManager 
from Migrator import Migrator
from MigratorArgs import MigratorArgs
from CSVTransformer import CSVTransformer
from Harmonizer import Harmonizer

def main(adHoc=None):
    argsParsed = MigratorArgs.help()
    args = MigratorArgs(argsParsed)

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

    if args.harmonize:
        harmonizer = Harmonizer(cohortOrigin = args.cohortdest, 
                                cohortDest   = args.harmonizedest, 
                                mapping      = args.contentmapping,
                                cohortSep    = args.cohortsep,
                                fileManager  = fm)
        harmonizer.harmonize()

    if args.migrate:
        etl = Migrator(cohortDir        = args.cohortdest,
                       person           = args.patientcsv,
                       observations     = args.obsdir,
                       fileManager      = fm)
        if (adHoc):
            etl.setAdHocMethods(adHoc)
        etl.migrate("person")
        etl.migrate("observation")

        results = etl.getMigrationResults()
        dbConfig = args.getDBConfigs()
        fm.writeResults(results, dbConfig)
        
if __name__ == "__main__":
    main()
#todo
#corrigir o bug da harmonização, seguir o print 
#nao meter tudo como string. existem 3 tipos de dados: value_as_number,value_as_string,value_as_concept_id
#criterios de exclusao
#visit e observation period