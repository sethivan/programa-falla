'''
Proporciona la classe "Movement".
'''
from database import Database
from datetime import date

class Movement():
	'''
	Aquesta classe controla els atributs
	de la taula "movement" de la base de dades.

	Atributs:
	---------
	id : int
		El identificador a la taula "movement" de la base de dades.
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
	description : string
		Descripció del moviment.
	receipt_number : int
		Número de rebut.

	Mètodes:
	--------
	@classmethod set_movement(transaction_date, amount, id_type, id_concept,
		falla_year, description, receipt_number, id_member)
	'''
	def __init__(
		self,
		id: int,
		transaction_date: date,
		amount: float,
		id_type: int,
		id_concept: int,
		falla_year: int,
		description: str,
		receipt_number: int
	):
		'''
		Inicialitza una nova instància de la classe Movement.

		Paràmetres:
		-----------
		id : int
			El identificador a la taula "movement" de la base de dades.
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
		description : string
			Descripció del moviment.
		receipt_number : int
			Número de rebut.
		'''
		self.id = id
		self.transaction_date = transaction_date
		self.amount = amount
		self.id_type = id_type
		self.id_concept = id_concept
		self.falla_year = falla_year
		self.description = description
		self.receipt_number = receipt_number


	@classmethod
	def set_movement(
		cls,
		transaction_date,
		amount,
		id_type,
		id_concept,
		falla_year,
		description,
		receipt_number,
		id_member
	):
		'''
		Inserta a la taula movement un nou moviment amb els paràmetres passats.

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
		description : string
			Descripció del moviment.
		receipt_number : int
			Número de rebut.
		id_member : int
			Identificador del faller sobre el que es fa el moviment.
		'''
		db = Database('sp')
		db.insert_movement(
			transaction_date,
			amount,
			id_type,
			id_concept,
			falla_year,
			id_member,
			description,
			receipt_number
		)
		db.close_connection()