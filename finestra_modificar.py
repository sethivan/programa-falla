import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import platform

from base_de_dades import BaseDeDades
from arxiu import Arxiu
from utils import Utils

from family import Family


class FinestraModificar(tk.Toplevel):

	def __init__(self, master=None):

		super().__init__(master)
		self.master=master
		sistema_operatiu=platform.system()
		if sistema_operatiu=='Windows':
			self.iconbitmap("escut.ico")
		self.resizable(0,0)
		self.title("Modificar Dades del Faller")
		utils=Utils()
		utils.definir_estil_global()
		self.configure(bg="#ffffff", pady=5, padx=5)

		self.nom=tk.StringVar()
		self.cognoms=tk.StringVar()
		self.naixement=tk.StringVar()
		self.sexe=tk.StringVar()
		self.dni=tk.StringVar()
		self.adresa=tk.StringVar()
		self.telefon=tk.StringVar()
		self.correu=tk.StringVar()
		self.familia=tk.StringVar()

		self.id=0 # Atribut on guardem el id del faller que ens passa la finestra "gestionar".
		self.id_familia=0
		self.identificadors=[] #variable per a controlar el camp idfamilia de la llista de noms del combo
		self.identificador_familia=0 #variable on guardem el valor final del idfamilia
		self.modificacio=0

		# Frames en els que dividim la finestra.
		label_estil_dades=ttk.Label(self, text="Introduir dades", style="Titol.TLabel")
		label_frame_dades=ttk.LabelFrame(self, style="Marc.TFrame", labelwidget=label_estil_dades)
		label_frame_dades.grid(row=0, column=0, padx=5, pady=5, ipadx=4, ipady=5)

		label_estil_familiar=ttk.Label(self, text="Buscar familiar del faller", style="Titol.TLabel")
		label_frame_familiar=ttk.LabelFrame(self, style="Marc.TFrame", labelwidget=label_estil_familiar)
		label_frame_familiar.grid(row=1, column=0, padx=5, pady=5, ipady=5)

		# Widgets per a cada frame.

		# Frame Dades personals.
		self.label_nom=ttk.Label(label_frame_dades, text="Nom:", style="Etiqueta.TLabel")
		self.label_nom.grid(row=0, column=0, padx=7, pady=2, sticky="w")

		self.entry_nom=ttk.Entry(label_frame_dades, textvariable=self.nom)
		self.entry_nom.grid(row=1, column=0, padx=7)
		self.entry_nom.focus()

		self.label_cognoms=ttk.Label(label_frame_dades, text="Cognoms", style="Etiqueta.TLabel")
		self.label_cognoms.grid(row=0, column=1, pady=2, sticky="w")

		self.entry_cognoms=ttk.Entry(label_frame_dades, width=30, textvariable=self.cognoms)
		self.entry_cognoms.grid(row=1, column=1)

		self.label_sexe=ttk.Label(label_frame_dades, text="Sexe", style="Etiqueta.TLabel")
		self.label_sexe.grid(row=2, column=0, padx=7, pady=5, sticky="w")

		self.radio_button_masculi=ttk.Radiobutton(
			label_frame_dades,
			text="M",
			style="Radio.TRadiobutton",
			variable=self.sexe,
			value=1
		)
		self.radio_button_femeni=ttk.Radiobutton(
			label_frame_dades,
			text="F",
			style="Radio.TRadiobutton",
			variable=self.sexe,
			value=2
		)
		self.radio_button_masculi.grid(row=3, column=0, padx=7, sticky="w")
		self.radio_button_femeni.grid(row=3, column=0)

		self.label_naixement=ttk.Label(label_frame_dades, text="Data de naixement", style="Etiqueta.TLabel")
		self.label_naixement.grid(row=2, column=1, pady=5, sticky="w")

		self.entry_naixement=ttk.Entry(label_frame_dades, width=30, textvariable=self.naixement)
		self.entry_naixement.grid(row=3, column=1)

		self.label_dni=ttk.Label(label_frame_dades, text="DNI", style="Etiqueta.TLabel")
		self.label_dni.grid(row=4, column=0, padx=7, pady=2, sticky="w")

		self.entry_dni=ttk.Entry(label_frame_dades, textvariable=self.dni)
		self.entry_dni.grid(row=5, column=0, padx=7)

		self.label_adresa=ttk.Label(label_frame_dades, text="Adreça", style="Etiqueta.TLabel")
		self.label_adresa.grid(row=4, column=1, pady=2, sticky="w")

		self.entry_adresa=ttk.Entry(label_frame_dades, width=30, textvariable=self.adresa)
		self.entry_adresa.grid(row=5, column=1)

		self.label_telefon=ttk.Label(label_frame_dades, text="Telèfon", style="Etiqueta.TLabel")
		self.label_telefon.grid(row=6, column=0, padx=7, pady=2, sticky="w")

		self.entry_telefon=ttk.Entry(label_frame_dades, textvariable=self.telefon)
		self.entry_telefon.grid(row=7, column=0, padx=7)

		self.label_correu=ttk.Label(label_frame_dades, text="Correu electrònic", style="Etiqueta.TLabel")
		self.label_correu.grid(row=6, column=1, pady=2, sticky="w")

		self.entry_correu=ttk.Entry(label_frame_dades, width=30, textvariable=self.correu)
		self.entry_correu.grid(row=7, column=1)

		# Frame Familiar del faller.
		self.label_opcio_familiar=ttk.Label(label_frame_familiar, text="Familiar en la falla", style="Etiqueta.TLabel")
		self.label_opcio_familiar.grid(row=0, column=0, padx=5, pady=2, sticky="w")

		self.radio_button_familia_si=ttk.Radiobutton(
			label_frame_familiar,
			text="Si",
			style="Radio.TRadiobutton",
			variable=self.familia,
			value=1,
			command=self.habilitar_familia
		)
		self.radio_button_familia_no=ttk.Radiobutton(
			label_frame_familiar,
			text="No",
			style="Radio.TRadiobutton",
			variable=self.familia,
			value=2,
			command=self.deshabilitar_familia
		)
		self.radio_button_familia_si.grid(row=1, column=0, padx=5, sticky="w")
		self.radio_button_familia_no.grid(row=1, column=0)

		self.label_nom_familiar=ttk.Label(label_frame_familiar, text="Cognoms i nom:", style="Etiqueta.TLabel")
		self.label_nom_familiar.grid(row=2, column=0, padx=5, pady=2, sticky="w")

		self.combo_box_familia=ttk.Combobox(label_frame_familiar, width=30, postcommand=self.desplegar_familia)
		self.combo_box_familia.grid(row=3, column=0, padx=5)
		self.combo_box_familia.bind("<<ComboboxSelected>>", self.seleccionar_familia)

		# Botons.
		self.button_actualitzar=ttk.Button(self, text="Actualitzar dades", style="Boto.TButton", command=self.actualitzar)
		self.button_actualitzar.grid(row=3, column=0, padx=5, pady=5)


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
		faller=bd.llegir_faller(id)
		self.nom.set(faller.nom)
		self.cognoms.set(faller.cognoms)
		self.sexe.set(faller.sexe)
		self.naixement.set(faller.naixement)
		self.dni.set(faller.dni)
		self.adresa.set(faller.adresa)
		self.telefon.set(faller.telefon)
		self.correu.set(faller.correu)
		self.id_familia=str(faller.familia.id)
		llistat_fallers=bd.llegir_fallers_per_familia(faller.familia.id)
		llista=[]
		for faller in llistat_fallers:
			if faller.id!=id:
				llista=llista + [(faller.cognoms + ", " + faller.nom)]
		if len(llistat_fallers)>1:
			self.familia.set(1)
			self.combo_box_familia.set(llista[0])
		elif len(llistat_fallers)==1:
			self.familia.set(2)
			self.deshabilitar_familia()
		bd.tancar_conexio()
		self.grab_set()
		self.transient(self.master)
		self.mainloop()

	
	def habilitar_familia(self):
		'''
		Habilita el combobox per a indicar la familia del faller
		quan el Radiobutton de familia esta en "si".
		'''
		bd=BaseDeDades("falla.db")
		self.combo_box_familia.configure(state="normal")
		faller=bd.llegir_faller(self.id)
		llistat_fallers=bd.llegir_fallers_per_familia(faller.familia.id)
		llista=[]
		for faller in llistat_fallers:
			if faller.id!=self.id:
				llista=llista + [(faller.cognoms + ", " + faller.nom)]
		if len(llistat_fallers)>1:
			self.combo_box_familia.set(llista[0])
		bd.tancar_conexio()

	
	def deshabilitar_familia(self):
		'''
		Deshabilita el combobox per a indicar la familia del faller
		quan el Radiobutton de familia esta en "no" i elimina el seu contingut.
		'''
		self.combo_box_familia.configure(state="disabled")
		self.combo_box_familia.delete(0, tk.END) # Borra tot el contingut de la llista.
		self.combo_box_familia.set("") # Borra l'element que es queda a la vista.
		self.identificador_familia=0 # Borra l'identificador de familia en cas que s'haguera creat.

	
	def desplegar_familia(self):
		'''
		Controla el combobox comparant la cadena escrita amb la base de dades i mostrant els resultats en el combobox.
		Utilitza l'atribut "self.identificadors" per a passar el identificador de familia a la funció "seleccionar_familia".
		'''
		bd=BaseDeDades("falla.db")
		cadena=self.combo_box_familia.get()
		llistat_fallers=bd.llegir_fallers_per_cognom(cadena)
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
		self.identificador_familia=self.identificadors[index]
		self.identificadors=[]
	

	def actualitzar(self):
		'''
		Es fica en marxa al fer clic en el botó "actualitzar".
		Es lligen totes les dades presents en el formulari i s'actualitza la base de dades.
		En el cas del canvi de familia, s'evalúa si aquest canvi existeix i es recalculen
		els diferents descomptes familiars.
		'''
		arxiu=Arxiu("exercici")
		bd=BaseDeDades("falla.db")
		exercici_actual=arxiu.llegir_exercici_actual()
		faller=bd.llegir_faller(self.id)
		try:
			edat=faller.calcular_edat(self.naixement.get(), exercici_actual)
		except ValueError:
			messagebox.showwarning("Error", "El format per a la data ha de ser dd-mm-yyyy")
		else:
			valor=messagebox.askquestion("Modificar dades","Vols modificar les dades del faller?")
			if valor=="yes":
				category_id=faller.calculate_category(edat)
				faller.category=bd.llegir_categoria(category_id)
				faller.nom=self.nom.get()
				faller.cognoms=self.cognoms.get()
				faller.sexe=self.sexe.get()
				faller.dni=self.dni.get()
				faller.adresa=self.adresa.get()
				faller.telefon=self.telefon.get()
				faller.correu=self.correu.get()
				if faller.naixement!=self.naixement.get():
					valor=messagebox.askquestion("Modificar dades","Has modificat la data de naixement del faller i s'haurà de crear un nou historial, estas segur?")
					if valor=="yes":
						faller.naixement=self.naixement.get()
						exercici=faller.calcular_primer_exercici(faller.naixement)
						historial={}
						while exercici < exercici_actual:
							historial[exercici]=["baixa", ""]
							exercici=exercici+1
						historial[exercici_actual]=["vocal", "Sants Patrons"]
						nom_arxiu="historials"+"/"+str(faller.id)
						arxiu=Arxiu(nom_arxiu)
						arxiu.modificar_historial(historial)
				# Canvis de familia.
				llistat_fallers=bd.llegir_fallers_per_familia(faller.familia.id)
				if faller.familia.id!=self.identificador_familia and self.identificador_familia!=0:					
					# Si estava sol i entra en familia.
					if len(llistat_fallers)==1:
						faller.familia=bd.llegir_familia(self.identificador_familia)
						bd.actualitzar_faller(faller)
						bd.eliminar_familia(self.id_familia)
						llistat_fallers=[]
						llistat_fallers=bd.llegir_fallers_per_familia(faller.familia.id)
						faller.familia.calcular_descompte(llistat_fallers)
						bd.actualitzar_familia(faller.familia)
					# Si estava en familia i canvia de familia.
					else:
						faller.familia=bd.llegir_familia(self.identificador_familia)
						bd.actualitzar_faller(faller)
						# Actualitzem familia vella
						llistat_fallers=[]
						llistat_fallers=bd.llegir_fallers_per_familia(self.id_familia)
						familia=Family(self.id_familia,0,0)
						familia.calcular_descompte(llistat_fallers)
						bd.actualitzar_familia(familia)
						# Actualitzem familia nova
						llistat_fallers=[]
						llistat_fallers=bd.llegir_fallers_per_familia(faller.familia.id)
						faller.familia.calcular_descompte(llistat_fallers)
						bd.actualitzar_familia(faller.familia)
				# Si estava en familia i passa a estar sol	
				elif len(llistat_fallers)>1 and self.identificador_familia==0:					
					familia=Family(0, 0, 0)
					bd.crear_familia(familia)
					faller.familia=bd.llegir_ultima_familia()
					print(faller.familia.descompte)
					bd.actualitzar_faller(faller)
					# Actualitzem familia vella
					llistat_fallers=[]
					llistat_fallers=bd.llegir_fallers_per_familia(self.id_familia)
					familia=Family(self.id_familia,0,0)
					familia.calcular_descompte(llistat_fallers)
					bd.actualitzar_familia(familia)
				bd.tancar_conexio()
				self.destroy()