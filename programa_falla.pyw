import tkinter as tk #importem les llibreries gràfiques
from tkinter import messagebox #importem el sistema de missatges emergents
#from gestionar import *
#from introduir import *
#from assignar import *
#from moviment import *
#from informe import *
#from historial import *

#import pickle


class Aplicacio(tk.Frame):

		
	def __init__(self, master=None): #el constructor construeix la finestra d'aplicació

		super().__init__(master)
		self.master=master
		self.master.state('zoomed')
		self.master.title("Falla Sants Patrons")
		self.master.iconbitmap("escut.ico")
		

		self.barraMenu=tk.Menu()
		#barraMenu=Menu(self.root) #guardem el menú en una variable
		self.master.config(menu=self.barraMenu) #construïm el menú
		self.arxiuMenu=tk.Menu(self.barraMenu, tearoff=0) #creem els diferents elements i subelements
		self.arxiuMenu.add_command(label="Eixir", command=self.Eixir)
		self.fallerMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.fallerMenu.add_command(label="Gestionar", command=self.Gestionar, accelerator="Ctrl+G")
		self.master.bind_all("<Control-g>", self.EventGestionar) #bindegem el submenú Buscar
		self.fallerMenu.add_command(label="Introduir", command=self.Introduir, accelerator="Ctrl+I")
		self.master.bind_all("<Control-i>", self.EventIntroduir)
		self.loteriaMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.loteriaMenu.add_command(label="Assignar", command=self.Assignar)
		self.rifaMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.rifaMenu.add_command(label="Assignar", command=self.AssignarRifa)
		self.historialMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.historialMenu.add_command(label="Modificar", command=self.ModificarHistorial)
		self.llistatsMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.llistatsMenu.add_command(label="Moviments", command=self.MovimentsDia)
		self.llistatsMenu.add_command(label="General", command=self.LlistatGeneral)
		self.llistatsMenu.add_command(label="Fallers", command=self.LlistatFallers)
		self.llistatsMenu.add_command(label="Altes i Baixes", command=self.LlistatAltesBaixes)
		self.llistatsMenu.add_command(label="Rifes", command=self.LlistatRifes)
		self.exerciciMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.exerciciMenu.add_command(label="Nou", command=self.NouExercici)
		self.ajudaMenu=tk.Menu(self.barraMenu, tearoff=0)
		self.ajudaMenu.add_command(label="Info", command=self.Info)
		self.barraMenu.add_cascade(label="Arxiu", menu=self.arxiuMenu) #els afegim a la barra
		self.barraMenu.add_cascade(label="Faller", menu=self.fallerMenu)
		self.barraMenu.add_cascade(label="Loteria", menu=self.loteriaMenu)
		self.barraMenu.add_cascade(label="Rifa", menu=self.rifaMenu)
		self.barraMenu.add_cascade(label="Historial", menu=self.historialMenu)
		self.barraMenu.add_cascade(label="Llistats", menu=self.llistatsMenu)
		self.barraMenu.add_cascade(label="Exercici", menu=self.exerciciMenu)
		self.barraMenu.add_cascade(label="Ajuda", menu=self.ajudaMenu)


	def EventGestionar(self, event): #funció per al bindeig

		self.Gestionar()


	def Gestionar(self):

		#FinestraGestionar(self.root)
		pass
	

	def EventIntroduir(self, event): #funció per al bindeig

		self.Introduir()

	
	def Introduir(self):

		#FinestraIntroduir(self.root)
		pass


	def Assignar(self):

		#FinestraAssignar(self.root)
		pass


	def AssignarRifa(self):

		pass
		#valor=messagebox.askquestion("Assignar rifa","Estàs segur que vols assignar 15€ de rifa als fallers corresponents?")
		#if valor=="yes":
			#elFaller=Faller()
			#res=elFaller.BuscarFallerAmbRifa()
			#elMoviment=Moviment()
			#elMoviment.ExerciciActual() 
			#for val in res:
				#elMoviment.InsertarAsignacio(15, 3, elMoviment.exercici, val[0], "rifa") #els assignem la rifa
			#messagebox.showinfo("Assignar rifa","La rifa s'ha assignat correctament")


	def ModificarHistorial(self):

		#FinestraHistorial(self.root)
		pass


	def MovimentsDia(self):

		#elInforme=Informe()
		#elInforme.MovimentsDia()
		pass


	def LlistatGeneral(self):

		#elInforme=Informe()
		#elInforme.LlistatGeneral()
		pass


	def LlistatFallers(self):

		#elInforme=Informe()
		#elInforme.LlistatFallers()
		pass


	def LlistatAltesBaixes(self):

		#elInforme=Informe()
		#elInforme.LlistatAltesBaixes()
		pass


	def LlistatRifes(self):

		#elInforme=Informe()
		#elInforme.FallersAmbRifa()
		pass
		

	def NouExercici(self):

		#elMoviment=Moviment()
		#elMoviment.NouExercici()
		pass

	
	def Eixir(self):

		valor=messagebox.askquestion("Eixir","Vols eixir de l'aplicació?")
		if valor=="yes":
			self.master.destroy()


	def Info(self):

		messagebox.showinfo("Informació","Aplicació creada per Ivan Mas")


#def main(): #funció principal que llança l'aplicació
	#app=Aplicacio()
	#return(0)

#if __name__=='__main__': #comprova si es un módul importat o l'arxiu principal
	#main()

root=tk.Tk()
app=Aplicacio(root)
app.mainloop()