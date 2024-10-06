from datetime import date, datetime

from member import Member

class Lottery():

	def __init__(
		self,
		id: int,
		lottery_name: str,
		assignment_date: date,
		tickets_male: int,
		tickets_female: int,
		tickets_childish: int,
		tenths_male: int,
		tenths_female: int,
		tenths_childish: int,
		assigned: bool,
		member: Member = None
	):
		self.id = id
		self.lottery_name = lottery_name
		self.assignment_date = assignment_date
		self.tickets_male = tickets_male
		self.tickets_female = tickets_female
		self.tickets_childish = tickets_childish
		self.tenths_male = tenths_male
		self.tenths_female = tenths_female
		self.tenths_childish = tenths_childish
		self.assigned = assigned
		self.member = member


	'''
	fet com a columna virtual a la taula lottery
	def calculate_price(self):
		price = (self.tickets_male * 4) + (self.tickets_female * 4) + (self.tickets_childish * 4) + (self.tenths_male * 20) + (self.tenths_female * 20) + (self.tenths_childish * 20)
		return price
	

	def calcular_benefici(self):
		benefit = self.tickets_male + self.tickets_female + self.tickets_childish + (self.tenths_male * 3) + (self.tenths_female * 3) + (self.tenths_childish * 3)
		return benefit'''