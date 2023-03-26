import pickle


class Arxiu():
    
    def __init__(self, nom_arxiu):
        
        self.nom_arxiu=nom_arxiu


    def llegir_exercici_actual(self):

        fitxer=open(self.nom_arxiu,"rb")
        llista=pickle.load(fitxer)
        fitxer.close
        del(fitxer)
        return(int(llista[0]))
