import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import platform
from pathlib import Path

from utils import Utils
from arxiu import Arxiu

from falla import Falla
from lottery import Lottery
from movement import Movement
from member import Member
from family import Family
from category import Category


class ManageLotteryWindow(tk.Toplevel):
	'''
	Esta classe representa una nova finestra que depén de la finestra principal.

	Atributs:
	---------
	master : tk.Tk o tk.Toplevel
		La instància principal de l'aplicació o de la finestra que crea esta nova finestra.
	'''

	def __init__(self, master = None):
		'''
		Inicialitza una nova instància de la classe ManageLotteryWindow.

		Parametres:
		-----------
		master : tk.Tk o tk.Toplevel, opcional
			La instància principal de l'aplicació o de la finestra que crea esta nova finestra.
			Si no es proporciona, es creará una nueva instancia de tk.Tk().
		'''
		super().__init__(master)
		self.master = master
		self.sistema_operatiu = platform.system()
		base_path = Path(__file__).parent.resolve()
		if self.sistema_operatiu == 'Windows':
			self.iconbitmap(base_path / 'images' / 'escut.ico')
		self.resizable(0,0)
		self.title("Loteria")
		utils = Utils()
		utils.define_global_style()
		self.configure(bg = "#ffffff", pady = 5, padx = 5)
	
		self.blockade = 0

		self.member_id = tk.IntVar()
		self.tickets_male = tk.IntVar()
		self.tickets_female = tk.IntVar()
		self.tickets_childish = tk.IntVar()
		self.tenths_male = tk.IntVar()
		self.tenths_female = tk.IntVar()
		self.tenths_childish = tk.IntVar()
		self.price = tk.IntVar()
		self.benefit = tk.IntVar()
		self.total = tk.IntVar()
		self.total_tickets_male = tk.IntVar()
		self.total_tickets_female = tk.IntVar()
		self.total_tickets_childish = tk.IntVar()
		self.total_tenths_male = tk.IntVar()
		self.total_tenths_female = tk.IntVar()
		self.total_tenths_childish = tk.IntVar()
		self.total_price = tk.IntVar()
		self.total_benefit = tk.IntVar()
		self.total_sum = tk.IntVar()

		self.member_ids = []

		label_style_introduce = ttk.Label(self, text = "Introduir, modificar o eliminar fila", style = "Titol.TLabel")
		label_frame_introduce = ttk.LabelFrame(self, style = "Marc.TFrame", labelwidget = label_style_introduce)
		label_frame_introduce.grid(row = 0, column = 0, ipadx = 2, ipady = 2)

		label_style_totals = ttk.Label(self, text = "Totals", style = "Titol.TLabel")
		label_frame_totals = ttk.LabelFrame(self, style = "Marc.TFrame", labelwidget = label_style_totals)
		label_frame_totals.grid(row = 2, column = 0, ipadx = 2, ipady = 2)

		label_style_lottery_name = ttk.Label(self, text = "Sorteig", style = "Titol.TLabel")
		label_frame_lottery_name = ttk.LabelFrame(self, style = "Marc.TFrame", labelwidget = label_style_lottery_name)
		label_frame_lottery_name.grid(row = 3, column = 0, ipadx = 2, ipady = 2)

		# Widgets per a cada frame.

		# Frame "Introduir".
		self.label_name = ttk.Label(label_frame_introduce, text = "Nom")
		self.label_name.grid(row = 0, column = 0, padx = 2)

		self.label_member_id = ttk.Label(label_frame_introduce, text = "Id")
		self.label_member_id.grid(row = 0, column = 1, padx = 2)

		self.label_tickets_male = ttk.Label(label_frame_introduce, text = "Paperetes Masc")
		self.label_tickets_male.grid(row = 0, column = 2, padx = 2)

		self.label_tickets_female = ttk.Label(label_frame_introduce, text = "Paperetes Fem")
		self.label_tickets_female.grid(row = 0, column = 3, padx = 2)

		self.label_tickets_childish = ttk.Label(label_frame_introduce, text = "Paperetes Inf")
		self.label_tickets_childish.grid(row = 0, column = 4, padx = 2)

		self.label_tenths_male = ttk.Label(label_frame_introduce, text = "Dècims Masc")
		self.label_tenths_male.grid(row = 0, column = 5, padx = 2)

		self.label_tenths_female = ttk.Label(label_frame_introduce, text = "Dècims Fem")
		self.label_tenths_female.grid(row = 0, column = 6, padx = 2)

		self.label_tenths_childish = ttk.Label(label_frame_introduce, text = "Dècims Inf")
		self.label_tenths_childish.grid(row = 0, column = 7, padx = 2)

		self.combo_box_member = ttk.Combobox(label_frame_introduce, width = 30, postcommand = self.display_member)
		self.combo_box_member.grid(row = 1, column = 0)
		self.combo_box_member.bind("<<ComboboxSelected>>", self.select_member)

		self.entry_member_id = ttk.Entry(label_frame_introduce, state = "disabled", textvariable = self.member_id)
		self.entry_member_id.grid(row = 1, column = 1, padx = 2)

		self.entry_tickets_male = ttk.Entry(label_frame_introduce, textvariable = self.tickets_male)
		self.entry_tickets_male.grid(row = 1, column = 2, padx = 2)
		self.entry_tickets_male.bind('<FocusOut>', self.calculate_totals)

		self.entry_tickets_female = ttk.Entry(label_frame_introduce, textvariable = self.tickets_female)
		self.entry_tickets_female.grid(row = 1, column = 3, padx = 2)
		self.entry_tickets_female.bind('<FocusOut>', self.calculate_totals)

		self.entry_tickets_childish = ttk.Entry(label_frame_introduce, textvariable = self.tickets_childish)
		self.entry_tickets_childish.grid(row = 1, column = 4, padx = 2)
		self.entry_tickets_childish.bind('<FocusOut>', self.calculate_totals)

		self.entry_tenths_male = ttk.Entry(label_frame_introduce, textvariable = self.tenths_male)
		self.entry_tenths_male.grid(row = 1, column = 5, padx = 2)
		self.entry_tenths_male.bind('<FocusOut>', self.calculate_totals)

		self.entry_tenths_female = ttk.Entry(label_frame_introduce, textvariable = self.tenths_female)
		self.entry_tenths_female.grid(row = 1, column = 6, padx = 2)
		self.entry_tenths_female.bind('<FocusOut>', self.calculate_totals)

		self.entry_tenths_childish = ttk.Entry(label_frame_introduce, textvariable = self.tenths_childish)
		self.entry_tenths_childish.grid(row = 1, column = 7, padx = 2)
		self.entry_tenths_childish.bind('<FocusOut>', self.calculate_totals)

		self.label_price = ttk.Label(label_frame_introduce, text = "diners")
		self.label_price.grid(row = 2, column = 0, padx = 2)

		self.entry_price = ttk.Entry(label_frame_introduce, state = "disabled", textvariable = self.price)
		self.entry_price.grid(row = 2, column = 1, padx = 2)

		self.label_benefit = ttk.Label(label_frame_introduce, text = "Benefici")
		self.label_benefit.grid(row = 2, column = 2, padx = 2)

		self.entry_benefit = ttk.Entry(label_frame_introduce, state = "disabled", textvariable = self.benefit)
		self.entry_benefit.grid(row = 2, column = 3, padx = 2)

		self.label_total = ttk.Label(label_frame_introduce, text = "Total")
		self.label_total.grid(row = 2, column = 4, padx = 2)

		self.entry_total = ttk.Entry(label_frame_introduce, state = "disabled", textvariable = self.total)
		self.entry_total.grid(row = 2, column = 5, padx = 2)

		self.button_add = ttk.Button(label_frame_introduce, style = "Boto.TButton", text = "Afegir", command = self.add_field)
		self.button_add.grid(row = 2, column = 6, padx = 2)

		self.button_modify = ttk.Button(label_frame_introduce, style = "Boto.TButton", state = "disabled", text = "Modificar", command = self.modificar_fila)
		self.button_modify.grid(row = 2, column = 7, padx = 2)

		self.button_delete = ttk.Button(label_frame_introduce, style = "Boto.TButton", state = "disabled", text = "Eliminar fila", command = self.eliminar_fila)
		self.button_delete.grid(row = 2, column = 8, padx = 2)

		self.tree_lottery = ttk.Treeview(self, height = 20)
		self.tree_lottery["columns"] = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve")
		self.tree_lottery.column("#0", width = 40)
		self.tree_lottery.column("one", width = 160)
		self.tree_lottery.column("two", width = 80)
		self.tree_lottery.column("three", width = 80)
		self.tree_lottery.column("four", width = 80)
		self.tree_lottery.column("five", width = 80)
		self.tree_lottery.column("six", width = 80)
		self.tree_lottery.column("seven", width = 80)
		self.tree_lottery.column("eight", width = 80)
		self.tree_lottery.column("nine", width = 80)
		self.tree_lottery.column("ten", width = 80)
		self.tree_lottery.column("eleven", width = 80)
		self.tree_lottery.column("twelve", width = 80)
		self.tree_lottery.heading("#0", text = "id")
		self.tree_lottery.heading("one", text = "nom")
		self.tree_lottery.heading("two", text = "pap. masc.")
		self.tree_lottery.heading("three", text = "pap. fem.")
		self.tree_lottery.heading("four", text = "pap. inf.")
		self.tree_lottery.heading("five", text = "dèc. masc.")
		self.tree_lottery.heading("six", text = "dèc. fem.")
		self.tree_lottery.heading("seven", text = "dèc. inf.")
		self.tree_lottery.heading("eight", text = "diners")
		self.tree_lottery.heading("nine", text = "benefici")
		self.tree_lottery.heading("ten", text = "total")
		self.tree_lottery.heading("eleven", text = "assignada")
		self.tree_lottery.heading("twelve", text = "id faller")
		self.tree_lottery.grid(row = 1, column = 0, padx = 10, pady = 5)
		self.tree_lottery.bind("<<TreeviewSelect>>", self.fila_seleccionada)

		self.scroll_lottery_table = ttk.Scrollbar(self, command = self.tree_lottery.yview)
		self.scroll_lottery_table.grid(row = 1, column = 1, sticky = "nsew")

		self.tree_lottery.config(yscrollcommand = self.scroll_lottery_table.set)

		# Frame "Totals".
		self.label_total_tickets_male = ttk.Label(label_frame_totals, text = "Paperetes Masc", style = "Etiqueta.TLabel")
		self.label_total_tickets_male.grid(row = 0, column = 0, padx = 2)

		self.label_total_tickets_female = ttk.Label(label_frame_totals, text = "Paperetes Fem", style = "Etiqueta.TLabel")
		self.label_total_tickets_female.grid(row = 0, column = 1, padx = 2)

		self.label_total_tickets_childish = ttk.Label(label_frame_totals, text = "Paperetes Inf", style = "Etiqueta.TLabel")
		self.label_total_tickets_childish.grid(row = 0, column = 2, padx = 2)

		self.label_total_tenths_male = ttk.Label(label_frame_totals, text = "Dècims Masc", style = "Etiqueta.TLabel")
		self.label_total_tenths_male.grid(row = 0, column = 3, padx = 2)

		self.label_total_tenths_female = ttk.Label(label_frame_totals, text = "Dècims Fem", style = "Etiqueta.TLabel")
		self.label_total_tenths_female.grid(row = 0, column = 4, padx = 2)

		self.label_total_tenths_childish = ttk.Label(label_frame_totals, text = "Dècims Inf", style = "Etiqueta.TLabel")
		self.label_total_tenths_childish.grid(row = 0, column = 5, padx = 2)

		self.label_price = ttk.Label(label_frame_totals, text = "Diners", style = "Etiqueta.TLabel")
		self.label_price.grid(row = 0, column = 6, padx = 2)

		self.label_benefits = ttk.Label(label_frame_totals, text = "Benefici", style = "Etiqueta.TLabel")
		self.label_benefits.grid(row = 0, column = 7, padx = 2)

		self.label_total = ttk.Label(label_frame_totals, text = "Total", style = "Etiqueta.TLabel")
		self.label_total.grid(row = 0, column = 8, padx = 2)

		self.entry_total_tickets_male = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_tickets_male)
		self.entry_total_tickets_male.grid(row = 1, column = 0, padx = 2)
		self.total_tickets_male.set("0")

		self.entry_total_tickets_female = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_tickets_female)
		self.entry_total_tickets_female.grid(row = 1, column = 1, padx = 2)
		self.total_tickets_female.set("0")

		self.entry_total_tickets_childish = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_tickets_childish)
		self.entry_total_tickets_childish.grid(row = 1, column = 2, padx = 2)
		self.total_tickets_childish.set("0")

		self.entry_total_tenths_male = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_tenths_male)
		self.entry_total_tenths_male.grid(row = 1, column = 3, padx = 2)
		self.total_tenths_male.set("0")

		self.entry_total_tenths_female = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_tenths_female)
		self.entry_total_tenths_female.grid(row = 1, column = 4, padx = 2)
		self.total_tenths_female.set("0")

		self.entry_total_tenths_childish = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_tenths_childish)
		self.entry_total_tenths_childish.grid(row = 1, column = 5, padx = 2)
		self.total_tenths_childish.set("0")

		self.entry_price = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_price)
		self.entry_price.grid(row = 1, column = 6, padx = 2)
		self.total_price.set("0")

		self.entry_benefit = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_benefit)
		self.entry_benefit.grid(row = 1, column = 7, padx = 2)
		self.total_benefit.set("0")

		self.entry_total_sum = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_sum)
		self.entry_total_sum.grid(row = 1, column = 8, padx = 2)
		self.total_sum.set("0")

		# Frame "Sorteig".
		self.combo_box_lottery_name = ttk.Combobox(label_frame_lottery_name, width = 30, postcommand = self.desplegar_sortejos)
		self.combo_box_lottery_name.grid(row = 0, column = 0)

		self.button_obrir=ttk.Button(label_frame_lottery_name, text="Obrir", command=self.obrir)
		self.button_obrir.grid(row=0, column=2, padx=2)

		self.button_guardar=ttk.Button(label_frame_lottery_name, text="Guardar", command=self.guardar)
		self.button_guardar.grid(row=0, column=3, padx=2)

		self.button_assignar=ttk.Button(label_frame_lottery_name, text="Assignar", command=self.assignar)
		self.button_assignar.grid(row=0, column=4, padx=2)

		self.button_netejar=ttk.Button(label_frame_lottery_name, text="Netejar", command=self.netejar)
		self.button_netejar.grid(row=0, column=5, padx=2)

		self.reset_fields()



	def reset_fields(self):

		self.combo_box_member.focus()
		self.tickets_male.set("0")
		self.tickets_female.set("0")
		self.tickets_childish.set("0")
		self.tenths_male.set("0")
		self.tenths_female.set("0")
		self.tenths_childish.set("0")
		self.price.set("0")
		self.benefit.set("0")
		self.total_sum.set("0")

	
	def display_member(self):
		'''
		Controla el combobox comparant la cadena escrita amb la base de dades i mostrant els resultats en el combobox.
		Utilitza l'atribut "self.member_ids" per a passar el identificador de faller a la funció "select_member".
		'''
		falla = Falla()
		surname = self.combo_box_member.get()
		falla.get_members("surname", surname)
		members_list = []
		self.member_ids = []
		for member in falla.members_list:
			self.member_ids = self.member_ids + [member.id]
			members_list = members_list + [(
				member.surname + ", " + member.name
			)]
		self.combo_box_member["values"] = members_list


	def select_member(self, event):
		'''
		Controla la selecció del combobox per a guardar el identificador del faller i omplir les dades a partir d'aquest.
		'''
		index = self.combo_box_member.current()
		self.member_id.set(self.member_ids[index])
		self.member_ids = []
		self.fill_name(self.member_id.get())


	def fill_name(self, id):
		result = Member.get_member(id)
		family = Family(result[12], result[13], result[14])
		category = Category(result[15], result[16], result[17], result[18])
		member = Member(
			result[0],
			result[1],
			result[2],
			result[3],
			result[4],
			result[5],
			result[6],
			result[7],
			result[8],
			result[11],
			family,
			category
		)
		self.combo_box_member.set(member.surname + ", " + member.name)


	def calculate_totals(self, event):
		self.price.set((self.tickets_male.get()*4) + (self.tickets_female.get()*4) + (self.tickets_childish.get()*4) + 
				(self.tenths_male.get()*20) + (self.tenths_female.get()*20) + (self.tenths_childish.get()*20))
		self.benefit.set(self.tickets_male.get() + self.tickets_female.get() + self.tickets_childish.get() +
				(self.tenths_male.get()*3) + (self.tenths_female.get()*3) + (self.tenths_childish.get()*3))
		self.total.set(self.price.get() + self.benefit.get())


	def add_field(self):
		self.calculate_totals('<FocusOut>')
		if self.member_id.get() == "":
			messagebox.showwarning("Error", "El camp nom ha de contindre un nom de faller vàlid")
		else:
			self.tree_lottery.insert("", "end", text=self.member_id.get(),
				values = (self.combo_box_member.get(), self.tickets_male.get(), self.tickets_female.get(), self.tickets_childish.get(),
			   	self.tenths_male.get(), self.tenths_female.get(), self.tenths_childish.get(),
				self.price.get(), self.benefit.get(), self.total.get(), 0, self.member_id.get()))
			
			self.total_tickets_male.set(self.total_tickets_male.get() + self.tickets_male.get())
			self.total_tickets_female.set(self.total_tickets_female.get() + self.tickets_female.get())
			self.total_tickets_childish.set(self.total_tickets_childish.get() + self.tickets_childish.get())
			self.total_tenths_male.set(self.total_tenths_male.get() + self.tenths_male.get())
			self.total_tenths_female.set(self.total_tenths_female.get() + self.tenths_female.get())
			self.total_tenths_childish.set(self.total_tenths_childish.get() + self.tenths_childish.get())
			self.total_price.set(self.total_price.get() + self.price.get())
			self.total_benefit.set(self.total_benefit.get() + self.benefit.get())
			self.total_sum.set(self.total_sum.get() + self.total.get())

			self.member_id.set("")
			self.combo_box_member.set("")
			self.reset_fields()


	def fila_seleccionada(self, event):
		fila=self.tree_lottery.selection()
		self.combo_box_member.config(state="disabled")
		self.button_modify.config(state="normal")
		self.button_delete.config(state="normal")
		id=self.tree_lottery.item(fila, option="text")
		llista_dades=self.tree_lottery.item(fila, option="values")
		if llista_dades[10]==1:
			messagebox.showwarning("Error", "No es pot seleccionar una fila que ja ha segut assignada")
		else:
			self.combo_box_member.set(llista_dades[0])
			self.member_id.set(llista_dades[11])
			self.tickets_male.set(llista_dades[1])
			self.tickets_female.set(llista_dades[2])
			self.tickets_childish.set(llista_dades[3])
			self.tenths_male.set(llista_dades[4])
			self.tenths_female.set(llista_dades[5])
			self.tenths_childish.set(llista_dades[6])
			self.calculate_totals('<FocusOut>') # Calculem la resta de camps.


	def modificar_fila(self):
		bd=BaseDeDades('falla.db')
		utils=Utils()
		data=utils.calcular_data_actual()
		self.calculate_totals('<FocusOut>') # Calculem els totals per si no s'ha fet abans.
		fila=self.tree_lottery.selection()
		id=self.tree_lottery.item(fila, option="text")
		llista_dades=self.tree_lottery.item(fila, option="values")
		sorteig=self.combo_box_lottery_name.get()
		if llista_dades[10]==1:
			messagebox.showerror("Error", "No es pot modificar una fila de loteria ja assignada")
		else:
			# Restem els valors dels camps de la fila que anem a modificar.
			self.total_tickets_male.set(self.total_tickets_male.get()-llista_dades[1])
			self.total_tickets_female.set(self.total_tickets_female.get()-llista_dades[2])
			self.total_tickets_childish.set(self.total_tickets_childish.get()-llista_dades[3])
			self.total_tenths_male.set(self.total_tenths_male.get()-llista_dades[4])
			self.total_tenths_female.set(self.total_tenths_female.get()-llista_dades[5])
			self.total_tenths_childish.set(self.total_tenths_childish.get()-llista_dades[6])
			self.total_price.set(self.total_price.get()-llista_dades[7])
			self.total_benefit.set(self.total_benefit.get()-llista_dades[8])
			self.total_sum.set(self.total_sum.get()-llista_dades[9])
			# Passem a la taula els valors modificats prèviament.
			self.tree_lottery.item(fila, text=self.member_id.get(), values=(self.combo_box_member.get(),
				self.tickets_male.get(), self.tickets_female.get(), self.tickets_childish.get(),
				self.tenths_male.get(), self.tenths_female.get(), self.tenths_childish.get(),
				self.price.get(), self.benefit.get(), self.total.get()))
			# Sumem els nous valors dels camps.
			self.total_tickets_male.set(self.total_tickets_male.get()+self.tickets_male.get())
			self.total_tickets_female.set(self.total_tickets_female.get()+self.tickets_female.get())
			self.total_tickets_childish.set(self.total_tickets_childish.get()+self.tickets_childish.get())
			self.total_tenths_male.set(self.total_tenths_male.get()+self.tenths_male.get())
			self.total_tenths_female.set(self.total_tenths_female.get()+self.tenths_female.get())
			self.total_tenths_childish.set(self.total_tenths_childish.get()+self.tenths_childish.get())
			self.total_price.set(self.total_price.get()+self.price.get())
			self.total_benefit.set(self.total_benefit.get()+self.benefit.get())
			self.total_sum.set(self.total_sum.get()+self.total.get())
			# Mirem si el registre està en la base de dades i en cas de ser així el modifiquem.
			ultim_id=bd.llegir_ultim_id_loteria()
			if ultim_id<=id:
				messagebox.showinfo("Info", "El registre encara no està a la base de dades. Es guardarà al fer clic en Guardar junt amb la resta de registres")
			else:
				loteria=Lottery(id, sorteig, data, self.tickets_male.get(), self.tickets_female.get(), self.tickets_childish.get(),
					self.tenths_male.get(), self.tenths_female.get(), self.tenths_childish.get(), 0)
				bd.actualitzar_loteria(loteria)
		# Resetegem camps.
		self.member_id.set("")
		self.combo_box_member.set("")
		self.combo_box_member.config(state="normal")
		self.button_modify.config(state="disabled")
		self.button_delete.config(state="disabled")
		self.reset_fields()
		bd.tancar_conexio()


	def eliminar_fila(self):
		bd=BaseDeDades('falla.db')
		fila=self.tree_lottery.selection()
		id=self.tree_lottery.item(fila, option="text")
		llista_dades=self.tree_lottery.item(fila, option="values")
		# Podem borrar en el cas de que la loteria no estiga assignada.
		if llista_dades[10]==1:
			messagebox.showerror("Error", "No es pot eliminar una fila de loteria ja assignada")
		else:
			# Restem els valors de la fila que anem a borrar.
			self.total_tickets_male.set(self.total_tickets_male.get()-llista_dades[1])
			self.total_tickets_female.set(self.total_tickets_female.get()-llista_dades[2])
			self.total_tickets_childish.set(self.total_tickets_childish.get()-llista_dades[3])
			self.total_tenths_male.set(self.total_tenths_male.get()-llista_dades[4])
			self.total_tenths_female.set(self.total_tenths_female.get()-llista_dades[5])
			self.total_tenths_childish.set(self.total_tenths_childish.get()-llista_dades[6])
			self.total_price.set(self.total_price.get()-llista_dades[7])
			self.total_benefit.set(self.total_benefit.get()-llista_dades[8])
			self.total_sum.set(self.total_sum.get()-llista_dades[9])
			# Eliminem la fila a l'arbre.
			self.tree_lottery.delete(fila)
			# Eliminem el registre de la fila a la base de dades en cas de que ja estiga guardat.
			ultim_id=bd.llegir_ultim_id_loteria()
			if ultim_id>id:
				bd.eliminar_loteria(id)
		# Canviem la configuració dels botons.
		self.combo_box_member.config(state="normal")
		self.button_modify.config(state="disabled")
		self.button_delete.config(state="disabled")
		bd.tancar_conexio()


	def desplegar_sortejos(self):
		bd=BaseDeDades('falla.db')
		llistat_sortejos=bd.llegir_sortejos()
		self.combo_box_lottery_name["values"]=llistat_sortejos
		bd.tancar_conexio()


	def obrir(self):
		sorteig=self.combo_box_lottery_name.get()
		# Resetegem tot per a obrir sobre formulari en blanc.
		self.reset_fields()
		self.tree_lottery.delete(*self.tree_lottery.get_children()) # Borrem les dades de la taula.
		self.member_id.set("")
		self.combo_box_member.config(state="normal")
		self.combo_box_member.set("")
		self.total_tickets_male.set("0")
		self.total_tickets_female.set("0")
		self.total_tickets_childish.set("0")
		self.total_tenths_male.set("0")
		self.total_tenths_female.set("0")
		self.total_tenths_childish.set("0")
		self.total_price.set("0")
		self.total_benefit.set("0")
		self.total_sum.set("0")
		# Traguem el llistat de loteries corresponent al sorteig triat.
		bd=BaseDeDades('falla.db')
		llistat_loteries=bd.llegir_loteries_per_sorteig(sorteig)
		total_tickets_male=0
		total_tickets_female=0
		total_tickets_childish=0
		total_tenths_male=0
		total_tenths_female=0
		total_tenths_childish=0
		total_price=0
		total_benefit=0
		for loteria in llistat_loteries:
			total_tickets_male=total_tickets_male + loteria.tickets_male
			total_tickets_female=total_tickets_female + loteria.tickets_female
			total_tickets_childish=total_tickets_childish + loteria.tickets_childish
			total_tenths_male=total_tenths_male + loteria.tenths_male
			total_tenths_female=total_tenths_female + loteria.tenths_female
			total_tenths_childish=total_tenths_childish + loteria.tenths_childish
			price=loteria.calcular_price()
			total_price=total_price + price
			benefit=loteria.calcular_benefit()
			total_benefit=total_benefit + benefit
			total=price+benefit
			nom=loteria.faller.cognoms + ", " + loteria.faller.nom
			llista_dades=[nom, loteria.tickets_male, loteria.tickets_female, loteria.tickets_childish, loteria.tenths_male, loteria.tenths_female, loteria.tenths_childish, price, benefit, total, loteria.assignada]
			self.tree_lottery.insert("", "end", text=loteria.id, values=llista_dades)
		bd.tancar_conexio()


	def guardar(self):
		utils=Utils()
		data=utils.calcular_data_actual
		bd=BaseDeDades('falla.db')
		sorteig=self.combo_box_lottery_name.get()
		ultim_id=bd.llegir_ultim_id_loteria()
		llistat_files=self.tree_lottery.get_children()
		for fila in llistat_files:
			id=self.tree_lottery.item(fila, option="text")
			llistat_dades=self.tree_lottery.item(fila, option="values")
			faller=bd.llegir_faller(llistat_dades[12])
			loteria=Lottery(id, sorteig, data, llistat_dades[1], llistat_dades[2], llistat_dades[3], llistat_dades[4], llistat_dades[5], llistat_dades[6], faller)
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
			llistat_files=self.tree_lottery.get_children()
			bd=BaseDeDades('falles.db')
			for fila in llistat_files:
				id=self.tree_lottery.item(fila, option="text")
				llistat_dades=self.tree_lottery.item(fila, option="values")
				moviment=Movement(0, data, llistat_dades[8], 1, 2, exercici_actual, self.combo_box_lottery_name.get())
				bd.crear_moviment(moviment)
				moviment=Movement(0, data, llistat_dades[9], 2, 1, exercici_actual, self.combo_box_lottery_name.get())
				bd.crear_moviment(moviment)
				# Actualització de tots els registres a estat assignat.
				bd.actualitzar_assignada_loteria(id)
			self.button_assignar.config(state="disabled")


	def netejar(self):

		self.reset_fields()
		self.tree_lottery.delete(*self.tree_lottery.get_children())
		self.member_id.set("")
		self.combo_box_member.config(state="normal")
		self.combo_box_member.set("")
		self.total_tickets_male.set("0")
		self.total_tickets_female.set("0")
		self.total_tickets_childish.set("0")
		self.total_tenths_male.set(0)
		self.total_tenths_female.set(0)
		self.total_tenths_childish.set(0)
		self.total_price.set(0)
		self.total_benefit-set(0)
		self.total_sum.set(0)
		self.combo_box_lottery_name.set("")
		self.button_add.config(state="normal")
		self.button_assignar.config(state="normal")