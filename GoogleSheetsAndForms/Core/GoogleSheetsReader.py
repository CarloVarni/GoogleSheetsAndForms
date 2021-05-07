
from GoogleSheetsAndForms.Core.GoogleReader import GoogleReader
from GoogleSheetsAndForms.Core.Messages import NOTE, FAIL
from GoogleSheetsAndForms.Core.Context import Context

class GoogleSheetsReader(GoogleReader):
    def __init__(self, NAME: str, SPREADSHEET_ID: str, RANGE: list):
        super(GoogleSheetsReader, self).__init__(NAME, SPREADSHEET_ID)
        self.__RANGE: list[str] = RANGE

    @property
    def SPREADSHEET_ID(self) -> str:
        return self.ID

    @property
    def RANGE(self) -> list:
        return self.__RANGE
    
    def __str__(self):
        output = "GoogleReader: '" + self.NAME + "' \n"
        output += "   \\__ SPREADSHEET_ID: '{0}'\n".format(self.SPREADSHEET_ID)
        output += "   \\__ RANGE: {}\n".format(self.RANGE)
        output += "   \\__ Output Values Collection Name: {0}\n".format(self.ValuesCollectionName)
        return output
    
    def execute(self, CTX: Context):
        if not isinstance(CTX, Context):
            raise Exception(FAIL("Execute method accept Context objects as input!"))

        if len(self.ValuesCollectionName) == 0:
            raise Exception(FAIL("Property 'ValuesCollectionName' is blank for '{0}'!".format(self.NAME)))
        if len(self.ValuesCollectionName) != len(self.__RANGE):
            raise Exception(FAIL("Different number of RANGES and Collection Names for '{0}'".format(self.NAME)))

        print(NOTE("Reading data from Google Sheet ... "))
        print("   \\__ Getting Google Sheet '{}' with range(s) '{}'".format(self.SPREADSHEET_ID, self.RANGE))
        print()
        
        result = CTX.retrieve("__SERVICE")["sheets"].spreadsheets().values().batchGet(spreadsheetId=self.SPREADSHEET_ID,
                                                                                      ranges=self.RANGE).execute()
        values = result.get('valueRanges', [])

        for i in range(0, len(self.ValuesCollectionName)):
            CTX.store(self.ValuesCollectionName[i], values[i]['values'])
            
        
