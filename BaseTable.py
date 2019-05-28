import pandas as pd

class BaseTable(object):
    '''Class base to build the table mapping.

    Constructor arguments:
    :param cohort:       the cohort sctruturd readed from CSV file
    :param size:         the number of entries in the table
    :param harmonizer:   object with ad hoc methods to harmonize that types of fields
    :param columnsDst:   list of columns from the destination table
    :param columnMapper: ????
    :param table:        destination table name to identify the ad hoc methods following our syntax
    			         - Sintax: set_<table name>_<field name>
    '''
    def __init__(self, cohort, size, harmonizer, columnsDst, columnMapper, table):
        self.columnsDst     = columnsDst
        self.columnMapper   = columnMapper
        self.cohort         = cohort
        self.harmonizer     = harmonizer
        self.table          = table
        self.mapping        = pd.DataFrame(index=range(size), columns=columnsDst) 
        self.__populate()

    def __populate(self):
        for element in self.columnsDst:
            sourceField = None
            if(element in self.columnMapper):
                sourceField = self.columnMapper[element]

            methodName = "set_" + self.table + "_" + element
            if(hasattr(self.harmonizer, methodName)):
                self.mapping[element] = getattr(self.harmonizer, methodName)(self.cohort[sourceField] if sourceField in self.cohort else None)
            else:
                self.mapping[element] = self.cohort[sourceField] if sourceField in self.cohort else None
        #print(self.mapping)
        
    def getMapping(self):
        return self.mapping

    def getDataTypesForSQL():
        return {}
   