'''
Proporciona la classe "Categoria".
'''
class Categoria():
	'''
	Aquesta classe controla els atributs de la taula "categoria" de la base de dades.

	Atributs:
	---------
	id : int
		El identificador a la taula "categoria" de la base de dades.
	quota : float
		Quantitat a pagar corresponent a dita categoria.
	nom : string
		Forma amb la que es nombra dita categoria.
	descripcio : string
		Informació curta sobre les edats a les quals correspon la categoria.
	'''

	
	def __init__(self, id, quota, nom, descripcio):
		'''
		Inicialitza una nova instància de la classe Categoria.

		Paràmetres:
		-----------
		id : int
			El identificador a la taula "categoria" de la base de dades.
		quota : float
			Quantitat a pagar corresponent a dita categoria.
		nom : string
			Forma amb la que es nombra dita categoria.
		descripcio : string
			Informació curta sobre les edats a les quals correspon la categoria.
		'''
		self.id=id
		self.quota=quota
		self.nom=nom
		self.descripcio=descripcio

	
	# Getters i setters
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
		'''
		A partir de l'edat del faller assigna l'id de la categoria a la que pertany.

		Paràmetres:
		-----------
		edat : int
			L'edat del faller a data 19 de març del present exercici.
		'''
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