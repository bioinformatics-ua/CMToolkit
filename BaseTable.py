import pandas as pd

class BaseTable(object):
    '''Class base to build the table mapping.

    Constructor arguments:
    :param cohort:       the cohort sctruturd readed from CSV file
    :param size:         the number of entries in the table
    :param harmonizerAdHoc:   object with ad hoc methods to harmonize that types of fields
    :param columnsDst:   list of columns from the destination table
    :param columnMapper: ????
    :param table:        destination table name to identify the ad hoc methods following our syntax

    Ad hoc methods:
        - Sintax to deal with a field: set_<table name>_<field name>
        - Sintax to pre process the cohort: filter_<table name>
    '''
    def __init__(self, cohort, size, harmonizerAdHoc, columnsDst, columnMapper, table, contentMapping):
        self.cohort          = cohort
        self.columnsDst      = columnsDst
        self.columnMapper    = columnMapper
        self.harmonizerAdHoc = harmonizerAdHoc
        self.table           = table
        self.contentMapping  = contentMapping
        self.mapping         = pd.DataFrame(index=range(size), columns=columnsDst)

        self.__populate()

    def __populate(self):
        for element in self.columnsDst:
            sourceField = None
            if(element in self.columnMapper):
                sourceField = self.columnMapper[element]

            self.mapping[element] = None #Default value as None
            methodName = "set_" + self.table + "_" + element

            if(hasattr(self.harmonizerAdHoc, methodName)): #In case of exist an ad hoc method defined
                self.mapping[element] = getattr(self.harmonizerAdHoc, methodName)(self.cohort[sourceField] if sourceField in self.cohort else None)
            else:
                if(sourceField in self.cohort): #Normal behavior
                    #todo
                    #caso exista mapeamento de conteudo
                    #caso seja direto
                    optionsForSourceField = self.contentMapping[self.contentMapping['sourceCode'].str.contains(sourceField)]
                    if(not optionsForSourceField.empty): #There is a mapping in the measruements file
                        values = optionsForSourceField["targetConceptId"].values
                        sourceFieldMap = pd.Series(values, index=optionsForSourceField['sourceName']).to_dict()
                        self.mapping[element] = self.cohort[sourceField].map(sourceFieldMap)
                    else:
                        self.mapping[element] = self.cohort[sourceField]
                    
    def getMapping(self):
        return self.mapping

    #####################
    ### Class methods ###
    #####################
    def cohortFilter(cohort, table, harmonizerAdHoc):
        methodName = "filter_" + table
        if(hasattr(harmonizerAdHoc, methodName)):
            cohort = getattr(harmonizerAdHoc, methodName)(cohort)
        return cohort

    def getDataTypesForSQL():
        return {}
   