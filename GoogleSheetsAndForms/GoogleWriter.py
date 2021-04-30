
from GoogleSheetsAndForms.Messages import NOTE, FAIL
from GoogleSheetsAndForms.Context import Context

class GoogleWriter:
    def __init__(self, NAME: str, SPREADSHEET_ID: str, RANGE: str):
        self.__NAME: str = NAME
        self.__SPREADSHEET_ID: str = SPREADSHEET_ID
        self.__RANGE: str = RANGE

        self.__ValuesCollectionName: str = ""
        self.__OutputLabels: list[str] = []
        
    @property
    def NAME(self) -> str:
        return self.__NAME

    @property
    def SPREADSHEET_ID(self) -> str:
        return self.__SPREADSHEET_ID

    @property
    def RANGE(self) -> str:
        return self.__RANGE

    @property
    def ValuesCollectionName(self) -> str:
        return self.__ValuesCollectionName

    @ValuesCollectionName.setter
    def ValuesCollectionName(self, value: str):
        if not isinstance(value, str):
            raise Exception(FAIL("Property Error : 'ValuesCollectionName' property of class 'GoogleWriter' must be a string!"))
        if len(value) == 0:
            raise Exception(FAIL("Property Error : 'ValuesCollectionName' property of class 'GoogleWriter' must not be blank!"))
        self.__ValuesCollectionName = value

    @property
    def OutputLabels(self) -> list:
        return self.__OutputLabels

    @OutputLabels.setter
    def OutputLabels(self, value: list):
        if not isinstance(value, list):
            raise Exception(FAIL("Property Error : 'OutputLabels' property of class 'GoogleWriter' must be a list of strings!"))
        if len(value) == 0:
            raise Exception(FAIL("Property Error : 'OutputLabels' property of class 'GoogleWriter' must contain at least one entry!"))
        for el in value:
            if not isinstance(el, str):
                raise Exception(FAIL("Property Error : 'OutputLabels' property of class 'GoogleWriter' must be a list of strings!"))
            if len(el) == 0:
                raise Exception(FAIL("Property Error : 'OutputLabels' property of class 'GoogleWriter' must not contain blank entries!"))
        self.__OutputLabels = value
    
    def __str__(self):
        output = "GoogleWriter: '" + self.NAME + "' \n"
        output += "   \\__ SPREADSHEET_ID: '" + self.SPREADSHEET_ID + "'\n"
        output += "   \\__ RANGE: " + self.RANGE + "\n"
        output += "   \\__ Labels: {}\n".format(self.OutputLabels)
        output += "   \\__ InputCollection Name: {0}\n".format(self.ValuesCollectionName)
        return output
    
    def execute(self, CTX: Context):
        if not isinstance(CTX, Context):
            raise Exception(FAIL("Execute method accept Context objects as input!"))
        
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

        
