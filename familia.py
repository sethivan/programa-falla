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

		membres=0
		maxima=False
		for faller in llistat_fallers:
			if faller.alta==1:
				membres=membres+1
				if faller.categoria.id==1:
					maxima=True
		if maxima==True and membres==3:
			self.descompte=5
		elif maxima==True and membres>=4:
			self.descompte=10
		else:
			self.descompte=0