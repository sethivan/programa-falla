'''
Módul que conté la classe FinestraIntroduir.
És la finestra en la qual s'indiquen les dades del nou faller per a guardar-lo
a la base de dades.
'''
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import platform

from base_de_dades import BaseDeDades
from arxiu import Arxiu
from utils import Utils

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

		self.identificadors=[] # Atribut per guardar els id_familia de la llista del combo.
		self.identificador_familia=0 # Atribut on guardem el valor final de l'id_familia.
		
		# Frames en els que dividim la finestra.
		label_estil_dades=ttk.Label(self, text="Introduir dades", style="Titol.TLabel")
		label_frame_dades=ttk.LabelFrame(self, style="Marc.TFrame", labelwidget=label_estil_dades)
		label_frame_dades.grid(row=0, column=0, padx=5, pady=5, ipadx=4, ipady=5)

		label_estil_familiar=ttk.Label(self, text="Buscar familiar del faller", style="Titol.TLabel")
		label_frame_familiar=ttk.LabelFrame(self, style="Marc.TFrame", labelwidget=label_estil_familiar)
		label_frame_familiar.grid(row=1, column=0, padx=5, pady=5, ipady=5)

		# Widgets per a cada frame.

		# Frame "Introduir dades".
		self.label_nom=ttk.Label(label_frame_dades, text="Nom", style="Etiqueta.TLabel")
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

		# Frame "Buscar familiar del faller".
		self.label_opcio_familiar=ttk.Label(label_frame_familiar, text="Familiar en la falla?", style="Etiqueta.TLabel")
		self.label_opcio_familiar.grid(row=0, column=0, padx=5, pady=2, sticky="w")

		self.radio_button_familiar_si=ttk.Radiobutton(
			label_frame_familiar, 
			text="Si",
			style="Radio.TRadiobutton",
			variable=self.familia,
			value=1,
			command=self.habilitar_familia
		)
		self.radio_button_familiar_no=ttk.Radiobutton(
			label_frame_familiar, 
			text="No",
			style="Radio.TRadiobutton",
			variable=self.familia, 
			value=2, 
			command=self.deshabilitar_familia
		)
		self.radio_button_familiar_si.grid(row=1, column=0, padx=5, sticky="w")
		self.radio_button_familiar_no.grid(row=1, column=0)

		self.label_nom_familiar=ttk.Label(label_frame_familiar, text="Cognoms i nom", style="Etiqueta.TLabel")
		self.label_nom_familiar.grid(row=2, column=0, padx=5, pady=2, sticky="w")

		self.combo_box_familiar_faller=ttk.Combobox(
			label_frame_familiar, 
			width=30, 
			postcommand=self.desplegar_familia
		)
		self.combo_box_familiar_faller.grid(row=3, column=0, padx=5)
		self.combo_box_familiar_faller.bind("<<ComboboxSelected>>", self.seleccionar_familia)
		self.combo_box_familiar_faller.configure(state="disabled")

		#Botó "Introduir".
		self.button_introduir=ttk.Button(self, text="Introduir", style="Boto.TButton", command=self.introduir_faller)
		self.button_introduir.grid(row=3, column=0, padx=5, pady=5)


	def iniciar(self):
		'''
		Inicia la nova finestra.
		'''
		self.sexe.set(1)
		self.familia.set(2)
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
		faller=Faller(0,"","","",0,"","","",0,"")					#mirar el tema de metodes de classe en chatgpt (ja esta explicat)
		exercici_actual=arxiu.llegir_exercici_actual()
		try:
			edat=faller.calcular_edat(self.naixement.get(), exercici_actual)	#mirar el tema de metodes de classe en chatgpt (ja esta explicat)
		except:
			messagebox.showerror("Error", "El format per a la data ha de ser dd-mm-aaaa")
		else:
			valor=messagebox.askquestion("Alta nova", "Donar d'alta el nou faller?")
			if valor=="yes":
				bd=BaseDeDades("falla.db")
				category_id=faller.calculate_category(edat)		#mirar el tema de metodes de classe en chatgpt (ja esta explicat)
				faller.category=bd.llegir_categoria(category_id)
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
						familia
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
						familia
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
				self.sexe.set(1)
				self.familia.set(2)
				self.deshabilitar_familia()
				self.entry_nom.focus()
