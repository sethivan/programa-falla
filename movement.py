from database import Database
from datetime import date

from member import Member

class Movement():

	def __init__(self, id: int, transaction_date: date, amount: float, id_type: int, id_concept: int, falla_year: int,
			  	description: str, receipt_number: int, member: Member = None):

		self.id = id
		self.transaction_date = transaction_date
		self.amount = amount
		self.id_type = id_type
		self.id_concept = id_concept
		self.falla_year = falla_year
		self.description = description
		self.receipt_number = receipt_number
		self.member = member


	@classmethod
	def insert_movement(cls, amount, id_type, id_concept, description, receipt_number, id_member):
		db = Database('sp')
		db.insert_movement(amount, id_type, id_concept, description, receipt_number, id_member)
		db.close_connection()