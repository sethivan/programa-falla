from datetime import date, datetime

from database import Database

from member import Member

class Lottery():

	def __init__(
		self,
		id: int,
		lottery_id: int,
		lottery_name: str,
		assignment_date: date,
		falla_year: int,
		tickets_male: int,
		tickets_female: int,
		tickets_childish: int,
		tenths_male: int,
		tenths_female: int,
		tenths_childish: int,
		assigned: bool,
		price: float = 0,
		benefit: float = 0,
		member: Member = None
	):
		self.id = id
		self.lottery_id = lottery_id
		self.lottery_name = lottery_name
		self.assignment_date = assignment_date
		self.falla_year = falla_year
		self.tickets_male = tickets_male
		self.tickets_female = tickets_female
		self.tickets_childish = tickets_childish
		self.tenths_male = tenths_male
		self.tenths_female = tenths_female
		self.tenths_childish = tenths_childish
		self.assigned = assigned
		self.price = price,
		self.benefit = benefit,
		self.member = member

	#borrable si no es gasta al final
	@classmethod
	def get_last_id(cls, lottery_name, falla_year):
		db = Database('sp')
		lottery_id = db.select_last_lottery_id(lottery_name, falla_year)
		return lottery_id
	

	@classmethod
	def set_lottery(
		cls,
		lottery_id,
		lottery_name,
		falla_year,
		tickets_male,
		tickets_female,
		tickets_childish,
		tenths_male,
		tenths_female,
		tenths_childish,
		assigned,
		id_member
	):
		db = Database('sp')
		db.insert_lottery(
			lottery_id,
			lottery_name,
			falla_year,
			tickets_male,
			tickets_female,
			tickets_childish,
			tenths_male,
			tenths_female,
			tenths_childish,
			assigned,
			id_member
		)
		db.close_connection()
