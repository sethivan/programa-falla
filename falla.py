'''
Proporciona la classe "Falla".
'''
from tkinter import messagebox

from base_de_dades import BaseDeDades
from utils import Utils
from arxiu import Arxiu

from moviment import Moviment


class Falla():
    '''
	Aquesta classe pot controlar llistats de les classes "faller" i "moviment" i operar amb elles.

	Atributs:
	---------
	llistat_fallers : llista
        Llistat d'objectes de la classe "Faller".
    llistat_moviments : llista
        Llistat d'objectes de la classe "Moviment".
	'''

    
    def __init__(self, llistat_fallers=None, llistat_moviments=None):
        '''
		Inicialitza una nova instància de la classe Falla.
        Disposa de dos paràmetres que mostren les relacions que manté amb la classe "Faller" i la clase "Moviment".

		Paràmetres:
		-----------
		llistat_fallers : llista
            Llistat d'objectes de la classe "Faller".
        llistat_moviments : llista
            Llistat d'objectes de la classe "Moviment".
		'''
        self.llistat_fallers=llistat_fallers
        self.llistat_moviments=llistat_moviments

    
    # Getters i setters
    @property
    def llistat_fallers(self):
        
        return self._llistat_fallers
	
    
    @llistat_fallers.setter
    def llistat_fallers(self, value):
        
        self._llistat_fallers=value


    @property
    def llistat_moviments(self):

        return self._llistat_moviments
	

    @llistat_moviments.setter
    def llistat_moviments(self, value):
		
        self._llistat_moviments=value
   
    
    def assignar_rifa_auto(self):
        '''
        Crea un moviment per cadascún dels fallers amb obligació de pagar rifa i
        el guarda a la base de dades.
        '''
        valor=messagebox.askquestion("Assignar rifa",
                                     "Estàs segur que vols assignar 15€ de rifa als fallers corresponents?")
        if valor=="yes":
            arxiu=Arxiu("exercici")
            utils=Utils()
            bd=BaseDeDades("falla.db")
            datafinal=utils.calcular_data_actual()
            self.llistat_fallers=bd.llegir_fallers_adults()
            exercici_actual=arxiu.llegir_exercici_actual()
            try:
                for faller in self.llistat_fallers:
                    moviment=Moviment(0, datafinal, 15, 1, 3, exercici_actual, "rifa", 0, faller)
                    bd.crear_moviment(moviment)          
            except TypeError:
                bd.tancar_conexio()
                messagebox.showerror("Assignar rifa", "La rifa no s'ha pogut assignar correctament")
            else:
                bd.tancar_conexio()
                messagebox.showinfo("Assignar rifa", "La rifa s'ha assignat correctament")


    def calcular_assignacions_pagaments(self, id, exercici):
        '''
        Llig els moviments del faller i suma les quotes, loteries i rifes assignades i pagades
        i torna un llistat amb aquests sumatoris.

        Paràmetres:
        -----------
        id : int
            Identificador del faller.
        exercici : int
            Exercici del qual volem extraure els moviments.

        Retorna:
        --------
        llista_assignacions_pagaments : llista
            Llistat amb els sumatoris d'assignacions i pagaments totals.
        '''
        bd=BaseDeDades("falla.db")
        quota_assignada=0
        quota_pagada=0
        loteria_assignada=0
        loteria_pagada=0
        rifa_assignada=0
        rifa_pagada=0
        self.llistat_moviments=bd.llegir_moviments(id, exercici)
        for moviment in self.llistat_moviments:
            if moviment.tipo==1 and moviment.concepte==1:
                quota_assignada=quota_assignada+moviment.quantitat
            elif moviment.tipo==2 and moviment.concepte==1:
                quota_pagada=quota_pagada+moviment.quantitat
            elif moviment.tipo==1 and moviment.concepte==2:
                loteria_assignada=loteria_assignada+moviment.quantitat
            elif moviment.tipo==2 and moviment.concepte==2:
                loteria_pagada=loteria_pagada+moviment.quantitat
            elif moviment.tipo==1 and moviment.concepte==3:
                rifa_assignada=rifa_assignada+moviment.quantitat
            elif moviment.tipo==2 and moviment.concepte==3:
                rifa_pagada=rifa_pagada+moviment.quantitat
        bd.tancar_conexio()
        llista_assignacions_pagaments=[]
        llista_assignacions_pagaments.extend([quota_assignada, quota_pagada, loteria_assignada, loteria_pagada, rifa_assignada, rifa_pagada])
        return llista_assignacions_pagaments