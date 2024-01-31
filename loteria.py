class Loteria():

	def __init__(self, id, sorteig, data, paperetes_masculina, paperetes_femenina, paperetes_infantil,
			decims_masculina, decims_femenina, decims_infantil, assignada, faller=None):

		self.id=id
		self.sorteig=sorteig
		self.data=data
		self.paperetes_masculina=paperetes_masculina
		self.paperetes_femenina=paperetes_femenina
		self.paperetes_infantil=paperetes_infantil
		self.decims_masculina=decims_masculina
		self.decims_femenina=decims_femenina
		self.decims_infantil=decims_infantil
		self.assignada=assignada
		self.faller=faller


	def calcular_diners(self):
		diners=(self.paperetes_masculina*4)+(self.paperetes_femenina*4)+(self.paperetes_infantil*4)+(self.decims_masculina*20)+(self.decims_femenina*20)+(self.decims_infantil*20)
		return diners
	

	def calcular_benefici(self):
		benefici=self.paperetes_masculina+self.paperetes_femenina+self.paperetes_infantil+(self.decims_masculina*3)+(self.decims_femenina*3)+(self.decims_infantil*3)
		return benefici