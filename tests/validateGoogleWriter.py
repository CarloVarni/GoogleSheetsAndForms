
from GoogleSheetsAndForms.Core.Messages import NOTE, OK, FAIL

class Validator:
    def __init__(self, NAME):
        self.__NAME = NAME
        self.InputCollections = []
        self.ReferenceData = []
        
    @property
    def NAME(self):
        return self.__NAME

    def __str__(self):
        output = "Validator: '{0}'\n".format(self.NAME)
        output += "   \\__ Input Collection Names: '{}'\n".format(self.InputCollections)
        output += "   \\__ Reference Collection Name: '{}'\n".format(self.ReferenceData)
        return output
    
    def execute(self, CTX):
        if len(self.InputCollections) == 0:
            raise Exception(FAIL("No Input Collection available!"))
        if len(self.ReferenceData) == 0:
            raise Exception(FAIL("No Reference Collection available!"))
        
        print(NOTE("Comparing Data Collections ..."))

        for i in range(0, len(self.InputCollections)):
            print("   \\__ Comaparing '{0}'[input] with '{1}'[reference]".format(self.InputCollections[i], self.ReferenceData[i]))
            inputs = CTX.retrieve(self.InputCollections[i])
            references = CTX.retrieve(self.ReferenceData[i])
            try:
                self.compareCollections(inputs, references)
                print("      \\__ Validation Status: {0}".format(OK("SUCCESS")))
            except Exception:
                print("      \\__ Validation Status: {0}\n".format(FAIL("FAILURE")))
                raise Exception(FAIL("GoogleWriter Validator FAILED"))
        print()

    def compareCollections(self, inputs, references):
        if len(inputs) != len(references):
            raise Exception(FAIL("Wrong size of collection"))
        
        for i in range(0, len(inputs)):
            IN = inputs[i]
            REF = references[i]
            if IN != REF:
                raise Exception(FAIL("Input and Reference Entries are different!"))
        
    

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

def retrieveFewViewCounts():
    return [
        ["5508"],
        ["4160"],
        ["4465"],
        ["4475"],
        ["2574"],
        ["5166"],
        ["3532"],
        ["4602"],
        ["5065"],
        ["3729"],
    ]


def retrieveRandomNumbers():
    from random import random

    output = []
    for i in range(0, 4):
        toAdd = []
        for j in range(0, 15):
            toAdd.append(str(random()))
        output.append(toAdd)

    return output



def createRefDictionary(inputs, labels):
    output = []
    for el in inputs:
        toAdd = {}
        for i in range(0, len(labels)):
            toAdd[labels[i]] = el[i]
        output.append(toAdd)

    return output




if __name__ == '__main__':

    from GoogleSheetsAndForms.Core.GoogleBot import GoogleBot
    from GoogleSheetsAndForms.Core.GoogleSheetsReader import GoogleSheetsReader
    from GoogleSheetsAndForms.Core.GoogleWriter import GoogleWriter
    from GoogleSheetsAndForms.Core.DataAdder import DataAdder
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


    
    # Main Code
    googleBot = GoogleBot("GoogleBot", jsonFile)

    # Module
    SPREADSHEET = "1rVk0Teog5d1lvKmosHle-ZruT185bPKZL2_Z5rGVHgQ"
    RANGES = [
        "WRITER!A2:I11",
        "WRITER!K2:K11",
        "WRITER!A14:O17"
    ]
    FORMATS = [
        [str, str, str, str, str, str, str, str, str],
        [str],
        [str, str, str, str]
    ]
    LABELS = [
        ["ID", "TITLE", "CREATED AT", "DATE", "URL", "VIEWABLE", "VIEW_COUNT", "LANGUAGE", "DURATION"],
        ["VIEW COUNTS"],
        ["N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9", "N10", "N11", "N12", "N13", "N14", "N15"]
    ]    
    DATA = [
        retrieveAllVODS(),
        retrieveFewViewCounts(),
        retrieveRandomNumbers()
    ]

    collectionDataNameList = []
    collectionDataList = []
    for i in range(0, len(RANGES)):
        collectionDataNameList.append("DATA_RAW_" + RANGES[i])
        collectionDataNameList.append("DATA_" + RANGES[i])

        collectionDataList.append(DATA[i])
        collectionDataList.append(createRefDictionary(DATA[i], LABELS[i]))

    dataAdder = DataAdder("DataAdder")
    dataAdder.OutputCollectionName = collectionDataNameList
    dataAdder.Data = collectionDataList
    googleBot.addExecutable(dataAdder)
    
    
    for i in range(0, len(RANGES)):
        RANGE = [RANGES[i]]
        DATA_COLLECTION = DATA[i]
        FORMAT = FORMATS[i]
        LABEL = LABELS[i]

        # Write everything to a Google Sheet
        googleWriter = GoogleWriter("GoogleWriter_" + RANGE[0], SPREADSHEET, RANGE[0])
        googleWriter.ValuesCollectionName = "DATA_" + RANGE[0]
        googleWriter.OutputLabels = LABEL
        googleBot.addExecutable(googleWriter)
    
    googleReader = GoogleSheetsReader("GoogleSheetsReader", SPREADSHEET, RANGES)
    googleReader.ValuesCollectionName = ["VODS", "VIEWS", "RANDOM"]
    googleBot.addExecutable(googleReader)

    # Validator
    validator = Validator("GoogleWriterValidator")
    validator.InputCollections = googleReader.ValuesCollectionName
    validator.ReferenceData = ["DATA_RAW_" + el for el in RANGES]
    googleBot.addExecutable(validator)
    
    googleBot.execute()
