################################
# PROGRAMA FALLA SANTS PATRONS #
################################

# Programa per a la gestió de la oficina de la Falla Sants Patrons d'Alzira.
# Control de fallers, families, edats, quotes, pagaments, rifes, loteries, historials, etc.
# Desenvolupat per Ivan Mas Presentación 2020


import tkinter as tk #importem les llibreries gràfiques
from tkinter import messagebox #importem el sistema de missatges emergents
from faller import *
from moviment import *
#from gestionar import *
#from introduir import *
#from assignar import *
#from informe import *
#from historial import *
#import pickle


class Aplicacio(tk.Frame):

		
	def __init__(self, master=None): #el constructor construeix la finestra d'aplicació

		super().__init__(master) #heretem de la classe Frame
		self.master=master
		self.master.state('zoomed') #la finestra s'obri maximitzada
		self.master.title("Falla Sants Patrons")
		self.master.iconbitmap("escut.ico")
		self.pack()
		
		# MENÚ #

		self.barraMenu=tk.Menu() #guardem el menú en una variable
		self.master.config(menu=self.barraMenu) #construïm el menú

		#submenú arxiu
		self.arxiuMenu=tk.Menu(self.barraMenu, tearoff=0) #creem els diferents elements i subelements
		self.arxiuMenu.add_command(label="Eixir", command=self.Eixir)

		#submenú faller
		self.fallerMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.fallerMenu.add_command(label="Gestionar", command=self.Gestionar, accelerator="Ctrl+G")
		self.master.bind_all("<Control-g>", self.EventGestionar) #bindegem el submenú "Gestionar"
		self.fallerMenu.add_command(label="Introduir", command=self.Introduir, accelerator="Ctrl+I")
		self.master.bind_all("<Control-i>", self.EventIntroduir) #bindegem el submenú "Introduir"

		#submenú loteria
		self.loteriaMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.loteriaMenu.add_command(label="Assignar", command=self.AssignarLoteria)

		#submenú rifa
		self.rifaMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.rifaMenu.add_command(label="Assignar", command=self.AssignarRifa)

		#submenú historial
		self.historialMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.historialMenu.add_command(label="Modificar", command=self.ModificarHistorial)

		#submenú llistats
		self.llistatsMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.llistatsMenu.add_command(label="Moviments", command=self.MovimentsDia)
		self.llistatsMenu.add_command(label="General", command=self.LlistatGeneral)
		self.llistatsMenu.add_command(label="Fallers", command=self.LlistatFallers)
		self.llistatsMenu.add_command(label="Altes i Baixes", command=self.LlistatAltesBaixes)
		self.llistatsMenu.add_command(label="Rifes", command=self.LlistatRifes)

		#submenú exercici
		self.exerciciMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.exerciciMenu.add_command(label="Nou", command=self.NouExercici)

		#submenú ajuda
		self.ajudaMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.ajudaMenu.add_command(label="Info", command=self.Info)

		#afegim tots els submenús a la barra
		self.barraMenu.add_cascade(label="Arxiu", menu=self.arxiuMenu)
		self.barraMenu.add_cascade(label="Faller", menu=self.fallerMenu)
		self.barraMenu.add_cascade(label="Loteria", menu=self.loteriaMenu)
		self.barraMenu.add_cascade(label="Rifa", menu=self.rifaMenu)
		self.barraMenu.add_cascade(label="Historial", menu=self.historialMenu)
		self.barraMenu.add_cascade(label="Llistats", menu=self.llistatsMenu)
		self.barraMenu.add_cascade(label="Exercici", menu=self.exerciciMenu)
		self.barraMenu.add_cascade(label="Ajuda", menu=self.ajudaMenu)
	
	
	def Gestionar(self): #funció que obre la finestra "Gestionar" del menú "Faller"

		#FinestraGestionar(self.root)
		pass


	def EventGestionar(self, event): #funció per al bindeig del submenú "Gestionar"

		self.Gestionar()
	

	def Introduir(self): #funció que obre la finestra "Introduir" del menú "Faller"

		#FinestraIntroduir(self.root)
		pass

	
	def EventIntroduir(self, event): #funció per al bindeig del submenú "Introduir"

		self.Introduir()


	def AssignarLoteria(self): #funció que obre la finestra "Assignar" del menú "Loteria"

		#FinestraAssignar(self.root)
		pass


	def AssignarRifa(self): #funció per a assignar la rifa corresponent als fallers

		valor=messagebox.askquestion("Assignar rifa","Estàs segur que vols assignar 15€ de rifa als fallers corresponents?")
		if valor=="yes":
			elFaller=Faller()
			res=elFaller.BuscarFallerAmbRifa()
			elMoviment=Moviment()
			elMoviment.ExerciciActual() 
			for val in res:
				elMoviment.InsertarMoviment(15, 1, 3, elMoviment.exercici, val[0], "rifa") #els assignem la rifa
			messagebox.showinfo("Assignar rifa","La rifa s'ha assignat correctament")


	def ModificarHistorial(self): #funció que obre la finestra "Modificar" del menú "Historial"

		#FinestraHistorial(self.root)
		pass


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
		

	def NouExercici(self): #funció per a crear un nou exercici faller

		#elMoviment=Moviment()
		#elMoviment.NouExercici()
		pass

	
	def Eixir(self): #funció per a tancar el programa

		valor=messagebox.askquestion("Eixir","Vols eixir de l'aplicació?")
		if valor=="yes":
			self.master.destroy()


	def Info(self): #funció que mostra una finestra amb informació del programa

		messagebox.showinfo("Informació","Aplicació creada per Ivan Mas")


if __name__=='__main__':
	
	root=tk.Tk()
	app=Aplicacio(root)
	app.mainloop()