'''
Proporciona la classe "Falla".
'''
from tkinter import messagebox

from base_de_dades import BaseDeDades
from utils import Utils
from arxiu import Arxiu

from moviment import Moviment
from categoria import Categoria


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
            data=utils.calcular_data_actual()
            data_actual=data[0] + "-" + data[1] + "-" + data[2]
            self.llistat_fallers=bd.llegir_fallers_adults()
            exercici_actual=arxiu.llegir_exercici_actual()
            try:
                for faller in self.llistat_fallers:
                    moviment=Moviment(0, data_actual, 15, 1, 3, exercici_actual, "rifa", 0, faller)
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
    

    def nou_exercici(self):

		#creem una cópia en fitxer binari del resultat de l'exercici
        bd=BaseDeDades("falla.db")
        arxiu=Arxiu("exercici")
        llistat_fallers=bd.llegir_fallers_complets_per_alta(1)
        exercici_actual=arxiu.llegir_exercici_actual()
        llista=[] #llista on anem a acumular els valors	de tots els fallers
        for faller in llistat_fallers:
            valors=[] #llista on acumulem les dades de cada faller
            quota_assignada=0 #resetejem a cada iteració per a que no s'acumulen
            quota_pagada=0
            loteria_assignada=0
            loteria_pagada=0
            rifa_assignada=0
            rifa_pagada=0
            valors.append(faller.id)
            quota_base=bd.llegir_quota_faller(faller.id)
            descompte=(faller.familia.descompte*quota_base/100)
            quota=quota_base-descompte
            llista_assignacions_pagaments=self.calcular_assignacions_pagaments(faller.id, exercici_actual)
            quota_assignada=llista_assignacions_pagaments[0]
            quota_pagada=llista_assignacions_pagaments[1]
            loteria_assignada=llista_assignacions_pagaments[2]
            loteria_pagada=llista_assignacions_pagaments[3]
            rifa_assignada=llista_assignacions_pagaments[4]
            rifa_pagada=llista_assignacions_pagaments[5]
            quota_final=quota+quota_assignada
            total_assignacions=quota_final+loteria_assignada+rifa_assignada
            total_pagaments=quota_pagada+loteria_pagada+rifa_pagada
            valors.append("{0:.2f}".format(quota_final))
            valors.append("{0:.2f}".format(loteria_assignada))
            valors.append("{0:.2f}".format(rifa_assignada))
            valors.append("{0:.2f}".format(total_assignacions))
            valors.append("{0:.2f}".format(quota_pagada))
            valors.append("{0:.2f}".format(loteria_pagada))
            valors.append("{0:.2f}".format(rifa_pagada))
            valors.append("{0:.2f}".format(total_pagaments))
            valors.append("{0:.2f}".format(total_assignacions-total_pagaments))
            llista.append(valors)
        #falta crear la carpeta resums
        arxiu=Arxiu("resum "+str(exercici_actual))
        arxiu.crear_resum(llista)
        messagebox.showinfo("Info", "Resum de l'any anterior guardat correctament")


		#modifiquem l'arxiu binari exercici amb l'any actual del sistema
        llista=[]
        arxiu=Arxiu("exercici")
        utils=Utils()
        data_actual=utils.calcular_data_actual()
        dia_actual=int(data_actual[0])
        mes_actual=int(data_actual[1])
        any_actual=int(data_actual[2])
        if mes_actual>3: #si s'obri exercici després de març, l'exercici es l'any següent
            any_exercici=any_actual+1
        elif mes_actual<2: #si s'obri exercici abans de març, l'any coincideix amb l'exercici
            any_exercici=any_actual
        elif mes_actual==3 and dia_actual>19:
            any_exercici=any_actual+1
        elif mes_actual==3 and dia_actual<=19:
            any_exercici=any_actual
        llista.append(any_exercici)
        arxiu.modificar_exercici_actual(llista)
        messagebox.showinfo("Info", "Nou any assignat correctament")

        
        #assignem la nova categoria a cada faller que haja canviat
        categoria=Categoria(0,0,"","")
        exercici_actual=arxiu.llegir_exercici_actual()
        for faller in llistat_fallers:
            if faller.categoria.id>1:
                edat=faller.calcular_edat(faller.naixement, exercici_actual)
                categoria.calcular_categoria(edat)
                if categoria.id!=faller.categoria.id:
                    categoria=bd.llegir_categoria(categoria.id)
                    faller.categoria=categoria
                    bd.actualitzar_faller(faller)
        messagebox.showinfo("Info", "Categories de fallers actualitzades")


		#recuperem l'arxiu binari de l'exercici anterior i asignem els valors distints de 0 a l'exercici actual
        arxiu=Arxiu("resum "+str(exercici_actual-1))
        llista=arxiu.llegir_resum()
        data=data_actual[0] + "-" + data_actual[1] + "-" + data_actual[2]
        for valor in llista:
             if valor[9]!="0.00":
                faller=bd.llegir_faller(valor[0])
                moviment=Moviment(0, data, valor[9], 1, 1, exercici_actual, "any anterior", 0, faller)
                bd.crear_moviment(moviment)
        messagebox.showinfo("Info", "Deutes i sobrants de l'exercici anterior actualitzats")
        messagebox.showinfo("Info", "El canvi d'exercici s'ha realitzat correctament")
