import mysql.connector
from tkinter import messagebox

from utils import Utils


class Database:
	'''
	Aquesta classe controla la conexió amb MariaDb i totes les operacions CRUD
	amb la base de dades.

	Atributs:
	---------
	db_name : string
		Nom de la base de dades.
	'''
	def __init__(self, db_name):
		'''
		Inicialitza una nova instància de la classe Database.
		Conexió MariaDb.

		Paràmetres:
		-----------
		db_name : string
			Nom de la base de dades.
		'''
		self.verify_existence_db(db_name)
		self.mysqlConnection = mysql.connector.connect(
			host = "localhost",
			user = "root",
			password = "hamuclaulo07",
			database = db_name
		)
		if self.mysqlConnection.is_connected():
			self.mysqlCursor = self.mysqlConnection.cursor()
		else:
			messagebox.showerror(
				"Error",
				"No s'ha pogut establir la conexió amb la base de dades."
			)

	
	def close_connection(self):
		'''
		Tancament de la conexió.
		'''
		self.mysqlCursor.close()
		self.mysqlConnection.close()


	def verify_existence_db(self, db_name):
		'''
		Verifica la existència de la base de dades i en cas contrari la crea.

		Paràmetres:
		-----------
		db_name : string
			Nom de la base de dades.
		'''
		try:
			self.mysqlConnection = mysql.connector.connect(
				host = "localhost",
				user = "root",
				password = "hamuclaulo07"
			)
			if self.mysqlConnection.is_connected():
				self.mysqlCursor = self.mysqlConnection.cursor()
			else:
				messagebox.showerror(
					"Error",
					"No s'ha pogut establir la conexió amb la base de dades."
				)
			query = f"SHOW DATABASES LIKE '{db_name}'"
			self.mysqlCursor.execute(query)
			result = self.mysqlCursor.fetchone()
			self.close_connection()
			if result:
				pass
			else:
				messagebox.showerror(
					"Error",
					"La base de dades no existeix. Es crearà automàticament."
				)
				self.create_database(db_name)
				self.create_tables(db_name)
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"No s'ha pogut verificar l'existència de la base de dades."
			)


	def create_database(self, db_name):
		'''
		Crea la BBDD
		'''
		self.mysqlConnection = mysql.connector.connect(
				host = "localhost",
				user = "root",
				password = "hamuclaulo07"
			)
		if self.mysqlConnection.is_connected():
			self.mysqlCursor = self.mysqlConnection.cursor()
		else:
			messagebox.showerror(
				"Error",
				"No s'ha pogut establir la conexió amb la base de dades."
			)
		query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
		try:
			self.mysqlCursor.execute(query)
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"No s'ha pogut crear la base de dades"
			)


	def create_tables(self, db_name):
		'''
		Crea les diferents taules
		'''
		self.mysqlConnection = mysql.connector.connect(
					host = "localhost",
					user = "root",
					password = "hamuclaulo07",
					database = db_name
				)
		if self.mysqlConnection.is_connected():
			self.mysqlCursor = self.mysqlConnection.cursor()
		else:
			messagebox.showerror(
				"Error",
				"No s'ha pogut establir la conexió amb la base de dades."
			)

		query="""
		CREATE TABLE IF NOT EXISTS member(
			id INT AUTO_INCREMENT PRIMARY KEY,
			name VARCHAR(50) NOT NULL,
			surname VARCHAR(100) NOT NULL,
			birthdate DATE NOT NULL,
			gender ENUM('M', 'F'),
			dni VARCHAR(10),
			address VARCHAR(100),
			phoneNumber VARCHAR(15),
			isRegistered BOOLEAN,
			familyFk INT,
			categoryFk INT,
			email VARCHAR(50)
		)
		"""
		try:
			self.mysqlCursor.execute(query)
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"No s'ha pogut crear la taula member"
			)
		
		query = """
		CREATE TABLE IF NOT EXISTS category(
			id INT AUTO_INCREMENT PRIMARY KEY,
			fee DECIMAL(10, 2) NOT NULL,
			name VARCHAR(10),
			description VARCHAR(50)
		)
		"""
		try:
			self.mysqlCursor.execute(query)
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"No s'ha pogut crear la taula category"
			)

		query = """
		CREATE TABLE IF NOT EXISTS family(
			id INT AUTO_INCREMENT PRIMARY KEY,
			discount DECIMAL(10, 2) NOT NULL,
			isDirectDebited BOOLEAN
		)
		"""
		try:
			self.mysqlCursor.execute(query)
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"No s'ha pogut crear la taula family"
			)
		
		query = """
		CREATE TABLE IF NOT EXISTS movement(
			id INT AUTO_INCREMENT PRIMARY KEY,
			transactionDate DATE NOT NULL,
			amount DECIMAL(10, 2) NOT NULL,
			idType INT NOT NULL,
			idConcept INT NOT NULL,
			fallaYear INT NOT NULL,
			memberFk INT,
			description VARCHAR(100),
			receiptNumber INT
		)
		"""
		try:
			self.mysqlCursor.execute(query)
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"No s'ha pogut crear la taula movement"
			)

		query = """
		ALTER TABLE member
			ADD CONSTRAINT member_family_FK
			FOREIGN KEY(familyFk)
			REFERENCES family(id)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
			ADD CONSTRAINT member_category_FK
			FOREIGN KEY(categoryFk)
			REFERENCES category(id)
			ON DELETE CASCADE
			ON UPDATE CASCADE
		"""
		try:
			self.mysqlCursor.execute(query)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Ha fallat la creació de les FK de la taula member."
			)

		query = """
		ALTER TABLE movement
			ADD CONSTRAINT movement_member_FK
			FOREIGN KEY(memberFk)
			REFERENCES member(id)
			ON DELETE CASCADE
			ON UPDATE CASCADE
		"""
		try:
			self.mysqlCursor.execute(query)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Ha fallat la creació de la FK de la taula moviment."
			)
		finally:
			self.close_connection()


	def export_category_to_mysql(self, result):
		'''
		Exportació taula categoria a sp.category
		'''
		query = "INSERT INTO category (id, fee, name, description) \
			VALUES (%s, %s, %s, %s)"
		try:
			for row in result:
				self.mysqlCursor.execute(query, row)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			self.mysqlConnection.rollback()
			messagebox.showerror(
				"Error",
				"No s'han pogut insertar les dades a la taula category"
			)
		finally:
			self.close_connection()


	def export_family_to_mysql(self, result):
		'''
		Exportació taula familia a sp.family
		'''
		query = "INSERT INTO family (id, discount, isDirectDebited) \
			VALUES (%s, %s, %s)"
		try:
			for row in result:
				self.mysqlCursor.execute(query, row)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			self.mysqlConnection.rollback()
			messagebox.showerror(
				"Error",
				"No s'han pogut insertar les dades a la taula family"
			)
		finally:
			self.close_connection()


	def export_member_to_mysql(self, result):
		'''
		Exportació taula faller a sp.member
		'''
		utils = Utils()
		query = "INSERT INTO member \
			(id, name, surname, birthdate, gender, dni, address, phoneNumber, \
				isRegistered, familyFk, categoryFk, email) \
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		try:
			for row in result:
				as_list = list(row)
				date = utils.convert_to_mariadb_date(as_list[3])
				as_list[3] = date
				self.mysqlCursor.execute(query, as_list)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			self.mysqlConnection.rollback()
			messagebox.showerror(
				"Error",
				"No s'han pogut insertar les dades a la taula member"
			)
		finally:
			self.close_connection()


	def export_movements_to_mysql(self, result):
		'''
		Exportació taula moviment a sp.movement
		'''
		utils=Utils()
		query="INSERT INTO movement \
			(id, transactionDate, amount, idType, idConcept, fallaYear, \
				memberFk, description, receiptNumber) \
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
		try:
			for row in result:
				as_list = list(row)
				date = utils.convert_to_mariadb_date(as_list[1])
				as_list[1] = date
				self.mysqlCursor.execute(query, as_list)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			self.mysqlConnection.rollback()
			messagebox.showerror(
				"Error",
				"No s'han pogut insertar les dades a la taula movement"
			)
		finally:
			self.close_connection()


	# Mètodes per a operacions CRUD en la taula member.
	def insert_member(
			self,
			name,
			surname,
			birthdate,
			gender,
			dni,
			address,
			phone_number,
			is_registered,
			email,
			id_family,
			id_category
		):
		'''
		Escriu a la base de dades les dades del faller que se li passa
		com a paràmetre a la taula "member".

		Paràmetres:
		-----------
		name : string
			Nom el faller.
		surname : string
			Cognoms del faller.
		birthdate : date
			Data de naixement.
		gender : int
			Sexe.
		dni : string
			Dni.
		address : string
			Adreça.
		phone_number : string
			Telèfon.
		is_registered : bool
			Marca si està donat d'alta o no.
		email : string
			Correu electrònic.
		id_family : int
			Identificador de la familia a la que pertany.
		id_category : int
			Identificador de la categoria de la falla a la que pertany.
		'''
		query = "INSERT INTO member \
			(name, surname, birthdate, gender, dni, address, phoneNumber, \
				isRegistered, email, familyFk, categoryFk) \
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		data = name, surname, birthdate, gender, dni, address, phone_number, \
			is_registered, email, id_family, id_category
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al insertar faller a la base de dades"
			)


	def select_member(self, id):
		'''
		Llig de la taula "member" aquell faller amb
		l'id que se li passa per paràmetre.

		Paràmetres:
		-----------
		id : int
			Identificador del faller.

		Retorna:
		--------
		member : list
			Llistat de les dades del faller.
		'''
		query = "SELECT * FROM member INNER JOIN family \
			ON member.familyFk = family.id INNER JOIN category \
				ON member.categoryFk = category.id where member.id = %s"
		try:
			self.mysqlCursor.execute(query, (id,))
			member = self.mysqlCursor.fetchone()
			return member
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir membre de la base de dades"
			)


	def select_last_member(self):
		'''
		Llig l'últim registre de la taula "member".

		Retorna:
		--------
		member : list
			Llistat de les dades del faller.
		'''
		query = "SELECT * FROM member ORDER BY id DESC LIMIT 1"
		try:
			self.mysqlCursor.execute(query)
			member = self.mysqlCursor.fetchone()
			return member
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir l'últim membre de la base de dades"
			)


	def select_members_by_surname(self, surname):
		'''
		Llig de la taula "member" tots aquells fallers
		amb un cognom que conté la cadena passada per paràmetre.

		Paràmetres:
		-----------
		surname : string
			Cadena a la que s'ha de pareixer el cognom dels fallers.

		Retorna:
		--------
		members_list : list
			Llistat de fallers.
		'''
		query = "SELECT * FROM member INNER JOIN family \
			ON member.familyFk = family.id INNER JOIN category \
				ON member.categoryFk = category.id \
					WHERE member.surname LIKE %s"
		try:
			self.mysqlCursor.execute(query, (f"%{surname}%",))
			members_list = self.mysqlCursor.fetchall()
			return members_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir membres per cognom a la base de dades"
			)


	def select_adult_members(self):
		'''
		Llig de la taula "member" tots aquells fallers amb 14 anys o més
		(categories 1 i 2) i els afegeix a una llista de fallers.

		Retorna:
		--------
		members_list : list
			Llistat de fallers.
		'''
		query = "SELECT * FROM member INNER JOIN family \
			ON member.familyFk = family.id INNER JOIN category \
				ON member.categoryFk = category.id \
					WHERE member.isRegistered and \
						(member.categoryFk = 1 or member.categoryFk = 2) \
							ORDER BY member.surname"
		try:
			self.mysqlCursor.execute(query)
			members_list = self.mysqlCursor.fetchall()
			return members_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els membres adults de la base de dades"
			)


	def select_registered_members(self, is_registered):
		'''
		Llig de la taula "member" tots aquells fallers actius
		i els afegeix a una llista de fallers.

		Retorna:
		--------
		members_list : list
			Llistat de fallers.
		'''
		query = "SELECT * FROM member INNER JOIN family \
			ON member.familyFk = family.id INNER JOIN category \
				ON member.categoryFk = category.id \
					WHERE member.isRegistered = %s \
						ORDER BY member.surname"
		try:
			self.mysqlCursor.execute(query, (is_registered,))
			members_list = self.mysqlCursor.fetchall()
			return members_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els membres actius de la base de dades"
			)


	def select_members_by_family(self, id_family):
		'''
		Llig de la taula "member" tots aquells fallers
		amb l'identificador de familia passat per paràmetre.

		Paràmetres:
		-----------
		id_family : int
			Identificador de la familia del faller.

		Retorna:
		--------
		members_list : list
			Llistat de fallers.
		'''
		query = "SELECT * FROM member INNER JOIN family \
			ON member.familyFk = family.id INNER JOIN category \
				ON member.categoryFk = category.id WHERE member.familyFk = %s"
		try:
			self.mysqlCursor.execute(query, (id_family,))
			members_list = self.mysqlCursor.fetchall()
			return members_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els membres per familia de la base de dades"
			)


	def select_members_by_category(self, id_category):
		'''
		Llig de la taula "member" tots aquells fallers
		amb l'identificador de categoria passat per paràmetre.

		Paràmetres:
		-----------
		id_category : int
			Identificador de la categoria del faller.

		Retorna:
		--------
		members_list : list
			Llistat de fallers.
		'''
		query = "SELECT * FROM member INNER JOIN family \
			ON member.familyFk = family.id INNER JOIN category \
				ON member.categoryFk = category.id WHERE member.categoryFk = %s"
		try:
			self.mysqlCursor.execute(query, (id_category,))
			members_list = self.mysqlCursor.fetchall()
			return members_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els membres per categoria de la base de dades"
			)


	def select_membership_history(self, id):
		query = "SELECT * FROM membership_history WHERE id = %s"
		try:
			self.mysqlCursor.execute(query, (id,))
			membership_history = self.mysqlCursor.fetchall()
			return membership_history
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir l'historial del faller de la base de dades"
			)


	def update_member(
			self,
			id,
			name,
			surname,
			birthdate,
			gender,
			dni,
			address,
			phone_number,
			is_registered,
			email,
			id_family,
			id_category
		):
		'''
		Actualitza la taula "member" amb les dades del faller
		que se li passa per paràmetre.

		Paràmetres:
		-----------
		id : int
			Identificador del faller.
		name : string
			Nom el faller.
		surname : string
			Cognoms del faller.
		birthdate : date
			Data de naixement.
		gender : int
			Sexe.
		dni : string
			Dni.
		address : string
			Adreça.
		phone_number : string
			Telèfon.
		is_registered : bool
			Marca si està donat d'alta o no.
		email : string
			Correu electrònic.
		id_family : int
			Identificador de la familia a la que pertany.
		id_category : int
			Identificador de la categoria de la falla a la que pertany.
		'''
		query = "UPDATE member SET name = %s, surname = %s, birthdate = %s, \
			gender = %s, dni = %s, address = %s, phoneNumber = %s, \
				isRegistered = %s, email = %s, familyFk = %s, categoryFk = %s \
					WHERE id = %s"
		data = name, surname, birthdate, gender, dni, address, \
			phone_number, is_registered, email, id_family, id_category, id
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al actualitzar les dades del faller a la base de dades"
			)


	# Mètodes per a operacions CRUD en la taula family.
	def insert_family(self, discount, is_direct_debited):
		'''
		Escriu a la base de dades les dades de la familia que se li passa
		com a paràmetre a la taula "family".

		Paràmetres:
		-----------
		discount : float
			Descompte familiar.
		is_direct_debited : boolean
			Si està domiciliat o no.
		'''
		query = "INSERT INTO family (discount, isDirectDebited) \
			VALUES (%s, %s)"
		data = discount, is_direct_debited
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al insertar una nova familia a la base de dades"
			)


	def select_family(self, id):
		'''
		Llig de la taula "family" aquella familia
		amb l'id que se li passa per paràmetre.

		Paràmetres:
		-----------
		id : integer
			Identificador de la familia.

		Retorna:
		--------
		family : list
			Llista de dades de la familia.
		'''
		query = "SELECT * FROM family where id = %s"
		try:
			self.mysqlCursor.execute(query, (id,))
			family = self.mysqlCursor.fetchone()
			return family
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir una familia de la base de dades"
			)


	def select_last_family(self):
		'''
		Llig l'últim registre de la taula "family".

		Retorna:
		--------
		family : list
			Llista de dades de la familia.
		'''
		query = "SELECT * FROM family ORDER BY id DESC LIMIT 1"
		try:
			self.mysqlCursor.execute(query)
			family = self.mysqlCursor.fetchone()
			return family
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir l'última familia de la base de dades"
			)


	def select_families(self):
		'''
		Llig tot el contingut de la taula "family" i els afegeix a una llista de families.

		Retorna:
		--------
		families_list : list
			Llistat de families.
		'''
		query = "SELECT * FROM family"
		try:
			self.mysqlCursor.execute(query)
			families_list = self.mysqlCursor.fetchall()
			return families_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir les families de la base de dades"
			)


	def select_discount_by_member(self, id_member):
		'''
		Llig de la taula "family" el descompte familiar.

		Paràmetres:
		-----------
		id_member : integer
			Identificador del membre de la familia.

		Retorna:
		--------
		discount : float
			Llista de dades de la familia.
		'''
		query = "SELECT discount FROM family INNER JOIN member \
			ON family.id = member.familyFk WHERE member.id = %s"
		try:
			self.mysqlCursor.execute(query, (id_member,))
			discount = self.mysqlCursor.fetchone()
			return discount
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir el descompte familiar de la base de dades"
			)


	def update_family(self, id, discount, is_direct_debited):
		'''
		Actualitza la taula "family" amb les dades
		de la familia que se li passa per paràmetre.

		Paràmetres:
		-----------
		id : int
			Identificador de la familia.
		discount : float
			Descompte familiar.
		is_direct_debited : boolean
			Si està domiciliat o no.
		'''
		query = "UPDATE family SET discount = %s, isDirectDebited = %s \
			WHERE id = %s"
		data = discount, is_direct_debited, id
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al modificar la familia de la base de dades"
			)


	def delete_family(self, id):
		'''
		Elimina de la base de dades la familia, el id de la qual,
		se li passa per paràmetre.

		Paràmetres:
		-----------
		id : int
			Identificador de la familia a eliminar.
		'''
		query = "DELETE FROM family WHERE id = %s"
		try:
			self.mysqlCursor.execute(query, (id,))
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al eliminar la familia de la base de dades"
			)


	# Mètodes per a operacions CRUD en la taula movement.
	def select_fee_assignment_movements_by_member(self, id_member, falla_year):
		'''
		Llig els moviments d'assignació de quota del faller i exercici
		passats per paràmetre.

		Paràmetres:
		-----------
		id_member : int
			Identificador del faller.
		falla_year : int
			Exercici faller.

		Retorna:
		--------
		movements_list : list
			Llistat de moviments.
		'''
		query = "SELECT amount FROM movement \
			WHERE memberFk = %s and idType = 1 \
				and idConcept = 1 and fallaYear = %s"
		try:
			self.mysqlCursor.execute(query, (id_member, falla_year))
			movements_list = self.mysqlCursor.fetchall()
			return movements_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els moviments d'assignació de quota"
			)


	def select_lottery_assignment_movements_by_member(
			self,
			id_member,
			falla_year
		):
		'''
		Llig els moviments d'assignació de loteria del faller
		i exercici passats per paràmetre.

		Paràmetres:
		-----------
		id_member : int
			Identificador del faller.
		falla_year : int
			Exercici faller.
		
		Retorna:
		--------
		movements_list : list
			Llistat de moviments.
		'''
		query = "SELECT amount FROM movement \
			WHERE memberFk = %s and idType = 1 and \
				idConcept = 2 and fallaYear = %s"
		try:
			self.mysqlCursor.execute(query, (id_member, falla_year))
			movements_list = self.mysqlCursor.fetchall()
			return movements_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els moviments d'assignacio de loteria"
			)


	def select_raffle_assignment_movements_by_member(
			self,
			id_member,
			falla_year
		):
		'''
		Llig els moviments d'assignació de rifa del faller
		i exercici passats per paràmetre.

		Paràmetres:
		-----------
		id_member : int
			Identificador del faller.
		falla_year : int
			Exercici faller.
		
		Retorna:
		--------
		movements_list : list
			Llistat de moviments.
		'''
		query = "SELECT amount FROM movement \
			WHERE memberFk = %s and idType = 1 \
				and idConcept = 3 and fallaYear = %s"
		try:
			self.mysqlCursor.execute(query, (id_member, falla_year))
			movements_list = self.mysqlCursor.fetchall()
			return movements_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els moviments d'assignacio de rifa"
			)


	def select_fee_payment_movements_by_member(self, id_member, falla_year):
		'''
		Llig els moviments de pagament de quota del faller
		i exercici passats per paràmetre.

		Paràmetres:
		-----------
		id_member : int
			Identificador del faller.
		falla_year : int
			Exercici faller.

		Retorna:
		--------
		movements_list : list
			Llistat de moviments.
		'''
		query = "SELECT amount FROM movement \
			WHERE memberFk = %s and idType = 2 \
				and idConcept = 1 and fallaYear = %s"
		try:
			self.mysqlCursor.execute(query, (id_member, falla_year))
			movements_list = self.mysqlCursor.fetchall()
			return movements_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els moviments de pagament de quota")


	def select_lottery_payment_movements_by_member(
			self,
			id_member,
			falla_year
		):
		'''
		Llig els moviments de pagament de loteria del faller
		i exercici passats per paràmetre.

		Paràmetres:
		-----------
		id_member : int
			Identificador del faller.
		falla_year : int
			Exercici faller.

		Retorna:
		--------
		movements_list : list
			Llistat de moviments.
		'''
		query = "SELECT amount FROM movement \
			WHERE memberFk = %s and idType = 2 \
				and idConcept = 2 and fallaYear = %s"
		try:
			self.mysqlCursor.execute(query, (id_member, falla_year))
			movements_list = self.mysqlCursor.fetchall()
			return movements_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els moviments de pagament de loteria"
			)


	def select_raffle_payment_movements_by_member(self, id_member, falla_year):
		'''
		Llig els moviments de pagament de rifa del faller
		i exercici passats per paràmetre.

		Paràmetres:
		-----------
		id_member : int
			Identificador del faller.
		falla_year : int
			Exercici faller.

		Retorna:
		--------
		movements_list : list
			Llistat de moviments.
		'''
		query = "SELECT amount FROM movement \
			WHERE memberFk = %s and idType = 2 \
				and idConcept = 3 and fallaYear = %s"
		try:
			self.mysqlCursor.execute(query, (id_member, falla_year))
			movements_list = self.mysqlCursor.fetchall()
			return movements_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els moviments de pagament de rifa"
			)


	def select_payment_movements_by_date(self, date, description):
		'''
		Llig tots els moviments de pagament de la data
		passada per paràmetre.

		Paràmetres:
		-----------
		date : string
			Data.
		description : string
			Dexcripció de pagat per caixa o banc.

		Retorna:
		--------
		movements_list : list
			Llistat de moviments.
		'''
		query = "SELECT * FROM movement \
			INNER JOIN member ON movement.memberFk = member.id \
			WHERE transactionDate = %s and idType = 2 \
				and description = %s"
		try:
			self.mysqlCursor.execute(query, (date, description))
			movements_list = self.mysqlCursor.fetchall()
			return movements_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els moviments del dia"
			)


	def insert_movement(
			self,
			transaction_date,
			amount,
			id_type,
			id_concept,
			falla_year,
			id_member,
			description,
			receipt_number
		):
		'''
		Escriu a la base de dades el moviment que se li passa
		com a paràmetre a la taula "movement".

		Paràmetres:
		-----------
		transaction_date : date
			Data en que s'efectua el moviment.
		amount : float
			Quantitat de diners.
		id_type : int
			Tipo de moviment. Pot ser assignació o pagament.
		id_concept : int
			Concepte. Pot ser quota, loteria o rifa.
		falla_year : int
			Exercici faller.
		id_member : int
			Identificador del faller sobre el que es fa el moviment.
		description : string
			Descripció del moviment.
		receipt_number : int
			Número de rebut.
		'''
		query = "INSERT INTO movement \
			(transactionDate, amount, idType, idConcept, fallaYear, \
				memberFk, description, receiptNumber) \
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
		data = transaction_date, amount, id_type, id_concept, \
			falla_year, id_member, description, receipt_number
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al insertar un moviment a la base de dades"
			)


	def select_movements_by_member(self, id_member, falla_year):
		'''
		Llig de la taula "movement" tots aquells moviments amb
		l'identificador de faller i l'exercici passats per paràmetre.

		Paràmetres:
		-----------
		id_member : int
			Identificador del faller.
		falla_year : int
			Exercici per al qual es volen recuperar les dades.

		Retorna:
		--------
		movements_list : list
			Llistat de moviments.
		'''
		query = "SELECT * FROM movement WHERE memberFk = %s AND fallaYear = %s"
		try:
			self.mysqlCursor.execute(query, (id_member, falla_year))
			movements_list = self.mysqlCursor.fetchall()
			return movements_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els moviments per faller de la base de dades"
			)


	# Mètodes per a operacions CRUD en la taula category.
	def select_category(self, id):
		'''
		Llig de la taula "category" aquella categoria 
		amb l'id que se li passa per paràmetre.

		Paràmetres:
		-----------
		id : int
			Identificador de la categoria.

		Retorna:
		--------
		category : list
			Llistat de dades de la categoria.
		'''
		query = "SELECT * FROM category where id = %s"
		try:
			self.mysqlCursor.execute(query, (id,))
			category = self.mysqlCursor.fetchone()
			return category
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir la categoria de la base de dades"
			)


	def select_categories(self):
		'''
		Llig totes les categories de la taula "category"

		Retorna:
		--------
		categories_list : list
			Llistat de categories.
		'''
		query = "SELECT * FROM category"
		try:
			self.mysqlCursor.execute(query)
			categories_list = self.mysqlCursor.fetchall()
			return categories_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir les categories de la base de dades"
			)


	def select_fee_by_member(self, id_member):
		'''
		Llig de la taula "category" en combinació amb la taula "member"
		la quota de la categoria a la que pertany el faller.

		Paràmetres:
		-----------
		id_member : int
			Identificador del faller.

		Retorna:
		--------
		fee : int
			Quota assignada al faller per la categoria a la que correspon.
		'''
		query = "SELECT fee FROM category INNER JOIN member \
			ON category.id = member.categoryFk WHERE member.id = %s"
		try:
			self.mysqlCursor.execute(query, (id_member,))
			fee = self.mysqlCursor.fetchone()
			return fee
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir la quota del faller de la base de dades"
			)


	def update_category(self, id, fee, name, description):
		'''
		Actualitza la taula "category" amb les dades de la categoria
		que se li passa per paràmetre.

		Paràmetres:
		-----------
		id : int
			El identificador a la taula "category" de la base de dades.
		fee : float
			Quantitat a pagar corresponent a dita categoria.
		name : string
			Forma amb la que es nombra dita categoria.
		description : string
			Informació sobre les edats a les quals correspon la categoria.
		'''
		query = "UPDATE category \
			SET fee = %s, name = %s, description = %s WHERE id = %s"
		data = fee, name, description, id
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al modificar les dades de la categoria"
			)


	def select_current_falla_year(self):
		'''
		Llig l'exercici actual.

		Retorna:
		--------
		falla_year : int
			Exercici actual.
		'''
		query = "SELECT code FROM falla_year ORDER BY code DESC LIMIT 1"
		try:
			self.mysqlCursor.execute(query)
			falla_year = self.mysqlCursor.fetchone()
			return falla_year[0]
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir l'exercici a la base de dades"
			)