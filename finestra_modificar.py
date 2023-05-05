import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import LabelFrame

from base_de_dades import BaseDeDades
from arxiu import Arxiu

from familia import Familia
from categoria import Categoria


class FinestraModificar(tk.Toplevel):

	def __init__(self, master=None):

		super().__init__(master)
		self.master=master
		self.resizable(0,0)
		self.title("Modificar Dades del Faller")
		self.iconbitmap("escut.ico")

		self.nom=StringVar()
		self.cognoms=StringVar()
		self.naixement=StringVar()
		self.sexe=StringVar()
		self.dni=StringVar()
		self.adresa=StringVar()
		self.telefon=StringVar()
		self.correu=StringVar()
		self.familia=StringVar()

		self.id=0 # Atribut on guardem el id del faller que ens passa la finestra "gestionar".
		self.fam=0
		self.identificadors=[] #variable per a controlar el camp idfamilia de la llista de noms del combo
		self.identfamilia=0 #variable on guardem el valor final del idfamilia
		self.modificacio=0

		# Frames en els que dividim la finestra.
		label_frame_dades=LabelFrame(self, text="Modificar dades")
		label_frame_dades.grid(row=0, column=0, columnspan=4, ipadx=2, ipady=2)

		label_frame_familiar=LabelFrame(self, text="Modificar familiar del faller")
		label_frame_familiar.grid(row=1, column=0, columnspan=4, ipadx=2, ipady=2)

		# Widgets per a cada frame.

		# Frame Dades personals.
		self.label_nom=Label(label_frame_dades, text="Nom:")
		self.label_nom.grid(row=0, column=0, sticky="e")

		self.entry_nom=Entry(label_frame_dades, textvariable=self.nom)
		self.entry_nom.grid(row=0, column=1)

		self.label_cognoms=Label(label_frame_dades, text="Cognoms:")
		self.label_cognoms.grid(row=0, column=2, sticky="e")

		self.entry_cognoms=Entry(label_frame_dades, textvariable=self.cognoms)
		self.entry_cognoms.grid(row=0, column=3)

		self.label_sexe=Label(label_frame_dades, text="Sexe:")
		self.label_sexe.grid(row=1, column=0, sticky="e")

		self.radio_button_masculi=Radiobutton(label_frame_dades, text="M", variable=self.sexe, value=1)
		self.radio_button_femeni=Radiobutton(label_frame_dades, text="F", variable=self.sexe, value=2)
		self.radio_button_masculi.grid(row=1, column=1, sticky="w")
		self.radio_button_femeni.grid(row=1, column=1)
		self.radio_button_masculi.select()

		self.label_naixement=Label(label_frame_dades, text="Data de naixement:")
		self.label_naixement.grid(row=1, column=2, sticky="e")

		self.entry_naixement=Entry(label_frame_dades, textvariable=self.naixement)
		self.entry_naixement.grid(row=1, column=3)

		self.label_dni=Label(label_frame_dades, text="DNI:")
		self.label_dni.grid(row=2, column=0, sticky="e")

		self.entry_dni=Entry(label_frame_dades, textvariable=self.dni)
		self.entry_dni.grid(row=2, column=1)

		self.label_adresa=Label(label_frame_dades, text="Adreça:")
		self.label_adresa.grid(row=2, column=2, sticky="e")

		self.entry_adresa=Entry(label_frame_dades, textvariable=self.adresa)
		self.entry_adresa.grid(row=2, column=3)

		self.label_telefon=Label(label_frame_dades, text="Telèfon:")
		self.label_telefon.grid(row=3, column=0, sticky="e")

		self.entry_telefon=Entry(label_frame_dades, textvariable=self.telefon)
		self.entry_telefon.grid(row=3, column=1)

		self.label_correu=Label(label_frame_dades, text="Correu electrònic:")
		self.label_correu.grid(row=3, column=2, sticky="e")

		self.entry_correu=Entry(label_frame_dades, textvariable=self.correu)
		self.entry_correu.grid(row=3, column=3)

		# Frame Familiar del faller.
		self.label_nom_familiar=Label(label_frame_familiar, text="Cognoms i nom:")
		self.label_nom_familiar.grid(row=0, column=0)

		self.combo_box_familia=ttk.Combobox(label_frame_familiar, width=30, postcommand=self.desplegar_familia)
		self.combo_box_familia.grid(row=0, column=1)
		self.combo_box_familia.bind("<<ComboboxSelected>>", self.seleccionar_familia)

		self.label_opcio_familiar=Label(label_frame_familiar, text="Familiar en la falla:")
		self.label_opcio_familiar.grid(row=1, column=0, sticky="e")

		self.radio_button_familia_si=Radiobutton(label_frame_familiar, text="Si", variable=self.familia, value=1)
		self.radio_button_familia_no=Radiobutton(label_frame_familiar, text="No", variable=self.familia, value=2)
		self.radio_button_familia_si.grid(row=1, column=1, sticky="w")
		self.radio_button_familia_no.grid(row=1, column=1)
		self.radio_button_familia_no.select()

		# Botons.
		self.button_actualitzar=Button(self, text="Actualitzar dades", command=self.Actualitzarbt)
		self.button_actualitzar.grid(row=3, column=0, padx=5)

		self.button_canvi_familia=Button(self, text="Canviar familia", command=self.CanviFamiliabt)
		self.button_canvi_familia.grid(row=3, column=1, padx=5)


	def iniciar(self, id):
		'''
		Ompli el formulari complet a partir de l'id del faller.

		Paràmetres:
		-----------
		id : integer
			Identificador del faller passat per la finestra "gestionar".
		'''
		bd=BaseDeDades("falla.db")
		self.id=id
		faller=bd.llegir_faller_complet(id)
		self.nom.set(faller.nom)
		self.cognoms.set(faller.cognoms)
		self.sexe.set(faller.sexe)
		self.naixement.set(faller.naixement)
		self.dni.set(faller.dni)
		self.adresa.set(faller.adresa)
		self.telefon.set(faller.telefon)
		self.correu.set(faller.correu)
		self.fam=str(faller.familia.id)
		llistat_fallers=bd.llegir_fallers_per_familia(faller.familia.id)
		llista=[]
		familiars=0
		for faller in llistat_fallers:
			if faller.id!=id:
				llista=llista + [(faller.cognoms + ", " + faller.nom)]
			familiars=familiars+1
		if familiars>1:
			self.combo_box_familia.set(llista[0])
			self.familia.set(1)
		elif familiars==1:
			self.familia.set(2)	
		bd.tancar_conexio()
		self.grab_set()
		self.transient(self.master)
		self.mainloop()


	def desplegar_familia(self):
		'''
		Controla el combobox comparant la cadena escrita amb la base de dades i mostrant els resultats en el combobox.
		Utilitza l'atribut "self.identificadors" per a passar el identificador de familia a la funció "seleccionar_familia".
		'''
		bd=BaseDeDades("falla.db")
		cadena=self.combo_box_familia.get()
		llistat_fallers=bd.llegir_fallers_amb_familia_per_cognom(cadena)
		llista=[]
		self.identificadors=[]
		for faller in llistat_fallers:
			self.identificadors=self.identificadors+[faller.familia.id]
			llista=llista + [(faller.cognoms + ", " + faller.nom)]
		self.combo_box_familia["values"]=llista
		bd.tancar_conexio()


	def seleccionar_familia(self, event):
		'''
		Controla la selecció del combobox per a guardar el identificador de la familia i omplir les dades a partir d'aquest.
		'''
		index=self.combo_box_familia.current()
		self.identfamilia=self.identificadors[index]
		self.identificadors=[]
	

	def Actualitzarbt(self):
		
		arxiu=Arxiu("exercici")
		bd=BaseDeDades("falla.db")
		categoria=Categoria(0,0,"","")
		exercici_actual=arxiu.llegir_exercici_actual()
		faller=bd.llegir_faller_complet(self.id)
		try:
			edat=faller.calcular_edat(self.naixement.get(), exercici_actual)
		except ValueError:
			messagebox.showwarning("Error", "El format per a la data ha de ser dd-mm-yyyy")
		else:
			valor=messagebox.askquestion("Modificar dades","Vols modificar les dades del faller?")
			if valor=="yes":
				#crear un historial nou si ha canviat la data de naixement PENDENT!!!!!!!!
				categoria.calcular_categoria(edat)
				categoria=bd.llegir_categoria(categoria.id)
				faller.nom=self.nom.get()
				faller.cognoms=self.cognoms.get()
				faller.naixement=self.naixement.get()
				faller.sexe=self.sexe.get()
				faller.dni=self.dni.get()
				faller.adresa=self.adresa.get()
				faller.telefon=self.telefon.get()
				faller.correu=self.correu.get()
				faller.categoria=categoria
				bd.actualitzar_faller(faller)
				self.destroy()

	
	def CanviFamiliabt(self):
		
		#cadena=self.identfamilia
		#elFaller=Faller()
		bd=BaseDeDades("falla.db")
		faller=bd.llegir_faller_complet(self.id)
		if self.familia.get()=="1": #si va a pertanyer a una familia
			familia=bd.llegir_familia(self.identfamilia)
			faller.familia=familia
			bd.actualitzar_faller(faller)
			#elFaller.ModificarFamilia(self.id, cadena)
		else: #creem familia nova
			#laFamilia=Familia()
			#laFamilia.InsertarFamilia()
			#laFamilia.RecuperarUltimaFamilia()
			#ultimid=laFamilia.id
			#elFaller.ModificarFamilia(self.id, ultimid)
			familia=Familia(0, 0, 0)
			bd.crear_familia(familia)
			familia=bd.llegir_ultima_familia()
			faller.familia=familia
			bd.actualitzar_faller(faller)
		#comprovar els descomptes familiars en les dos families
		#familia 1
		#res1=elFaller.BuscarFallerPerIdfamilia(self.fam)
		#fem el càlcul dels descompte a partir dels membres i si hi ha una quota màxima
		#membres=0
		#maxima=False
		#descompte=0
		#for faller in llistat_fallers:
			#if faller.alta==1: #si el faller está actiu
				#membres=membres + 1
				#if val[10]==1: #si la quota es màxima
					#maxima=True
		familia=bd.llegir_familia(self.fam)
		llistat_fallers=bd.llegir_fallers_amb_categoria_per_familia(self.fam)
		
		#laFamilia=Familia()
		membres=familia.calcular_membres(llistat_fallers)
		if membres==0:
			bd.eliminar_familia(self.fam)
			#laFamilia.BorrarFamilia(self.fam)
		else:
			familia.calcular_descompte(llistat_fallers)
			bd.actualitzar_familia(familia)
			#if maxima==True and membres==3:
				#descompte=5
			#if maxima==True and membres>=4:
				#descompte=10
			#laFamilia.AsignarDescompteFamilia(self.fam, descompte) #asignem el descompte a la familia
		
		#familia 2
		faller=bd.llegir_faller_complet(self.id)
		#elFaller2=Faller()
		#elFaller2.BuscarFallerPerId(self.id)
		#fam2=str(elFaller2.familia)
		llistat_fallers=bd.llegir_fallers_amb_categoria_per_familia(faller.familia.id)
		#res2=elFaller.BuscarFallerPerIdfamilia(fam2)
		#fem el càlcul dels descompte a partir dels membres i si hi ha una quota màxima
		faller.familia.calcular_descompte(llistat_fallers)
		bd.actualitzar_familia(faller.familia)
		#membres=0
		#maxima=False
		#descompte=0
		#for val in res2:
			#if val[8]==1: #si el faller está actiu
				#membres=membres + 1
				#if val[10]==1: #si la quota es màxima
					#maxima=True
		#if maxima==True and membres==3:
			#descompte=5
		#if maxima==True and membres>=4:
			#descompte=10
		#laFamilia=Familia()
		#laFamilia.AsignarDescompteFamilia(fam2, descompte) #asignem el descompte a la familia