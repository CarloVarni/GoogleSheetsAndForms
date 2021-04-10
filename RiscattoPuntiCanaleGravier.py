

class Richieste:
    def __init__(self,name,results):
        self.name = name
        self.modulo = self.getLinkModulo( results )
        self.idForm = []
        self.richieste = []
        self.processSheet( results )

        if self.name == "DISEGNI":
            self.idForm = ['entry.1943497073','entry.1374345851']
        elif self.name == "CANZONI":
            self.idForm = ['entry.1400530917','entry.1530943645']
        else:
            raise Exception("Cannot determine the Google Form IDs for the requests " + self.name )
            
    def __str__(self):
        output = "Link of the Google Form: " + self.modulo + "\n"
        output += "List of requests : "  + self.name + "\n" 
        for el in self.richieste:
            text = "   \\__ " + el['AccountTwitch'] + " [" + el['DataRiscatto'] + "]: '" + el['Richiesta'] + "' [" + el['Inserita'] + "]"
            output += text + "\n"
        return output

    def getFormIdName(self):
        return self.idForm[0]

    def getFormIdRichiesta(self):
        return self.idForm[1]
    
    def getLinkModulo(self,objects):
        import re

        reMatches = None
        try:
            reMatches = re.findall("(http.*)",objects[0][0])
        except:
            raise Exception( "Error while retrieving the link of the Google Form for Google Sheet " + self.name )

        if reMatches == None or len( reMatches ) == 0:
            raise Exception( "Cannot Retrieve the link of the Google Form for Google Sheet "+ self.name )

        return reMatches[0].strip()

    def validateRequest(self,account,data,richiesta,inserita):
        if len(account) == 0:
            raise Exception( "Invalid Twitch Account for entry in Google Sheet " + self.name )
        if len(data) == 0:
            raise Exception( "Invalid Date for entry in Google Sheet " + self.name )
        if len(richiesta) == 0:
            raise Exception( "Invalid Request for entry in Google Sheet " + self.name )
        if inserita != "Y" and inserita != "N":
            raise Exception( "Invalid 'Inserted status' [Y/N] for entry in Google Sheet " + self.name )
        
    def addRequest(self,account,data,richiesta,inserita):
        self.validateRequest( account,data,richiesta,inserita )

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

    print( 'Getting Google Sheet "' + SAMPLE_SPREADSHEET_ID + '"' )
    
    # add credentials to the account
    creds = None
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(jsonFle, SCOPES)
    except:
        raise Exception("Error while getting Service Account Credentials ...!")
        
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
        
    richieste = objects.getRequests( filtered=False )
    for i in range(0,len(richieste)):
        el = richieste[i]
        if el['Inserita'] == "Y":
            continue;

        try:
            d = {}
            d[id_nome] = el['AccountTwitch']
            d[id_richiesta] = el['Richiesta']    
            requests.post( linkModulo.replace("viewform","formResponse"),data=d)
            print("         \\__ Form Submitted for " + d[id_nome])

            el['Inserita'] = "Y"
            time.sleep(1)            
        except:
            print("         \\__ Error Occured for " + d[id_nome])
            

def updateValues(service,disegni,canzoni):
    print( "Updating Google Sheet ..." )
    
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
        print( "NOTE TO THE USER:" )
        print( "   \__ This code is being run on 'Testing' mode! No official form will be submitted, nor the offical Google Sheet will be updated." )
        print( "   \__ To run on 'Official' mode use --official" )
        print( "" )

    try:
        myfile = open(jsonFile, "r")
        myfile.close()
    except:
        raise Exception("JSON file cannot be opened!")
        
    ### Read and Store Data from Google Sheet
    [service,disegni,canzoni] = retrieveValues(jsonFile)
    RichiesteDisegni = Richieste( "DISEGNI",disegni )
    RichiesteCanzoni = Richieste( "CANZONI",canzoni )
    
    print(RichiesteDisegni)
    print(RichiesteCanzoni)

    ### Compile Form
    print( "Compiling Google Forms ... " )
    compileForm(RichiesteDisegni,officialSubmit=officialRequest)
    compileForm(RichiesteCanzoni,officialSubmit=officialRequest)    
    print("")
    
    ### Update Google Sheet
    if officialRequest:
        updateValues( service,RichiesteDisegni,RichiesteCanzoni )
    
    



    
