

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
            raise Exception("Non è possibile determinare i form ID per le richieste " + name )
            
    def __str__(self):
        output = "Link Modulo: " + self.modulo + "\n"
        output += "Elenco delle richieste : "  + self.name + "\n" 
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
        return re.findall("(http.*)",objects[0][0])[0].strip()
    
    def addRequest(self,account,data,richiesta,inserita):
        toAdd = {}
        toAdd['AccountTwitch'] = account
        toAdd['DataRiscatto'] = data
        toAdd['Richiesta'] = richiesta
        toAdd['Inserita'] = inserita
        self.richieste.append( toAdd )

    def processSheet(self,results):
        for i in range(3,len(results)):
            el = results[i]
            self.addRequest( el[0],el[1],el[2],el[7] )

    def getRequests(self,filtered=True):
        if not filtered:
            return self.richieste
        return [x for x in self.richieste if not x['Inserita'] ]

    
def retrieveValues():
    import gspread        
    from oauth2client.service_account import ServiceAccountCredentials
    from googleapiclient.discovery import build
    
    # define the scope
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '16d1gW6F5CFTNRySIWiJbpjKFmgFvkT5PpsJnT0oFZuY'
    SAMPLE_RANGE_NAME_DISEGNI = 'DISEGNI!A2:H'
    SAMPLE_RANGE_NAME_CANZONI = 'CANZONI!A2:H'

    print( 'Getting google sheet "' + SAMPLE_SPREADSHEET_ID + '"' )
    
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('./data/RiscattoPuntiCanale-b1487f27cab1.json', SCOPES)
    
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


def compileForm(name,objects):
    import requests
    import time

    print( "   \\__ Compilazione moduli per " + name )
    print( "      \\__ Modulo: " + objects.modulo )

    linkModulo = objects.modulo
    id_nome = objects.getFormIdName()
    id_richiesta = objects.getFormIdRichiesta()

    ### TMP
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
            print("      \\__ Form Submitted for " + d[id_nome])

            el['Inserita'] = "Y"
            time.sleep(1)            
        except:
            print("      \\__ Error Occured for " + d[id_nome])
            

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

    ### Read and Store Data from Google Sheet
    [service,disegni,canzoni] = retrieveValues()
    RichiesteDisegni = Richieste( "DISEGNI",disegni )
    RichiesteCanzoni = Richieste( "CANZONI",canzoni )
    
    print(RichiesteDisegni)
    print(RichiesteCanzoni)

    ### Compile Form
    print( "Compiling Google forms ... " )
    compileForm("DISEGNI",RichiesteDisegni)
    compileForm("CANZONI",RichiesteCanzoni)    
    print("")
    
    ### Update Google Sheet
    updateValues( service,RichiesteDisegni,RichiesteCanzoni )
    
    



    
