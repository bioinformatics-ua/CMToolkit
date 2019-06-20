import pandas as pd
from MigratorArgs import MigratorArgs

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
    def __init__(self, cohort, size, harmonizerAdHoc, columnsDst, columnMapper, table, contentMapping, commonHarmonizerMethods):
        self.cohort          = cohort
        self.columnsDst      = columnsDst
        self.columnMapper    = columnMapper
        self.harmonizerAdHoc = harmonizerAdHoc
        self.table           = table
        self.contentMapping  = contentMapping
        self.mapping         = pd.DataFrame(index=range(size), columns=columnsDst)

        args = MigratorArgs()
        self.__populate(commonHarmonizerMethods, adhocMethodsActive=args.adhocmethods)

    def __populate(self, commonHarmonizerMethods, adhocMethodsActive=False):
        for element in self.columnsDst:
            sourceField = None
            if(element in self.columnMapper):
                sourceField = self.columnMapper[element]

            self.mapping[element] = None #Default value as None
            methodName = "set_" + self.table + "_" + element

            if(hasattr(self.harmonizerAdHoc, methodName)): 
                #In case of exist an ad hoc method defined
                self.mapping[element] = getattr(self.harmonizerAdHoc, methodName)(self.cohort[sourceField] if sourceField in self.cohort else None)
            elif (hasattr(commonHarmonizerMethods, methodName)) and adhocMethodsActive: 
                #In case of a method similar to the ad hoc, but since it is common in all the cohorts we decide to inserte in the original code
                self.mapping[element] = self.__standardAdHocMethod(commonHarmonizerMethods, methodName, self.cohort, sourceField)
            else:
                if(sourceField in self.cohort): #Normal behavior
                    self.mapping[element] = self.cohort[sourceField]



    def __standardAdHocMethod(self, commonHarmonizerMethods, methodName, cohort, sourceField):
        try:
            return getattr(commonHarmonizerMethods, methodName)(cohort[sourceField] if sourceField in cohort else None) 
        except:
            raise Exception("The " + sourceField + " field tried to call the " + methodName + " method. Maybe this concept was not mapped in the Usagi!")

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

    def getDataTypesForSQL(table):
        for cls in BaseTable.__subclasses__():
            if(cls.__name__.lower() == table):
                return cls.getDataTypesForSQL()
        return {}
   