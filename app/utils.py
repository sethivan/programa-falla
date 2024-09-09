'''
Proporciona la classe "Utils".
'''
from datetime import datetime
import tkinter.ttk as ttk


class Utils():
	'''
	Aquesta classe controla els estils de l'aplicació i les operacions amb dates.
	'''

	
	def define_global_style(self):
		'''
		Definició dels estils per als widgets ttk de la finestra.
		'''
		self.estil=ttk.Style()
		self.estil.theme_use('clam')
		self.estil.configure(".", font=("Ubuntu", 10))
		self.estil.configure(
			"Marc.TFrame", background="#ffffff", relief="groove"
		)
		self.estil.configure(
			"Titol.TLabel",
			background="#ffffff",
			foreground="#e95420",
			font=("Ubuntu", 11)
		)
		self.estil.configure(
			"Portada.TLabel",
			background="#ffffff",
			foreground="#e95420",
			font=("Ubuntu", 40)
		)
		self.estil.configure("Etiqueta.TLabel", background="#ffffff")
		self.estil.map("Entrada.TEntry", foreground=[('disabled','black')])
		self.estil.configure("Check.TCheckbutton", background="#ffffff")
		self.estil.map(
			"Check.TCheckbutton", background=[('disabled', '#eae9e7')]
		)
		self.estil.configure("Radio.TRadiobutton", background="#ffffff")
		self.estil.map(
			"Radio.TRadiobutton",
			background=[('active', '#e95420')],
			foreground=[('active', '#ffffff')]
		)
		self.estil.configure(
			"Boto.TButton",
			background="#ffffff",
			foreground="#000000",
			font=("Ubuntu", 11)
		)
		self.estil.map(
			"Boto.TButton",
			background=[('active', '#e95420')],
			foreground=[('active', '#ffffff'), ('disabled', '#aea79f')]
		)


	def convert_to_mariadb_date(self, spanish_date):
		'''
		Converteix la data en format espanyol a format mariaDb.

		Paràmetres:
		-----------
		spanish_date : string
			Data en format espanyol.

		Retorna:
		--------
		mariadb_date : date
			Data en format anglés.
		'''
		date = datetime.strptime(spanish_date, '%d-%m-%Y')
		mariadb_date = date.strftime('%Y-%m-%d')
		return mariadb_date


	def convert_to_spanish_date(self, english_date):
		'''
		Converteix la data en format mariaDb a format espanyol.

		Paràmetres:
		-----------
		mariadb_date : date
			Data en format anglés.

		Retorna:
		--------
		spanish_date : string
			Data en format espanyol.
		'''
		spanish_date = english_date.strftime('%d-%m-%Y')
		return spanish_date
	

	def calculate_current_date(self):
		'''
		Llegim la data actual del sistema i la tornem en format llista.

		Retorna:
		--------
		current_date : list
			Llistat amb el dia, mes i any actuals.
		'''
		date = datetime.now()
		current_year = datetime.strftime(date, '%Y')
		current_month = datetime.strftime(date, '%m')
		current_day = datetime.strftime(date, '%d')
		current_date = []
		current_date.append(current_day)
		current_date.append(current_month)
		current_date.append(current_year)
		return current_date

