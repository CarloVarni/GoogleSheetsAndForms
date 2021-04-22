
from GoogleSheetsAndForms.Messages import NOTE, FAIL

class GoogleWriter:
    def __init__(self, NAME, SPREADSHEET_ID, RANGE):
        self.__NAME = NAME
        self.__SPREADSHEET_ID = SPREADSHEET_ID
        self.__RANGE = RANGE

        self.ValuesCollectionName = ""
        self.OutputLabels = []
        
    @property
    def NAME(self):
        return self.__NAME

    @property
    def SPREADSHEET_ID(self):
        return self.__SPREADSHEET_ID

    @property
    def RANGE(self):
        return self.__RANGE

    def __str__(self):
        output = "GoogleWriter: '" + self.NAME + "' \n"
        output += "   \\__ SPREADSHEET_ID: " + self.SPREADSHEET_ID + "\n"
        output += "   \\__ RANGE: " + self.RANGE + "\n"
        output += "   \\__ Labels: {}\n".format(self.OutputLabels)
        output += "   \\__ InputCollection Name: {0}\n".format(self.ValuesCollectionName)
        return output
    
    def execute(self, CTX):
        if self.ValuesCollectionName == "":
            raise Exception(FAIL("Property 'ValuesCollectionName' is blank for '{0}'!".format(self.NAME)))

        print(NOTE("Updating Google Sheet " + self.NAME + " ..."))
        
        service = CTX.retrieve("__SERVICE")
        updatedRequests = CTX.retrieve(self.ValuesCollectionName)

        data = []
        for el in updatedRequests:
            toAdd = []
            for key in self.OutputLabels:
                if key is None:
                    toAdd.append("")
                else:
                    toAdd.append(el[key])
            data.append(toAdd)
            
        value_range_body = {'values': data,
                            'majorDimension': 'ROWS'} 
        service.spreadsheets().values().update(spreadsheetId=self.SPREADSHEET_ID,
                                               range=self.RANGE,
                                               valueInputOption="RAW",
                                               body=value_range_body).execute()
        print("   \\__ Google sheet updated : " + self.NAME)
        print()

        
