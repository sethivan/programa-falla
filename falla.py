from tkinter import messagebox

from base_de_dades import BaseDeDades
from utils import Utils
from arxiu import Arxiu

from moviment import Moviment


class Falla():

    
    def __init__(self):

        self.llistat_fallers=[]
        self.llistat_moviments=[]
   
    
    def assignar_rifa_auto(self):

        valor=messagebox.askquestion("Assignar rifa","Estàs segur que vols assignar 15€ de rifa als fallers corresponents?")
        if valor=="yes":
            arxiu=Arxiu("exercici")
            utils=Utils()
            datafinal=utils.calcular_data_actual()
            self.llistat_fallers=self.llegir_fallers("adults","")
            exercici_actual=arxiu.llegir_exercici_actual()
            try:
                for faller in self.llistat_fallers:
                    moviment=Moviment(0, datafinal, 15, 1, 3, exercici_actual, "rifa", 0, faller)
                    self.llistat_moviments.append(moviment)
                self.crear_moviments(self.llistat_moviments)
            except TypeError:
                messagebox.showerror("Assignar rifa", "La rifa no s'ha pogut assignar correctament")
            else:
                messagebox.showinfo("Assignar rifa", "La rifa s'ha assignat correctament")

    
    def llegir_fallers(self, opcio, variable):

        bd=BaseDeDades("falla.db")
        if opcio=="cognoms":
            self.llistat_fallers=bd.llegir_fallers_per_cognom(variable)
        elif opcio=="familia":
            self.llistat_fallers=bd.llegir_fallers_per_familia(variable)
        elif opcio=="adults":
            self.llistat_fallers=bd.llegir_fallers_adults()
        bd.tancar_conexio()
        return self.llistat_fallers
    

    def crear_moviments(self, llistat_moviments):
        
        bd=BaseDeDades("falla.db")
        for moviment in llistat_moviments:
            bd.crear_moviment(moviment)
        bd.tancar_conexio()


    def calcular_assignacions_pagaments(self, id, exercici):

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