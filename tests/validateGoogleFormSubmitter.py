
def retrieveAllVODS():
    return [
        ['995684704', 'TBoI Repentance - DEVO VINCERE!!!', '2021-04-21T18:03:59Z', '2021-04-21T18:03:59Z', 'https://www.twitch.tv/videos/995684704', 'public', '4114', 'it', '2h51m10s'],
        ['994521272', 'Finiamo Mario Galaxy, ma non posso arrabbiarmi...', '2021-04-20T18:00:22Z', '2021-04-20T18:00:22Z', 'https://www.twitch.tv/videos/994521272', 'public', '3888', 'it', '4h1m10s'],
        ['993410111', 'Finiamo Everhood!', '2021-04-19T18:10:27Z', '2021-04-19T18:10:27Z', 'https://www.twitch.tv/videos/993410111', 'public', '2192', 'it', '2h33m46s'],
        ['993402468', 'Finiamo Everhood!', '2021-04-19T18:04:12Z', '2021-04-19T18:04:12Z', 'https://www.twitch.tv/videos/993402468', 'public', '203', 'it', '5m12s'],
        ['992323837', 'La vita di Gravier', '2021-04-18T18:02:16Z', '2021-04-18T18:02:16Z', 'https://www.twitch.tv/videos/992323837', 'public', '4198', 'it', '2h55m39s'],
        ['991054896', 'Continuiamo Everhood perché il gioco e nice!', '2021-04-17T18:00:39Z', '2021-04-17T18:00:39Z', 'https://www.twitch.tv/videos/991054896', 'public', '2794', 'it', '2h57m33s'],
        ['989737687', 'TBoI Repentance, ma 1 Morte = 1 Minuti di Plank', '2021-04-16T18:02:16Z', '2021-04-16T18:02:16Z', 'https://www.twitch.tv/videos/989737687', 'public', '4242', 'it', '2h40m42s'],
        ['988555317', 'Finiamo Mario Galaxy! (Se la connessione lo permette...)', '2021-04-15T18:04:08Z', '2021-04-15T18:04:08Z', 'https://www.twitch.tv/videos/988555317', 'public', '3739', 'it', '3h31m4s'],
        ['987223744', "Guardiamo l'INDIE WORLD Nintendo!", '2021-04-14T15:31:05Z', '2021-04-14T15:31:05Z', 'https://www.twitch.tv/videos/987223744', 'public', '2484', 'it', '1h3m38s'],
        ['987222199', "Guardiamo l'INDIE WORLD Nintendo!", '2021-04-14T15:29:16Z', '2021-04-14T15:29:16Z', 'https://www.twitch.tv/videos/987222199', 'public', '139', 'it', '36s'],
    ]


if __name__ == '__main__':

    from GoogleSheetsAndForms.Core.GoogleBot import GoogleBot
    from GoogleSheetsAndForms.Core.DataAdder import DataAdder
    from GoogleSheetsAndForms.Request import Request
    from GoogleSheetsAndForms.Core.GoogleFormSubmitter import GoogleFormSubmitter
    from GoogleSheetsAndForms.Core.Messages import FAIL
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--json', nargs=1, required=True)
    args = parser.parse_args()    

    jsonFile = args.json[0]
    try:
        myfile = open(jsonFile, "r")
        myfile.close()
    except Exception:
        raise Exception(FAIL("JSON file cannot be opened!"))


    # Info
    FORM = "1FAIpQLSfPIKINX5I-snrFCHZiXfCh-IEtUtfm0D3X37iBk08wdN8FUA"
    IDs = [
        "entry.991192545",
        "entry.579164628",
        "entry.1946890330",
        "entry.409446985",
        "entry.64677947",
        "entry.341864836",
        "entry.346238205",
        "entry.750962308",
        "entry.1435080864",
        "entry.1351012077",
        "entry.974512993"
    ]
    LABELS = ["SUBMITTER", "TODAY", "ID", "TITLE", "CREATED AT", "DATE", "URL", "VIEWABLE", "VIEW_COUNT", "LANGUAGE", "DURATION"]

    from datetime import date

    today = date.today()
    
    DATA = retrieveAllVODS()
    for i in range(0, len(DATA)):
        DATA[i] = ["GoogleFormSubmitter Validator", today.strftime("%d/%m/%Y")] + DATA[i]

    request = Request("Request for Validation", LABELS)
    request.processInput(DATA)
    
    # Main Code
    googleBot = GoogleBot("GoogleBot", jsonFile)
    
    # Module
    dataAdder = DataAdder("DataAdder")
    dataAdder.OutputCollectionName = ["VALUES"]
    dataAdder.Data = [request]
    googleBot.addExecutable(dataAdder)
    
    formSumbitter = GoogleFormSubmitter("GoogleFormSubmitter", FORM)
    formSumbitter.InputLabels = LABELS
    formSumbitter.FormIds = IDs
    formSumbitter.RequestCollectionName = "VALUES"
    formSumbitter.UpdatedRequestCollectionName = "VALUES_SUBMITTED"
    googleBot.addExecutable(formSumbitter)

    googleBot.execute()
