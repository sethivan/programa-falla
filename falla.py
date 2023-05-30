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
    

    def nou_exercici(self):

		#creem una cópia en fitxer binari del resultat de l'exercici
        bd=BaseDeDades("falla.db")
        arxiu=Arxiu("exercici")
        falla=Falla()
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
			#elFaller.BuscarQuotaFaller(val[0]) #busquem la quota corresponent al faller
            descompte=(faller.familia.descompte*quota_base/100)
			#laFamilia.BuscarDescompteFamilia(val[0]) #busquem el descompte familiar del faller
            quota=quota_base-descompte
            llista_assignacions_pagaments=falla.calcular_assignacions_pagaments(faller.id, exercici_actual)
			#elMoviment.BuscarMoviments(val[0],str(elMoviment.exercici)) #busquem tots els moviments de l'exercici
            quota_assignada=llista_assignacions_pagaments[0]
            quota_pagada=llista_assignacions_pagaments[1]
            loteria_assignada=llista_assignacions_pagaments[2]
            loteria_pagada=llista_assignacions_pagaments[3]
            rifa_assignada=llista_assignacions_pagaments[4]
            rifa_pagada=llista_assignacions_pagaments[5]
            quota_final=quota+quota_assignada
			#quotafinal=elFaller.quota-(laFamilia.descompte*elFaller.quota/100)+elMoviment.quotaasignada
            total_assignacions=quota_final+loteria_assignada+rifa_assignada
			#totalasig=quotafinal+elMoviment.loteriaasignada+elMoviment.rifaasignada
            total_pagaments=quota_pagada+loteria_pagada+rifa_pagada
			#totalpag=elMoviment.quotapagada+elMoviment.loteriapagada+elMoviment.rifapagada
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
        print(llista)
        arxiu=Arxiu("resum "+str(exercici_actual))
        arxiu.crear_resum(llista)
        #fitxer=open("resum "+str(elMoviment.exercici),"wb")
		#pickle.dump(llista, fitxer)
		#fitxer.close()
		#del(fitxer)

'''

		#modifiquem l'arxiu binari exercici amb l'any actual del sistema
		llista=[]
		fitxer=open("exercici","wb") #obrim l'arxiu exercici per a guardar l'exercici actual
		data=datetime.now()
		anyactual=int(datetime.strftime(data,'%Y'))
		mesactual=int(datetime.strftime(data, '%m'))
		diaactual=int(datetime.strftime(data, '%d'))
		if mesactual>3: #si s'obri exercici després de març, l'exercici es l'any següent
			anyexercici=anyactual+1
		if mesactual<2: #si s'obri exercici abans de març, l'any coincideix amb l'exercici
			anyexercici=anyactual
		if mesactual==3 and diaactual>19:
			anyexercici=anyactual+1
		if mesactual==3 and diactual<=19:
			anyexercici=anyactual
		llista.append(anyexercici)
		pickle.dump(llista, fitxer)
		fitxer.close()
		del(fitxer)

		#asignem la nova categoria a cada faller
		elFaller=Faller()
		res=elFaller.BuscarFallerAlta(1)
		elMoviment=Moviment()
		elMoviment.ExerciciActual()
		naixement=0
		edat=0
		categ=0
		for val in res:
			naixement=val[3]
			if val[10]>1:
				edat=elFaller.EdatFaller(naixement, elMoviment.exercici) #per a calcular l'edat
				categ=elFaller.AsignarCategoria(edat) #i la categoria
				elFaller.ModificarCategoria(val[0],str(categ))

		#recuperem l'arxiu binari de l'exercici anterior i asignem els valors distints de 0 a l'exercici actual
		elMoviment=Moviment()
		elMoviment.ExerciciActual()
		fitxer=open("resum "+str(elMoviment.exercici-1),"rb")
		lista=pickle.load(fitxer)
		fitxer.close()
		del(fitxer)
		for val in lista:
			if val[9]!="0.00":
				elMoviment.InsertarAsignacio(val[9], 1, elMoviment.exercici, val[0], "any anterior", 0)
                                
                                '''
