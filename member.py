from datetime import date, datetime

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


	def calculate_age(self, birthdate, falla_year):

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


	def calcular_edat(self, naixement, exercici):
		'''
		A partir de la data de naixement i l'exercici actual calculem l'edat del faller a data 19 de març del present exercici.

		Paràmetres:
		-----------
		naixement : string
			La data de naixement del faller.
		exercici : int
			L'exercici actual.
		
		Retorna:
        --------
        edat : int
            L'edat del faller a data 19 de març del present exercici.
		'''
		naixement_faller=date.strptime(naixement, '%d-%m-%Y')
		any_naixement=date.strftime(naixement_faller, '%Y')
		mes_naixement=date.strftime(naixement_faller, '%m')
		dia_naixement=date.strftime(naixement_faller, '%d')
		data_exercici=date.strptime(str(exercici), '%Y')
		any_exercici=date.strftime(data_exercici, '%Y')
		if int(mes_naixement)>3 or (int(mes_naixement)==3 and int(dia_naixement)>19):
			edat=int(any_exercici)-int(any_naixement)-1
		else:
			edat=int(any_exercici)-int(any_naixement)
		return edat
	

	def calculate_category(self, age):
		'''
		A partir de l'edat del faller assigna l'id de la categoria a la que pertany.

		Paràmetres:
		-----------
		edat : int
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
	

	def pay_fee(self, amount, receipt_number):
		Movement.insert_movement(amount, 2, 1, "quota", receipt_number, self.id)


	def pay_lottery(self, amount, receipt_number):
		Movement.insert_movement(amount, 2, 2, "loteria", receipt_number, self.id)


	def pay_raffle(self, amount, receipt_number):
		Movement.insert_movement(amount, 2, 3, "rifa", receipt_number, self.id)