import sqlite3
from tkinter import messagebox
import mysql.connector
from pathlib import Path

from arxiu import Arxiu
from utils import Utils

class ExportSqliteToMariaDb:
	
	def __init__(self, nom_db):
		base_path = Path(__file__).parent.resolve()
		self.conexio = sqlite3.connect(base_path / 'previous version' / 'falla.db')
		self.cursor = self.conexio.cursor()

		self.mysqlConnection = mysql.connector.connect(
			host = "localhost",
			user = "root",
			password = "hamuclaulo07",
			database = nom_db
		)

		if self.mysqlConnection.is_connected():
			self.mysqlCursor = self.mysqlConnection.cursor()

			self.insert_fallaYear(2022, "2021-03-20", "2022-03-19")
			self.insert_fallaYear(2023, "2022-03-20", "2023-03-19")
			self.insert_fallaYear(2024, "2023-03-20", "2024-06-26")
			self.import_categoria_from_sqlite()
			self.import_familia_from_sqlite()
			self.import_faller_from_sqlite()
			self.import_moviment_from_sqlite()
			self.import_summary_from_file(base_path / 'previous version' / 'resum 2022', 2022)
			self.import_summary_from_file(base_path / 'previous version' / 'resum 2023', 2023)
			self.import_summary_from_file(base_path / 'previous version' / 'resum 2024', 2024)
			self.import_lottery_from_file(base_path / 'previous version' / 'nadal 2023-24', 'nadal', 2024)
			self.import_lottery_from_file(base_path / 'previous version' / 'loteria xiquet 23-24', 'xiquet', 2024)
			self.import_faller_actiu_from_sqlite()

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
			self.insert_family(value[0], value[1], value[2])
	

	def import_faller_from_sqlite(self):

		self.cursor.execute("SELECT * FROM faller")
		result = self.cursor.fetchall()
		utils = Utils()
		for value in result:
			mariadbDate = utils.convert_to_mariadb_date(value[3])
			self.insert_member(value[0], value[1], value[2], mariadbDate, value[4], value[5], value[6], value[7], value[8], value[9], value[10], value[11])


	def import_faller_actiu_from_sqlite(self):
		self.cursor.execute("SELECT id FROM faller WHERE alta = 1")
		result = self.cursor.fetchall()
		for value in result:
			self.insert_membership_history(2025, value[0])
	

	def import_moviment_from_sqlite(self):

		self.cursor.execute("SELECT * FROM moviment")
		result = self.cursor.fetchall()
		utils = Utils()
		for value in result:
			mariadbDate = utils.convert_to_mariadb_date(value[1])
			self.insert_movement(value[0], mariadbDate, value[2], value[3], value[4], value[5], value[6], value[7], value[8])
	

	def tancar_conexio(self):

		self.conexio.close()
		self.mysqlCursor.close()
		self.mysqlConnection.close()


	def import_summary_from_file(self, file, falla_year):
		arxiu = Arxiu(file)
		result = arxiu.llegir_resum()
		for value in result:
			self.insert_summary(value[0], falla_year, value[1], value[2], value[3], value[5], value[6], value[7])
			self.insert_membership_history(falla_year, value[0])


	def import_lottery_from_file(self, file, lottery_name, falla_year):
		arxiu = Arxiu(file)
		result = arxiu.llegir_loteria()
		i=0
		for val in result:
			if len(result)>i:
				memberFk = result[i]
				value=result[i+1]
				i=i+2
				self.insert_lottery(lottery_name, falla_year, memberFk, value[1], value[2], value[3], value[4], value[5], value[6], 1)
			


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


	def insert_member(self, id, name, surname, birthdate, gender, dni, address, phone_number, is_registered, id_family, id_category, email):
		query = "INSERT INTO member \
			(id, name, surname, birthdate, gender, dni, address, phoneNumber, \
				isRegistered, familyFk, categoryFk, email) \
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		data = id, name, surname, birthdate, gender, dni, address, phone_number, is_registered, id_family, id_category, email
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


	def insert_summary(
			self,
			id_member,
			falla_year,
			assignedFee,
			assignedLottery,
			assignedRaffle,
			payedFee,
			payedLottery,
			payedRaffle
		):
		query = "INSERT INTO summaryMembersFallaYear \
			(memberFk, fallaYearFk, assignedFee, assignedLottery, assignedRaffle, payedFee, \
				payedLottery, payedRaffle) \
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
		data = id_member, falla_year, assignedFee, assignedLottery, assignedRaffle, payedFee, payedLottery, payedRaffle
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al insertar el resum anual del faller"
			)


	def insert_membership_history(self, falla_year, id_member):
		position = "vocal"
		falla = "Sants Patrons"
		query = "INSERT INTO membershipHistory (fallaYearFk, position, falla, memberFk) VALUES (%s, %s, %s, %s)"
		data = falla_year, position, falla, id_member
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al insertar el historial del faller"
			)


	def insert_lottery(
			self,
			lottery_name,
			falla_year,
			member,
			tickets_male,
			tickets_female,
			tickets_childish,
			tenths_male,
			tenths_female,
			tenths_childish,
			is_assigned
		):
		assigned = None
		query = "INSERT INTO lottery \
			(lotteryName, assigned, fallaYearFk, memberFk, ticketsMale, ticketsFemale, ticketsChildish, tenthsMale, tenthsFemale, tenthsChildish, isAssigned) \
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		data = lottery_name, assigned, falla_year, member, tickets_male, tickets_female, tickets_childish, tenths_male, tenths_female, tenths_childish, is_assigned
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error as e:
			messagebox.showerror(
				"Error",
				"Error al insertar el arxiu de loteria"
			)