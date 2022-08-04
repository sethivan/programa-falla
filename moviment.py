import sqlite3
from datetime import date
from datetime import datetime
import pickle
from faller import *
from familia import *


class Moviment():

	def __init__(self):

		self.quotaasignada=0
		self.quotapagada=0
		self.loteriaasignada=0
		self.loteriapagada=0
		self.rifaasignada=0
		self.rifapagada=0
		self.exercici=0 #usada


	def NouExercici(self):

		#creem una cópia en fitxer binari del resultat de l'exercici
		elFaller=Faller()
		res=elFaller.BuscarFallerAlta(1)
		elMoviment=Moviment()
		elMoviment.ExerciciActual()
		laFamilia=Familia()
		llista=[] #llista on anem a acumular els valors	
		for val in res:
			values=[]
			elMoviment.quotaasignada=0 #resetejem a cada iteració per a que no s'acumulen
			elMoviment.quotapagada=0
			elMoviment.loteriaasignada=0
			elMoviment.loteriapagada=0
			elMoviment.rifaasignada=0
			elMoviment.rifapagada=0
			values=values+[val[0]]
			elFaller.BuscarQuotaFaller(val[0]) #busquem la quota corresponent al faller
			laFamilia.BuscarDescompteFamilia(val[0]) #busquem el descompte familiar del faller
			elMoviment.BuscarMoviments(val[0],str(elMoviment.exercici)) #busquem tots els moviments de l'exercici
			quotafinal=elFaller.quota-(laFamilia.descompte*elFaller.quota/100)+elMoviment.quotaasignada
			totalasig=quotafinal+elMoviment.loteriaasignada+elMoviment.rifaasignada
			totalpag=elMoviment.quotapagada+elMoviment.loteriapagada+elMoviment.rifapagada
			values.append("{0:.2f}".format(quotafinal))
			values.append("{0:.2f}".format(elMoviment.loteriaasignada))
			values.append("{0:.2f}".format(elMoviment.rifaasignada))
			values.append("{0:.2f}".format(totalasig))
			values.append("{0:.2f}".format(elMoviment.quotapagada))
			values.append("{0:.2f}".format(elMoviment.loteriapagada))
			values.append("{0:.2f}".format(elMoviment.rifapagada))
			values.append("{0:.2f}".format(totalpag))
			values.append("{0:.2f}".format(totalasig-totalpag))
			llista.append(values)
		fitxer=open("resum "+str(elMoviment.exercici),"wb")
		pickle.dump(llista, fitxer)
		fitxer.close()
		del(fitxer)

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
		if mesactual==3 and diaactual<=19:
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


	def ExerciciActual(self): #funció que torna en la variable self.exercici el valor de l'exercici actual

		fitxer=open("exercici","rb")
		llista=pickle.load(fitxer) #recuperem el valor de l'exercici guardat
		fitxer.close()
		del(fitxer)
		self.exercici=int(llista[0]) #l'associem a la variable de la classe


	def BuscarMoviments(self, num, exer):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		query_params=(num,exer)
		elCursor.execute("SELECT * FROM moviment WHERE idfaller=? and exercici=?", query_params)
		resultat=elCursor.fetchall()
		for valors in resultat:
			if valors[3]==1 and valors[4]==1:
				self.quotaasignada=self.quotaasignada+valors[2]
			elif valors[3]==2 and valors[4]==1:
				self.quotapagada=self.quotapagada+valors[2]
			elif valors[3]==1 and valors[4]==2:
				self.loteriaasignada=self.loteriaasignada+valors[2]
			elif valors[3]==2 and valors[4]==2:
				self.loteriapagada=self.loteriapagada+valors[2]
			elif valors[3]==1 and valors[4]==3:
				self.rifaasignada=self.rifaasignada+valors[2]
			elif valors[3]==2 and valors[4]==3:
				self.rifapagada=self.rifapagada+valors[2]
		laConexio.commit()
		laConexio.close()


	def InsertarPagament(self, quantitat, concepte, exercici, idfaller, descripcio, rebut):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		data=datetime.now()
		anyactual=datetime.strftime(data,'%Y')
		mesactual=datetime.strftime(data, '%m')
		diaactual=datetime.strftime(data, '%d')
		datafinal=diaactual + "-" + mesactual + "-" + anyactual
		dades=datafinal, quantitat, 2, concepte, exercici, idfaller, descripcio, rebut
		elCursor.execute("INSERT INTO moviment VALUES (null,?,?,?,?,?,?,?,?)",(dades))
		laConexio.commit()
		laConexio.close()


	def InsertarMoviment(self, quantitat, tipo, concepte, exercici, idfaller, descripcio): #funció que inserta en la base de dades el moviment passat per paràmetres

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		data=datetime.now()
		anyactual=datetime.strftime(data,'%Y')
		mesactual=datetime.strftime(data, '%m')
		diaactual=datetime.strftime(data, '%d')
		datafinal=diaactual + "-" + mesactual + "-" + anyactual
		dades=datafinal, quantitat, tipo, concepte, exercici, idfaller, descripcio, 0
		elCursor.execute("INSERT INTO moviment VALUES (null,?,?,?,?,?,?,?,?)",(dades))
		laConexio.commit()
		laConexio.close()


	def RecuperarMoviments(self, num, exer):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		query_params=(num,exer)
		elCursor.execute("SELECT * FROM moviment WHERE idfaller=? and exercici=?", query_params)
		resultat=elCursor.fetchall()
		laConexio.commit()
		laConexio.close()
		return(resultat)


	def MovimentsDia(self):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		data=datetime.now()
		anyactual=datetime.strftime(data,'%Y')
		mesactual=datetime.strftime(data, '%m')
		diaactual=datetime.strftime(data, '%d')
		datafinal=diaactual + "-" + mesactual + "-" + anyactual
		query_params=(datafinal,)
		elCursor.execute("SELECT * FROM moviment WHERE data=?", query_params)
		resultat=elCursor.fetchall()
		laConexio.commit()
		laConexio.close()
		return(resultat)