import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import LabelFrame

from base_de_dades import BaseDeDades
from arxiu import Arxiu


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
		self.resizable(0,0)
		self.title("Introduir Faller")
		self.iconbitmap("escut.ico")

		self.id=StringVar()
		self.infantil=StringVar()
		self.punts=StringVar()
		self.adult=StringVar()
		self.falla=StringVar()
		self.any_inici=StringVar()
		self.any_final=StringVar()

		self.identificadors=[]

		label_frame_buscar=LabelFrame(self, text="Buscar faller")
		label_frame_buscar.grid(row=0, column=0, ipadx=2, ipady=2)

		self.label_nom=Label(label_frame_buscar, text="Nom")
		self.label_nom.grid(row=0, column=0, padx=2)

		self.combo_box_faller=ttk.Combobox(label_frame_buscar, width=30, postcommand=self.dropdown_opened_historial)
		self.combo_box_faller.grid(row=0, column=1)
		self.combo_box_faller.bind("<<ComboboxSelected>>", self.selection_changed_historial)

		self.label_id=Label(label_frame_buscar, text="Id")
		self.label_id.grid(row=0, column=2, padx=2)

		self.entry_id=Entry(label_frame_buscar, state="disabled", textvariable=self.id)
		self.entry_id.grid(row=0, column=3, padx=2)

		self.tree_historial=ttk.Treeview(self, height=10)
		self.tree_historial["columns"]=("uno", "dos", "tres", "quatre")
		self.tree_historial.column("#0", width=80)
		self.tree_historial.column("uno", width=80)
		self.tree_historial.column("dos", width=80)
		self.tree_historial.column("tres", width=80)
		self.tree_historial.column("quatre", width=80)
		self.tree_historial.heading("#0", text="exercici")
		self.tree_historial.heading("uno", text="càrrec")
		self.tree_historial.heading("dos", text="punts")
		self.tree_historial.heading("tres", text="anys")
		self.tree_historial.heading("quatre", text="falla")
		self.tree_historial.grid(row=1, column=0, padx=10, pady=5)
		#self.tree_historial.bind("<<TreeviewSelect>>", self.item_selected)

		self.scroll_taula=Scrollbar(self, command=self.tree_historial.yview)
		self.scroll_taula.grid(row=1, column=1, sticky="nsew")

		self.tree_historial.config(yscrollcommand=self.scroll_taula.set)

		label_frame_totals=LabelFrame(self, text="Totals")
		label_frame_totals.grid(row=2, column=0, ipadx=2, ipady=2)

		self.label_infantil=Label(label_frame_totals, text="Anys d'infantil:")
		self.label_infantil.grid(row=0, column=0, padx=2)

		self.entry_infantil=Entry(label_frame_totals, state="disabled", textvariable=self.infantil)
		self.entry_infantil.grid(row=0, column=1, padx=2)

		self.label_punts=Label(label_frame_totals, text="Punts:")
		self.label_punts.grid(row=0, column=2, padx=2)

		self.entry_punts=Entry(label_frame_totals, state="disabled", textvariable=self.punts)
		self.entry_punts.grid(row=0, column=3, padx=2)

		self.label_adult=Label(label_frame_totals, text="Anys d'adult:")
		self.label_adult.grid(row=0, column=4, padx=2)

		self.entry_adult=Entry(label_frame_totals, state="disabled", textvariable=self.adult)
		self.entry_adult.grid(row=0, column=5, padx=2)

		label_frame_modificar=LabelFrame(self, text="Modificar")
		label_frame_modificar.grid(row=3, column=0, ipadx=2, ipady=2)

		self.label_interval=Label(label_frame_modificar, text="Interval d'anys:")
		self.label_interval.grid(row=1, column=0, padx=2)

		self.entry_any_inici=Entry(label_frame_modificar, textvariable=self.any_inici)
		self.entry_any_inici.grid(row=1, column=1, padx=2)

		self.entry_any_final=Entry(label_frame_modificar, textvariable=self.any_final)
		self.entry_any_final.grid(row=1, column=2, padx=2)

		self.combo_box_carrec=ttk.Combobox(label_frame_modificar, width=20, state="readonly", values=["baixa", "vocal", "fallera major infantil", "president infantil", "directiu", "cort JFL", "fallera major", "president", "fallera major Alzira", "president JLF"])
		self.combo_box_carrec.grid(row=1, column=3)

		self.label_falla=Label(label_frame_modificar, text="Falla:")
		self.label_falla.grid(row=1, column=4, padx=2)

		self.entry_falla=Entry(label_frame_modificar, textvariable=self.falla)
		self.entry_falla.grid(row=1, column=5, padx=2)

		self.button_modificar=Button(label_frame_modificar, text="Modificar càrrec", command=self.modificar)
		self.button_modificar.grid(row=1, column=6)


	def iniciar(self):
		'''
		Inicia la nova finestra.
		'''
		self.grab_set()
		self.transient(self.master)
		self.mainloop()
	
	
	def dropdown_opened_historial(self):

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


	def selection_changed_historial(self, event):

		index=self.combo_box_faller.current()
		self.id.set(self.identificadors[index])
		cadena=self.id.get()
		self.identificadors=[]
		self.OmplirHistorial(cadena)


	def OmplirHistorial(self, num):

		bd=BaseDeDades("falla.db")
		faller=bd.llegir_faller(num)
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
		anycadete=anyexercici+14 #afegim 14 anys a l'any del primer exercici per a treure el primer de cadet
		while (anyexercici < anycadete) and (anyexercici <= exercici_actual): #traguem els anys de cadet
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
		while anyexercici <= exercici_actual: #traguem els punts i anys d'adult
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
		self.infantil.set(anysinfantil)
		self.punts.set(punts)
		self.adult.set(anysadult)


	def modificar(self):

		nom_arxiu="historials"+"/"+self.id.get()
		arxiu=Arxiu(nom_arxiu)
		anyinici=int(self.any_inici.get())
		anyfinal=int(self.any_final.get())
		carrec=self.combo_box_carrec.get()
		falla=self.falla.get()
		historial=arxiu.llegir_historial()
		while anyinici<=anyfinal:
			llista=[carrec, falla]
			historial[anyinici]=llista
			anyinici=anyinici+1
		arxiu.modificar_historial(historial)
		cadena=self.id.get()
		self.OmplirHistorial(cadena)
		