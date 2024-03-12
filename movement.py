from database import Database
from datetime import date

class Movement():

	def __init__(self, id: int, transaction_date: date, amount: float, id_type: int, id_concept: int, falla_year: int,
			  	description: str, receipt_number: int):

		self.id = id
		self.transaction_date = transaction_date
		self.amount = amount
		self.id_type = id_type
		self.id_concept = id_concept
		self.falla_year = falla_year
		self.description = description
		self.receipt_number = receipt_number


	@classmethod
	def set_movement(cls, transaction_date, amount, id_type, id_concept, falla_year, description, receipt_number, id_member):
		db = Database('sp')
		db.insert_movement(transaction_date, amount, id_type, id_concept, falla_year, description, receipt_number, id_member)
		db.close_connection()