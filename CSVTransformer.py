import csv
import pandas as pd
import numpy as np
import argparse

class CSVTransformer(object):
    '''Class design to transform the cohort CSV files into a strcuture where 
    each line will be added in the DB.

    :constant MARK: the mark used in the files to indenfy which are the ones that have been transformed
    '''
    MARK       = "T_"
    
    '''
    Constructor arguments:
    :param todo
    '''
    def __init__(self, headers, measures, cohortdir, cohortdest, cohortsep):
        self.cohortdir  = cohortdir
        self.headers    = headers
        self.measures   = measures
        self.cohortdest = cohortdest
        self.cohortsep  = cohortsep 
        

    def transform(self):
        fixedColumns = self.__readColumnMapper(self.headers)
        measurementsColumns = self.__readColumnMapper(self.measures)
        self.__validateMappers(fixedColumns, measurementsColumns)

        for csv in fixedColumns:
            self.__transform(csv, fixedColumns[csv], measurementsColumns[csv])

    def __transform(self, csv, fixedColumns, measurementsColumns):
        dfRead = pd.read_csv('{}{}'.format(self.cohortdir, csv), na_values='null', sep=self.cohortsep)
        dfHeaders = dfRead.reindex(columns=fixedColumns)
        dfMeasures = dfRead.reindex(columns=measurementsColumns)  

        #Duplicate static columns considering the numebr of measurements by row
        dfProcessed = pd.DataFrame(np.repeat(dfHeaders.values, len(measurementsColumns),axis=0))
        dfProcessed.columns = dfHeaders.columns

        #Convert the matrix into a key:value dataframe
        listDictMeasures = dfMeasures.to_dict(orient='records')
        dfKVMeasures = pd.DataFrame([(i, j) for a in listDictMeasures for i, j in a.items()], columns=["Variable", "Measure"])
        
        #Merge the shit
        dfOutput = pd.merge(dfProcessed, dfKVMeasures, left_index=True, right_index=True)
        dfOutput.to_csv('{}{}{}'.format(self.cohortdest, self.mark, csv), sep=self.cohortsep, index=False)
    
    def __readColumnMapper(self, file):
        '''
        Read the column mapper. Structure:
        {"csv file 1":["column 1", "column 2",... ], ...}
        '''
        content = {}
        with open(file) as fp:
            for line in fp:
                row = line.split("=")
                content[row[0]] = []
                for concept in row[1].split("\t"):
                    content[row[0]] += [concept.strip()]
        fp.close()
        return content

    def __validateMappers(self, fixedColumns, measurementsColumns):
        for fixedColumnsKey in fixedColumns.keys():
            if fixedColumnsKey not in measurementsColumns.keys():
                raise Exception("The mapper files does not match, key: " + fixedColumnsKey)