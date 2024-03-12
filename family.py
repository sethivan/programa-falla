from database import Database

class Family():

	def __init__(self, id: int, discount: float, is_direct_debited: bool, members_list: list = None):

		self.id = id
		self.discount = discount
		self.is_direct_debited = is_direct_debited
		self.members_list = members_list


	@classmethod
	def get_family(cls, id):
		db = Database('sp')
		if id == 0:
			family = db.select_last_family()
		else:
			family = db.select_family(id)
		db.close_connection()
		return family
	

	@classmethod
	def set_family(cls, discount, is_direct_debited):
		db = Database('sp')
		db.insert_family(discount, is_direct_debited)
		db.close_connection()


	def modify_family(self, id, discount, is_direct_debited):
		db = Database('sp')
		db.update_family(id, discount, is_direct_debited)
		db.close_connection()


	def calculate_discount(self, members_list):
		'''
		A partir del llistat de fallers d'una mateixa familia calculem el descompte segons els membres actius.

		Paràmetres:
		-----------
		llistat_fallers : llista
			Llistat de fallers que pertanyen a la mateixa familia.
		'''
		family_members = 0
		is_maximum_fee = False
		for member in members_list:
			if member.is_registered:
				family_members = family_members + 1
				if member.category.id == 1:
					is_maximum_fee = True
		if is_maximum_fee and family_members == 3:
			self.discount = 5
		elif is_maximum_fee and family_members >= 4:
			self.discount = 10
		else:
			self.discount = 0


	def calculate_family_members(self, members_list):
		family_members = 0
		for member in members_list:
			if member.isRegistered:
				family_members = family_members + 1
		return family_members
	

	def calcular_membres(self, llistat_fallers):
		'''
		A partir del llistat de fallers d'una mateixa familia calculem els membres actius.

		Paràmetres:
		-----------
		llistat_fallers : llista
			Llistat de fallers que pertanyen a la mateixa familia.

		Retorna:
        --------
        membres : int
            Membres actius de la familia.
		'''
		membres=0
		for faller in llistat_fallers:
			if faller.alta==1:
				membres=membres+1
		return membres


	def pay_fee(self, amount, members_list):
		for member in members_list:
			#quota_base=bd.llegir_quota_faller(faller.id)	ficar quota en la classe faller
			pass


	def pay_lottery(self, amount, members_list):
		pass


	def pay_raffle(self, amount, members_list):
		pass