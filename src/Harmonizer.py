import glob
import pandas as pd
from CSVTransformer import CSVTransformer

class Harmonizer(object):
    '''Class design to harmonize the transformed CSV cohort files.

    :constant MARK: the mark used in the files to indenfy which are the ones that have been harmonized
    '''
    MARK       = "TH_"
    
    '''
    Constructor arguments:
    :param todo
    '''
    def __init__(self, cohortOrigin, cohortDest, mapping, cohortSep, fileManager):
        self.cohortOrigin   = cohortOrigin 
        self.cohortDest     = cohortDest 
        self.mapping        = mapping
        self.cohortSep      = cohortSep
        self.fileManager    = fileManager
        self.contentMapping = self.__loadContentMapping()

    def harmonize(self):
        cohorts = glob.glob('{}*.{}'.format(self.cohortOrigin, "csv"))
        for file in cohorts:
            self.__harmonize(file)

    def __harmonize(self, file):
        sourceCode = file.split(CSVTransformer.MARK)[1]
        dfRead = pd.read_csv('{}{}'.format(self.cohortOrigin, file), na_values='null', sep=self.cohortSep)
        dfRead = self.__filter(dfRead)
        dfRead = self.__harmonizeVariableConcept(sourceCode, dfRead)
        dfRead = self.__harmonizeMeasureConcept(dfRead)
        dfRead = self.__harmonizeMeasureString(dfRead)
        dfRead = self.__harmonizeMeasureAll(dfRead)
        dfRead.to_csv('{}{}{}'.format(self.cohortDest, Harmonizer.MARK, sourceCode), sep=self.cohortSep, index=False)
    
    def __filter(self, dfRead):
        return dfRead[pd.notnull(dfRead["Measure"])]

    def __harmonizeVariableConcept(self, sourceCode, dfRead):
        dfMapping = self.fileManager.getContentMappingBySourceCode(sourceCode)
        dfMapping = dfMapping.reindex(columns=["sourceName", "targetConceptId"])
        mapping = dfMapping.set_index("sourceName")["targetConceptId"].to_dict()
        
        variableSeries = dfRead["Variable"]
        dfRead["VariableConcept"] = pd.Series(variableSeries.map(mapping), index=dfRead.index)
        return dfRead

    def __harmonizeMeasureConcept(self, dfRead):
        dfRead["MeasureConcept"] = dfRead[["Variable", "Measure"]].apply(tuple, axis=1).map(self.contentMapping)
        return dfRead

    def __harmonizeMeasureString(self, dfRead):
        dfRead["MeasureString"] = dfRead["Measure"]
        dfRead["MeasureString"] = dfRead["MeasureString"][dfRead["MeasureConcept"].isnull()]
        return dfRead

    def __loadContentMapping(self):
        cohorts = []
        for file in glob.glob('{}*.{}'.format(self.cohortOrigin, "csv")):
            cohorts += [file.split(CSVTransformer.MARK)[1]]
        dfMapping = self.fileManager.getContentMapping(cohorts)

        keyMappingSeries = dfMapping[["sourceCode", "sourceName"]].apply(tuple, axis=1)
        keyMapping = pd.concat([keyMappingSeries, dfMapping["targetConceptId"]], axis=1)
        keyMapping = keyMapping.rename(columns={0: 'source'})

        return keyMapping.set_index("source")["targetConceptId"].to_dict()
    
    def __harmonizeMeasureAll(self, dfRead):
        #pdOuput = 
        #for row in dfRead:
        #    pdOuput.add(Harmonizer.harmonizer(row))
        #return pdOutput
        return dfRead