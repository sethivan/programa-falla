class Moviment():

	def __init__(self, id, data, quantitat, tipo, concepte, exercici, descripcio, rebut, faller=None):

		self.id=id
		self.data=data
		self.quantitat=quantitat
		self.tipo=tipo
		self.concepte=concepte
		self.exercici=exercici
		self.descripcio=descripcio
		self.rebut=rebut
		self.faller=faller


	@property
	def id(self):

		return self._id
	

	@id.setter
	def id(self, value):
		
		self._id=value


	@property
	def data(self):

		return self._data
	

	@data.setter
	def data(self, value):
		
		self._data=value
	

	@property
	def quantitat(self):

		return self._quantitat
	

	@quantitat.setter
	def quantitat(self, value):
		
		self._quantitat=value


	@property
	def tipo(self):

		return self._tipo
	

	@tipo.setter
	def tipo(self, value):
		
		self._tipo=value


	@property
	def concepte(self):

		return self._concepte
	

	@concepte.setter
	def concepte(self, value):
		
		self._concepte=value


	@property
	def exercici(self):

		return self._exercici
	

	@exercici.setter
	def exercici(self, value):
		
		self._exercici=value


	@property
	def descripcio(self):

		return self._descripcio
	

	@descripcio.setter
	def descripcio(self, value):
		
		self._descripcio=value


	@property
	def rebut(self):

		return self._rebut
	

	@rebut.setter
	def rebut(self, value):
		
		self._rebut=value


	@property
	def faller(self):

		return self._faller
	

	@faller.setter
	def faller(self, value):
		
		self._faller=value