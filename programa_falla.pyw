'''

PROGRAMA FALLA SANTS PATRONS

Programa de gestió de l'oficina de la Falla Sants Patrons d'Alzira.
Control de fallers, families, quotes, pagaments, rifes, loteries, historials, etc.

Desenvolupat per Ivan Mas Presentación 2020.

'''

import tkinter as tk
from tkinter import messagebox
import os

from finestra_introduir import FinestraIntroduir
from finestra_gestionar import FinestraGestionar
from finestra_historial import FinestraHistorial

from arxiu import Arxiu
from utils import Utils
from base_de_dades import BaseDeDades

from falla import Falla


class Aplicacio(tk.Frame):
	"""
    Aquesta classe representa l'aplicació principal de la interfície gràfica d'usuari.

    Atributs:
    ---------
    master : tk.Tk
        La instància principal de l'aplicació.
    """
		
		
	def __init__(self, master=None):
		"""
        Inicialitza una nova instància de la classe Aplicacio.

        Paràmetres:
        -----------
        master : tk.Tk, opcional
            La instància principal de l'aplicació. Si no es proporciona,
			es crearà una nova instància de tk.Tk().
        """
		super().__init__(master) # Heretem de la classe Frame.
		self.master=master
		self.master.state('zoomed') # La finestra s'obri maximitzada.
		self.master.title("Falla Sants Patrons")
		self.master.iconbitmap("escut.ico")
		self.pack()
		
		# Barra de menú.
		self.barraMenu=tk.Menu() # Guardem el menú en una variable.
		self.master.config(menu=self.barraMenu) # Construïm el menú.

		# Submenú Arxiu.
		self.arxiuMenu=tk.Menu(self.barraMenu, tearoff=0) # Creem els elements i subelements.
		self.arxiuMenu.add_command(label="Eixir", command=self.eixir)

		# Submenú Faller.
		self.fallerMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.fallerMenu.add_command(label="Gestionar", command=self.gestionar, accelerator="Ctrl+G")
		# Bindegem el submenú "Gestionar".
		self.master.bind_all("<Control-g>", self.EventGestionar)
		self.fallerMenu.add_command(label="Introduir", command=self.introduir, accelerator="Ctrl+I")
		self.master.bind_all("<Control-i>", self.event_introduir) # Bindegem el submenú "Introduir".

		# Submenú Loteria.
		self.loteriaMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.loteriaMenu.add_command(label="Assignar", command=self.AssignarLoteria)

		# Submenú Rifa.
		self.rifaMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.rifaMenu.add_command(label="Assignar", command=self.assignar_rifa)

		# Submenú Historial.
		self.historialMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.historialMenu.add_command(label="Modificar", command=self.modificar_historial)
		self.historialMenu.add_command(label="Borrar", command=self.borrar_historial)

		# Submenú Llistats.
		self.llistatsMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.llistatsMenu.add_command(label="Moviments", command=self.MovimentsDia)
		self.llistatsMenu.add_command(label="General", command=self.LlistatGeneral)
		self.llistatsMenu.add_command(label="Fallers", command=self.LlistatFallers)
		self.llistatsMenu.add_command(label="Altes i Baixes", command=self.LlistatAltesBaixes)
		self.llistatsMenu.add_command(label="Rifes", command=self.LlistatRifes)

		# Submenú Exercici.
		self.exerciciMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.exerciciMenu.add_command(label="Nou", command=self.nou_exercici)

		# Submenú Ajuda.
		self.ajudaMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.ajudaMenu.add_command(label="Info", command=self.info)

		# Afegim tots els submenús a la barra.
		self.barraMenu.add_cascade(label="Arxiu", menu=self.arxiuMenu)
		self.barraMenu.add_cascade(label="Faller", menu=self.fallerMenu)
		self.barraMenu.add_cascade(label="Loteria", menu=self.loteriaMenu)
		self.barraMenu.add_cascade(label="Rifa", menu=self.rifaMenu)
		self.barraMenu.add_cascade(label="Historial", menu=self.historialMenu)
		self.barraMenu.add_cascade(label="Llistats", menu=self.llistatsMenu)
		self.barraMenu.add_cascade(label="Exercici", menu=self.exerciciMenu)
		self.barraMenu.add_cascade(label="Ajuda", menu=self.ajudaMenu)

		# Comprovació que s'efectua cada vegada que es fica en marxa el programa.
		self.arrancar()


	def arrancar(self):
		'''
		Comprova si existeixen els arxius necessaris per a que funcione el programa i en cas de que falten, els crea.
		Si es crea algún arxiu, avisa a l'usuari de que ho ha fet per a que prenga les mesures necessàries.
		'''
		if not os.path.exists("exercici"):
			llista=[]
			arxiu=Arxiu("exercici")
			utils=Utils()
			data_actual=utils.calcular_data_actual()
			dia_actual=int(data_actual[0])
			mes_actual=int(data_actual[1])
			any_actual=int(data_actual[2])
			if mes_actual>3:
				any_exercici=any_actual+1
			elif mes_actual<2:
				any_exercici=any_actual
			elif mes_actual==3 and dia_actual>19:
				any_exercici=any_actual+1
			elif mes_actual==3 and dia_actual<=19:
				any_exercici=any_actual
			llista.append(any_exercici)
			arxiu.modificar_exercici_actual(llista)
			messagebox.showwarning("Avís", "No hi havia cap arxiu amb l'informació de l'exercici i s'ha creat un nou")
		if not os.path.exists("falla.db"):
			bd=BaseDeDades("falla.db")
			bd.crear_taules()
			bd.tancar_conexio()
			messagebox.showwarning("Avís", "No hi havia cap base de dades del programa i s'ha creat una nova")
	
	
	def gestionar(self):
		''' 
		Crea una nova instància de la classe FinestraGestionar
		que obri la finestra "Gestionar" del menú "Faller".
		'''
		gestionar=FinestraGestionar(self)
		gestionar.iniciar()


	def EventGestionar(self, event):
		'''
		Bindeig del submenú "Gestionar".
		'''
		self.gestionar()
	

	def introduir(self):
		''' 
		Crea una nova instància de la classe FinestraIntroduir
		que obri la finestra "Introduir" del menú "Faller".
		'''
		introduir = FinestraIntroduir(self)
		introduir.iniciar()

	
	def event_introduir(self, event):
		'''
		Bindeig del submenú "Introduir".
		'''
		self.introduir()


	def AssignarLoteria(self): #funció que obre la finestra "Assignar" del menú "Loteria"

		#FinestraAssignar(self.root)
		pass


	def assignar_rifa(self):
		'''
		Crea una nova instància de la classe Falla per que assigne la rifa corresponent als fallers.
		'''
		falla=Falla()
		falla.assignar_rifa_auto()


	def modificar_historial(self):
		''' 
		Crea una nova instància de la classe FinestraHistorial
		que obri la finestra "Modificar" del menú "Historial".
		'''
		historial = FinestraHistorial(self)
		historial.iniciar()


	def borrar_historial(self):
		'''
		Crea una nova instància e la classe Falla per que borre l'historial de tots els fallers.
		'''
		falla=Falla()
		falla.borrar_historial()


	def MovimentsDia(self): #funció per a traure el llistat en pdf dels moviments del dia

		#elInforme=Informe()
		#elInforme.MovimentsDia()
		pass


	def LlistatGeneral(self): #funció per a traure el llistat en pdf dels comptes actualitzats dels fallers

		#elInforme=Informe()
		#elInforme.LlistatGeneral()
		pass


	def LlistatFallers(self): #funció per a traure el llistat en pdf dels fallers amb les seues dades

		#elInforme=Informe()
		#elInforme.LlistatFallers()
		pass


	def LlistatAltesBaixes(self): #funció per a traure el llistat en pdf de les altes i baixes de fallers respecte a l'exercici anterior

		#elInforme=Informe()
		#elInforme.LlistatAltesBaixes()
		pass


	def LlistatRifes(self): #funció per a traure el llistat en pdf d'aquells fallers a qui els correpon rifa

		#elInforme=Informe()
		#elInforme.FallersAmbRifa()
		pass
		

	def nou_exercici(self): #funció per a crear un nou exercici faller
		'''
		Crea una nova instància de la classe Falla per a que cree un exercici nou.
		'''
		falla=Falla()
		falla.nou_exercici()

	
	def eixir(self):
		'''
		Tanca la finestra principal de l'aplicació.
		'''
		valor=messagebox.askquestion("Eixir","Vols eixir de l'aplicació?")
		if valor=="yes":
			self.master.destroy()


	def info(self):
		'''
		Mostra una finestra emergent amb informació del programa.
		'''
		messagebox.showinfo("Informació","Aplicació creada per Ivan Mas")


if __name__=='__main__':
	'''
	Inicia l'aplicació.
	'''
	root=tk.Tk()
	app=Aplicacio(root)
	app.mainloop()