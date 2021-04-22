
import gspread        
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

from GoogleSheetsAndForms.Context import Context
from GoogleSheetsAndForms.Messages import FAIL, NOTE

class GoogleBot:
    def __init__(self, name: str, JSON: str):
        self.__NAME = name
        self.__SCOPES: list = ["https://www.googleapis.com/auth/spreadsheets"] 
        self.__JSON: str = JSON
        self.__EXECUTABLE: list = []
        self.__CTX = Context()
        
        # add credentials to the account
        creds = None
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.__JSON, self.__SCOPES)
        except Exception:
            raise Exception(FAIL("Error while getting Service Account Credentials ...!"))

        # authorize the clientsheet 
        gspread.authorize(creds)

        self.__CTX.store("__SERVICE", build('sheets', 'v4', credentials=creds))

    def __str__(self):
        output = "Google Bot '{0}'\n".format(self.NAME)
        output += "   \\__ CREDS AT JSON FILE : '{0}'\n".format(self.JSON)
        output += "   \\__ SCOPES : {0}\n".format(self.SCOPES)
        return output
        
    @property
    def NAME(self):
        return self.__NAME
    
    @property
    def SCOPES(self):
        return self.__SCOPES

    @property
    def JSON(self):
        return self.__JSON

    def addExecutable(self, executable):
        self.__EXECUTABLE.append(executable)
        
    def execute(self):
        print(NOTE("Scheduling sequence for '" + self.NAME + "'"))
        for el in self.__EXECUTABLE:
            print("   \\__ " + el.NAME)
        print()

        print(NOTE("Sequence details ..."))
        for el in self.__EXECUTABLE:
            print(el)
        
        for el in self.__EXECUTABLE:
            el.execute(self.__CTX)
