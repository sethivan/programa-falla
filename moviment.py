class Moviment():

	def __init__(self, id, data, quantitat, tipo, concepte, exercici, descripcio, rebut, faller=None):

		self.id=id
		self.data=data
		self.quantitat=quantitat
		self.tipo=tipo
		self.concepte=concepte
		self.exercici=exercici
		self.descripcio=descripcio
		self.rebut=rebut
		self.faller=faller


	@property
	def id(self):

		return self._id
	

	@id.setter
	def id(self, value):
		
		self._id=value


	@property
	def data(self):

		return self._data
	

	@data.setter
	def data(self, value):
		
		self._data=value
	

	@property
	def quantitat(self):

		return self._quantitat
	

	@quantitat.setter
	def quantitat(self, value):
		
		self._quantitat=value


	@property
	def tipo(self):

		return self._tipo
	

	@tipo.setter
	def tipo(self, value):
		
		self._tipo=value


	@property
	def concepte(self):

		return self._concepte
	

	@concepte.setter
	def concepte(self, value):
		
		self._concepte=value


	@property
	def exercici(self):

		return self._exercici
	

	@exercici.setter
	def exercici(self, value):
		
		self._exercici=value


	@property
	def descripcio(self):

		return self._descripcio
	

	@descripcio.setter
	def descripcio(self, value):
		
		self._descripcio=value


	@property
	def rebut(self):

		return self._rebut
	

	@rebut.setter
	def rebut(self, value):
		
		self._rebut=value


	@property
	def faller(self):

		return self._faller
	

	@faller.setter
	def faller(self, value):
		
		self._faller=value

		'''

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
		'''