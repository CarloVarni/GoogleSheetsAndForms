
from GoogleSheetsAndForms.RequestMaker import RequestMaker
from GoogleSheetsAndForms.Core.Messages import OK, WARNING, FAIL
import re

class RequestMaker_PuntiCanaleGravier(RequestMaker):
    def __init__(self, NAME: str):
        super().__init__(NAME,
                         validateFunction=self.defaultValidateFunction,
                         printFunction=self.defaultPrintFormat)

        # This is case dependent
        self.InputFormat: list = [str, str, str, None, None, None, None, str]
        self.InputLabels: list = ['AccountTwitch', 'DataRiscatto', 'Richiesta', None, None, None, None, 'Inserita']
        
    def defaultPrintFormat(self, listReqs: list) -> str:
        size = [0, 0, 0]  # Y/OTHER/N
        
        listRequets = ""        
        for el in listReqs:

            MESSAGE = None
            if el['Inserita'] == "Y":
                MESSAGE = OK
                size[0] += 1
            elif el['Inserita'] == "N":
                MESSAGE = FAIL
                size[2] += 1
            else:
                MESSAGE = WARNING
                size[1] += 1

            listRequets += "   \\__ [" + MESSAGE(el['Inserita']) + "] {0} [{1}]: '{2}'".format(el['AccountTwitch'], el['DataRiscatto'], el['Richiesta']) + "\n"

        output = "List of {0} [{1},{2},{3}] requests ... \n".format(str(sum(size)),
                                                                    OK(size[0]),
                                                                    WARNING(size[1]),
                                                                    FAIL(size[2]))
        output += listRequets
        return output
    
    def defaultValidateFunction(self, req: dict):
        account = req['AccountTwitch']
        data = req['DataRiscatto']
        richiesta = req['Richiesta']
        inserita = req['Inserita']

        # Check account name
        if len(account) == 0:
            raise Exception(FAIL("Invalid Twitch Account for entry in Google Sheet " + self.name))
        
        # Chech date
        calendarDate = re.findall("^([0-9]{2})/([0-9]{2})/([0-9]{4})$", data)
        if len(data) == 0 or len(calendarDate) != 1:
            raise Exception(FAIL("Invalid Date for entry in Google Sheet " + self.name))

        [dd, mm, yyyy] = calendarDate[0]
        dd, mm, yyyy = int(dd), int(mm), int(yyyy)
        if mm > 12 or dd > 31 or yyyy < 2021:
            raise Exception(FAIL("Invalid Date for entry in Google Sheet " + self.name))
        
        # Check request entry
        if len(richiesta) == 0:
            raise Exception(FAIL("Invalid Request for entry in Google Sheet " + self.name))

        # check request status
        if inserita != "Y" and inserita != "N" and inserita != "C":
            raise Exception(FAIL("Invalid 'Inserted status' [Y/N] for entry in Google Sheet " + self.name))
