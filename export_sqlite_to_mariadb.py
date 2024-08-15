import sqlite3
from tkinter import messagebox
import traceback
import mysql.connector


from database import Database
from member import Member
from family import Family
from movement import Movement
from category import Category
from loteria import Loteria

class ExportSqliteToMariaDb:
	
	def __init__(self, nom_db):
		self.conexio = sqlite3.connect("falla.db")
		self.cursor = self.conexio.cursor()

		self.mysqlConnection = mysql.connector.connect(
			host = "localhost",
			user = "root",
			password = "hamuclaulo07",
			database = nom_db
		)
		if self.mysqlConnection.is_connected():
			self.mysqlCursor = self.mysqlConnection.cursor()

			#self.import_categoria_from_sqlite()
			#self.import_familia_from_sqlite()
			#self.import_faller_from_sqlite()
			self.insert_fallaYear(2019, "2021-03-20", "2022-03-19")
			#self.insert_fallaYear(2022, "2021-03-20", "2022-03-19")
			#self.insert_fallaYear(2023, "2022-03-20", "2023-03-19")
			#self.insert_fallaYear(2024, "2023-03-20", "2024-06-26")
			#self.import_moviment_from_sqlite()
		else:
			messagebox.showerror(
				"Error",
				"No s'ha pogut establir la conexió amb la base de dades."
			)

	
	def import_categoria_from_sqlite(self):

		self.cursor.execute("SELECT id, quota FROM categoria")
		result = self.cursor.fetchall()
		for value in result:
			self.update_category(value[0], value[1])
	

	def import_familia_from_sqlite(self):

		self.cursor.execute("SELECT * FROM familia")
		result = self.cursor.fetchall()
		for value in result:
			self.insert_family(value[0], value[1], value[2], value[3])
	

	def import_faller_from_sqlite(self):

		self.cursor.execute("SELECT * FROM faller")
		result = self.cursor.fetchall()
		for value in result:
			self.insert_member(value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8], value[9], value[10], value[11])
	

	def import_moviment_from_sqlite(self):

		self.cursor.execute("SELECT * FROM moviment")
		result = self.cursor.fetchall()
		for value in result:
			self.insert_member(value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8])
	

	def tancar_conexio(self):

		self.conexio.close()
		self.mysqlCursor.close()
		self.mysqlConnection.close()


	def update_category(self, id, fee):
		query = "UPDATE category \
			SET fee = %s WHERE id = %s"
		data = fee, id
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al insertar una nova categoria a la base de dades"
			)


	def insert_family(self, id, discount, is_direct_debited):
		query = "INSERT INTO family (id, discount, isDirectDebited) \
			VALUES (%s, %s, %s)"
		data = id, discount, is_direct_debited
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al insertar una nova familia a la base de dades"
			)


	def insert_member(self, id, name, surname, birthdate, gender, dni, address, phone_number, is_registered, email, id_family, id_category):
		query = "INSERT INTO member \
			(id, name, surname, birthdate, gender, dni, address, phoneNumber, \
				isRegistered, email, familyFk, categoryFk) \
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		data = id, name, surname, birthdate, gender, dni, address, phone_number, is_registered, email, id_family, id_category
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al insertar faller a la base de dades"
			)


	def insert_movement(self, id, transaction_date, amount, id_type, id_concept, falla_year, id_member, description, receipt_number):
		query = "INSERT INTO movement \
			(id, transactionDate, amount, idType, idConcept, fallaYearFk, \
				memberFk, description, receiptNumber) \
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
		data = id, transaction_date, amount, id_type, id_concept, \
			falla_year, id_member, description, receipt_number
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al insertar un moviment a la base de dades"
			)

	'''def delete_fallaYear(self):
		query = "DELETE FROM fallaYear"
		try:
			self.mysqlCursor.execute(query)
			self.mysqlConnection.commit()
		except mysql.connector.Error as err:
			messagebox.showerror(
				"Error",
				"Error al eliminar l'exercici de la base de dades:"
			)
			print({err})'''


	def insert_fallaYear(self, code, created, finished):
		query = "INSERT INTO fallaYear (code, created, finished) VALUES (%s, %s, %s)"
		data = code, created, finished
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error as err:
			messagebox.showerror(
				"Error",
				"Error al insertar un exercici a la base de dades"
			)
			print({err})


	# Mètodes per a operacions CRUD en la taula faller.

	def llegir_fallers(self):
		'''
		Llig de la taula "faller" tots els fallers
		i els afegeix a una llista d'objectes de la classe Faller.

		Retorna:
		--------
		llista_fallers : llista
			Llistat d'objectes de la classe Faller.
		'''
		try:
			self.cursor.execute("SELECT * FROM faller INNER JOIN familia ON faller.idfamilia = familia.id INNER JOIN categoria ON faller.idcategoria = categoria.id")
			resultat = self.cursor.fetchall()
			llistat_fallers=[]
			for valors in resultat:
				familia= Family(valors[12], valors[13], valors[14])
				categoria= Category(valors[15], valors[16], valors[17], valors[18])
				faller = Member(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[6], valors[7], valors[8], valors[11], familia, categoria)
				llistat_fallers.append(faller)
			return llistat_fallers
		except sqlite3.Error as e:
			messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
			return None
		except ConnectionError as e:
			messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
			return None
		

	def llegir_fallers_per_familia_i_alta(self, id_familia, alta):
		'''
		Llig de la taula "faller" tots aquells fallers amb l'identificador de familia
		passat per paràmetre.

		Paràmetres:
		-----------
		id_familia : integer
			Identificador de la familia del faller.
		alta : integer
			Identificador de l'estat d'alta del faller.

		Retorna:
		--------
		llistat_fallers : llista
			Llistat d'objectes de la classe Faller.
		'''
		dades=id_familia, alta
		try:
			self.cursor.execute("SELECT * FROM faller INNER JOIN familia ON faller.idfamilia = familia.id INNER JOIN categoria ON faller.idcategoria = categoria.id WHERE faller.idfamilia=? and faller.alta=?", (dades))
			resultat = self.cursor.fetchall()
			llistat_fallers=[]
			for valors in resultat:
				familia= Family(valors[12], valors[13], valors[14])
				categoria= Category(valors[15], valors[16], valors[17], valors[18])
				faller = Member(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[6], valors[7], valors[8], valors[11], familia, categoria)
				llistat_fallers.append(faller)
			return llistat_fallers
		except sqlite3.Error as e:
			messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
			return None
		except ConnectionError as e:
			messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
			return None
		
		
	def llegir_fallers_per_alta(self, alta):
		'''
		Llig de la taula "faller" tots aquells fallers amb l'estat d'alta del faller
		passat per paràmetre.

		Paràmetres:
		-----------
		alta : integer
			Identificador de l'estat d'alta del faller.

		Retorna:
		--------
		llistat_fallers : llista
			Llistat d'objectes de la classe Faller.
		'''
		query_params=(alta,)
		try:
			self.cursor.execute("SELECT * FROM faller INNER JOIN familia ON faller.idfamilia = familia.id INNER JOIN categoria ON faller.idcategoria = categoria.id WHERE faller.alta=? ORDER BY faller.cognoms", query_params)
			resultat = self.cursor.fetchall()
			llistat_fallers=[]
			for valors in resultat:
				familia= Family(valors[12], valors[13], valors[14])
				categoria= Category(valors[15], valors[16], valors[17], valors[18])
				faller = Member(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[6], valors[7], valors[8], valors[11], familia, categoria)
				llistat_fallers.append(faller)
			return llistat_fallers
		except sqlite3.Error as e:
			messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
			return None
		except ConnectionError as e:
			messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
			return None


	def llegir_fallers_per_categoria(self, categoria):
		'''
		Llig de la taula "faller" tots aquells fallers amb la categoria del faller
		passada per paràmetre.

		Paràmetres:
		-----------
		categoria : integer
			Identificador de la categoria del faller.

		Retorna:
		--------
		llistat_fallers : llista
			Llistat d'objectes de la classe Faller.
		'''
		query_params=(categoria,)
		try:
			self.cursor.execute("SELECT * FROM faller INNER JOIN familia ON faller.idfamilia = familia.id INNER JOIN categoria ON faller.idcategoria = categoria.id WHERE faller.alta=1 and faller.idcategoria=? ORDER BY faller.cognoms", query_params)
			resultat = self.cursor.fetchall()
			llistat_fallers=[]
			for valors in resultat:
				familia= Family(valors[12], valors[13], valors[14])
				categoria= Category(valors[15], valors[16], valors[17], valors[18])
				faller = Member(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[6], valors[7], valors[8], valors[11], familia, categoria)
				llistat_fallers.append(faller)
			return llistat_fallers
		except sqlite3.Error as e:
			messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
			return None
		except ConnectionError as e:
			messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
			return None


	# Mètodes per a operacions CRUD en la taula familia
		
	
	def llegir_families(self):
		'''
		Llig de la taula "familia" totes les families
		i les afegeix a una llista d'objectes de la classe Familia.

		Retorna:
		--------
		llista_families : llista
			Llistat d'objectes de la classe Familia.
		'''
		try:
			self.cursor.execute("SELECT * FROM familia")
			resultat = self.cursor.fetchall()
			llistat_families=[]
			for valors in resultat:
				familia= Family(valors[0], valors[1], valors[2])
				llistat_families.append(familia)
			return llistat_families
		except sqlite3.Error as e:
			messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
			return None
		except ConnectionError as e:
			messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
			return None
	
	
	# Mètodes per a operacions CRUD en la taula moviment.
		
	def llegir_moviments_per_data_tipo(self, data, tipo):
		query_params=(data, tipo,)
		try:
			self.cursor.execute("SELECT * FROM moviment INNER JOIN faller ON moviment.idfaller=faller.id WHERE moviment.data=? and moviment.tipo=?", query_params)
			resultat=self.cursor.fetchall()
			llistat_moviments=[]
			for valors in resultat:
				faller=Member(valors[9], valors[10], valors[11], valors[12], valors[13], valors[14], valors[15], valors[16], valors[17], valors[18])
				moviment=Movement(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[7], valors[8], faller)
				llistat_moviments.append(moviment)
			return llistat_moviments
		except sqlite3.Error as e:
			messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
			return None
		except ConnectionError as e:
			messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
			return None
	
	
	def llegir_moviments_per_data_tipo_descripcio(self, data, tipo, descripcio):
		query_params=(data, tipo, descripcio)
		try:
			self.cursor.execute("SELECT * FROM moviment INNER JOIN faller ON moviment.idfaller=faller.id WHERE moviment.data=? and moviment.tipo=? and moviment.descripcio=?", query_params)
			resultat=self.cursor.fetchall()
			llistat_moviments=[]
			for valors in resultat:
				faller=Member(valors[9], valors[10], valors[11], valors[12], valors[13], valors[14], valors[15], valors[16], valors[17], valors[18])
				moviment=Movement(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[7], valors[8], faller)
				llistat_moviments.append(moviment)
			return llistat_moviments
		except sqlite3.Error as e:
			messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
			return None
		except ConnectionError as e:
			messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
			return None
		

	# Mètodes per a operacions CRUD en la taula categoria.
		
	def crear_categoria(self, categoria):
		'''
		Escriu a la base de dades la categoria que se li passa com a paràmetre a la taula "categoria".

		Paràmetres:
		-----------
		categoria : Categoria
			Objecte de la classe Categoria.
		'''
		dades=categoria.fee, categoria.name, categoria.description
		self.cursor.execute("INSERT INTO categoria VALUES (null, ?, ?, ?)",(dades))
		self.conexio.commit()


	# Mètodes per a operacions CRUD en la taula loteria.

	def crear_loteria(self, loteria):
		'''
		Escriu a la base de dades la loteria que se li passa com a paràmetre a la taula "loteria".

		Paràmetres:
		-----------
		loteria : Loteria
			Objecte de la classe Loteria.
		'''
		dades=loteria.sorteig, loteria.data, loteria.paperetes_masculina, loteria.paperetes_femenina, loteria.paperetes_infantil, loteria.decims_masculina, loteria.decims_femenina, loteria.decims_infantil, loteria.assignada, loteria.faller.id
		self.cursor.execute("INSERT INTO categoria VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(dades))
		self.conexio.commit()

	def llegir_loteries_per_sorteig(self, sorteig):
		query_params=(sorteig,)
		try:
			self.cursor.execute("SELECT * FROM loteria INNER JOIN faller ON loteria.idfaller = faller.id WHERE loteria.sorteig=?", query_params)
			resultat = self.cursor.fetchall()
			llistat_loteries=[]
			for valors in resultat:
				faller=Member(valors[10], valors[11], valors[12], valors[13], valors[14], valors[15], valors[16], valors[17], valors[18], valors[19])
				loteria= Loteria(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[6], valors[7], valors[8], valors[9], faller)
				llistat_loteries.append(loteria)
			return llistat_loteries
		except sqlite3.Error as e:
			messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
			return None
		except ConnectionError as e:
			messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
			return None
		

	def llegir_sortejos(self):
		try:
			self.cursor.execute("SELECT DISTINCT sorteig FROM loteria")
			llistat_sortejos = self.cursor.fetchall()
			return llistat_sortejos
		except sqlite3.Error as e:
			messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
			return None
		except ConnectionError as e:
			messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
			return None


	def llegir_ultim_id_loteria(self):
		try:
			self.cursor.execute("SELECT * FROM loteria ORDER BY id DESC LIMIT 1")
			resultat = self.cursor.fetchone()
			if resultat is not None:
				return resultat
			else:
				return None
		except (sqlite3.Error, TypeError, ValueError) as e:
			print("Error al llegir la loteria de la base de dades:", e)
			return None


	def actualitzar_loteria(self, loteria):
		'''
		Actualitza la taula "loteria" amb l'objecte de la classe Loteria que se li passa per paràmetre.

		Paràmetres:
		-----------
		loteria : Loteria
			Objecte de la classe Loteria.
		'''
		dades=loteria.paperetes_masculina, loteria.paperetes_femenina, loteria.paperetes_infantil, loteria.decims_masculina, loteria.decims_femenina, loteria.decims_infantil, loteria.id
		try:
			self.cursor.execute("UPDATE loteria SET paperetes_masculina=?, paperetes_femenina=?, paperetes_infantil=?, decims_masculina=?, decims_femenina=?, decims_infantil=? WHERE id=?", (dades))
		except sqlite3.Error:
			messagebox.showerror("Error", "Hi ha un problema amb la base de dades")
		else:
			self.conexio.commit()


	def actualitzar_assignada_loteria(self, id):
		assignada=1
		dades=assignada, id
		try:
			self.cursor.execute("UPDATE loteria SET assignada=? WHERE id=?", (dades))
		except sqlite3.Error:
			messagebox.showerror("Error", "Hi ha un problema amb la base de dades")
		else:
			self.conexio.commit()


	def eliminar_loteria(self, id):
		'''
		Elimina de la base de dades la loteria el id de la qual se li passa per paràmetre

		Paràmetres:
		-----------
		id : integer
			Identificador de la loteria a eliminar.
		'''
		self.cursor.execute("DELETE FROM loteria WHERE id=?", (id,))
		self.conexio.commit()