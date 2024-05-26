import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import platform

from export_sqlite_to_mariadb import BaseDeDades
from arxiu import Arxiu
from utils import Utils


class FinestraHistorial(tk.Toplevel):
	'''
	Esta classe representa una nova finestra que depén de la finestra principal.

	Atributs:
	---------
	master : tk.Tk o tk.Toplevel
		La instància principal de l'aplicació o de la finestra que crea esta nova finestra.
	'''


	def __init__(self, master=None):
		'''
		Inicialitza una nova instància de la classe FinestraHistorial.

		Parametres:
		-----------
		master : tk.Tk o tk.Toplevel, opcional
			La instància principal de l'aplicació o de la finestra que crea esta nova finestra.
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

		self.id=tk.StringVar()
		self.infantil=tk.StringVar()
		self.punts=tk.StringVar()
		self.adult=tk.StringVar()
		self.falla=tk.StringVar()
		self.any_inici=tk.StringVar()
		self.any_final=tk.StringVar()

		self.identificadors=[] # Atribut per guardar els id_faller del llistat del combo.

		# Frames en els que dividim la finestra.
		label_estil_buscar=ttk.Label(self, text="Buscar faller", style="Titol.TLabel")
		label_frame_buscar=ttk.LabelFrame(self, style="Marc.TFrame", labelwidget=label_estil_buscar)
		label_frame_buscar.grid(row=0, column=0, ipadx=3, ipady=5, pady=5)

		label_frame_taula=tk.LabelFrame(self, borderwidth=0, background="#ffffff")
		label_frame_taula.grid(row=1, column=0, padx=10, pady=10)

		label_estil_totals=ttk.Label(self, text="Totals", style="Titol.TLabel")
		label_frame_totals=ttk.LabelFrame(self, style="Marc.TFrame", labelwidget=label_estil_totals)
		label_frame_totals.grid(row=2, column=0, ipady=5, pady=5)

		label_estil_modificar=ttk.Label(self, text="Modificar", style="Titol.TLabel")
		label_frame_modificar=ttk.LabelFrame(self, style="Marc.TFrame", labelwidget=label_estil_modificar)
		label_frame_modificar.grid(row=3, column=0, ipadx=3, ipady=5, pady=5)

		# Widgets per a cada frame.

		# Frame "Buscar".
		self.label_nom=ttk.Label(label_frame_buscar, text="Nom", style="Etiqueta.TLabel")
		self.label_nom.grid(row=0, column=0, padx=2)

		self.combo_box_faller=ttk.Combobox(label_frame_buscar, width=30, postcommand=self.desplegar_historial)
		self.combo_box_faller.grid(row=0, column=1)
		self.combo_box_faller.bind("<<ComboboxSelected>>", self.seleccionar_historial)

		self.label_id=ttk.Label(label_frame_buscar, text="Id", style="Etiqueta.TLabel")
		self.label_id.grid(row=0, column=2, padx=2)

		self.entry_id=ttk.Entry(label_frame_buscar, state="disabled", textvariable=self.id)
		self.entry_id.grid(row=0, column=3, padx=2)

		# Frame "Taula".
		self.tree_historial=ttk.Treeview(label_frame_taula, height=10)
		self.tree_historial["columns"]=("uno", "dos", "tres", "quatre")
		self.tree_historial.column("#0", width=80)
		self.tree_historial.column("uno", width=80)
		self.tree_historial.column("dos", width=80)
		self.tree_historial.column("tres", width=80)
		self.tree_historial.column("quatre", width=120)
		self.tree_historial.heading("#0", text="exercici")
		self.tree_historial.heading("uno", text="càrrec")
		self.tree_historial.heading("dos", text="punts")
		self.tree_historial.heading("tres", text="anys")
		self.tree_historial.heading("quatre", text="falla")
		self.tree_historial.grid(row=1, column=0)

		self.scroll_taula=ttk.Scrollbar(label_frame_taula, command=self.tree_historial.yview)
		self.scroll_taula.grid(row=1, column=1, sticky="nsew")

		self.tree_historial.config(yscrollcommand=self.scroll_taula.set)

		# Frame "Totals".
		self.label_infantil=ttk.Label(label_frame_totals, text="Anys d'infantil", style="Etiqueta.TLabel")
		self.label_infantil.grid(row=0, column=0, padx=5, pady=2, sticky="w")

		self.entry_infantil=ttk.Entry(label_frame_totals, style="Entrada.TEntry", state="disabled", textvariable=self.infantil)
		self.entry_infantil.grid(row=1, column=0, padx=5, sticky="w")

		self.label_punts=ttk.Label(label_frame_totals, text="Punts", style="Etiqueta.TLabel")
		self.label_punts.grid(row=0, column=1, padx=5, pady=2, sticky="w")

		self.entry_punts=ttk.Entry(label_frame_totals, style="Entrada.TEntry", state="disabled", textvariable=self.punts)
		self.entry_punts.grid(row=1, column=1, padx=5, sticky="w")

		self.label_adult=ttk.Label(label_frame_totals, text="Anys d'adult", style="Etiqueta.TLabel")
		self.label_adult.grid(row=0, column=2, padx=5, pady=2, sticky="w")

		self.entry_adult=ttk.Entry(label_frame_totals, style="Entrada.TEntry", state="disabled", textvariable=self.adult)
		self.entry_adult.grid(row=1, column=2, padx=5, sticky="w")

		# Frame "Modificar".
		self.label_inicial=ttk.Label(label_frame_modificar, text="Any inicial", style="Etiqueta.TLabel")
		self.label_inicial.grid(row=0, column=0, padx=5, pady=2, sticky="w")

		self.entry_any_inici=ttk.Entry(label_frame_modificar, state="disabled", textvariable=self.any_inici)
		self.entry_any_inici.grid(row=1, column=0, padx=5, sticky="w")

		self.label_final=ttk.Label(label_frame_modificar, text="Any final", style="Etiqueta.TLabel")
		self.label_final.grid(row=2, column=0, padx=5, pady=2, sticky="w")

		self.entry_any_final=ttk.Entry(label_frame_modificar, state="disabled", textvariable=self.any_final)
		self.entry_any_final.grid(row=3, column=0, padx=5, sticky="w")

		self.label_carrec=ttk.Label(label_frame_modificar, text="Càrrec", style="Etiqueta.TLabel")
		self.label_carrec.grid(row=0, column=1, padx=5, pady=2, sticky="w")

		self.combo_box_carrec=ttk.Combobox(label_frame_modificar, width=20, state="disabled", values=["baixa", "vocal", "fallera major infantil", "president infantil", "directiu", "cort JFL", "fallera major", "president", "fallera major Alzira", "president JLF"])
		self.combo_box_carrec.current(1)
		self.combo_box_carrec.grid(row=1, column=1, padx=5, sticky="w")

		self.label_falla=ttk.Label(label_frame_modificar, text="Falla", style="Etiqueta.TLabel")
		self.label_falla.grid(row=2, column=1, padx=5, pady=2, sticky="w")

		self.entry_falla=ttk.Entry(label_frame_modificar, state="disabled", textvariable=self.falla)
		self.falla.set("Sants Patrons")
		self.entry_falla.grid(row=3, column=1, padx=5, sticky="w")

		self.button_modificar=ttk.Button(label_frame_modificar, state="disabled", text="Modificar historial", style="Boto.TButton", command=self.modificar)
		self.button_modificar.grid(row=2, column=2, rowspan=2, padx=5, sticky="s")


	def iniciar(self):
		'''
		Inicia la nova finestra.
		'''
		self.grab_set()
		self.transient(self.master)
		self.mainloop()
	
	
	def desplegar_historial(self):
		'''
		Controla el combobox comparant la cadena escrita amb la base de dades i mostrant els resultats en el combobox.
		Utilitza l'atribut "self.identificadors" per a passar el identificador de faller a la funció "seleccionar_historial".
		'''
		bd=BaseDeDades("falla.db")
		cadena=self.combo_box_faller.get()
		llistat_fallers=bd.llegir_fallers_per_cognom(cadena)
		llista=[]
		self.identificadors=[]
		for faller in llistat_fallers:
			self.identificadors=self.identificadors+[faller.id]
			llista=llista + [(faller.cognoms + ", " + faller.nom)]
		self.combo_box_faller["values"]=llista
		bd.tancar_conexio()


	def seleccionar_historial(self, event):
		'''
		Controla la selecció del combobox per a guardar el identificador del faller i omplir l'historial a partir d'aquest.
		'''
		index=self.combo_box_faller.current()
		self.id.set(self.identificadors[index])
		cadena=self.id.get()
		self.identificadors=[]
		self.omplir_historial(cadena)


	def omplir_historial(self, id):
		'''
		Ompli l'historial del faller a partir de l'id.
		'''
		bd=BaseDeDades("falla.db")
		faller=bd.llegir_faller(id)
		self.combo_box_faller.set(faller.cognoms + ", " + faller.nom)
		self.tree_historial.delete(*self.tree_historial.get_children())
		nom_arxiu="historials"+"/"+str(faller.id)
		arxiu=Arxiu(nom_arxiu)
		historial=arxiu.llegir_historial()
		anyexercici=faller.calcular_primer_exercici(faller.naixement)
		arxiu=Arxiu("exercici")
		exercici_actual=arxiu.llegir_exercici_actual()
		punts=0
		anysinfantil=0
		anysadult=0
		anycadete=anyexercici+14 # Afegim 14 anys a l'any del primer exercici per a treure el primer any de cadet.
		while (anyexercici < anycadete) and (anyexercici <= exercici_actual): # Calculem els anys d'infantil.
			llista=historial[anyexercici]
			carrec=llista[0]
			falla=llista[1]
			if carrec=="baixa":
				self.tree_historial.insert("", "end", text=anyexercici, values=(carrec, 0, 0, falla))
			if carrec=="vocal":
				self.tree_historial.insert("", "end", text=anyexercici, values=(carrec, 0, 1, falla))
				anysinfantil=anysinfantil+1
			if carrec=="fallera major infantil" or carrec=="president infantil":
				self.tree_historial.insert("", "end", text=anyexercici, values=(carrec, 0, 2, falla))
				anysinfantil=anysinfantil+2
			anyexercici=anyexercici+1
		while anyexercici <= exercici_actual: # Calculem els punts i anys d'adult.
			llista=historial[anyexercici]
			carrec=llista[0]
			falla=llista[1]
			if carrec=="baixa":
				self.tree_historial.insert("", "end", text=anyexercici, values=(carrec, 0, 0, falla))
			if carrec=="vocal":
				if punts>=100:
					self.tree_historial.insert("", "end", text=anyexercici, values=(carrec, 0, 1, falla))
					anysadult=anysadult+1
				else:
					self.tree_historial.insert("", "end", text=anyexercici, values=(carrec, 5, 0, falla))
					punts=punts+5
			if carrec=="directiu" or carrec=="cort JLF":
				if punts>=100:
					self.tree_historial.insert("", "end", text=anyexercici, values=(carrec, 0, 1, falla))
					anysadult=anysadult+1
				else:
					self.tree_historial.insert("", "end", text=anyexercici, values=(carrec, 8, 0, falla))
					punts=punts+8
			if carrec=="fallera major" or carrec=="president":
				if punts>=100:
					self.tree_historial.insert("", "end", text=anyexercici, values=(carrec, 0, 1, falla))
					anysadult=anysadult+1
				else:
					self.tree_historial.insert("", "end", text=anyexercici, values=(carrec, 10, 0, falla))
					punts=punts+10
			if carrec=="fallera major Alzira" or carrec=="president JLF":
				if punts>=100:
					self.tree_historial.insert("", "end", text=anyexercici, values=(carrec, 0, 1, falla))
					anysadult=anysadult+1
				else:
					self.tree_historial.insert("", "end", text=anyexercici, values=(carrec, 12, 0, falla))
					punts=punts+12
			anyexercici=anyexercici+1
		# Omplim les dades finals calculades.
		self.infantil.set(anysinfantil)
		self.punts.set(punts)
		self.adult.set(anysadult)
		# Fiquem en marxa els camps i botons per a poder modificar l'historial.
		self.entry_any_inici.config(state="normal")
		self.entry_any_final.config(state="normal")
		self.combo_box_carrec.config(state="readonly")
		self.entry_falla.config(state="normal")
		self.button_modificar.config(state="normal")
		bd.tancar_conexio()


	def modificar(self):
		'''
		Modifica l'historial del faller amb les dades del formulari.
		'''
		nom_arxiu="historials"+"/"+self.id.get()
		arxiu=Arxiu(nom_arxiu)
		try:
			anyinici=int(self.any_inici.get())
			anyfinal=int(self.any_final.get())
		except ValueError:
			messagebox.showwarning("Error", "Has d'escriure un any vàlid")
		else:
			carrec=self.combo_box_carrec.get()
			falla=self.falla.get()
			historial=arxiu.llegir_historial()
			if anyfinal<anyinici:
				messagebox.showwarning("Error", "L'any inicial ha de ser menor o igual a l'any final")
			while anyinici<=anyfinal:
				llista=[carrec, falla]
				historial[anyinici]=llista
				anyinici=anyinici+1
			arxiu.modificar_historial(historial)
			cadena=self.id.get()
			self.omplir_historial(cadena)
		