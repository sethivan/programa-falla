class Categoria():

	def __init__(self, id, quota, nom, descripcio):

		self.id=id
		self.quota=quota
		self.nom=nom
		self.descripcio=descripcio


	@property
	def id(self):

		return self._id
	

	@id.setter
	def id(self, value):
		
		self._id=value
	

	@property
	def quota(self):

		return self._quota
	

	@quota.setter
	def quota(self, value):
		
		self._quota=value
	

	@property
	def nom(self):

		return self._nom
	

	@nom.setter
	def nom(self, value):
		
		self._nom=value
	

	@property
	def descripcio(self):

		return self._descripcio
	

	@descripcio.setter
	def descripcio(self, value):
		
		self._descripcio=value
	


	def calcular_categoria(self, edat):

		if edat<5:
			self.id=5
		elif 5<=edat<=9:
			self.id=4
		elif 10<=edat<=13:
			self.id=3
		elif 14<=edat<=17:
			self.id=2
		else:
			self.id=1