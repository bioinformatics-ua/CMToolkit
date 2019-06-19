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

    fm = FileManager(args)

    if args.transformcsv:
        csvTransformer = CSVTransformer(headers     = args.headers, 
                                        measures    = args.measures, 
                                        cohortdir   = args.cohortdir, 
                                        cohortdest  = args.cohortdest, 
                                        cohortsep   = args.cohortsep)
        csvTransformer.transform()

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
#acabar a harmonizaçao ou seja, ler do usagi o mapeamento e fazer coisas
#existe 2 tipos de mapeamentos escritos no migrator
#nao meter tudo como string, ver se é data ou numero e meter no tipo certo
#criterios de exclusao
#visit e observation period