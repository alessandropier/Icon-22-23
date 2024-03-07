import os

import prediction
import recommender

def main():
    bool = False
    esegui = True
    while esegui == True:
        if bool:
            string = "Vuoi che ti suggerisca un altro videogioco ? - Premi 1\n" \
                     + "Vuoi sapere la classificazione PEGI di un altro videogioco? - Premi 2\n" \
                     + "Vuoi uscire? - Premi 3\n"
        else:
            string = "Benvenuto!\n" + "Vuoi che ti suggerisca un videogioco ? - Premi 1\n" \
                     + "Vuoi sapere la classificazione PEGI di un videogioco? - Premi 2\n" \
                     + "Vuoi uscire? - Premi 3\n"
        response = input(string)
        
        # Recommender System
        if response == '1':
            name = ''
            platform = ''
            publisher = ''
            rating = ''
            type = ''
            year =''
            classification = ''
            platforms = []

            print("Ti faro' delle domande per poterti suggerire un videogioco.")
            name = input("Suggeriscimi il nome di un videogioco che hai apprezzato\n").lower()
            platform = input("A che piattaforma fai riferimento?\n").lower()
            publisher = input("Qual è il publisher del videogioco?\n").lower()
            rating = input("Se dovessi valutarlo, che voto gli daresti da 0 a 20?\n").lower()
            while rating == "" or rating.isalpha() or int(rating) not in range(0, 20):
                print ("Inserire un valore compreso tra 0 e 20\n")
                rating = input("Se dovessi valutarlo, che voto gli daresti da 0 a 20?\n").lower()
            
            type = input("Qual è il genere di questo videogioco?\n").lower()
            year = input("Qual è l'anno di pubblicazione del videogioco?\n").lower()
            
            string = input("Qual è la classificazione pegi del videogioco? (Se non sai cosa si intende, premi 1)\n").lower()
            while string == '1':
                print("Quando parliamo di classificazione intendiamo se il videogioco è giocabile dalle seguenti fasce di età:\n" +
                      "- +3 \n" +
                      "- +7 \n" +
                      "- +12\n" +
                      "- +16\n" +
                      "- +18\n")

                string = input("Ora sai dirmi qual è la classificazione? (se non sai cos'è digita 1, altrimenti scrivi Si)\n").lower()
                while string not in ["Si", "si", "1"]:
                    print("Input non valido! Inserire 1 o Si\n")
                    string = input("Ora sai dirmi qual è la classificazione? (se non sai cos'è digita 1, altrimenti scrivi Si)\n").lower()

            if string not in ["+3", "+7", "+12", "+16", "+18"]:
                if string not in ["Si", "si", "1"]:
                    print("Quando parliamo di classificazione intendiamo se il videogioco è giocabile dalle seguenti fasce di età:\n" +
                      "- +3 \n" +
                      "- +7 \n" +
                      "- +12\n" +
                      "- +16\n" +
                      "- +18\n")
                type_ = input("Qual è la classificazione?\n").lower()
            else:
                type_ = string
                
            while type_ not in ["+3", "+7", "+12", "+16", "+18"]: 
                print("Input non valido!\n")
                print("Quando parliamo di classificazione intendiamo se il videogioco è giocabile dalle seguenti fasce di età:\n" +
                      "- +3 \n" +
                      "- +7 \n" +
                      "- +12\n" +
                      "- +16\n" +
                      "- +18\n")
                type_ = input("Qual è la classificazione?\n").lower()
                
            classification = type_
            
            piattaforme_nel_dataset = ["wii", "pc", "ps3", "ds", "ps2", "n64", "gba", "psp", "3ds", "ps4", "snes", "wiiu", "gb"]
            print("Queste sono le piattaforme che il nostro sistema possiede:\n")
            aux = 0
            while aux != '1':
                i = 0
                for element in piattaforme_nel_dataset:
                    #if element not in platforms:
                        #print(f"{i}) {element}")
                    print(f"{i}) {element}")
                    i = i + 1
                    
                if platforms == []:
                    aux = input("Per che piattaforma vorresti ricevere raccomandazioni?\n").lower()
                else:
                    aux = input("Vorresti aggiungere un'altra piattaforma? (Premere 1 per uscire)\n").lower()
                
                if aux != '1' and aux not in piattaforme_nel_dataset:
                    print("Piattaforma non presente nel sistema, inserirne una valida.")
                elif aux in piattaforme_nel_dataset and aux not in platforms:
                    platforms.append(aux)
                elif aux in piattaforme_nel_dataset and aux in platforms:
                    print("Piattaforma già inserita, sceglierne una nuova.")
                elif aux == '1' and platforms == []:
                    aux = 0
                    print("Inserire almeno una piattaforma.")

            recommender.set_recommender(name, platform, publisher, rating, type, year, classification, platforms)
            print("\n")
            os.system("pause")
            bool = True
            print("\n")
        
        #Previsione della classificazione
        elif response == '2':
            name = input("Qual è il nome del gioco che vuoi classificare?\n").lower()

            genre = input("Qual è il genere del gioco che vuoi classificare?\n").lower()

            publisher = input("Qual è il publisher del gioco che vuoi classificare?\n").lower()
            
            platform = input("Qual è la piattaforma del gioco che vuoi classificare?\n").lower()
            
            rating = input("Se dovessi valutarlo, che voto gli daresti da 0 a 20?\n").lower()
            while rating == "" or rating.isalpha() or int(rating) not in range(0, 20):
                print ("Inserire un valore compreso tra 0 e 20\n")
                rating = input("Se dovessi valutarlo, che voto gli daresti da 0 a 20?\n").lower()

            year = input("Qual è l'anno di uscita del gioco che vuoi classificare?\n").lower()
        
            prediction.predict_classification(name, genre, publisher, platform, rating, year)
            print("\n")
            os.system("pause")
            bool = True
            print("\n\n")
        
        elif response == '3':
            print("Arrivederci.")
            esegui = False
        
        else:
            print("Valore non valido! Inserire un valore compreso tra 1 e 3.\n\n")
            bool = True
        

if __name__ == '__main__':
    main()