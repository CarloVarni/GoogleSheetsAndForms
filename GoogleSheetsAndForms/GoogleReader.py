
from GoogleSheetsAndForms.Messages import NOTE, FAIL

class GoogleReader:
    def __init__(self, NAME, SPREADSHEET_ID, RANGE):
        self.__NAME = NAME
        self.__SPREADSHEET_ID = SPREADSHEET_ID
        self.__RANGE = RANGE

        self.__ValuesCollectionName = [""]
        
    @property
    def NAME(self):
        return self.__NAME

    @property
    def SPREADSHEET_ID(self):
        return self.__SPREADSHEET_ID

    @property
    def RANGE(self):
        return self.__RANGE

    @property
    def ValuesCollectionName(self):
        return self.__ValuesCollectionName

    @ValuesCollectionName.setter
    def ValuesCollectionName(self, value):
        if not isinstance(value, list):
            raise Exception(FAIL("Property Error : 'ValuesCollectionName' property of class 'GoogleReader' must be a list of strings!"))
        if len(value) == 0:
            raise Exception(FAIL("Property Error : 'ValuesCollectionName' property of class 'GoogleReader' must contain at least one entry!"))
        for el in value:
            if not isinstance(el, str):
                raise Exception(FAIL("Property Error : 'ValuesCollectionName' property of class 'GoogleReader' must be a list of strings!"))
            if len(el) == 0:
                raise Exception(FAIL("Property Error : 'ValuesCollectionName' property of class 'GoogleReader' must not contain blank entries!"))

        self.__ValuesCollectionName = value
    
    def __str__(self):
        output = "GoogleReader: '" + self.NAME + "' \n"
        output += "   \\__ SPREADSHEET_ID: '{0}'\n".format(self.SPREADSHEET_ID)
        output += "   \\__ RANGE: {}\n".format(self.RANGE)
        output += "   \\__ Output Values Collection Name: {0}\n".format(self.ValuesCollectionName)
        return output
    
    def execute(self, CTX):
        if len(self.ValuesCollectionName) == 0:
            raise Exception(FAIL("Property 'ValuesCollectionName' is blank for '{0}'!".format(self.NAME)))

        if len(self.ValuesCollectionName) != len(self.__RANGE):
            raise Exception(FAIL("Different number of RANGES and Collection Names for '{0}'".format(self.NAME)))

        print(NOTE("Reading data from Google Sheet ... "))
        print("   \\__ Getting Google Sheet '{}' with range(s) '{}'".format(self.SPREADSHEET_ID, self.RANGE))
        print()
        
        result = CTX.retrieve("__SERVICE").spreadsheets().values().batchGet(spreadsheetId=self.SPREADSHEET_ID,
                                                                            ranges=self.RANGE).execute()
        values = result.get('valueRanges', [])

        for i in range(0, len(self.ValuesCollectionName)):
            CTX.store(self.ValuesCollectionName[i], values[i]['values'])
            
        
