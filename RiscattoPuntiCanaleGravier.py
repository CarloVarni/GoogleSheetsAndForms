
import re

class bcolors:
    OK = '\033[1;32m' #GREEN
    WARNING = '\033[1;33m' #YELLOW
    FAIL = '\033[1;31m' #RED
    NOTE = '\033[1;35m' #PURPLE 
    RESET = '\033[0;0m' #RESET COLOR
    
class Richieste:
    def __init__(self,name: str,results: list):
        self.__name: str = name
        self.__modulo: str = self.getLinkModulo( results )
        self.__idForm: list = []
        self.__richieste: list = []
        self.__size: list = [0,0,0] # Y/OTHER/N
        self.processSheet( results )

        if self.name == "DISEGNI":
            self.__idForm = ['entry.1943497073','entry.1374345851']
        elif self.name == "CANZONI":
            self.__idForm = ['entry.1400530917','entry.1530943645']
        else:
            raise Exception( bcolors.FAIL + "Cannot determine the Google Form IDs for the requests " + self.name + bcolors.RESET )

    @property
    def name(self):
        return self.__name

    @property
    def modulo(self):
        return self.__modulo
    
    @property
    def richieste(self):
        return self.__richieste
    
    def __str__(self):
        output = bcolors.NOTE + "Summary of requests for Google Sheet: " + self.name + bcolors.RESET + "\n" 
        output += "Link of the Google Form: '" + self.modulo + "'\n"
        output += "List of " + str(self.size()) + " " + self.sizeText() + " requests : "  + self.name + "\n" 
        for el in self.richieste:
            text = "   \\__ ["
            if el['Inserita'] == "Y":
                text += bcolors.OK
            elif el['Inserita'] == "C":
                text += bcolors.WARNING
            else:
                text += bcolors.FAIL

            text += "{0}{1}] ".format(el['Inserita'],bcolors.RESET) 
            text += "{0} [{1}]: '{2}'".format(el['AccountTwitch'],el['DataRiscatto'],el['Richiesta'])
            output += text + "\n"
        return output

    def size(self,component=""):
        if component == "": return sum(self.__size)
        if component == "Y": return self.__size[0]
        if component == "N": return self.__size[2]
        return self.__size[1]

    def sizeText(self):
        text = "[{},{},{}]".format( bcolors.OK + str(self.__size[0]) + bcolors.RESET,
                                    bcolors.WARNING + str(self.__size[1]) + bcolors.RESET,
                                    bcolors.FAIL + str(self.__size[2]) + bcolors.RESET )
        return text
    
    def getFormIdName(self):
        return self.__idForm[0]

    def getFormIdRichiesta(self):
        return self.__idForm[1]
    
    def getLinkModulo(self,objects):
        reMatches = None
        try:
            reMatches = re.findall("(http.*)",objects[0][0])
        except:
            raise Exception( bcolors.FAIL + "Error while retrieving the link of the Google Form for Google Sheet " + self.name + bcolors.RESET )

        if reMatches == None or len( reMatches ) == 0:
            raise Exception( bcolors.FAIL + "Cannot Retrieve the link of the Google Form for Google Sheet "+ self.name + bcolors.RESET )

        return reMatches[0].strip()

    def validateRequest(self,account,data,richiesta,inserita):
        # Check account name
        if len(account) == 0:
            raise Exception( bcolors.FAIL + "Invalid Twitch Account for entry in Google Sheet " + self.name + bcolors.RESET )

        # Chech date
        calendarDate = re.findall("^([0-9]{2})/([0-9]{2})/([0-9]{4})$",data)
        if len(data) == 0 or len(calendarDate) != 1:
            raise Exception( bcolors.FAIL + "Invalid Date for entry in Google Sheet " + self.name + bcolors.RESET )

        [dd,mm,yyyy] = calendarDate[0]
        dd,mm,yyyy = int(dd),int(mm),int(yyyy)
        if mm > 12 or dd > 31 or yyyy < 2021:
            raise Exception( bcolors.FAIL + "Invalid Date for entry in Google Sheet " + self.name + bcolors.RESET )
        
        # Check request entry
        if len(richiesta) == 0:
            raise Exception( bcolors.FAIL + "Invalid Request for entry in Google Sheet " + self.name + bcolors.RESET )

        # check request status
        if inserita != "Y" and inserita != "N" and inserita != "C":
            raise Exception( bcolors.FAIL + "Invalid 'Inserted status' [Y/N] for entry in Google Sheet " + self.name + bcolors.RESET)

        
    def addRequest(self,account,data,richiesta,inserita):
        self.validateRequest( account.strip(),
                              data.strip(),
                              richiesta.strip(),
                              inserita.strip() )

        toAdd = {}
        toAdd['AccountTwitch'] = account.strip()
        toAdd['DataRiscatto'] = data.strip()
        toAdd['Richiesta'] = richiesta.strip()
        toAdd['Inserita'] = inserita.strip()
        self.richieste.append( toAdd )

    def processSheet(self,results):
        for i in range(3,len(results)):
            el = results[i]
            self.addRequest( el[0],el[1],el[2],el[7] )
            if el[7] == "Y":
                self.__size[0] += 1
            elif el[7] == "N":
                self.__size[2] += 1
            else:
                self.__size[1] += 1
                
    def getRequests(self,filtered):
        if not filtered:
            return self.richieste
        return [x for x in self.richieste if x['Inserita'] == "Y" ]

    
def retrieveValues(jsonFle):
    import gspread        
    from oauth2client.service_account import ServiceAccountCredentials
    from googleapiclient.discovery import build
    
    # define the scope
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '16d1gW6F5CFTNRySIWiJbpjKFmgFvkT5PpsJnT0oFZuY'
    SAMPLE_RANGE_NAME_DISEGNI = 'DISEGNI!A2:H'
    SAMPLE_RANGE_NAME_CANZONI = 'CANZONI!A2:H'

    print( bcolors.NOTE + "Reading data from Google Sheet ... " + bcolors.RESET )
    print( 'Getting Google Sheet "' + SAMPLE_SPREADSHEET_ID + '"' )
    
    # add credentials to the account
    creds = None
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(jsonFle, SCOPES)
    except:
        raise Exception( bcolors.FAIL + "Error while getting Service Account Credentials ...!" + bcolors.RESET)
        
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    
    service = build('sheets', 'v4', credentials=creds)
    
    # Read Sheet dei disegni    
    print( "   \\__ Retrieving DISEGNI sheet..." )
    sheet_disegni = service.spreadsheets()
    result_disegni = sheet_disegni.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                range=SAMPLE_RANGE_NAME_DISEGNI).execute()
    values_disegni = result_disegni.get('values', [])

    print( "   \\__ Retrieving CANZONI sheet..." )
    sheet_canzoni = service.spreadsheets()
    result_canzoni = sheet_canzoni.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                range=SAMPLE_RANGE_NAME_CANZONI).execute()
    values_canzoni = result_canzoni.get('values', [])
    print("")
    return [service,values_disegni,values_canzoni]


def compileForm(objects,officialSubmit=False):
    import requests
    import time

    print( "   \\__ Compiling Forms for " + objects.name )
    print( "      \\__ Form: " + objects.modulo )

    linkModulo = objects.modulo
    id_nome = objects.getFormIdName()
    id_richiesta = objects.getFormIdRichiesta()
    
    ### This is for Testing
    if not officialSubmit:
        linkModulo = "https://docs.google.com/forms/d/e/1FAIpQLSdIh7YJVqFpbs-X0AWkAukWRbKn4z-zYlLBPt1EbApVGdShig/viewform"
        id_nome = 'entry.1911042707'
        id_richiesta = 'entry.1222566434'

    counterUpdatedRequests = 0
    counterFailedRequests = 0
    
    richieste = objects.getRequests( filtered=False )
    for i in range(0,len(richieste)):
        el = richieste[i]
        if el['Inserita'] != "N":
            continue;

        try:
            d = {}
            d[id_nome] = el['AccountTwitch']
            d[id_richiesta] = el['Richiesta']    
            requests.post( linkModulo.replace("viewform","formResponse"),data=d)
            print( "         \\__ Form Submitted for: " + d[id_nome])

            el['Inserita'] = "Y"
            counterUpdatedRequests += 1
            time.sleep(1)            
        except:
            print( bcolors.FAIL + "         \\__ Error Occured for " + d[id_nome] + bcolors.RESET)
            counterFailedRequests += 1
            
    print( bcolors.OK + "      \\__ Total Entries Submitted : " + str( counterUpdatedRequests ) + bcolors.RESET )
    if counterFailedRequests != 0:
        print( bcolors.FAIL + "         \\__ Total Entries Failed : " + str( counterFailedRequests ) + bcolors.RESET )

def updateValues(service,disegni,canzoni):
    print( bcolors.NOTE + "Updating Google Sheet ..." + bcolors.RESET )
    
    # The ID and range of a sample spreadsheet.   
    SAMPLE_SPREADSHEET_ID = '16d1gW6F5CFTNRySIWiJbpjKFmgFvkT5PpsJnT0oFZuY'
    SAMPLE_RANGE_NAME_DISEGNI = 'DISEGNI!H5:H'
    SAMPLE_RANGE_NAME_CANZONI = 'CANZONI!H5:H'

    ## Update Disegni
    RichiesteDisegni = disegni.getRequests( filtered=False )
    value_range_body_disegni = {'values': [ [x['Inserita'] for x in RichiesteDisegni] ],
                                'majorDimension' : 'COLUMNS'}
    service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                           range=SAMPLE_RANGE_NAME_DISEGNI,
                                           valueInputOption="RAW",
                                           body=value_range_body_disegni).execute()
    print( "   \\__ Google sheet updated : DISEGNI" )
    
    ## Update Canzoni
    RichiesteCanzoni = canzoni.getRequests( filtered=False )
    value_range_body_canzoni = {'values': [ [x['Inserita'] for x in RichiesteCanzoni] ],
                                'majorDimension' : 'COLUMNS'}
    service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                           range=SAMPLE_RANGE_NAME_CANZONI,
                                           valueInputOption="RAW",
                                           body=value_range_body_canzoni).execute()
    print( "   \\__ Google sheet updated : CANZONI" )

    
if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--official',action='store_true' )
    parser.add_argument('-j', '--json', nargs=1, required=True )
    args = parser.parse_args()    

    jsonFile = args.json[0]
    officialRequest = args.official

    if not officialRequest:
        print( bcolors.WARNING + "NOTE TO THE USER:" + bcolors.RESET )
        print( bcolors.WARNING + "   \__ This code is being run on 'Testing' mode! No official form will be submitted, nor the offical Google Sheet will be updated." + bcolors.RESET )
        print( bcolors.WARNING + "   \__ To run on 'Official' mode use --official" + bcolors.RESET )
        print( "" )

    try:
        myfile = open(jsonFile, "r")
        myfile.close()
    except:
        raise Exception( bcolors.FAIL + "JSON file cannot be opened!" + bcolors.RESET )
        
    ### Read and Store Data from Google Sheet
    [service,disegni,canzoni] = retrieveValues(jsonFile)
    RichiesteDisegni = Richieste( "DISEGNI",disegni )
    RichiesteCanzoni = Richieste( "CANZONI",canzoni )
    
    print( bcolors.OK + "Total of " + str( RichiesteDisegni.size() + RichiesteCanzoni.size() ) + " entries... \n" + bcolors.RESET )
    print(RichiesteDisegni)
    print(RichiesteCanzoni)
    
    ### Compile Form
    print( bcolors.NOTE + "Compiling Google Forms ... " + bcolors.RESET )
    compileForm(RichiesteDisegni,officialSubmit=officialRequest)
    compileForm(RichiesteCanzoni,officialSubmit=officialRequest)    
    print("")
    
    ### Update Google Sheet
    if officialRequest:
        updateValues( service,RichiesteDisegni,RichiesteCanzoni )
    
    



    

