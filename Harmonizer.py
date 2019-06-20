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
        dfRead = self.__harmonizeVariableConcept(sourceCode, dfRead)
        dfRead = self.__harmonizeMeasureConcept(dfRead)
        dfRead.to_csv('{}{}{}'.format(self.cohortDest, Harmonizer.MARK, sourceCode), sep=self.cohortSep, index=False)

    def __harmonizeVariableConcept(self, sourceCode, dfRead):
        dfMapping = self.fileManager.getContentMappingBySourceCode(sourceCode)
        dfMapping = dfMapping.astype(str)
        dfMapping = dfMapping.reindex(columns=["sourceName", "targetConceptId"])
        mapping = dfMapping.set_index("sourceName")["targetConceptId"].to_dict()

        variableSeries = dfRead["Variable"]
        dfRead["VariableConcept"] = pd.Series(variableSeries.map(mapping), index=dfRead.index)
        return dfRead

    def __harmonizeMeasureConcept(self, dfRead):
        print("isto tem erros __harmonizeMeasureConcept")
        mapping = self.contentMapping.set_index("sourceName")["targetConceptId"].to_dict()
        measureSeries = dfRead["Measure"]
        dfRead["MeasureConcept"] = pd.Series(measureSeries.map(mapping), index=dfRead.index)
        return dfRead

    def __loadContentMapping(self):
        cohorts = []
        for file in glob.glob('{}*.{}'.format(self.cohortOrigin, "csv")):
            cohorts += [file.split(CSVTransformer.MARK)[1]]
        dfMapping = self.fileManager.getContentMapping(cohorts)
        dfMapping = dfMapping.astype(str)
        return dfMapping.reindex(columns=["sourceName", "targetConceptId"])