'''
Proporciona la classe "Arxiu".
'''
import pickle
import os
import errno


class Arxiu():
    '''
    Aquesta classe proporciona interacció amb els diferents arxius binaris que
    formen part de l'aplicació.

    Atributs:
    ---------
    nom_arxiu : string
        Nom de l'arxiu amb el qual anem a operar.
    '''
    
    def __init__(self, nom_arxiu):
        '''
        Inicialitza una nova instància de la classe Arxiu.

        Paràmetres:
        -----------
        nom_arxiu : string
            Nom de l'arxiu amb el qual anem a operar.
        '''
        self.nom_arxiu=nom_arxiu


    def llegir_exercici_actual(self):
        '''
        Llig l'exercici de l'arxiu on està guardat i el retorna.

        Retorna:
        --------
        exercici_actual : int
            Valor numèric corresponent a l'any de l'exercici actual.
        '''
        fitxer=open(self.nom_arxiu,"rb")
        llista=pickle.load(fitxer)
        fitxer.close
        del(fitxer)
        exercici_actual=int(llista[0])
        return exercici_actual
    

    def crear_historial(self, historial):
        '''
        Crea un nou arxiu binari amb l'historial que se li passa com a paràmetre.
        En cas de no existir la carpeta "historials", la crea.

        Paràmetres:
        -----------
        historial : diccionari
            Diccionari amb l'historial d'exercicis, càrrecs
            i pertinença a falles del faller.

        Excepcions:
        -----------
        OSError : Gestiona un error si ja està creat el directori.
        '''
        try:
            os.mkdir("historials")
        except OSError as e:
            if e.errno!=errno.EEXIST:
                raise
        fitxer=open(self.nom_arxiu,"wb")
        pickle.dump(historial, fitxer)
        fitxer.close()
        del(fitxer)

    
    def llegir_historial(self):
        '''
        Llig l'historial de l'arxiu binari que va associat al fitxer i el retorna.

        Retorna:
        --------
        historial : diccionari
            Diccionari amb l'historial d'exercicis, càrrecs
            i pertinença a falles del faller.
        '''
        fitxer=open(self.nom_arxiu,"rb")
        historial=pickle.load(fitxer)
        fitxer.close()
        del(fitxer)
        return historial
    

    def modificar_historial(self, historial):
        '''
        Modifica l'arxiu binari amb l'historial que se li passa com a paràmetre.

        Paràmetres:
        -----------
        historial : diccionari
            Diccionari amb l'historial d'exercicis, càrrecs
            i pertinença a falles del faller.
        '''
        fitxer=open(self.nom_arxiu,"wb")
        pickle.dump(historial, fitxer)
        fitxer.close()
        del(fitxer)
