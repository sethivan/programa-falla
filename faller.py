import sqlite3
from datetime import datetime, timedelta
from tkinter import messagebox

from moviment import Moviment


class Faller():

	def __init__(self):

		self.nom=""
		self.cognoms=""
		self.naixement=""
		self.sexe=0
		self.dni=""
		self.adresa=""
		self.telefon=""
		self.alta=0
		self.familia=0
		self.correu=""
		self.quota=0

	
	def LlistatFallers(self):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		elCursor.execute("SELECT * FROM faller")
		resultat=elCursor.fetchall()
		laConexio.commit()
		laConexio.close()
		return(resultat)


	def BuscarFallerPerId(self, num):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		query_params=(num,)
		elCursor.execute("SELECT * FROM faller WHERE id=?", query_params)
		resultat=elCursor.fetchall()
		for valors in resultat:
			self.nom=valors[1]
			self.cognoms=valors[2]
			self.naixement=valors[3]
			self.sexe=valors[4]
			self.dni=valors[5]
			self.adresa=valors[6]
			self.telefon=valors[7]
			self.alta=valors[8]
			self.familia=valors[9]
			self.correu=valors[11]
		laConexio.commit()
		laConexio.close()


	def BuscarFallerPerNom(self, nom):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		valor="%" + nom + "%" #afegim els % com a caràcters desconeguts
		query_params=(valor,) #convertim el string en una tupla per al execute
		elCursor.execute("SELECT * FROM faller WHERE cognoms LIKE ?",query_params)
		resultat=elCursor.fetchall()
		laConexio.commit()
		laConexio.close()
		return(resultat)


	def BuscarFallerPerIdfamilia(self, num):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		query_params=(num,)
		elCursor.execute("SELECT * FROM faller WHERE idfamilia=?", query_params)
		resultat=elCursor.fetchall()
		laConexio.commit()
		laConexio.close()
		return(resultat)


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


	def IntroduirFaller(self, nom, cognoms, naixement, sexe, dni, adresa, telefon, fam, categ, correu):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		dades=nom, cognoms, naixement, sexe, dni, adresa, telefon, 1, fam, categ, correu
		elCursor.execute("INSERT INTO faller VALUES (null,?,?,?,?,?,?,?,?,?,?,?)",(dades))
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


	def EdatFaller(self, cadena, exercici):

		dataFaller=datetime.strptime(cadena, '%d-%m-%Y')
		lanyfaller=datetime.strftime(dataFaller,'%Y')
		mesfaller=datetime.strftime(dataFaller, '%m')
		diafaller=datetime.strftime(dataFaller, '%d')
		dataexercici=datetime.strptime(str(exercici), '%Y')
		lanyexercici=datetime.strftime(dataexercici, '%Y')
		if int(mesfaller)>3 or (int(mesfaller)==3 and int(diafaller)>19):
			edat=int(lanyexercici)-int(lanyfaller)-1
		else:
			edat=int(lanyexercici)-int(lanyfaller)
		return(edat)


	def PrimerExercici(self, cadena):

		dataFaller=datetime.strptime(cadena, '%d-%m-%Y')
		lanyfaller=datetime.strftime(dataFaller,'%Y')
		mesfaller=datetime.strftime(dataFaller, '%m')
		diafaller=datetime.strftime(dataFaller, '%d')
		if int(mesfaller)>3 or (int(mesfaller)==3 and int(diafaller)>19):
			exercici=int(lanyfaller)+1
		else:
			exercici=int(lanyfaller)
		return(exercici)


	def AsignarCategoria(self, edat):

		if edat<5:
			categoria=5
		elif 5<=edat<=9:
			categoria=4
		elif 10<=edat<=14:
			categoria=3
		elif 15<=edat<=17:
			categoria=2
		else:
			categoria=1
		return(categoria)


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


	def BuscarFallerAmbRifa(self): #funció que torna una llista amb tots els fallers donats d'alta i majors de 13 anys

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		try:
			elCursor.execute("SELECT * FROM faller WHERE alta=1 and (idcategoria=1 or idcategoria=2) ORDER BY cognoms")
		except sqlite3.OperationalError:
			messagebox.showwarning("Error", "Hi ha un problema amb la base de dades")
		else:
			resultat=elCursor.fetchall()
			return(resultat)
		finally:
			laConexio.close()


	def AssignarRifa(self): #funció per a assignar la rifa corresponent als fallers

		valor=messagebox.askquestion("Assignar rifa","Estàs segur que vols assignar 15€ de rifa als fallers corresponents?")
		if valor=="yes":
			elFaller=Faller()
			res=elFaller.BuscarFallerAmbRifa()
			elMoviment=Moviment()
			elMoviment.ExerciciActual()			
			try:
				for val in res:
					elMoviment.InsertarMoviment(15, 1, 3, elMoviment.exercici, val[0], "rifa") #els assignem la rifa
			except TypeError: #el contingut de la variable "res" es "None" si no torna res la funció "BuscarFallerAmbRifa"
				messagebox.showinfo("Assignar rifa","La rifa no s'ha pogut assignar correctament")
			else:
				messagebox.showinfo("Assignar rifa","La rifa s'ha assignat correctament")