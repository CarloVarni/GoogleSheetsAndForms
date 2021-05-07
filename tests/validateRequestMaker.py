
from GoogleSheetsAndForms.Core.Messages import NOTE, OK, FAIL

class Validator:
    def __init__(self, NAME):
        self.__NAME = NAME
        self.InputCollections = []
        self.ReferenceData = []
        self.Labels = []
        
    @property
    def NAME(self):
        return self.__NAME

    def __str__(self):
        output = "Validator: '{0}'\n".format(self.NAME)
        output += "   \\__ Input Collection Names: '{}'\n".format(self.InputCollections)
        output += "   \\__ Reference Collection Name: '{}'\n".format(self.ReferenceData)
        output += "   \\__ Labels:\n"
        for el in self.Labels:
            output += "      \\__ {}\n".format(el)
        return output
    
    def execute(self, CTX):
        if len(self.InputCollections) == 0:
            raise Exception(FAIL("No Input Collection available!"))
        if len(self.ReferenceData) != len(self.InputCollections):
            raise Exception(FAIL("Reference and Input Collection must match!"))
        if len(self.InputCollections) != len(self.Labels):
            raise Exception(FAIL("Labels must match input and reference format"))

        print(NOTE("Comparing Data Collections ..."))        

        for i in range(0, len(self.InputCollections)):
            LABEL = self.Labels[i]
            INPUT = self.InputCollections[i]
            REFERENCE = self.ReferenceData[i]
        
            print("   \\__ Comparing '{0}' with '{1}' using labels {2}".format(INPUT, REFERENCE, LABEL))

            inputCollection = CTX.retrieve(INPUT).requests
            referenceCollection = CTX.retrieve(REFERENCE)
            try:
                self.validateRequests(LABEL, inputCollection, referenceCollection)
                print("      \\__ Validation Status: {0}\n".format(OK("SUCCESS")))
            except Exception:
                print("      \\__ Validation Status: {0}\n".format(FAIL("FAILURE")))
                raise Exception(FAIL("RequestMaker Validator FAILED"))
                
    def validateRequests(self, labels, requests, references):
        if requests is None:
            raise Exception(FAIL("Request object is None! Cannot Validate!"))
        if references is None:
            raise Exception(FAIL("Reference object is None! Cannot Validate!"))
            
        if len(requests) != len(references):
            raise Exception(FAIL("Wrong number of requests w.r.t. references"))
    
        shortlistedLabels = [key for key in labels if key is not None]
        for i in range(0, len(requests)):
            if len(shortlistedLabels) != len(requests[i]):
                raise Exception(FAIL("Wrong number of items stored inside the dictionary! It does not match the labels!"))
            
        for key in shortlistedLabels:            
            if requests[i][key] != references[i][key]:
                raise Exception(FAIL("Wrong values stored for key '{0}'".format(key)))
            
                
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
        ['986219301', 'Proviamo Everhood! (Undertale Rythm Game?)', '2021-04-13T18:04:13Z', '2021-04-13T18:04:13Z', 'https://www.twitch.tv/videos/986219301', 'public', '3315', 'it', '2h32m10s'],
        ['985063128', 'Super Mario Galaxy, ma skippo tutto!', '2021-04-12T18:02:48Z', '2021-04-12T18:02:48Z', 'https://www.twitch.tv/videos/985063128', 'public', '3697', 'it', '3h2m34s'],
        ['983968540', 'TBoI Repentance, ma 1 Morte = 10 Squat', '2021-04-11T18:04:16Z', '2021-04-11T18:04:16Z', 'https://www.twitch.tv/videos/983968540', 'public', '5508', 'it', '3h0m32s'],
        ['982672616', 'Super Mario Galaxy, ma faccio tutto in modo sbagliato!', '2021-04-10T18:00:49Z', '2021-04-10T18:00:49Z', 'https://www.twitch.tv/videos/982672616', 'public', '4160', 'it', '3h12m54s'],
        ['981333696', 'Iniziamo Mario Galaxy!', '2021-04-09T18:01:31Z', '2021-04-09T18:01:31Z', 'https://www.twitch.tv/videos/981333696', 'public', '4465', 'it', '3h5m18s'],
        ['980112618', 'TBoI Repentance, ma oggi nulla di strano...', '2021-04-08T18:02:21Z', '2021-04-08T18:02:21Z', 'https://www.twitch.tv/videos/980112618', 'public', '4475', 'it', '2h57m40s'],
        ['978911161', 'Grandi Progressi su Monster Hunter Rise!', '2021-04-07T18:06:42Z', '2021-04-07T18:06:42Z', 'https://www.twitch.tv/videos/978911161', 'public', '2574', 'it', '2h45m20s'],
        ['977695483', 'TBoI Repentance, ma 1 Morte = 1 Bicchiere di Acqua Frizzante', '2021-04-06T18:05:49Z', '2021-04-06T18:05:49Z', 'https://www.twitch.tv/videos/977695483', 'public', '5166', 'it', '3h6m8s'],
        ['976499410', 'Speedrun di Sekiro, ma non so giocare a Sekiro...', '2021-04-05T18:03:33Z', '2021-04-05T18:03:33Z', 'https://www.twitch.tv/videos/976499410', 'public', '3532', 'it', '2h55m36s'],
        ['975338900', 'Ultima live con Mio Fratello!', '2021-04-04T18:05:17Z', '2021-04-04T18:05:17Z', 'https://www.twitch.tv/videos/975338900', 'public', '4602', 'it', '3h10m54s'],
        ['974141645', 'TBoI Repentance, ma 1 Morte = 10 Flessioni', '2021-04-03T18:31:16Z', '2021-04-03T18:31:16Z', 'https://www.twitch.tv/videos/974141645', 'public', '5065', 'it', '2h51m0s'],
        ['971484298', 'Piantina VS THE WORLD!', '2021-04-01T18:02:28Z', '2021-04-01T18:02:28Z', 'https://www.twitch.tv/videos/971484298', 'public', '3729', 'it', '2h36m32s'],
        ['970243246', 'Prima Run di The Binding of Isaac Repentance!', '2021-03-31T18:03:27Z', '2021-03-31T18:03:27Z', 'https://www.twitch.tv/videos/970243246', 'public', '4831', 'it', '3h28m20s'],
        ['968758131', 'PRO-Player di Monster Hunter prova MH Rise! (Clickbait)', '2021-03-30T13:00:56Z', '2021-03-30T13:00:56Z', 'https://www.twitch.tv/videos/968758131', 'public', '2392', 'it', '2h57m52s'],
        ['967822212', 'Valuto TUTTI i Mostri di MH Rise!', '2021-03-29T18:03:20Z', '2021-03-29T18:03:20Z', 'https://www.twitch.tv/videos/967822212', 'public', '2332', 'it', '2h29m9s'],
        ['966404755', 'Oh no... sono dipendente da Monster Hunter Rise!', '2021-03-28T14:02:34Z', '2021-03-28T14:02:34Z', 'https://www.twitch.tv/videos/966404755', 'public', '3138', 'it', '3h5m54s'],
        ['965052770', 'Maratona Monster Hunter Rise!', '2021-03-27T13:30:49Z', '2021-03-27T13:30:49Z', 'https://www.twitch.tv/videos/965052770', 'public', '5412', 'it', '5h27m0s'],
        ['963792962', 'Monster Hunter Rise in compagnia!', '2021-03-26T15:46:39Z', '2021-03-26T15:46:39Z', 'https://www.twitch.tv/videos/963792962', 'public', '2697', 'it', '2h57m38s'],
        ['962573366', 'Speedrun Shao Yo% con Froz3n su BotW!', '2021-03-25T16:01:21Z', '2021-03-25T16:01:21Z', 'https://www.twitch.tv/videos/962573366', 'public', '4141', 'it', '2h5m12s'],
        ['961570446', 'Riusciamo a Finire? - KH2 Randomizer', '2021-03-24T19:02:59Z', '2021-03-24T19:02:59Z', 'https://www.twitch.tv/videos/961570446', 'public', '3533', 'it', '3h28m22s'],
        ['960352463', 'E ora come faccio? - KH2 Randomizer', '2021-03-23T19:02:03Z', '2021-03-23T19:02:03Z', 'https://www.twitch.tv/videos/960352463', 'public', '3520', 'it', '3h11m7s'],
        ['959167046', 'Una Giornata su Genshin Impact!', '2021-03-22T19:02:02Z', '2021-03-22T19:02:02Z', 'https://www.twitch.tv/videos/959167046', 'public', '2829', 'it', '2h41m34s'],
        ['958077172', 'Ancora una situazione TRAGICA! - KH2 Randomizer', '2021-03-21T19:04:10Z', '2021-03-21T19:04:10Z', 'https://www.twitch.tv/videos/958077172', 'public', '12077', 'it', '3h1m8s'],
        ['956529121', 'Gravier VS la Nazionale Italiana di Mario Kart 8!', '2021-03-20T15:58:34Z', '2021-03-20T15:58:34Z', 'https://www.twitch.tv/videos/956529121', 'public', '3164', 'it', '2h33m3s'],
        ['955382365', 'Gravier VS la Fortuna! - Kingdom Hearts 2 Randomizer', '2021-03-19T19:01:04Z', '2021-03-19T19:01:04Z', 'https://www.twitch.tv/videos/955382365', 'public', '3589', 'it', '3h12m52s'],
        ['953989971', 'Guardiamo la Square Enix Presents!', '2021-03-18T16:32:59Z', '2021-03-18T16:32:59Z', 'https://www.twitch.tv/videos/953989971', 'public', '2767', 'it', '1h26m34s'],
        ['952970859', 'Iniziamo Kingdom Hearts 2 Randomizer!', '2021-03-17T19:00:54Z', '2021-03-17T19:00:54Z', 'https://www.twitch.tv/videos/952970859', 'public', '6138', 'it', '3h12m36s'],
        ['950542443', 'Verso la Terza Prigione! - Persona 5 Strikers', '2021-03-15T19:04:06Z', '2021-03-15T19:04:06Z', 'https://www.twitch.tv/videos/950542443', 'public', '1622', 'it', '2h23m56s'],
        ['949431325', 'Smash Tutti Insieme!', '2021-03-14T19:02:48Z', '2021-03-14T19:02:48Z', 'https://www.twitch.tv/videos/949431325', 'public', '2481', 'it', '2h28m52s'],
        ['948098553', 'Parliamo, ma piano!', '2021-03-13T19:02:04Z', '2021-03-13T19:02:04Z', 'https://www.twitch.tv/videos/948098553', 'public', '1689', 'it', '1h51m34s'],
        ['946742301', 'Proviamo Maquette!', '2021-03-12T19:03:53Z', '2021-03-12T19:03:53Z', 'https://www.twitch.tv/videos/946742301', 'public', '2083', 'it', '3h34m2s'],
        ['943134475', 'Finiamo la Seconda Prigione! - Persona 5 Strikers', '2021-03-09T19:04:20Z', '2021-03-09T19:04:20Z', 'https://www.twitch.tv/videos/943134475', 'public', '1638', 'it', '2h39m22s'],
        ['940837822', 'Mario Kart 8 Tutti Insieme!', '2021-03-07T19:03:02Z', '2021-03-07T19:03:02Z', 'https://www.twitch.tv/videos/940837822', 'public', '2647', 'it', '2h17m42s'],
        ['938116424', 'Seconda Prigione di Persona 5 Strikers!', '2021-03-05T19:03:13Z', '2021-03-05T19:03:13Z', 'https://www.twitch.tv/videos/938116424', 'public', '1968', 'it', '2h53m48s'],
        ['936551545', 'Guardiamo la Smash Direct!', '2021-03-04T13:29:43Z', '2021-03-04T13:29:43Z', 'https://www.twitch.tv/videos/936551545', 'public', '1698', 'it', '1h27m38s'],
        ['935641954', 'È arrivato il momento di impaurirsi? - Little Nightmares 2', '2021-03-03T19:03:42Z', '2021-03-03T19:03:42Z', 'https://www.twitch.tv/videos/935641954', 'public', '2010', 'it', '3h15m8s'],
        ['934406084', 'Iniziamo Little Nightmares 2!', '2021-03-02T19:02:43Z', '2021-03-02T19:02:43Z', 'https://www.twitch.tv/videos/934406084', 'public', '2660', 'it', '2h39m50s'],
        ['933208638', 'Finiamo la Prima Prigione in Persona 5 Strikers!', '2021-03-01T19:02:44Z', '2021-03-01T19:02:44Z', 'https://www.twitch.tv/videos/933208638', 'public', '2375', 'it', '2h54m42s'],
        ['929039103', 'Parliamo del Pokemon Presents!', '2021-02-26T14:08:05Z', '2021-02-26T14:08:05Z', 'https://www.twitch.tv/videos/929039103', 'public', '5588', 'it', '1h55m14s'],
        ['928120564', 'Giochiamo Persona 5 Strikers prima dello State of Play!', '2021-02-25T19:06:04Z', '2021-02-25T19:06:04Z', 'https://www.twitch.tv/videos/928120564', 'public', '4276', 'it', '3h48m22s'],
        ['926874705', 'ContinuIAmo Persona 5 Strikers!', '2021-02-24T19:03:59Z', '2021-02-24T19:03:59Z', 'https://www.twitch.tv/videos/926874705', 'public', '3129', 'it', '2h50m35s'],
        ['925648450', 'Iniziamo Persona 5 Strikers!', '2021-02-23T19:03:22Z', '2021-02-23T19:03:22Z', 'https://www.twitch.tv/videos/925648450', 'public', '4413', 'it', '3h6m22s'],
        ['924424095', 'Animal Crossing Gacha!', '2021-02-22T19:00:18Z', '2021-02-22T19:00:18Z', 'https://www.twitch.tv/videos/924424095', 'public', '2075', 'it', '1h52m1s'],
        ['924231217', 'Finiamo 3D World con Froz3n, Poketonx e Frake!', '2021-02-22T16:01:07Z', '2021-02-22T16:01:07Z', 'https://www.twitch.tv/videos/924231217', 'public', '1976', 'it', '1h40m16s'],
    ]

def createRefDictionary(inputs, labels):
    output = []
    
    for el in inputs:
        toAdd = {}
        for i in range(0, len(labels)):
            if labels[i] is None:
                continue
            toAdd[labels[i]] = el[i]
        output.append(toAdd)
        
    return output


if __name__ == '__main__':

    from GoogleSheetsAndForms.Core.GoogleBot import GoogleBot
    from GoogleSheetsAndForms.Core.DataAdder import DataAdder
    from GoogleSheetsAndForms.RequestMaker import RequestMaker
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

    # Data Adder
    DATA = retrieveAllVODS()
    LABELS = ["ID", "TITLE", "CREATED_ON", "DATE", "URL", "VIEWABLE", "VIEW_COUNT", "LANGUAGE", "DURATION"]
    
    dataAdder = DataAdder("DataAdder")
    dataAdder.OutputCollectionName = ["VALUES", "VALUES_DICTS"]
    dataAdder.Data = [DATA, createRefDictionary(DATA, LABELS)]
    googleBot.addExecutable(dataAdder)
    
    # Module A
    requestMakerA = RequestMaker("RequestMaker_A")
    requestMakerA.ValuesCollectionName = "VALUES"
    requestMakerA.RequestCollectionName = "REQUESTS_A"
    requestMakerA.InputFormat = [str, str, None, str, str, None, str, None, str]
    requestMakerA.InputLabels = ["ID", "TITLE", None, "DATE", "URL", None, "VIEW_COUNT", None, "DURATION"]
    googleBot.addExecutable(requestMakerA)
    
    # Module B
    requestMakerB = RequestMaker("RequestMaker_B")
    requestMakerB.ValuesCollectionName = "VALUES"
    requestMakerB.RequestCollectionName = "REQUESTS_B"
    requestMakerB.InputFormat = [None, str, None, str, None, None, None, None, str]
    requestMakerB.InputLabels = [None, "TITLE", None, "DATE", None, None, None, None, "DURATION"]
    googleBot.addExecutable(requestMakerB)

    # Module C
    requestMakerC = RequestMaker("RequestMaker_C")
    requestMakerC.ValuesCollectionName = "VALUES"
    requestMakerC.RequestCollectionName = "REQUESTS_C"
    requestMakerC.InputFormat = [str, None, None, None, None, None, None, None, None]
    requestMakerC.InputLabels = ["ID", None, None, None, None, None, None, None, None]
    googleBot.addExecutable(requestMakerC)

    validator = Validator("RequestMaker Validator")
    validator.ReferenceData = ["VALUES_DICTS", "VALUES_DICTS", "VALUES_DICTS"]
    validator.InputCollections = [requestMakerA.RequestCollectionName,
                                  requestMakerB.RequestCollectionName,
                                  requestMakerC.RequestCollectionName]
    validator.Labels = [requestMakerA.InputLabels,
                        requestMakerB.InputLabels,
                        requestMakerC.InputLabels]
    googleBot.addExecutable(validator)
    
    googleBot.execute()

    
