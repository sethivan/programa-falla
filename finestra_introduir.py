from tkinter import * #importem les llibreries gràfiques
from tkinter import messagebox #importem el sistema de missatges emergents
from tkinter import ttk #importem les classes per al combobox
from tkinter import LabelFrame

from base_de_dades import BaseDeDades
from arxiu import Arxiu

from categoria import Categoria
from falla import Falla
from faller import Faller
from familia import Familia


class FinestraIntroduir():

	def __init__(self, num):

		self.introduir=Toplevel() #definim una nova finestra
		self.introduir.resizable(0,0)
		self.introduir.title("Introduir Faller")
		self.introduir.iconbitmap("escut.ico")
		self.introduir.transient(master=num) #la finestra sempre es dibuixa sobre la mestra i mai s'amaga
		self.introduir.grab_set() #cap event va a altra finestra fins que aquesta es tanque

		self.nom=StringVar()
		self.cognoms=StringVar()
		self.naixement=StringVar()
		self.sexe=StringVar()
		self.dni=StringVar()
		self.adresa=StringVar()
		self.telefon=StringVar()
		self.correu=StringVar()
		self.familia=StringVar()

		self.ident=[] #variable per a controlar el camp idfamilia de la llista de noms del combo
		self.identfamilia=0 #variable on guardem el valor final del idfamilia
		
		#Frames en els que dividim la finestra

		dadesLF=LabelFrame(self.introduir, text="Introduir dades")
		dadesLF.grid(row=0, column=0, columnspan=4, ipadx=2, ipady=2)

		familiarLF=LabelFrame(self.introduir, text="Buscar familiar del faller")
		familiarLF.grid(row=1, column=0, columnspan=4, ipadx=2, ipady=2)

		#Widgets per a cada frame

		#Frame Dades personals

		self.nomLabel=Label(dadesLF, text="Nom:")
		self.nomLabel.grid(row=0, column=0, sticky="e")

		self.nomEntry=Entry(dadesLF, textvariable=self.nom)
		self.nomEntry.grid(row=0, column=1)
		self.nomEntry.focus()

		self.cognomsLabel=Label(dadesLF, text="Cognoms:")
		self.cognomsLabel.grid(row=0, column=2, sticky="e")

		self.cognomsEntry=Entry(dadesLF, textvariable=self.cognoms)
		self.cognomsEntry.grid(row=0, column=3)

		self.sexeLabel=Label(dadesLF, text="Sexe:")
		self.sexeLabel.grid(row=1, column=0, sticky="e")

		self.masculiRadioButton=Radiobutton(dadesLF, text="M", variable=self.sexe, value=1)
		self.femeniRadioButton=Radiobutton(dadesLF, text="F", variable=self.sexe, value=2)
		self.masculiRadioButton.grid(row=1, column=1, sticky="w")
		self.femeniRadioButton.grid(row=1, column=1)
		self.masculiRadioButton.select() #seleccionem masculi com a predeterminat

		self.naixementLabel=Label(dadesLF, text="Data de naixement:")
		self.naixementLabel.grid(row=1, column=2, sticky="e")

		self.naixementEntry=Entry(dadesLF, textvariable=self.naixement)
		self.naixementEntry.grid(row=1, column=3)

		self.dniLabel=Label(dadesLF, text="DNI:")
		self.dniLabel.grid(row=2, column=0, sticky="e")

		self.dniEntry=Entry(dadesLF, textvariable=self.dni)
		self.dniEntry.grid(row=2, column=1)

		self.adresaLabel=Label(dadesLF, text="Adreça:")
		self.adresaLabel.grid(row=2, column=2, sticky="e")

		self.adresaEntry=Entry(dadesLF, textvariable=self.adresa)
		self.adresaEntry.grid(row=2, column=3)

		self.telefonLabel=Label(dadesLF, text="Telèfon:")
		self.telefonLabel.grid(row=3, column=0, sticky="e")

		self.telefonEntry=Entry(dadesLF, textvariable=self.telefon)
		self.telefonEntry.grid(row=3, column=1)

		self.correuLabel=Label(dadesLF, text="Correu electrònic:")
		self.correuLabel.grid(row=3, column=2, sticky="e")

		self.correuEntry=Entry(dadesLF, textvariable=self.correu)
		self.correuEntry.grid(row=3, column=3)

		#Frame Buscar familiar

		self.nomfamIntLabel=Label(familiarLF, text="Cognoms i nom:")
		self.nomfamIntLabel.grid(row=0, column=0)

		self.fallerfamCombo=ttk.Combobox(familiarLF, width=30, postcommand=self.dropdown_opened_familia)
		self.fallerfamCombo.grid(row=0, column=1)
		self.fallerfamCombo.bind("<<ComboboxSelected>>", self.selection_changed_familia)

		self.familiaLabel=Label(familiarLF, text="Familiar en la falla:")
		self.familiaLabel.grid(row=1, column=0, sticky="e")

		self.famsiRadioButton=Radiobutton(familiarLF, text="Si", variable=self.familia, value=1)
		self.famnoRadioButton=Radiobutton(familiarLF, text="No", variable=self.familia, value=2)
		self.famsiRadioButton.grid(row=1, column=1, sticky="w")
		self.famnoRadioButton.grid(row=1, column=1)
		self.famnoRadioButton.select() #seleccionem no com a predeterminat

		#Botó introduir

		self.introduirButton=Button(self.introduir, text="Introduir", command=self.introduir_faller)
		self.introduirButton.grid(row=3, column=0, padx=5)

		#Bucle que fa funcionar la finestra

		num.wait_window(self.introduir)


	def dropdown_opened_familia(self):

		cadena=self.fallerfamCombo.get()
		falla=Falla()
		llistat_fallers=falla.llegir_fallers("cognoms", cadena)
		llista=[] #llista on anem a acumular els valors
		self.ident=[]
		for faller in llistat_fallers:
			self.ident=self.ident+[faller.familia.id]
			llista=llista + [(faller.cognoms + ", " + faller.nom)]
		self.fallerfamCombo["values"]=llista #insertem cada valor en el desplegable


	def selection_changed_familia(self, event):

		index=self.fallerfamCombo.current()
		self.identfamilia=self.ident[index] #recollim la familia a la que pertany
		self.ident=[]
	

	def introduir_faller(self):
		
		arxiu=Arxiu("exercici")
		categoria=Categoria(0,0,"","")
		faller=Faller(0,"","","",0,"","","",0,"")
		falla=Falla()
		bd=BaseDeDades("falla.db")
		exercici=arxiu.llegir_exercici_actual()
		try:
			edat=faller.calcular_edat(self.naixement.get(), exercici)
		except:
			messagebox.showerror("Error", "El format per a la data ha de ser dd-mm-aaaa")
		else:
			valor=messagebox.askquestion("Alta nova", "Donar d'alta el nou faller?")
			if valor=="yes":
				categoria.calcular_categoria(edat)
				categoria=bd.llegir_categoria(categoria.id)
				if self.familia.get()=="1":
					familia=bd.llegir_familia(self.identfamilia)
					faller=Faller(0, self.nom.get(), self.cognoms.get(), self.naixement.get(), self.sexe.get(), self.dni.get(), self.adresa.get(), self.telefon.get(), 1, self.correu.get(), familia, categoria)
					bd.crear_faller(faller)
					llistat_fallers=falla.llegir_fallers("familia", self.identfamilia)
					familia.calcular_descompte(llistat_fallers)
					bd.actualitzar_familia(familia)
				else:
					familia=Familia(0, 0, 0)
					bd.crear_familia(familia)
					familia=bd.llegir_ultima_familia()
					faller=Faller(0, self.nom.get(), self.cognoms.get(), self.naixement.get(), self.sexe.get(), self.dni.get(), self.adresa.get(), self.telefon.get(), 1, self.correu.get(), familia, categoria)
					bd.crear_faller(faller)
				bd.tancar_conexio()
				#reiniciem tots els camps per a facilitar la introducció del següent faller
				self.nom.set("")
				self.cognoms.set("")
				self.naixement.set("")
				self.adresa.set("")
				self.dni.set("")
				self.telefon.set("")
				self.correu.set("")
				self.masculiRadioButton.select()
				self.fallerfamCombo.set("")
				self.famnoRadioButton.select()
				self.nomEntry.focus()
				

		
		
		'''
			#creem un historial nou i l'omplim
			naixement=self.naixementIntString.get()
			primer=elFaller2.PrimerExercici(naixement)
			anyexer=int(primer)
			historial={}
			while anyexer < exer:
				historial[anyexer]=["baixa", ""]
				anyexer=anyexer+1
			historial[exer]=["vocal", "Sants Patrons"]
			fallerid=elFaller2.id
			arxiu="historials"+"/"+str(fallerid)
			fitxer=open(arxiu,"wb")
			pickle.dump(historial, fitxer)
			fitxer.close()
			del(fitxer)

			'''
