import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import platform

from utils import Utils
from base_de_dades import BaseDeDades
from arxiu import Arxiu

from falla import Falla
from loteria import Loteria
from moviment import Moviment


class FinestraLoteria(tk.Toplevel):
	'''
	Esta classe representa una nova finestra que depén de la finestra principal.

	Atributs:
	---------
	master : tk.Tk o tk.Toplevel
		La instància principal de l'aplicació o de la finestra que crea esta nova finestra.
	'''

	def __init__(self, master=None):
		'''
		Inicialitza una nova instància de la classe FinestraLoteria.

		Parametres:
		-----------
		master : tk.Tk o tk.Toplevel, opcional
			La instància principal de l'aplicació o de la finestra que crea esta nova finestra.
			Si no es proporciona, es creará una nueva instancia de tk.Tk().
		'''
		super().__init__(master)
		self.master=master
		self.sistema_operatiu=platform.system()
		if self.sistema_operatiu=='Windows':
			self.iconbitmap("escut.ico")
		self.resizable(0,0)
		self.title("Loteria")
		utils=Utils()
		utils.definir_estil_global()
		self.configure(bg="#ffffff", pady=5, padx=5)
	
		self.bloqueig=0

		self.id=tk.IntVar()
		self.paperetes_masculina=tk.IntVar()
		self.paperetes_femenina=tk.IntVar()
		self.paperetes_infantil=tk.IntVar()
		self.decims_masculina=tk.IntVar()
		self.decims_femenina=tk.IntVar()
		self.decims_infantil=tk.IntVar()
		self.diners=tk.IntVar()
		self.benefici=tk.IntVar()
		self.total=tk.IntVar()
		self.total_paperetes_masculina=tk.IntVar()
		self.total_paperetes_femenina=tk.IntVar()
		self.total_paperetes_infantil=tk.IntVar()
		self.total_decims_masculina=tk.IntVar()
		self.total_decims_femenina=tk.IntVar()
		self.total_decims_infantil=tk.IntVar()
		self.total_diners=tk.IntVar()
		self.total_benefici=tk.IntVar()
		self.total_suma=tk.IntVar()

		self.identificadors=[]

		label_estil_introduir=ttk.Label(self, text="Introduir, modificar o eliminar fila", style="Titol.TLabel")
		label_frame_introduir=ttk.LabelFrame(self, style="Marc.TFrame", labelwidget=label_estil_introduir)
		label_frame_introduir.grid(row=0, column=0, ipadx=2, ipady=2)

		label_estil_totals=ttk.Label(self, text="Totals", style="Titol.TLabel")
		label_frame_totals=ttk.LabelFrame(self, style="Marc.TFrame", labelwidget=label_estil_totals)
		label_frame_totals.grid(row=2, column=0, ipadx=2, ipady=2)

		label_estil_sorteig=ttk.Label(self, text="Sorteig", style="Titol.TLabel")
		label_frame_sorteig=ttk.LabelFrame(self, style="Marc.TFrame", labelwidget=label_estil_sorteig)
		label_frame_sorteig.grid(row=3, column=0, ipadx=2, ipady=2)

		# Widgets per a cada frame.

		# Frame "Introduir".
		self.label_nom=ttk.Label(label_frame_introduir, text="Nom")
		self.label_nom.grid(row=0, column=0, padx=2)

		self.label_id=ttk.Label(label_frame_introduir, text="Id")
		self.label_id.grid(row=0, column=1, padx=2)

		self.label_paperetes_masculina=ttk.Label(label_frame_introduir, text="Paperetes Masc")
		self.label_paperetes_masculina.grid(row=0, column=2, padx=2)

		self.label_paperetes_femenina=ttk.Label(label_frame_introduir, text="Paperetes Fem")
		self.label_paperetes_femenina.grid(row=0, column=3, padx=2)

		self.label_paperetes_infantil=ttk.Label(label_frame_introduir, text="Paperetes Inf")
		self.label_paperetes_infantil.grid(row=0, column=4, padx=2)

		self.label_decims_masculina=ttk.Label(label_frame_introduir, text="Dècims Masc")
		self.label_decims_masculina.grid(row=0, column=5, padx=2)

		self.label_decims_femenina=ttk.Label(label_frame_introduir, text="Dècims Fem")
		self.label_decims_femenina.grid(row=0, column=6, padx=2)

		self.label_decims_infantil=ttk.Label(label_frame_introduir, text="Dècims Inf")
		self.label_decims_infantil.grid(row=0, column=7, padx=2)

		self.combo_box_faller=ttk.Combobox(label_frame_introduir, width=30, postcommand=self.desplegar_faller)
		self.combo_box_faller.grid(row=1, column=0)
		self.combo_box_faller.bind("<<ComboboxSelected>>", self.seleccionar_faller)

		self.entry_id=ttk.Entry(label_frame_introduir, state="disabled", textvariable=self.id)
		self.entry_id.grid(row=1, column=1, padx=2)

		self.entry_paperetes_masculina=ttk.Entry(label_frame_introduir, textvariable=self.paperetes_masculina)
		self.entry_paperetes_masculina.grid(row=1, column=2, padx=2)
		self.entry_paperetes_masculina.bind('<FocusOut>', self.calcular_totals)

		self.entry_paperetes_femenina=ttk.Entry(label_frame_introduir, textvariable=self.paperetes_femenina)
		self.entry_paperetes_femenina.grid(row=1, column=3, padx=2)
		self.entry_paperetes_femenina.bind('<FocusOut>', self.calcular_totals)

		self.entry_paperetes_infantil=ttk.Entry(label_frame_introduir, textvariable=self.paperetes_infantil)
		self.entry_paperetes_infantil.grid(row=1, column=4, padx=2)
		self.entry_paperetes_infantil.bind('<FocusOut>', self.calcular_totals)

		self.entry_decims_masculina=ttk.Entry(label_frame_introduir, textvariable=self.decims_masculina)
		self.entry_decims_masculina.grid(row=1, column=5, padx=2)
		self.entry_decims_masculina.bind('<FocusOut>', self.calcular_totals)

		self.entry_decims_femenina=ttk.Entry(label_frame_introduir, textvariable=self.decims_femenina)
		self.entry_decims_femenina.grid(row=1, column=6, padx=2)
		self.entry_decims_femenina.bind('<FocusOut>', self.calcular_totals)

		self.entry_decims_infantil=ttk.Entry(label_frame_introduir, textvariable=self.decims_infantil)
		self.entry_decims_infantil.grid(row=1, column=7, padx=2)
		self.entry_decims_infantil.bind('<FocusOut>', self.calcular_totals)

		self.label_diners=ttk.Label(label_frame_introduir, text="Diners")
		self.label_diners.grid(row=2, column=0, padx=2)

		self.entry_diners=ttk.Entry(label_frame_introduir, state="disabled", textvariable=self.diners)
		self.entry_diners.grid(row=2, column=1, padx=2)

		self.label_benefici=ttk.Label(label_frame_introduir, text="Benefici")
		self.label_benefici.grid(row=2, column=2, padx=2)

		self.entry_benefici=ttk.Entry(label_frame_introduir, state="disabled", textvariable=self.benefici)
		self.entry_benefici.grid(row=2, column=3, padx=2)

		self.label_total=ttk.Label(label_frame_introduir, text="Total")
		self.label_total.grid(row=2, column=4, padx=2)

		self.entry_total=ttk.Entry(label_frame_introduir, state="disabled", textvariable=self.total)
		self.entry_total.grid(row=2, column=5, padx=2)

		self.button_afegir=ttk.Button(label_frame_introduir, style="Boto.TButton", text="Afegir", command=self.afegir_camp)
		self.button_afegir.grid(row=2, column=6, padx=2)

		self.button_modificar=ttk.Button(label_frame_introduir, style="Boto.TButton", state="disabled", text="Modificar", command=self.modificar_fila)
		self.button_modificar.grid(row=2, column=7, padx=2)

		self.button_eliminar=ttk.Button(label_frame_introduir, style="Boto.TButton", state="disabled", text="Eliminar fila", command=self.eliminar_fila)
		self.button_eliminar.grid(row=2, column=8, padx=2)

		self.tree_loteria=ttk.Treeview(self, height=10) #li indiquem la altura
		self.tree_loteria["columns"]=("uno","dos","tres","quatre","cinc","sis","set","vuit","nou","deu","once","dotze")
		self.tree_loteria.column("#0", width=40)
		self.tree_loteria.column("uno", width=160)
		self.tree_loteria.column("dos", width=80)
		self.tree_loteria.column("tres", width=80)
		self.tree_loteria.column("quatre", width=80)
		self.tree_loteria.column("cinc", width=80)
		self.tree_loteria.column("sis", width=80)
		self.tree_loteria.column("set", width=80)
		self.tree_loteria.column("vuit", width=80)
		self.tree_loteria.column("nou", width=80)
		self.tree_loteria.column("deu", width=80)
		self.tree_loteria.column("once", width=80)
		self.tree_loteria.column("dotze", width=40)
		self.tree_loteria.heading("#0", text="id")
		self.tree_loteria.heading("uno", text="nom")
		self.tree_loteria.heading("dos", text="pap. masc.")
		self.tree_loteria.heading("tres", text="pap. fem.")
		self.tree_loteria.heading("quatre", text="pap. inf.")
		self.tree_loteria.heading("cinc", text="dèc. masc.")
		self.tree_loteria.heading("sis", text="dèc. fem.")
		self.tree_loteria.heading("set", text="dèc. inf.")
		self.tree_loteria.heading("vuit", text="diners")
		self.tree_loteria.heading("nou", text="benefici")
		self.tree_loteria.heading("deu", text="total")
		self.tree_loteria.heading("once", text="assignada")
		self.tree_loteria.heading("dotze", text="id faller")
		self.tree_loteria.grid(row=1, column=0, padx=10, pady=5)
		self.tree_loteria.bind("<<TreeviewSelect>>", self.fila_seleccionada)

		self.scroll_taula=ttk.Scrollbar(self, command=self.tree_loteria.yview) #barra de desplaçament per a la taula
		self.scroll_taula.grid(row=1, column=1, sticky="nsew") #la fem de l'altura de la taula

		self.tree_loteria.config(yscrollcommand=self.scroll_taula.set)

		# Frame "Totals".
		self.label_total_paperetes_masculina=ttk.Label(label_frame_totals, text="Paperetes Masc", style="Etiqueta.TLabel")
		self.label_total_paperetes_masculina.grid(row=0, column=0, padx=2)

		self.label_total_paperetes_femenina=ttk.Label(label_frame_totals, text="Paperetes Fem", style="Etiqueta.TLabel")
		self.label_total_paperetes_femenina.grid(row=0, column=1, padx=2)

		self.label_total_paperetes_infantil=ttk.Label(label_frame_totals, text="Paperetes Inf", style="Etiqueta.TLabel")
		self.label_total_paperetes_infantil.grid(row=0, column=2, padx=2)

		self.label_total_decims_masculina=ttk.Label(label_frame_totals, text="Dècims Masc", style="Etiqueta.TLabel")
		self.label_total_decims_masculina.grid(row=0, column=3, padx=2)

		self.label_total_decims_femenina=ttk.Label(label_frame_totals, text="Dècims Fem", style="Etiqueta.TLabel")
		self.label_total_decims_femenina.grid(row=0, column=4, padx=2)

		self.label_total_decims_infantil=ttk.Label(label_frame_totals, text="Dècims Inf", style="Etiqueta.TLabel")
		self.label_total_decims_infantil.grid(row=0, column=5, padx=2)

		self.label_diners=ttk.Label(label_frame_totals, text="Diners", style="Etiqueta.TLabel")
		self.label_diners.grid(row=0, column=6, padx=2)

		self.label_beneficis=ttk.Label(label_frame_totals, text="Benefici", style="Etiqueta.TLabel")
		self.label_beneficis.grid(row=0, column=7, padx=2)

		self.label_total=ttk.Label(label_frame_totals, text="Total", style="Etiqueta.TLabel")
		self.label_total.grid(row=0, column=8, padx=2)

		self.entry_total_paperetes_masculina=ttk.Entry(label_frame_totals, state="disabled", textvariable=self.total_paperetes_masculina)
		self.entry_total_paperetes_masculina.grid(row=1, column=0, padx=2)
		self.total_paperetes_masculina.set("0")

		self.entry_total_paperetes_femenina=ttk.Entry(label_frame_totals, state="disabled", textvariable=self.total_paperetes_femenina)
		self.entry_total_paperetes_femenina.grid(row=1, column=1, padx=2)
		self.total_paperetes_femenina.set("0")

		self.entry_total_paperetes_infantil=ttk.Entry(label_frame_totals, state="disabled", textvariable=self.total_paperetes_infantil)
		self.entry_total_paperetes_infantil.grid(row=1, column=2, padx=2)
		self.total_paperetes_infantil.set("0")

		self.entry_total_decims_masculina=ttk.Entry(label_frame_totals, state="disabled", textvariable=self.total_decims_masculina)
		self.entry_total_decims_masculina.grid(row=1, column=3, padx=2)
		self.total_decims_masculina.set("0")

		self.entry_total_decims_femenina=ttk.Entry(label_frame_totals, state="disabled", textvariable=self.total_decims_femenina)
		self.entry_total_decims_femenina.grid(row=1, column=4, padx=2)
		self.total_decims_femenina.set("0")

		self.entry_total_decims_infantil=ttk.Entry(label_frame_totals, state="disabled", textvariable=self.total_decims_infantil)
		self.entry_total_decims_infantil.grid(row=1, column=5, padx=2)
		self.total_decims_infantil.set("0")

		self.entry_diners=ttk.Entry(label_frame_totals, state="disabled", textvariable=self.total_diners)
		self.entry_diners.grid(row=1, column=6, padx=2)
		self.total_diners.set("0")

		self.entry_benefici=ttk.Entry(label_frame_totals, state="disabled", textvariable=self.total_benefici)
		self.entry_benefici.grid(row=1, column=7, padx=2)
		self.total_benefici.set("0")

		self.entry_total_suma=ttk.Entry(label_frame_totals, state="disabled", textvariable=self.total_suma)
		self.entry_total_suma.grid(row=1, column=8, padx=2)
		self.total_suma.set("0")

		# Frame "Sorteig".
		self.combo_box_sorteig=ttk.Combobox(label_frame_sorteig, width=30, postcommand=self.desplegar_sortejos)
		self.combo_box_sorteig.grid(row=0, column=0)

		self.button_obrir=ttk.Button(label_frame_sorteig, text="Obrir", command=self.obrir)
		self.button_obrir.grid(row=0, column=2, padx=2)

		self.button_guardar=ttk.Button(label_frame_sorteig, text="Guardar", command=self.guardar)
		self.button_guardar.grid(row=0, column=3, padx=2)

		self.button_assignar=ttk.Button(label_frame_sorteig, text="Assignar", command=self.assignar)
		self.button_assignar.grid(row=0, column=4, padx=2)

		self.button_netejar=ttk.Button(label_frame_sorteig, text="Netejar", command=self.netejar)
		self.button_netejar.grid(row=0, column=5, padx=2)

		self.resetejar_camps()



	def resetejar_camps(self): #reseteig dels camps d'entrada

		self.combo_box_faller.focus()
		self.paperetes_masculina.set("0")
		self.paperetes_femenina.set("0")
		self.paperetes_infantil.set("0")
		self.decims_masculina.set("0")
		self.decims_femenina.set("0")
		self.decims_infantil.set("0")
		self.diners.set("0")
		self.benefici.set("0")
		self.total_suma.set("0")

	
	def desplegar_faller(self):
		'''
		Controla el combobox comparant la cadena escrita amb la base de dades i mostrant els resultats en el combobox.
		Utilitza l'atribut "self.identificadors" per a passar el identificador de faller a la funció "seleccionar_faller".
		'''
		#bd=BaseDeDades("falla.db")
		falla=Falla()
		cadena=self.combo_box_faller.get()
		llistat_fallers=falla.llegir_fallers_per_cognom(cadena)
		llista=[] # Llista on anem a acumular els valors.
		self.identificadors=[]
		for faller in llistat_fallers:
			self.identificadors=self.identificadors+[faller.id]
			llista=llista + [(faller.cognoms + ", " + faller.nom)]
		self.combo_box_faller["values"]=llista # Insertem cada valor en el desplegable.
		#bd.tancar_conexio()


	def seleccionar_faller(self, event):
		'''
		Controla la selecció del combobox per a guardar el identificador del faller i omplir les dades a partir d'aquest.
		'''
		index=self.combo_box_faller.current()
		self.id.set(self.identificadors[index])
		self.identificadors=[]
		#self.omplir_dades(self.id.get())


	def omplir_nom(self, id):
		bd=BaseDeDades('falla.db')
		faller=bd.llegir_faller(id)
		self.combo_box_faller.set(faller.cognoms + ", " + faller.nom)
		bd.tancar_conexio()


	def calcular_totals(self, event):
		self.diners.set((self.paperetes_masculina.get()*4) + (self.paperetes_femenina.get()*4) + (self.paperetes_infantil.get()*4) + 
				(self.decims_masculina.get()*20) + (self.decims_femenina.get()*20) + (self.decims_infantil.get()*20))
		self.benefici.set(self.paperetes_masculina.get() + self.paperetes_femenina.get() + self.paperetes_infantil.get() +
				(self.decims_masculina.get()*3) + (self.decims_femenina.get()*3) + (self.decims_infantil.get()*3))
		self.total.set(self.diners.get() + self.benefici.get())


	def afegir_camp(self):
		self.calcular_totals('<FocusOut>') # Fem un càlcul del total per si no s'haguera fet abans.
		if self.id.get()=="":
			messagebox.showwarning("Error", "El camp nom ha de contindre un nom de faller vàlid")
		else:
			self.tree_loteria.insert("", "end", text=self.id.get(),
				values=(self.combo_box_faller.get(), self.paperetes_masculina.get(), self.paperetes_femenina.get(), self.paperetes_infantil.get(),
			   	self.decims_masculina.get(), self.decims_femenina.get(), self.decims_infantil.get(),
				self.diners.get(), self.benefici.get(), self.total.get(), 0, self.id.get()))
			# Acumulem en els camps totals cada valor afegit.
			self.total_paperetes_masculina.set(self.total_paperetes_masculina.get() + self.paperetes_masculina.get())
			self.total_paperetes_femenina.set(self.total_paperetes_femenina.get() + self.paperetes_femenina.get())
			self.total_paperetes_infantil.set(self.total_paperetes_infantil.get() + self.paperetes_infantil.get())
			self.total_decims_masculina.set(self.total_decims_masculina.get() + self.decims_masculina.get())
			self.total_decims_femenina.set(self.total_decims_femenina.get() + self.decims_femenina.get())
			self.total_decims_infantil.set(self.total_decims_infantil.get() + self.decims_infantil.get())
			self.total_diners.set(self.total_diners.get() + self.diners.get())
			self.total_benefici.set(self.total_benefici.get() + self.benefici.get())
			self.total_suma.set(self.total_suma.get() + self.total.get())
			# Resetejem camps.
			self.id.set("")
			self.combo_box_faller.set("")
			self.resetejar_camps()


	def fila_seleccionada(self, event):
		fila=self.tree_loteria.selection()
		self.combo_box_faller.config(state="disabled")
		self.button_modificar.config(state="normal")
		self.button_eliminar.config(state="normal")
		id=self.tree_loteria.item(fila, option="text")
		llista_dades=self.tree_loteria.item(fila, option="values")
		if llista_dades[10]==1:
			messagebox.showwarning("Error", "No es pot seleccionar una fila que ja ha segut assignada")
		else:
			self.combo_box_faller.set(llista_dades[0])
			self.id.set(llista_dades[11])
			self.paperetes_masculina.set(llista_dades[1])
			self.paperetes_femenina.set(llista_dades[2])
			self.paperetes_infantil.set(llista_dades[3])
			self.decims_masculina.set(llista_dades[4])
			self.decims_femenina.set(llista_dades[5])
			self.decims_infantil.set(llista_dades[6])
			self.calcular_totals('<FocusOut>') # Calculem la resta de camps.


	def modificar_fila(self):
		bd=BaseDeDades('falla.db')
		utils=Utils()
		data=utils.calcular_data_actual()
		self.calcular_totals('<FocusOut>') # Calculem els totals per si no s'ha fet abans.
		fila=self.tree_loteria.selection()
		id=self.tree_loteria.item(fila, option="text")
		llista_dades=self.tree_loteria.item(fila, option="values")
		sorteig=self.combo_box_sorteig.get()
		if llista_dades[10]==1:
			messagebox.showerror("Error", "No es pot modificar una fila de loteria ja assignada")
		else:
			# Restem els valors dels camps de la fila que anem a modificar.
			self.total_paperetes_masculina.set(self.total_paperetes_masculina.get()-llista_dades[1])
			self.total_paperetes_femenina.set(self.total_paperetes_femenina.get()-llista_dades[2])
			self.total_paperetes_infantil.set(self.total_paperetes_infantil.get()-llista_dades[3])
			self.total_decims_masculina.set(self.total_decims_masculina.get()-llista_dades[4])
			self.total_decims_femenina.set(self.total_decims_femenina.get()-llista_dades[5])
			self.total_decims_infantil.set(self.total_decims_infantil.get()-llista_dades[6])
			self.total_diners.set(self.total_diners.get()-llista_dades[7])
			self.total_benefici.set(self.total_benefici.get()-llista_dades[8])
			self.total_suma.set(self.total_suma.get()-llista_dades[9])
			# Passem a la taula els valors modificats prèviament.
			self.tree_loteria.item(fila, text=self.id.get(), values=(self.combo_box_faller.get(),
				self.paperetes_masculina.get(), self.paperetes_femenina.get(), self.paperetes_infantil.get(),
				self.decims_masculina.get(), self.decims_femenina.get(), self.decims_infantil.get(),
				self.diners.get(), self.benefici.get(), self.total.get()))
			# Sumem els nous valors dels camps.
			self.total_paperetes_masculina.set(self.total_paperetes_masculina.get()+self.paperetes_masculina.get())
			self.total_paperetes_femenina.set(self.total_paperetes_femenina.get()+self.paperetes_femenina.get())
			self.total_paperetes_infantil.set(self.total_paperetes_infantil.get()+self.paperetes_infantil.get())
			self.total_decims_masculina.set(self.total_decims_masculina.get()+self.decims_masculina.get())
			self.total_decims_femenina.set(self.total_decims_femenina.get()+self.decims_femenina.get())
			self.total_decims_infantil.set(self.total_decims_infantil.get()+self.decims_infantil.get())
			self.total_diners.set(self.total_diners.get()+self.diners.get())
			self.total_benefici.set(self.total_benefici.get()+self.benefici.get())
			self.total_suma.set(self.total_suma.get()+self.total.get())
			# Mirem si el registre està en la base de dades i en cas de ser així el modifiquem.
			ultim_id=bd.llegir_ultim_id_loteria()
			if ultim_id<=id:
				messagebox.showinfo("Info", "El registre encara no està a la base de dades. Es guardarà al fer clic en Guardar junt amb la resta de registres")
			else:
				loteria=Loteria(id, sorteig, data, self.paperetes_masculina.get(), self.paperetes_femenina.get(), self.paperetes_infantil.get(),
					self.decims_masculina.get(), self.decims_femenina.get(), self.decims_infantil.get(), 0)
				bd.actualitzar_loteria(loteria)
		# Resetegem camps.
		self.id.set("")
		self.combo_box_faller.set("")
		self.combo_box_faller.config(state="normal")
		self.button_modificar.config(state="disabled")
		self.button_eliminar.config(state="disabled")
		self.resetejar_camps()
		bd.tancar_conexio()


	def eliminar_fila(self):
		bd=BaseDeDades('falla.db')
		fila=self.tree_loteria.selection()
		id=self.tree_loteria.item(fila, option="text")
		llista_dades=self.tree_loteria.item(fila, option="values")
		# Podem borrar en el cas de que la loteria no estiga assignada.
		if llista_dades[10]==1:
			messagebox.showerror("Error", "No es pot eliminar una fila de loteria ja assignada")
		else:
			# Restem els valors de la fila que anem a borrar.
			self.total_paperetes_masculina.set(self.total_paperetes_masculina.get()-llista_dades[1])
			self.total_paperetes_femenina.set(self.total_paperetes_femenina.get()-llista_dades[2])
			self.total_paperetes_infantil.set(self.total_paperetes_infantil.get()-llista_dades[3])
			self.total_decims_masculina.set(self.total_decims_masculina.get()-llista_dades[4])
			self.total_decims_femenina.set(self.total_decims_femenina.get()-llista_dades[5])
			self.total_decims_infantil.set(self.total_decims_infantil.get()-llista_dades[6])
			self.total_diners.set(self.total_diners.get()-llista_dades[7])
			self.total_benefici.set(self.total_benefici.get()-llista_dades[8])
			self.total_suma.set(self.total_suma.get()-llista_dades[9])
			# Eliminem la fila a l'arbre.
			self.tree_loteria.delete(fila)
			# Eliminem el registre de la fila a la base de dades en cas de que ja estiga guardat.
			ultim_id=bd.llegir_ultim_id_loteria()
			if ultim_id>id:
				bd.eliminar_loteria(id)
		# Canviem la configuració dels botons.
		self.combo_box_faller.config(state="normal")
		self.button_modificar.config(state="disabled")
		self.button_eliminar.config(state="disabled")
		bd.tancar_conexio()


	def desplegar_sortejos(self):
		bd=BaseDeDades('falla.db')
		llistat_sortejos=bd.llegir_sortejos()
		self.combo_box_sorteig["values"]=llistat_sortejos
		bd.tancar_conexio()


	def obrir(self):
		sorteig=self.combo_box_sorteig.get()
		# Resetegem tot per a obrir sobre formulari en blanc.
		self.resetejar_camps()
		self.tree_loteria.delete(*self.tree_loteria.get_children()) # Borrem les dades de la taula.
		self.id.set("")
		self.combo_box_faller.config(state="normal")
		self.combo_box_faller.set("")
		self.total_paperetes_masculina.set("0")
		self.total_paperetes_femenina.set("0")
		self.total_paperetes_infantil.set("0")
		self.total_decims_masculina.set("0")
		self.total_decims_femenina.set("0")
		self.total_decims_infantil.set("0")
		self.total_diners.set("0")
		self.total_benefici.set("0")
		self.total_suma.set("0")
		# Traguem el llistat de loteries corresponent al sorteig triat.
		bd=BaseDeDades('falla.db')
		llistat_loteries=bd.llegir_loteries_per_sorteig(sorteig)
		total_paperetes_masculina=0
		total_paperetes_femenina=0
		total_paperetes_infantil=0
		total_decims_masculina=0
		total_decims_femenina=0
		total_decims_infantil=0
		total_diners=0
		total_benefici=0
		for loteria in llistat_loteries:
			total_paperetes_masculina=total_paperetes_masculina + loteria.paperetes_masculina
			total_paperetes_femenina=total_paperetes_femenina + loteria.paperetes_femenina
			total_paperetes_infantil=total_paperetes_infantil + loteria.paperetes_infantil
			total_decims_masculina=total_decims_masculina + loteria.decims_masculina
			total_decims_femenina=total_decims_femenina + loteria.decims_femenina
			total_decims_infantil=total_decims_infantil + loteria.decims_infantil
			diners=loteria.calcular_diners()
			total_diners=total_diners + diners
			benefici=loteria.calcular_benefici()
			total_benefici=total_benefici + benefici
			total=diners+benefici
			nom=loteria.faller.cognoms + ", " + loteria.faller.nom
			llista_dades=[nom, loteria.paperetes_masculina, loteria.paperetes_femenina, loteria.paperetes_infantil, loteria.decims_masculina, loteria.decims_femenina, loteria.decims_infantil, diners, benefici, total, loteria.assignada]
			self.tree_loteria.insert("", "end", text=loteria.id, values=llista_dades)
		bd.tancar_conexio()


	def guardar(self):
		utils=Utils()
		data=utils.calcular_data_actual
		bd=BaseDeDades('falla.db')
		sorteig=self.combo_box_sorteig.get()
		ultim_id=bd.llegir_ultim_id_loteria()
		llistat_files=self.tree_loteria.get_children()
		for fila in llistat_files:
			id=self.tree_loteria.item(fila, option="text")
			llistat_dades=self.tree_loteria.item(fila, option="values")
			faller=bd.llegir_faller(llistat_dades[12])
			loteria=Loteria(id, sorteig, data, llistat_dades[1], llistat_dades[2], llistat_dades[3], llistat_dades[4], llistat_dades[5], llistat_dades[6], faller)
			if id>ultim_id:
				bd.crear_loteria(loteria)
		bd.tancar_conexio()


	def assignar(self):
		valor=messagebox.askquestion("Assignar", "Es guardaran tots els registres pendents i s'assignaran els diners i beneficis. L'operació no es pot desfer")
		if valor=="yes":
			utils=Utils()
			data=utils.calcular_data_actual()
			arxiu=Arxiu('exercici')
			exercici_actual=arxiu.llegir_exercici_actual()
			self.guardar()
			llistat_files=self.tree_loteria.get_children()
			bd=BaseDeDades('falles.db')
			for fila in llistat_files:
				id=self.tree_loteria.item(fila, option="text")
				llistat_dades=self.tree_loteria.item(fila, option="values")
				moviment=Moviment(0, data, llistat_dades[8], 1, 2, exercici_actual, self.combo_box_sorteig.get())
				bd.crear_moviment(moviment)
				moviment=Moviment(0, data, llistat_dades[9], 2, 1, exercici_actual, self.combo_box_sorteig.get())
				bd.crear_moviment(moviment)
				# Actualització de tots els registres a estat assignat.
				bd.actualitzar_assignada_loteria(id)
			self.button_assignar.config(state="disabled")


	def netejar(self):

		self.resetejar_camps()
		self.tree_loteria.delete(*self.tree_loteria.get_children())
		self.id.set("")
		self.combo_box_faller.config(state="normal")
		self.combo_box_faller.set("")
		self.total_paperetes_masculina.set("0")
		self.total_paperetes_femenina.set("0")
		self.total_paperetes_infantil.set("0")
		self.total_decims_masculina.set(0)
		self.total_decims_femenina.set(0)
		self.total_decims_infantil.set(0)
		self.total_diners.set(0)
		self.total_benefici-set(0)
		self.total_suma.set(0)
		self.combo_box_sorteig.set("")
		self.button_afegir.config(state="normal")
		self.button_assignar.config(state="normal")