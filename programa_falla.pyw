from tkinter import * #importem les llibreries gràfiques
from tkinter import messagebox #importem el sistema de missatges emergents
from gestionar import *
from introduir import *
from assignar import *
from moviment import *
from informe import *
from historial import *

#import pickle


class Aplicacio():

		
	def __init__(self): #el constructor construeix la finestra d'aplicació

		self.root=Tk()
		self.root.state('zoomed') #s'obri maximitzada
		self.root.resizable(0,0) #no es pot redimensionar
		self.root.title("Falla Sants Patrons")
		self.root.iconbitmap("escut.ico")

		barraMenu=Menu(self.root) #guardem el menú en una variable
		self.root.config(menu=barraMenu) #construïm el menú
		arxiuMenu=Menu(barraMenu, tearoff=0) #creem els diferents elements i subelements
		arxiuMenu.add_command(label="Eixir", command=self.Eixir)
		fallerMenu=Menu(barraMenu, tearoff=0)
		fallerMenu.add_command(label="Gestionar", command=self.Gestionar, accelerator="Ctrl+G")
		self.root.bind_all("<Control-g>", self.EventGestionar) #bindegem el submenú Buscar
		fallerMenu.add_command(label="Introduir", command=self.Introduir, accelerator="Ctrl+I")
		self.root.bind_all("<Control-i>", self.EventIntroduir)
		loteriaMenu=Menu(barraMenu, tearoff=0)
		loteriaMenu.add_command(label="Assignar", command=self.Assignar)
		rifaMenu=Menu(barraMenu, tearoff=0)
		rifaMenu.add_command(label="Assignar", command=self.AssignarRifa)
		historialMenu=Menu(barraMenu, tearoff=0)
		historialMenu.add_command(label="Modificar", command=self.ModificarHistorial)
		#historialMenu.add_command(label="Modificar", command=self.prova)
		llistatsMenu=Menu(barraMenu, tearoff=0)
		llistatsMenu.add_command(label="Moviments", command=self.MovimentsDia)
		llistatsMenu.add_command(label="General", command=self.LlistatGeneral)
		llistatsMenu.add_command(label="Fallers", command=self.LlistatFallers)
		llistatsMenu.add_command(label="Altes i Baixes", command=self.LlistatAltesBaixes)
		llistatsMenu.add_command(label="Rifes", command=self.LlistatRifes)
		exerciciMenu=Menu(barraMenu, tearoff=0)
		exerciciMenu.add_command(label="Nou", command=self.NouExercici)
		ajudaMenu=Menu(barraMenu, tearoff=0)
		ajudaMenu.add_command(label="Info", command=self.Info)
		barraMenu.add_cascade(label="Arxiu", menu=arxiuMenu) #els afegim a la barra
		barraMenu.add_cascade(label="Faller", menu=fallerMenu)
		barraMenu.add_cascade(label="Loteria", menu=loteriaMenu)
		barraMenu.add_cascade(label="Rifa", menu=rifaMenu)
		barraMenu.add_cascade(label="Historial", menu=historialMenu)
		barraMenu.add_cascade(label="Llistats", menu=llistatsMenu)
		barraMenu.add_cascade(label="Exercici", menu=exerciciMenu)
		barraMenu.add_cascade(label="Ajuda", menu=ajudaMenu)
			
		framePrincipal=Frame()
		framePrincipal.pack()

		self.root.mainloop()


	def EventGestionar(self, event): #funció per al bindeig

		self.Gestionar()


	def Gestionar(self):

		FinestraGestionar(self.root)
	

	def EventIntroduir(self, event): #funció per al bindeig

		self.Introduir()

	
	def Introduir(self):

		FinestraIntroduir(self.root)


	def Assignar(self):

		FinestraAssignar(self.root)


	def AssignarRifa(self):

		valor=messagebox.askquestion("Assignar rifa","Estàs segur que vols assignar 15€ de rifa als fallers corresponents?")
		if valor=="yes":
			elFaller=Faller()
			#res=elFaller.BuscarFallerPerCategoria(1) #busquem tots els fallers de categoria 1
			res=elFaller.BuscarFallerAmbRifa()
			elMoviment=Moviment()
			elMoviment.ExerciciActual() 
			for val in res:
				elMoviment.InsertarAsignacio(15, 3, elMoviment.exercici, val[0], "rifa") #els assignem la rifa
			#res2=elFaller.BuscarFallerPerCategoria(2) #busquem tots els fallers de categoria 2
			#for val in res2:
				#elMoviment.InsertarAsignacio(15, 3, elMoviment.exercici, val[0], "rifa") #els assignem la rifa
			messagebox.showinfo("Assignar rifa","La rifa s'ha assignat correctament")


	def ModificarHistorial(self):

		FinestraHistorial(self.root)

		
	def prova(self):

		
		try:
			os.mkdir("historials")
		except OSError as e:
			if e.errno!=errno.EEXIST:
				raise

		elMoviment=Moviment()
		elMoviment.ExerciciActual()
		anyactual=elMoviment.exercici
		elFaller=Faller()
		res=elFaller.LlistatFallers()
		for val in res:
			naixement=val[3]
			primer=elFaller.PrimerExercici(naixement)
			anyexer=int(primer)
			historial={}
			while anyexer < anyactual:
				historial[anyexer]=["baixa", ""]
				anyexer=anyexer+1
			alta=val[8]
			if alta==1:
				historial[anyactual]=["vocal", "Sants Patrons"]
			else:
				historial[anyactual]=["baixa", ""]
			fallerid=val[0]
			arxiu="historials"+"/"+str(fallerid)
			fitxer=open(arxiu,"wb")
			pickle.dump(historial, fitxer)
			fitxer.close()
			del(fitxer)

		fitxer=open(arxiu,"rb")
		diccionari=pickle.load(fitxer)
		fitxer.close()
		del(fitxer)

		print(diccionari)


	def MovimentsDia(self):

		elInforme=Informe()
		elInforme.MovimentsDia()


	def LlistatGeneral(self):

		elInforme=Informe()
		elInforme.LlistatGeneral()


	def LlistatFallers(self):

		elInforme=Informe()
		elInforme.LlistatFallers()


	def LlistatAltesBaixes(self):

		elInforme=Informe()
		elInforme.LlistatAltesBaixes()


	def LlistatRifes(self):

		elInforme=Informe()
		elInforme.FallersAmbRifa()
		

	def NouExercici(self):

		elMoviment=Moviment()
		elMoviment.NouExercici()

	
	def Eixir(self):

		valor=messagebox.askquestion("Eixir","Vols eixir de l'aplicació?")
		if valor=="yes":
			self.root.destroy()


	def Info(self):

		messagebox.showinfo("Informació","Aplicació creada per Ivan Mas")


def main(): #funció principal que llança l'aplicació
	app=Aplicacio()
	return(0)

if __name__=='__main__': #comprova si es un módul importat o l'arxiu principal
	main()