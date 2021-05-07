
import gspread        
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

from GoogleSheetsAndForms.Core.Context import Context
from GoogleSheetsAndForms.Core.Messages import FAIL, NOTE

class GoogleBot:
    def __init__(self, name: str, JSON: str):
        self.__NAME: str = name
        self.__SCOPES: list[str] = ["https://www.googleapis.com/auth/spreadsheets",
                                    "https://www.googleapis.com/auth/documents"]
        self.__JSON: str = JSON
        self.__EXECUTABLE: list = []
        self.__CTX: Context = Context()
        
    def __str__(self):
        output = "Google Bot '{0}'\n".format(self.NAME)
        output += "   \\__ CREDS AT JSON FILE : '{0}'\n".format(self.JSON)
        output += "   \\__ SCOPES : {0}\n".format(self.SCOPES)
        return output
        
    @property
    def NAME(self) -> str:
        return self.__NAME
    
    @property
    def SCOPES(self) -> list:
        return self.__SCOPES

    @property
    def JSON(self) -> str:
        return self.__JSON

    @property
    def EXECUTABLE(self) -> list:
        return self.__EXECUTABLE

    @property
    def CONTEXT(self) -> Context:
        return self.__CTX
    
    def addExecutable(self, executable):
        self.__EXECUTABLE.append(executable)
        
    def execute(self):
        print(NOTE("Scheduling sequence for '" + self.NAME + "'"))
        for el in self.EXECUTABLE:
            print("   \\__ " + el.NAME)
        print()

        print(NOTE("Sequence details ..."))
        for el in self.EXECUTABLE:
            print(el)

        # add credentials to the account
        creds = None
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.__JSON, self.__SCOPES)
        except Exception:
            raise Exception(FAIL("Error while getting Service Account Credentials ...!"))

        # authorize the client
        gspread.authorize(creds)

        services = {}
        for scope in self.SCOPES:
            if "spreadsheets" in scope:
                services["sheets"] = build('sheets', 'v4', credentials=creds)
            elif "documents" in scope:
                services["docs"] = build('docs', 'v1', credentials=creds)

        if len(services) == 0:
            raise Exception(FAIL("Google bot does not have SCOPES!"))
        self.__CTX.store("__SERVICE", services)

        # run all the algorithms
        for el in self.EXECUTABLE:
            el.execute(self.__CTX)
