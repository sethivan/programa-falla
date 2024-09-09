'''
Proporciona la classe "Category".
'''
from database import Database


class Category():
	'''
	Aquesta classe controla els atributs
	de la taula "category" de la base de dades.

	Atributs:
	---------
	id : int
		El identificador a la taula "category" de la base de dades.
	fee : float
		Quantitat a pagar corresponent a dita categoria.
	name : string
		Forma amb la que es nombra dita categoria.
	description : string
		Informació sobre les edats a les quals correspon la categoria.

	Mètodes:
	--------
	@classmethod get_category(id): list
	modify_category(id, fee, name, description)
	'''

	
	def __init__(self, id: int, fee: float, name: str, description: str):
		'''
		Inicialitza una nova instància de la classe Category.

		Paràmetres:
		-----------
		id : int
			El identificador a la taula "category" de la base de dades.
		fee : float
			Quantitat a pagar corresponent a dita categoria.
		name : string
			Forma amb la que es nombra dita categoria.
		description : string
			Informació sobre les edats a les quals correspon la categoria.
		'''
		self.id = id
		self.fee = fee
		self.name = name
		self.description = description


	@classmethod
	def get_category(cls, id):
		'''
		Recupera les dades de la categoria i les retorna en forma de llista.

		Paràmetres:
		-----------
		id : int
			El identificador de la categoria.

		Retorna:
		--------
		category : list
			Llista amb totes les dades de la categoria.
		'''
		db = Database('sp')
		category = db.select_category(id)
		db.close_connection()
		return category
	

	def modify_category(self, id, fee, name, description):
		'''
		Modifica les dades de la categoria.

		Paràmetres:
		-----------
		id : int
			El identificador a la taula "category" de la base de dades.
		fee : float
			Quantitat a pagar corresponent a dita categoria.
		name : string
			Forma amb la que es nombra dita categoria.
		description : string
			Informació sobre les edats a les quals correspon la categoria.
		'''
		db = Database('sp')
		db.update_category(id, fee, name, description)
		db.close_connection()
