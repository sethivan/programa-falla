import pickle
import os
import errno
import os.path as path


class Arxiu():
    
    def __init__(self, nom_arxiu):
        
        self.nom_arxiu=nom_arxiu


    def llegir_exercici_actual(self):

        fitxer=open(self.nom_arxiu,"rb")
        llista=pickle.load(fitxer)
        fitxer.close
        del(fitxer)
        return(int(llista[0]))
    

    def crear_historial(self, historial):
        
        try:
            os.mkdir("historials")
        except OSError as e:
            if e.errno!=errno.EEXIST:
                raise
        fitxer=open(self.nom_arxiu,"wb")
        pickle.dump(historial, fitxer)
        fitxer.close()
        del(fitxer)
