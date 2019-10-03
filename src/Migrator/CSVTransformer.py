import csv
import pandas as pd
import numpy as np
import argparse
import chardet
from FileManager import FileManager

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
        self.cohortdir      = cohortdir
        self.headers        = headers
        self.measures       = measures
        self.cohortdest     = cohortdest
        self.cohortsep      = cohortsep 
        self.fileManager    = FileManager()
        

    def transform(self):
        fixedColumns = self.__readColumnMapper(self.headers)
        measurementsColumns = self.__readColumnMapper(self.measures)
        self.__validateMappers(fixedColumns, measurementsColumns)

        for csv in fixedColumns:
            self.__transform(csv, fixedColumns[csv], measurementsColumns[csv])

    def __transform(self, csv, fixedColumns, measurementsColumns):
        with open('{}{}'.format(self.cohortdir, csv), 'rb') as f:
            result = chardet.detect(f.read())
        dfRead = pd.read_csv('{}{}'.format(self.cohortdir, csv), na_values='null', sep=self.cohortsep, dtype=str, 
                            encoding=result['encoding'])
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
        self.fileManager.toCsv(dataframe    = dfOutput, 
                               destDir      = self.cohortdest, 
                               destFile     = '{}{}'.format(CSVTransformer.MARK, csv), 
                               sep          = self.cohortsep)
    
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
                raise Exception("The mapper files does not match in headers or measures, key: ",fixedColumnsKey)