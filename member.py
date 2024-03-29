from datetime import date, datetime

from database import Database

from family import Family
from category import Category
from movement import Movement

class Member():

	def __init__(self, id: int, name: str, surname: str, birthdate: date, gender: int, dni: str, address: str, phone_number: str,
			  	is_registered: bool, email: str, family: Family = None, category: Category = None):

		self.id = id
		self.name = name
		self.surname = surname
		self.birthdate = birthdate
		self.gender = gender
		self.dni = dni
		self.address = address
		self.phone_number = phone_number
		self.is_registered = is_registered
		self.email = email
		self.family = family
		self.category = category
		self.membership_history = {}


	@classmethod
	def get_member(cls, id):
		db = Database('sp')
		if id == 0:
			member = db.select_last_member()
		else:
			member = db.select_member(id)
		db.close_connection()
		return member


	@classmethod
	def set_member(cls, name, surname, birthdate, gender, dni, address, phone_number, is_registered, email, id_family, id_category):
		db = Database('sp')
		db.insert_member(name, surname, birthdate, gender, dni, address, phone_number, is_registered, email, id_family, id_category)
		db.close_connection()


	def modify_member(self, id, name, surname, birthdate, gender, dni, address, phone_number, is_registered, email, id_family, id_category):
		db = Database('sp')
		db.update_member(id, name, surname, birthdate, gender, dni, address, phone_number, is_registered, email, id_family, id_category)
		db.close_connection()


	def get_membership_history(self, id):
		db = Database('sp')
		result = db.select_membership_history(id)
		db.close_connection()
		for value in result:
			self.membership_history[value[1]] = [value[2], value[3]]


	@classmethod
	def calculate_age(cls, birthdate, falla_year):
		'''
		A partir de la data de naixement i l'exercici actual calculem l'edat del faller a data 19 de març del present exercici.

		Paràmetres:
		-----------
		birthdate : string
			La data de naixement del faller.
		falla_year : int
			L'exercici actual.
		
		Retorna:
        --------
        age : int
            L'edat del faller a data 19 de març del present exercici.
		'''
		birthdate=datetime.strptime(birthdate, '%d-%m-%Y')
		year = date.strftime(birthdate, '%Y')
		month = date.strftime(birthdate, '%m')
		day = date.strftime(birthdate, '%d')
		falla_year = datetime.strptime(str(falla_year), '%Y')
		falla_year = date.strftime(falla_year, '%Y')
		if int(month) > 3 or (int(month) == 3 and int(day) > 19):
			age = int(falla_year) - int(year) - 1
		else:
			age = int(falla_year) - int(year)
		return age
	

	@classmethod
	def calculate_category(cls, age):
		'''
		A partir de l'edat del faller assigna l'id de la categoria a la que pertany.

		Paràmetres:
		-----------
		age : int
			L'edat del faller a data 19 de març del present exercici.
		'''
		if age<5:
			category_id=5
		elif 5<=age<=9:
			category_id=4
		elif 10<=age<=13:
			category_id=3
		elif 14<=age<=17:
			category_id=2
		else:
			category_id=1
		return category_id
	

	def calcular_primer_exercici(self, naixement):
		'''
		A partir de la data de naixement calculem quin podria haver segut el seu primer exercici.

		Paràmetres:
		-----------
		naixement : string
			La data de naixement del faller.
		
		Retorna:
        --------
        exercici : int
            Primer possible exercici del faller.
		'''
		naixement_faller=date.strptime(naixement, '%d-%m-%Y')
		any_naixement=date.strftime(naixement_faller,'%Y')
		mes_naixement=date.strftime(naixement_faller, '%m')
		dia_naixement=date.strftime(naixement_faller, '%d')
		if int(mes_naixement)>3 or (int(mes_naixement)==3 and int(dia_naixement)>19):
			exercici=int(any_naixement)+1
		else:
			exercici=int(any_naixement)
		return exercici
	

	def calculate_first_falla_year(self, birthdate):
		year = date.strftime(birthdate, '%Y')
		month = date.strftime(birthdate, '%m')
		day = date.strftime(birthdate, '%d')
		if int(month) > 3 or (int(month) == 3 and int(day) > 19):
			first_falla_year = int(year) + 1
		else:
			first_falla_year = int(year)
		return first_falla_year
	

	def pay_fee(self, transaction_date, amount, falla_year, description, receipt_number, id_member):
		Movement.set_movement(transaction_date, amount, 2, 1, falla_year, description, receipt_number, id_member)


	def pay_lottery(self, transaction_date, amount, falla_year, description, receipt_number, id_member):
		Movement.set_movement(transaction_date, amount, 2, 2, falla_year, description, receipt_number, id_member)


	def pay_raffle(self, transaction_date, amount, falla_year, description, receipt_number, id_member):
		Movement.set_movement(transaction_date, amount, 2, 3, falla_year, description, receipt_number, id_member)