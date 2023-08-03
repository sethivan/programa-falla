'''
Módul que conté la classe FinestraIntroduir.
És la finestra en la qual s'indiquen les dades del nou faller per a guardar-lo
a la base de dades.
'''
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import LabelFrame
import platform

from base_de_dades import BaseDeDades
from arxiu import Arxiu

from categoria import Categoria
from faller import Faller
from familia import Familia


class FinestraIntroduir(tk.Toplevel):
	'''
	Esta classe representa una nova finestra que depén de la finestra principal.

	Atributs:
	---------
	master : tk.Tk o tk.Toplevel
		La instància principal de l'aplicació o de la finestra que crea esta nova finestra.
	'''


	def __init__(self, master=None):
		'''
		Inicialitza una nova instància de la classe FinestraIntroduir.

		Parametres:
		-----------
		master : tk.Tk o tk.Toplevel, opcional
			La instància principal de l'aplicació o de la finestra
			que crea esta nova finestra.
			Si no es proporciona, es creará una nueva instancia de tk.Tk().
		'''
		super().__init__(master)
		self.master=master
		sistema_operatiu=platform.system()
		if sistema_operatiu=='Windows':
			self.iconbitmap("escut.ico")
		self.resizable(0,0)
		self.title("Introduir Faller")

		self.nom=tk.StringVar()
		self.cognoms=tk.StringVar()
		self.naixement=tk.StringVar()
		self.sexe=tk.StringVar()
		self.dni=tk.StringVar()
		self.adresa=tk.StringVar()
		self.telefon=tk.StringVar()
		self.correu=tk.StringVar()
		self.familia=tk.StringVar()

		self.identificadors=[] # Atribut per guardar els id_familia de la llista del combo.
		self.identificador_familia=0 # Atribut on guardem el valor final de l'id_familia.
		
		# Frames en els que dividim la finestra.
		label_frame_dades=LabelFrame(self, text="Introduir dades")
		label_frame_dades.grid(row=0, column=0, columnspan=4, ipadx=2, ipady=2)

		label_frame_familiar=LabelFrame(self, text="Buscar familiar del faller")
		label_frame_familiar.grid(row=1, column=0, columnspan=4, ipadx=2, ipady=2)

		# Widgets per a cada frame.

		# Frame "Introduir dades".
		self.label_nom=tk.Label(label_frame_dades, text="Nom:")
		self.label_nom.grid(row=0, column=0, sticky="e")

		self.entry_nom=tk.Entry(label_frame_dades, textvariable=self.nom)
		self.entry_nom.grid(row=0, column=1)
		self.entry_nom.focus()

		self.label_cognoms=tk.Label(label_frame_dades, text="Cognoms:")
		self.label_cognoms.grid(row=0, column=2, sticky="e")

		self.entry_cognoms=tk.Entry(label_frame_dades, textvariable=self.cognoms)
		self.entry_cognoms.grid(row=0, column=3)

		self.label_sexe=tk.Label(label_frame_dades, text="Sexe:")
		self.label_sexe.grid(row=1, column=0, sticky="e")

		self.radio_button_masculi=tk.Radiobutton(
			label_frame_dades,
			text="M",
			variable=self.sexe,
			value=1
		)
		self.radio_button_femeni=tk.Radiobutton(
			label_frame_dades,
			text="F",
			variable=self.sexe,
			value=2
		)
		self.radio_button_masculi.grid(row=1, column=1, sticky="w")
		self.radio_button_femeni.grid(row=1, column=1)
		self.radio_button_masculi.select() # Seleccionem masculí com a predeterminat.

		self.label_naixement=tk.Label(label_frame_dades, text="Data de naixement:")
		self.label_naixement.grid(row=1, column=2, sticky="e")

		self.entry_naixement=tk.Entry(label_frame_dades, textvariable=self.naixement)
		self.entry_naixement.grid(row=1, column=3)

		self.label_dni=tk.Label(label_frame_dades, text="DNI:")
		self.label_dni.grid(row=2, column=0, sticky="e")

		self.entry_dni=tk.Entry(label_frame_dades, textvariable=self.dni)
		self.entry_dni.grid(row=2, column=1)

		self.label_adresa=tk.Label(label_frame_dades, text="Adreça:")
		self.label_adresa.grid(row=2, column=2, sticky="e")

		self.entry_adresa=tk.Entry(label_frame_dades, textvariable=self.adresa)
		self.entry_adresa.grid(row=2, column=3)

		self.label_telefon=tk.Label(label_frame_dades, text="Telèfon:")
		self.label_telefon.grid(row=3, column=0, sticky="e")

		self.entry_telefon=tk.Entry(label_frame_dades, textvariable=self.telefon)
		self.entry_telefon.grid(row=3, column=1)

		self.label_correu=tk.Label(label_frame_dades, text="Correu electrònic:")
		self.label_correu.grid(row=3, column=2, sticky="e")

		self.entry_correu=tk.Entry(label_frame_dades, textvariable=self.correu)
		self.entry_correu.grid(row=3, column=3)

		# Frame "Buscar familiar del faller".
		self.label_nom_familiar=tk.Label(label_frame_familiar, text="Cognoms i nom:")
		self.label_nom_familiar.grid(row=0, column=0)

		self.combo_box_familiar_faller=ttk.Combobox(
			label_frame_familiar, 
			width=30, 
			postcommand=self.desplegar_familia
		)
		self.combo_box_familiar_faller.grid(row=0, column=1)
		self.combo_box_familiar_faller.bind("<<ComboboxSelected>>", self.seleccionar_familia)
		self.combo_box_familiar_faller.configure(state="disabled")

		self.label_opcio_familiar=tk.Label(label_frame_familiar, text="Familiar en la falla:")
		self.label_opcio_familiar.grid(row=1, column=0, sticky="e")

		self.radio_button_familiar_si=tk.Radiobutton(
			label_frame_familiar, 
			text="Si", 
			variable=self.familia, 
			value=1, 
			command=self.habilitar_familia
		)
		self.radio_button_familiar_no=tk.Radiobutton(
			label_frame_familiar, 
			text="No", 
			variable=self.familia, 
			value=2, 
			command=self.deshabilitar_familia
		)
		self.radio_button_familiar_si.grid(row=1, column=1, sticky="w")
		self.radio_button_familiar_no.grid(row=1, column=1)
		self.radio_button_familiar_no.select() # Seleccionem "no" com a predeterminat.

		#Botó "Introduir".
		self.button_introduir=tk.Button(self, text="Introduir", command=self.introduir_faller)
		self.button_introduir.grid(row=3, column=0, padx=5)


	def iniciar(self):
		'''
		Inicia la nova finestra.
		'''
		self.grab_set() # Manté el foco en la finestra.
		self.transient(self.master) # Manté la finestra sempre per damunt de la principal.
		self.mainloop()


	def habilitar_familia(self):
		'''
		Habilita el combobox per a indicar la familia del faller
		quan el Radiobutton de familia esta en "si".
		'''
		self.combo_box_familiar_faller.configure(state="normal")

	
	def deshabilitar_familia(self):
		'''
		Deshabilita el combobox per a indicar la familia del faller
		quan el Radiobutton de familia esta en "no" i elimina el seu contingut.
		'''
		self.combo_box_familiar_faller.configure(state="disabled")
		self.combo_box_familiar_faller.delete(0, tk.END) # Borra tot el contingut de la llista
		self.combo_box_familiar_faller.set("") # Borra l'element que es queda a la vista


	def desplegar_familia(self):
		'''
		Controla el combobox comparant la cadena escrita amb la base de dades
		i mostrant els resultats en el combobox.
		Utilitza la variable global "self.identificadors"
		per a guardar tots els identificadors del llistat.
		'''
		bd=BaseDeDades("falla.db")
		cadena=self.combo_box_familiar_faller.get()
		llistat_fallers=bd.llegir_fallers_per_cognom(cadena)
		llista=[] # Llista on anem a acumular els valors.
		self.identificadors=[]
		for faller in llistat_fallers:
			self.identificadors=self.identificadors+[faller.familia.id]
			llista=llista + [(faller.cognoms + ", " + faller.nom)]
		# Insertem cada valor en el desplegable.
		self.combo_box_familiar_faller["values"]=llista
		bd.tancar_conexio()


	def seleccionar_familia(self, event):
		'''
		Controla la selecció del combobox per a guardar el identificador de la familia
		a la variable "self.identificador_familia"
		'''
		index=self.combo_box_familiar_faller.current()
		# Recollim la familia a la que pertany.
		self.identificador_familia=self.identificadors[index]
		self.identificadors=[]
	

	def introduir_faller(self):
		'''
		Es fica en marxa al apretar el botó de "Introduir".
		Dona d'alta les dades introduides del nou faller a la base de dades.
		Si conforma una familia nova la dona d'alta.
		Si ja pertany a una familia l'inclou en ella i recalcula el descompte familiar.
		Crea un historial per al faller nou.
		'''
		arxiu=Arxiu("exercici")
		categoria=Categoria(0,0,"","")
		faller=Faller(0,"","","",0,"","","",0,"")
		exercici_actual=arxiu.llegir_exercici_actual()
		try:
			edat=faller.calcular_edat(self.naixement.get(), exercici_actual)
		except:
			messagebox.showerror("Error", "El format per a la data ha de ser dd-mm-aaaa")
		else:
			valor=messagebox.askquestion("Alta nova", "Donar d'alta el nou faller?")
			if valor=="yes":
				bd=BaseDeDades("falla.db")
				categoria.calcular_categoria(edat)
				categoria=bd.llegir_categoria(categoria.id)
				if self.familia.get()=="1":
					familia=bd.llegir_familia(self.identificador_familia)
					faller=Faller(
						0, 
						self.nom.get(), 
						self.cognoms.get(), 
						self.naixement.get(), 
						self.sexe.get(), 
						self.dni.get(), 
						self.adresa.get(), 
						self.telefon.get(), 
						1, 
						self.correu.get(), 
						familia, 
						categoria
					)
					bd.crear_faller(faller)
					llistat_fallers=bd.llegir_fallers_per_familia(
						self.identificador_familia
					)
					familia.calcular_descompte(llistat_fallers)
					bd.actualitzar_familia(familia)
				else:
					familia=Familia(0, 0, 0)
					bd.crear_familia(familia)
					familia=bd.llegir_ultima_familia()
					faller=Faller(
						0, 
						self.nom.get(), 
						self.cognoms.get(), 
						self.naixement.get(), 
						self.sexe.get(), 
						self.dni.get(), 
						self.adresa.get(), 
						self.telefon.get(), 
						1, 
						self.correu.get(), 
						familia, 
						categoria
					)
					bd.crear_faller(faller)
				
				# Creem un historial nou i l'omplim
				faller=bd.llegir_ultim_faller()
				exercici=faller.calcular_primer_exercici(faller.naixement)
				historial={}
				while exercici < exercici_actual:
					historial[exercici]=["baixa", ""]
					exercici=exercici+1
				historial[exercici_actual]=["vocal", "Sants Patrons"]
				nom_arxiu="historials"+"/"+str(faller.id)
				arxiu=Arxiu(nom_arxiu)
				arxiu.crear_historial(historial)
				bd.tancar_conexio()

				# Reiniciem tots els camps per a facilitar la introducció del següent faller.
				self.nom.set("")
				self.cognoms.set("")
				self.naixement.set("")
				self.adresa.set("")
				self.dni.set("")
				self.telefon.set("")
				self.correu.set("")
				self.radio_button_masculi.select()
				self.radio_button_familiar_no.select()
				self.deshabilitar_familia()
				self.entry_nom.focus()
