from datetime import datetime

class Faller():

	def __init__(self, id, nom, cognoms, naixement, sexe, dni, adresa, telefon, alta, correu, familia=None, categoria=None):

		self.id=id
		self.nom=nom
		self.cognoms=cognoms
		self.naixement=naixement
		self.sexe=sexe
		self.dni=dni
		self.adresa=adresa
		self.telefon=telefon
		self.alta=alta
		self.correu=correu
		self.familia=familia
		self.categoria=categoria


	@property
	def id(self):

		return self._id
	

	@id.setter
	def id(self, value):
		
		self._id=value


	@property
	def nom(self):

		return self._nom
	

	@nom.setter
	def nom(self, value):
		
		self._nom=value


	@property
	def cognoms(self):

		return self._cognoms
	

	@cognoms.setter
	def cognoms(self, value):
		
		self._cognoms=value


	@property
	def naixement(self):

		return self._naixement
	

	@naixement.setter
	def naixement(self, value):
		
		self._naixement=value


	@property
	def sexe(self):

		return self._sexe
	

	@sexe.setter
	def sexe(self, value):
		
		self._sexe=value


	@property
	def dni(self):

		return self._dni
	

	@dni.setter
	def dni(self, value):
		
		self._dni=value


	@property
	def adresa(self):

		return self._adresa
	

	@adresa.setter
	def adresa(self, value):
		
		self._adresa=value


	@property
	def telefon(self):

		return self._telefon
	

	@telefon.setter
	def telefon(self, value):
		
		self._telefon=value


	@property
	def alta(self):

		return self._alta
	

	@alta.setter
	def alta(self, value):
		
		self._alta=value


	@property
	def correu(self):

		return self._correu
	

	@correu.setter
	def correu(self, value):
		
		self._correu=value


	@property
	def familia(self):

		return self._familia
	

	@familia.setter
	def familia(self, value):
		
		self._familia=value


	@property
	def categoria(self):

		return self._categoria
	

	@categoria.setter
	def categoria(self, value):
		
		self._categoria=value


	def calcular_edat(self, naixement, exercici):
        
		naixement_faller=datetime.strptime(naixement, '%d-%m-%Y')
		any_naixement=datetime.strftime(naixement_faller, '%Y')
		mes_naixement=datetime.strftime(naixement_faller, '%m')
		dia_naixement=datetime.strftime(naixement_faller, '%d')
		data_exercici=datetime.strptime(str(exercici), '%Y')
		any_exercici=datetime.strftime(data_exercici, '%Y')
		if int(mes_naixement)>3 or (int(mes_naixement)==3 and int(dia_naixement)>19):
			edat=int(any_exercici)-int(any_naixement)-1
		else:
			edat=int(any_exercici)-int(any_naixement)
		return edat
	

	def calcular_primer_exercici(self, naixement):

		naixement_faller=datetime.strptime(naixement, '%d-%m-%Y')
		any_naixement=datetime.strftime(naixement_faller,'%Y')
		mes_naixement=datetime.strftime(naixement_faller, '%m')
		dia_naixement=datetime.strftime(naixement_faller, '%d')
		if int(mes_naixement)>3 or (int(mes_naixement)==3 and int(dia_naixement)>19):
			exercici=int(any_naixement)+1
		else:
			exercici=int(any_naixement)
		return exercici

     

'''



	def BuscarQuotaFaller(self, num):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		query_params=(num,)
		elCursor.execute("SELECT * FROM categoria INNER JOIN faller ON categoria.id=faller.idcategoria WHERE faller.id=?", query_params)
		resultat=elCursor.fetchall()
		for valors in resultat:
			self.quota=valors[1]
		laConexio.commit()
		laConexio.close()


	def AltaFaller(self,num):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		query_params=(num,)
		elCursor.execute("UPDATE faller SET alta=1 WHERE id=?", query_params)
		laConexio.commit()
		laConexio.close()


	def BuscarFallerAlta(self, num):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		query_params=(num,)
		elCursor.execute("SELECT * FROM faller WHERE alta=? ORDER BY cognoms", query_params)
		resultat=elCursor.fetchall()
		laConexio.commit()
		laConexio.close()
		return(resultat)


	def BaixaFaller(self,num):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		query_params=(num,)
		elCursor.execute("UPDATE faller SET alta=0 WHERE id=?", query_params)
		laConexio.commit()
		laConexio.close()


	def ModificarFaller(self, num, nom, cognoms, naixement, sexe, dni, adresa, telefon, categ, correu):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		dades=nom, cognoms, naixement, sexe, dni, adresa, telefon, categ, correu, num
		elCursor.execute("UPDATE faller SET nom=?, cognoms=?, naixement=?, sexe=?, dni=?, adreça=?, telefon=?, idcategoria=?, correu=? WHERE id=?",(dades))
		laConexio.commit()
		laConexio.close()


	def ModificarFamilia(self, num, fam):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		dades=fam, num
		elCursor.execute("UPDATE faller SET idfamilia=? WHERE id=?",(dades))
		laConexio.commit()
		laConexio.close()


	def ModificarCategoria(self, num, cat):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		dades=cat, num
		elCursor.execute("UPDATE faller SET idcategoria=? WHERE id=?",(dades))
		laConexio.commit()
		laConexio.close()


	def RecuperarUltimFaller(self):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		elCursor.execute("SELECT * FROM faller ORDER BY id DESC LIMIT 1")
		resultat=elCursor.fetchall()
		for valors in resultat:
			self.id=valors[0]
			self.familia=valors[9]
		laConexio.commit()
		laConexio.close()


	def BuscarFallerPerCategoria(self, num):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		query_params=(num,)
		elCursor.execute("SELECT * FROM faller WHERE idcategoria=?", query_params)
		resultat=elCursor.fetchall()
		laConexio.commit()
		laConexio.close()
		return(resultat)

'''