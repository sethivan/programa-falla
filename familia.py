class Familia():

	def __init__(self, id, descompte, domiciliacio):

		self.id=id
		self.descompte=descompte
		self.domiciliacio=domiciliacio


	@property
	def id(self):

		return self._id
	

	@id.setter
	def id(self, value):
		
		self._id=value


	@property
	def descompte(self):

		return self._descompte
	

	@descompte.setter
	def descompte(self, value):
		
		self._descompte=value


	@property
	def domiciliacio(self):

		return self._domiciliacio
	

	@domiciliacio.setter
	def domiciliacio(self, value):
		
		self._domiciliacio=value

	
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
