
if __name__ == '__main__':

    from GoogleSheetsAndForms.Core.GoogleBot import GoogleBot
    from GoogleSheetsAndForms.Core.GoogleSheetsReader import GoogleSheetsReader
    from GoogleSheetsAndForms.RequestMaker_PuntiCanaleGravier import RequestMaker_PuntiCanaleGravier
    from GoogleSheetsAndForms.GoogleFormSubmitter_PuntiCanaleGravier import GoogleFormSubmitter_PuntiCanaleGravier
    from GoogleSheetsAndForms.Core.GoogleWriter import GoogleWriter
    from GoogleSheetsAndForms.Core.Messages import FAIL, WARNING
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--official', action='store_true')
    parser.add_argument('-j', '--json', nargs=1, required=True)
    args = parser.parse_args()    

    jsonFile = args.json[0]
    officialRequest = args.official

    if not officialRequest:
        print(WARNING("NOTE TO THE USER:"))
        print(WARNING("   \\__ This code is being run on 'Testing' mode! No official form will be submitted, nor the offical Google Sheet will be updated."))
        print(WARNING("   \\__ To run on 'Official' mode use --official"))
        print()

    try:
        myfile = open(jsonFile, "r")
        myfile.close()
    except Exception:
        raise Exception(FAIL("JSON file cannot be opened!"))

    # Main Code 
    googleBot = GoogleBot("GoogleBot", jsonFile)

    # Read from Google Sheets
    readerDisegni = GoogleSheetsReader("GoogleSheetsReader DISEGNI", "16d1gW6F5CFTNRySIWiJbpjKFmgFvkT5PpsJnT0oFZuY", ["DISEGNI!A2:A2", "DISEGNI!A5:H"])
    readerDisegni.ValuesCollectionName = ["DISEGNI_METADATA", "DISEGNI_VALUES"]
    googleBot.addExecutable(readerDisegni)

    readerCanzoni = GoogleSheetsReader("GoogleSheetsReader CANZONI", "16d1gW6F5CFTNRySIWiJbpjKFmgFvkT5PpsJnT0oFZuY", ["CANZONI!A2:A2", "CANZONI!A5:H"])
    readerCanzoni.ValuesCollectionName = ["CANZONI_METADATA", "CANZONI_VALUES"]
    googleBot.addExecutable(readerCanzoni)


    
    # Create Requests out of data grom Google Sheets
    makerDisegni = RequestMaker_PuntiCanaleGravier("RequestMaker DISEGNI")
    makerDisegni.ValuesCollectionName = readerDisegni.ValuesCollectionName[1]
    makerDisegni.RequestCollectionName = readerDisegni.ValuesCollectionName[1].replace("VALUES", "REQUESTS")
    googleBot.addExecutable(makerDisegni)

    makerCanzoni = RequestMaker_PuntiCanaleGravier("RequestMaker CANZONI")
    makerCanzoni.ValuesCollectionName = readerCanzoni.ValuesCollectionName[1]
    makerCanzoni.RequestCollectionName = readerCanzoni.ValuesCollectionName[1].replace("VALUES", "REQUESTS")
    googleBot.addExecutable(makerCanzoni)


    
    # These are for Testing purposes
    formDisegni = '1FAIpQLSdIh7YJVqFpbs-X0AWkAukWRbKn4z-zYlLBPt1EbApVGdShig'
    idDisegni = ['entry.1911042707', None, 'entry.1222566434', None, None, None, None, None]

    formCanzoni = '1FAIpQLSdIh7YJVqFpbs-X0AWkAukWRbKn4z-zYlLBPt1EbApVGdShig'
    idCanzoni = ['entry.1911042707', None, 'entry.1222566434', None, None, None, None, None]

    # Thiese are for official Submissions
    if officialRequest:
        formDisegni = '1FAIpQLSdlIk9ip-Je0rsr2qOscOh4q3yyue7Iqv1YbmUdi3WfrGbMVQ'
        idDisegni = ['entry.1943497073', None, 'entry.1374345851', None, None, None, None, None]
        
        formCanzoni = '1FAIpQLSdxHcWVK5CHr6YKuGXmEKXQv_s_oeKdF6GEkrViibhT1C-Kxg'
        idCanzoni = ['entry.1400530917', None, 'entry.1530943645', None, None, None, None, None]

    # Submit entries to Google Forms       
    formSubmitterDisegni = GoogleFormSubmitter_PuntiCanaleGravier("GoogleFormSubmitter DISEGNI", formDisegni)
    formSubmitterDisegni.InputLabels = makerCanzoni.InputLabels
    formSubmitterDisegni.FormIds = idDisegni
    formSubmitterDisegni.RequestCollectionName = makerDisegni.RequestCollectionName
    formSubmitterDisegni.UpdatedRequestCollectionName = makerDisegni.RequestCollectionName + "_SUBMITTED"
    googleBot.addExecutable(formSubmitterDisegni)
    
    formSubmitterCanzoni = GoogleFormSubmitter_PuntiCanaleGravier("GoogleFormSubmitter CANZONI", formCanzoni)
    formSubmitterCanzoni.InputLabels = makerCanzoni.InputLabels
    formSubmitterCanzoni.FormIds = idCanzoni
    formSubmitterCanzoni.RequestCollectionName = makerCanzoni.RequestCollectionName
    formSubmitterCanzoni.UpdatedRequestCollectionName = makerCanzoni.RequestCollectionName + "_SUBMITTED"
    googleBot.addExecutable(formSubmitterCanzoni)


    
    # Update Google Sheet
    if officialRequest:
        writeDisegni = GoogleWriter("GoogleWriter DISEGNI", readerDisegni.SPREADSHEET_ID, "DISEGNI!H5:H")
        writeDisegni.ValuesCollectionName = formSubmitterDisegni.UpdatedRequestCollectionName
        writeDisegni.OutputLabels = ['Inserita']
        googleBot.addExecutable(writeDisegni)
        
        writerCanzoni = GoogleWriter("GoogleWriter CANZONI", readerCanzoni.SPREADSHEET_ID, "CANZONI!H5:H")
        writerCanzoni.ValuesCollectionName = formSubmitterCanzoni.UpdatedRequestCollectionName
        writerCanzoni.OutputLabels = ['Inserita']
        googleBot.addExecutable(writerCanzoni)

        

    # Run the code
    googleBot.execute()

    
