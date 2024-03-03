class Family():

	def __init__(self, id: int, discount: float, is_direct_debited: bool, members_list: list = None):

		self.id = id
		self.discount = discount
		self.is_direct_debited = is_direct_debited
		self.members_list = members_list


	def calculate_discount(self, members_list):
		family_members = 0
		is_maximum_fee = False
		for member in members_list:
			if member.isRegistered:
				family_members = family_members + 1
				if member.category.id == 1:
					is_maximum_fee = True
		if is_maximum_fee and family_members == 3:
			self.discount = 5
		elif is_maximum_fee and family_members >= 4:
			self.discount = 10
		else:
			self.discount = 0

	
	def calcular_descompte(self, llistat_fallers):
		'''
		A partir del llistat de fallers d'una mateixa familia calculem el descompte segons els membres actius.

		Paràmetres:
		-----------
		llistat_fallers : llista
			Llistat de fallers que pertanyen a la mateixa familia.
		'''
		membres=0
		maxima=False
		for faller in llistat_fallers:
			if faller.alta==1:
				membres=membres+1
				if faller.category.id==1:
					maxima=True
		if maxima==True and membres==3:
			self.descompte=5
		elif maxima==True and membres>=4:
			self.descompte=10
		else:
			self.descompte=0


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