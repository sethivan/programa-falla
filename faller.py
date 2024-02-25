from datetime import datetime

class Faller():

	def __init__(self, id, nom, cognoms, naixement, sexe, dni, adresa, telefon, alta, correu, familia=None, category=None):

		self.id=id
		self.nom=nom
		self.cognoms=cognoms
		self.naixement=naixement
		self.sexe=sexe
		self.dni=dni
		self.adresa=adresa
		self.telefon=telefon
		self.alta=alta
		self.correu=correu
		self.familia=familia
		self.category=category


	@property
	def id(self):

		return self._id
	

	@id.setter
	def id(self, value):
		
		self._id=value


	@property
	def nom(self):

		return self._nom
	

	@nom.setter
	def nom(self, value):
		
		self._nom=value


	@property
	def cognoms(self):

		return self._cognoms
	

	@cognoms.setter
	def cognoms(self, value):
		
		self._cognoms=value


	@property
	def naixement(self):

		return self._naixement
	

	@naixement.setter
	def naixement(self, value):
		
		self._naixement=value


	@property
	def sexe(self):

		return self._sexe
	

	@sexe.setter
	def sexe(self, value):
		
		self._sexe=value


	@property
	def dni(self):

		return self._dni
	

	@dni.setter
	def dni(self, value):
		
		self._dni=value


	@property
	def adresa(self):

		return self._adresa
	

	@adresa.setter
	def adresa(self, value):
		
		self._adresa=value


	@property
	def telefon(self):

		return self._telefon
	

	@telefon.setter
	def telefon(self, value):
		
		self._telefon=value


	@property
	def alta(self):

		return self._alta
	

	@alta.setter
	def alta(self, value):
		
		self._alta=value


	@property
	def correu(self):

		return self._correu
	

	@correu.setter
	def correu(self, value):
		
		self._correu=value


	@property
	def familia(self):

		return self._familia
	

	@familia.setter
	def familia(self, value):
		
		self._familia=value


	@property
	def category(self):

		return self._category
	

	@category.setter
	def category(self, value):
		
		self._category=value


	def calcular_edat(self, naixement, exercici):
		'''
		A partir de la data de naixement i l'exercici actual calculem l'edat del faller a data 19 de març del present exercici.

		Paràmetres:
		-----------
		naixement : string
			La data de naixement del faller.
		exercici : int
			L'exercici actual.
		
		Retorna:
        --------
        edat : int
            L'edat del faller a data 19 de març del present exercici.
		'''
		naixement_faller=datetime.strptime(naixement, '%d-%m-%Y')
		any_naixement=datetime.strftime(naixement_faller, '%Y')
		mes_naixement=datetime.strftime(naixement_faller, '%m')
		dia_naixement=datetime.strftime(naixement_faller, '%d')
		data_exercici=datetime.strptime(str(exercici), '%Y')
		any_exercici=datetime.strftime(data_exercici, '%Y')
		if int(mes_naixement)>3 or (int(mes_naixement)==3 and int(dia_naixement)>19):
			edat=int(any_exercici)-int(any_naixement)-1
		else:
			edat=int(any_exercici)-int(any_naixement)
		return edat
	

	def calculate_category(self, age):
		'''
		A partir de l'edat del faller assigna l'id de la categoria a la que pertany.

		Paràmetres:
		-----------
		edat : int
			L'edat del faller a data 19 de març del present exercici.
		'''
		if age<5:
			category_id=5
		elif 5<=age<=9:
			category_id=4
		elif 10<=age<=13:
			category_id=3
		elif 14<=age<=17:
			category_id=2
		else:
			category_id=1
		return category_id
	

	def calcular_primer_exercici(self, naixement):
		'''
		A partir de la data de naixement calculem quin podria haver segut el seu primer exercici.

		Paràmetres:
		-----------
		naixement : string
			La data de naixement del faller.
		
		Retorna:
        --------
        exercici : int
            Primer possible exercici del faller.
		'''
		naixement_faller=datetime.strptime(naixement, '%d-%m-%Y')
		any_naixement=datetime.strftime(naixement_faller,'%Y')
		mes_naixement=datetime.strftime(naixement_faller, '%m')
		dia_naixement=datetime.strftime(naixement_faller, '%d')
		if int(mes_naixement)>3 or (int(mes_naixement)==3 and int(dia_naixement)>19):
			exercici=int(any_naixement)+1
		else:
			exercici=int(any_naixement)
		return exercici