import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import LabelFrame

from arxiu import Arxiu
from base_de_dades import BaseDeDades
from utils import Utils

from falla import Falla
from moviment import Moviment
from finestra_modificar import FinestraModificar
#from informe import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


class FinestraGestionar(tk.Toplevel):
	

	def __init__(self, master=None):
		'''
		Inicialitza una nova instància de la classe FinestraIntroduir.

		Parametres:
		-----------
		master : tk.Tk o tk.Toplevel, opcional
			La instància principal de l'aplicació o de la finestra que crea esta nova finestra.
			Si no se proporciona, se creará una nueva instancia de tk.Tk().
		'''
		super().__init__(master)
		self.master=master
		self.resizable(0,0)
		self.title("Gestionar Faller")
		self.iconbitmap("escut.ico")

		self.exercici=tk.StringVar()
		self.id=tk.StringVar()
		self.nom=tk.StringVar()
		self.naixement=tk.StringVar()
		self.dni=tk.StringVar()
		self.adresa=tk.StringVar()
		self.telefon=tk.StringVar()
		self.correu=tk.StringVar()

		self.membres_familia=tk.StringVar()

		self.quota_assignada=tk.StringVar()
		self.quota_pagada=tk.StringVar()
		self.deute_quota=tk.StringVar()
		self.pagar_quota=tk.StringVar()
		self.loteria_assignada=tk.StringVar()
		self.loteria_pagada=tk.StringVar()
		self.deute_loteria=tk.StringVar()
		self.pagar_loteria=tk.StringVar()
		self.rifa_assignada=tk.StringVar()
		self.rifa_pagada=tk.StringVar()
		self.deute_rifa=tk.StringVar()
		self.pagar_rifa=tk.StringVar()
		self.total_assignat=tk.StringVar()
		self.total_pagat=tk.StringVar()
		self.deute_total=tk.StringVar()
		self.pagar_total=tk.StringVar()
		self.forma_pagament=tk.StringVar()
		
		self.quota_assignada_familia=tk.StringVar()
		self.quota_pagada_familia=tk.StringVar()
		self.deute_quota_familia=tk.StringVar()
		self.pagar_quota_familia=tk.StringVar()
		self.loteria_assignada_familia=tk.StringVar()
		self.loteria_pagada_familia=tk.StringVar()
		self.deute_loteria_familia=tk.StringVar()
		self.pagar_loteria_familia=tk.StringVar()
		self.rifa_assignada_familia=tk.StringVar()
		self.rifa_pagada_familia=tk.StringVar()
		self.deute_rifa_familia=tk.StringVar()
		self.pagar_rifa_familia=tk.StringVar()
		self.total_assignat_familia=tk.StringVar()
		self.total_pagat_familia=tk.StringVar()
		self.deute_total_familia=tk.StringVar()
		self.pagar_total_familia=tk.StringVar()
		self.forma_pagament_familia=tk.StringVar()
		
		self.concepte_assignacio=tk.StringVar()
		self.descripcio_assignacio=tk.StringVar()
		self.total_assignacio=tk.StringVar()

		self.identificadors=[] # Atribut per guardar els id_faller del llistat del combo.
		self.modificar_oberta=0 # Atribut amb què controlem l'obertura de la finestra FinestraModificar.
		self.id_anterior=0 # Atribut on guardem el id anteriorment buscat per a retornar-lo en cas d'error.
		
		# Frames en els que dividim la finestra
		label_frame_exercici=LabelFrame(self, text="Exercici")
		label_frame_exercici.grid(row=0, column=0, columnspan=1, pady=5, ipadx=20, ipady=2)

		label_frame_buscar=LabelFrame(self, text="Faller")
		label_frame_buscar.grid(row=0, column=1, columnspan=8, ipadx=2, ipady=2)

		label_frame_dades=LabelFrame(self, text="Dades personals")
		label_frame_dades.grid(row=1, column=0, columnspan=4, ipadx=2, ipady=2)

		label_frame_familia=LabelFrame(self, text="Familia")
		label_frame_familia.grid(row=1, column=4, columnspan=1, ipadx=2, ipady=2)

		label_frame_moviments=LabelFrame(self, text="Moviments")
		label_frame_moviments.grid(row=2, column=0, columnspan=4, padx=5, pady=5, ipadx=2, ipady=2)

		label_frame_moviments_familia=LabelFrame(self, text="Moviments de la familia")
		label_frame_moviments_familia.grid(row=2, column=4, columnspan=1, padx=5, pady=5, ipadx=2, ipady=2)

		label_frame_assignar=LabelFrame(self, text="Assignar")
		label_frame_assignar.grid(row=3, column=0, pady=5, ipady=2, sticky="n")

		label_frame_historial=LabelFrame(self, text="Historial de moviments")
		label_frame_historial.grid(row=3, column=1, columnspan=8, pady=5, ipady=2)

		# Widgets per a cada frame.

		# Frame "Exercici".
		self.entry_exercici=tk.Entry(label_frame_exercici, width=10, state="disabled", disabledforeground="black", textvariable=self.exercici)
		self.entry_exercici.pack()

		# Frame "Buscar faller"
		self.button_alta=tk.Button(label_frame_buscar, state="disabled", width=15, text="Donar d'alta", command=self.canviar_estat)
		self.button_alta.grid(row=0, column=0, padx=5, sticky="w"+"e")
		
		self.label_id=tk.Label(label_frame_buscar, text="ID del faller:")
		self.label_id.grid(row=0, column=1)

		self.entry_id=tk.Entry(label_frame_buscar, width=8, textvariable=self.id)
		self.entry_id.grid(row=0, column=2)
		self.entry_id.bind('<Return>', self.buscar_per_id)

		self.label_nom=tk.Label(label_frame_buscar, text="Cognoms i nom:")
		self.label_nom.grid(row=0, column=3)

		self.combo_box_faller=ttk.Combobox(label_frame_buscar, width=30, postcommand=self.desplegar_faller)
		self.combo_box_faller.grid(row=0, column=4)
		self.combo_box_faller.bind("<<ComboboxSelected>>", self.seleccionar_faller)

		# Frame "Dades personals".
		self.label_naixement=tk.Label(label_frame_dades, text="Data de naixement:")
		self.label_naixement.grid(row=0, column=0, sticky="e")

		self.entry_naixement=tk.Entry(label_frame_dades, state="disabled", textvariable=self.naixement)
		self.entry_naixement.grid(row=0, column=1)

		self.label_dni=tk.Label(label_frame_dades, text="DNI:")
		self.label_dni.grid(row=0, column=2, sticky="e")

		self.entry_dni=tk.Entry(label_frame_dades, state="disabled", textvariable=self.dni)
		self.entry_dni.grid(row=0, column=3)

		self.label_adresa=tk.Label(label_frame_dades, text="Adreça:")
		self.label_adresa.grid(row=1, column=0, sticky="e")

		self.entry_adresa=tk.Entry(label_frame_dades, state="disabled", textvariable=self.adresa)
		self.entry_adresa.grid(row=1, column=1)

		self.label_telefon=tk.Label(label_frame_dades, text="Telèfon:")
		self.label_telefon.grid(row=1, column=2, sticky="e")

		self.entry_telefon=tk.Entry(label_frame_dades, state="disabled", textvariable=self.telefon)
		self.entry_telefon.grid(row=1, column=3)

		self.label_correu=tk.Label(label_frame_dades, text="Correu electrònic:")
		self.label_correu.grid(row=2, column=0, sticky="e")

		self.entry_correu=tk.Entry(label_frame_dades, state="disabled", textvariable=self.correu)
		self.entry_correu.grid(row=2, column=1)

		self.button_modificar=tk.Button(label_frame_dades, state="disabled", text="Modificar dades", command=self.modificar)
		self.button_modificar.grid(row=2, column=3)

		#Frame "Familia".
		self.label_familia=tk.Label(label_frame_familia, text="Membres de la familia:")
		self.label_familia.grid(row=0, column=0)

		self.combo_box_familia=ttk.Combobox(label_frame_familia, postcommand=self.desplegar_familia)
		self.combo_box_familia.grid(row=0, column=1)
		self.combo_box_familia.bind("<<ComboboxSelected>>", self.seleccionar_familia)

		self.label_membres=tk.Label(label_frame_familia, text="Membres actius:")
		self.label_membres.grid(row=0, column=2)

		self.entry_membres=tk.Entry(label_frame_familia, width=4, state="disabled", disabledforeground="black", textvariable=self.membres_familia)
		self.entry_membres.grid(row=0, column=3)

		#Frame "Moviments".
		self.label_assignat=tk.Label(label_frame_moviments, text="Assignat")
		self.label_assignat.grid(row=0, column=1)

		self.label_pagat=tk.Label(label_frame_moviments, text="Pagat")
		self.label_pagat.grid(row=0, column=2)

		self.label_diferencia=tk.Label(label_frame_moviments, text="Diferència")
		self.label_diferencia.grid(row=0, column=3)

		self.label_quota=tk.Label(label_frame_moviments, text="Quota:")
		self.label_quota.grid(row=1, column=0, sticky="e")

		self.entry_quota_assignada=tk.Entry(label_frame_moviments, width=15, state="disabled", disabledforeground="black", textvariable=self.quota_assignada)
		self.entry_quota_assignada.grid(row=1, column=1)

		self.entry_quota_pagada=tk.Entry(label_frame_moviments, width=15, state="disabled", disabledforeground="black", textvariable=self.quota_pagada)
		self.entry_quota_pagada.grid(row=1, column=2)

		self.entry_deute_quota=tk.Entry(label_frame_moviments, width=15, state="disabled", disabledforeground="black", textvariable=self.deute_quota)
		self.entry_deute_quota.grid(row=1, column=3)

		self.entry_pagar_quota=tk.Entry(label_frame_moviments, width=15, state="disabled", textvariable=self.pagar_quota)
		self.entry_pagar_quota.grid(row=1, column=4)
		self.entry_pagar_quota.bind('<FocusOut>', lambda event: self.calcular_pagar_total(event, self.entry_pagar_quota))
		self.entry_pagar_quota.bind('<FocusIn>', lambda event: self.fer_seleccio(event, self.entry_pagar_quota))

		self.label_loteria=tk.Label(label_frame_moviments, text="Loteria:")
		self.label_loteria.grid(row=2, column=0, sticky="e")

		self.entry_loteria_assignada=tk.Entry(label_frame_moviments, width=15, state="disabled", disabledforeground="black", textvariable=self.loteria_assignada)
		self.entry_loteria_assignada.grid(row=2, column=1)

		self.entry_loteria_pagada=tk.Entry(label_frame_moviments, width=15, state="disabled", disabledforeground="black", textvariable=self.loteria_pagada)
		self.entry_loteria_pagada.grid(row=2, column=2)

		self.entry_deute_loteria=tk.Entry(label_frame_moviments, width=15, state="disabled", disabledforeground="black", textvariable=self.deute_loteria)
		self.entry_deute_loteria.grid(row=2, column=3)

		self.entry_pagar_loteria=tk.Entry(label_frame_moviments, width=15, state="disabled", textvariable=self.pagar_loteria)
		self.entry_pagar_loteria.grid(row=2, column=4)
		self.entry_pagar_loteria.bind('<FocusOut>', lambda event: self.calcular_pagar_total(event, self.entry_pagar_loteria))
		self.entry_pagar_loteria.bind('<FocusIn>', lambda event: self.fer_seleccio(event, self.entry_pagar_loteria))

		self.label_rifa=tk.Label(label_frame_moviments, text="Rifa:")
		self.label_rifa.grid(row=3, column=0, sticky="e")

		self.entry_rifa_assignada=tk.Entry(label_frame_moviments, width=15, state="disabled", disabledforeground="black", textvariable=self.rifa_assignada)
		self.entry_rifa_assignada.grid(row=3, column=1)

		self.entry_rifa_pagada=tk.Entry(label_frame_moviments, width=15, state="disabled", disabledforeground="black", textvariable=self.rifa_pagada)
		self.entry_rifa_pagada.grid(row=3, column=2)

		self.entry_deute_rifa=tk.Entry(label_frame_moviments, width=15, state="disabled", disabledforeground="black", textvariable=self.deute_rifa)
		self.entry_deute_rifa.grid(row=3, column=3)

		self.entry_pagar_rifa=tk.Entry(label_frame_moviments, width=15, state="disabled", textvariable=self.pagar_rifa)
		self.entry_pagar_rifa.grid(row=3, column=4)
		self.entry_pagar_rifa.bind('<FocusOut>', lambda event: self.calcular_pagar_total(event, self.entry_pagar_rifa))
		self.entry_pagar_rifa.bind('<FocusIn>', lambda event: self.fer_seleccio(event, self.entry_pagar_rifa))

		self.label_totals=tk.Label(label_frame_moviments, text="Totals:")
		self.label_totals.grid(row=4, column=0, sticky="e")

		self.entry_total_assignat=tk.Entry(label_frame_moviments, width=15, state="disabled", disabledforeground="black", textvariable=self.total_assignat)
		self.entry_total_assignat.grid(row=4, column=1)

		self.entry_total_pagat=tk.Entry(label_frame_moviments, width=15, state="disabled", disabledforeground="black", textvariable=self.total_pagat)
		self.entry_total_pagat.grid(row=4, column=2)

		self.entry_deute_total=tk.Entry(label_frame_moviments, width=15, state="disabled", disabledforeground="black", textvariable=self.deute_total)
		self.entry_deute_total.grid(row=4, column=3)

		self.entry_pagar_total=tk.Entry(label_frame_moviments, width=15, state="disabled", disabledforeground="black", textvariable=self.pagar_total)
		self.entry_pagar_total.grid(row=4, column=4)

		self.radio_button_caixa=tk.Radiobutton(label_frame_moviments, text="Caixa", variable=self.forma_pagament, value=1)
		self.radio_button_banc=tk.Radiobutton(label_frame_moviments, text="Banc", variable=self.forma_pagament, value=2)
		self.radio_button_caixa.grid(row=5, column=2)
		self.radio_button_banc.grid(row=5, column=3)
		self.radio_button_caixa.select()

		self.button_pagar=tk.Button(label_frame_moviments, state="disabled", text="Pagar", command=self.Pagar)
		self.button_pagar.grid(row=5, column=4, padx=5, sticky="w"+"e")

		# Frame "Moviments de la familia".
		self.label_assignat_familia=tk.Label(label_frame_moviments_familia, text="Assignat")
		self.label_assignat_familia.grid(row=0, column=1)

		self.label_pagat_familia=tk.Label(label_frame_moviments_familia, text="Pagat")
		self.label_pagat_familia.grid(row=0, column=2)

		self.label_diferencia_familia=tk.Label(label_frame_moviments_familia, text="Diferència")
		self.label_diferencia_familia.grid(row=0, column=3)

		self.Label_quota_familia=tk.Label(label_frame_moviments_familia, text="Quota:")
		self.Label_quota_familia.grid(row=1, column=0, sticky="e")

		self.entry_quota_assignada_familia=tk.Entry(label_frame_moviments_familia, width=15, state="disabled", disabledforeground="black", textvariable=self.quota_assignada_familia)
		self.entry_quota_assignada_familia.grid(row=1, column=1)

		self.entry_quota_pagada_familia=tk.Entry(label_frame_moviments_familia, width=15, state="disabled", disabledforeground="black", textvariable=self.quota_pagada_familia)
		self.entry_quota_pagada_familia.grid(row=1, column=2)

		self.entry_deute_quota_familia=tk.Entry(label_frame_moviments_familia, width=15, state="disabled", disabledforeground="black", textvariable=self.deute_quota_familia)
		self.entry_deute_quota_familia.grid(row=1, column=3)

		self.entry_pagar_quota_familia=tk.Entry(label_frame_moviments_familia, width=15, state="disabled", textvariable=self.pagar_quota_familia)
		self.entry_pagar_quota_familia.grid(row=1, column=4)
		self.entry_pagar_quota_familia.bind('<FocusOut>', lambda event: self.calcular_pagar_total(event, self.entry_pagar_quota_familia))
		self.entry_pagar_quota_familia.bind('<FocusIn>', lambda event: self.fer_seleccio(event, self.entry_pagar_quota_familia))

		self.label_loteria_familia=tk.Label(label_frame_moviments_familia, text="Loteria:")
		self.label_loteria_familia.grid(row=2, column=0, sticky="e")

		self.entry_loteria_assignada_familia=tk.Entry(label_frame_moviments_familia, width=15, state="disabled", disabledforeground="black", textvariable=self.loteria_assignada_familia)
		self.entry_loteria_assignada_familia.grid(row=2, column=1)

		self.entry_loteria_pagada_familia=tk.Entry(label_frame_moviments_familia, width=15, state="disabled", disabledforeground="black", textvariable=self.loteria_pagada_familia)
		self.entry_loteria_pagada_familia.grid(row=2, column=2)

		self.entry_deute_loteria_familia=tk.Entry(label_frame_moviments_familia, width=15, state="disabled", disabledforeground="black", textvariable=self.deute_loteria_familia)
		self.entry_deute_loteria_familia.grid(row=2, column=3)

		self.entry_pagar_loteria_familia=tk.Entry(label_frame_moviments_familia, width=15, state="disabled", textvariable=self.pagar_loteria_familia)
		self.entry_pagar_loteria_familia.grid(row=2, column=4)
		self.entry_pagar_loteria_familia.bind('<FocusOut>', lambda event: self.calcular_pagar_total(event, self.entry_pagar_loteria_familia))
		self.entry_pagar_loteria_familia.bind('<FocusIn>', lambda event: self.fer_seleccio(event, self.entry_pagar_loteria_familia))

		self.label_rifa_familia=tk.Label(label_frame_moviments_familia, text="Rifa:")
		self.label_rifa_familia.grid(row=3, column=0, sticky="e")

		self.entry_rifa_assignada_familia=tk.Entry(label_frame_moviments_familia, width=15, state="disabled", disabledforeground="black", textvariable=self.rifa_assignada_familia)
		self.entry_rifa_assignada_familia.grid(row=3, column=1)

		self.entry_rifa_pagada_familia=tk.Entry(label_frame_moviments_familia, width=15, state="disabled", disabledforeground="black", textvariable=self.rifa_pagada_familia)
		self.entry_rifa_pagada_familia.grid(row=3, column=2)

		self.entry_deute_rifa_familia=tk.Entry(label_frame_moviments_familia, width=15, state="disabled", disabledforeground="black", textvariable=self.deute_rifa_familia)
		self.entry_deute_rifa_familia.grid(row=3, column=3)

		self.entry_pagar_rifa_familia=tk.Entry(label_frame_moviments_familia, width=15, state="disabled", textvariable=self.pagar_rifa_familia)
		self.entry_pagar_rifa_familia.grid(row=3, column=4)
		self.entry_pagar_rifa_familia.bind('<FocusOut>', lambda event: self.calcular_pagar_total(event, self.entry_pagar_rifa_familia))
		self.entry_pagar_rifa_familia.bind('<FocusIn>', lambda event: self.fer_seleccio(event, self.entry_pagar_rifa_familia))

		self.label_total_familia=tk.Label(label_frame_moviments_familia, text="Totals:")
		self.label_total_familia.grid(row=4, column=0, sticky="e")

		self.entry_total_assignat_familia=tk.Entry(label_frame_moviments_familia, width=15, state="disabled", disabledforeground="black", textvariable=self.total_assignat_familia)
		self.entry_total_assignat_familia.grid(row=4, column=1)

		self.entry_total_pagat_familia=tk.Entry(label_frame_moviments_familia, width=15, state="disabled", disabledforeground="black", textvariable=self.total_pagat_familia)
		self.entry_total_pagat_familia.grid(row=4, column=2)

		self.entry_deute_total_familia=tk.Entry(label_frame_moviments_familia, width=15, state="disabled", disabledforeground="black", textvariable=self.deute_total_familia)
		self.entry_deute_total_familia.grid(row=4, column=3)

		self.entry_pagar_total_familia=tk.Entry(label_frame_moviments_familia, width=15, state="disabled", disabledforeground="black", textvariable=self.pagar_total_familia)
		self.entry_pagar_total_familia.grid(row=4, column=4)

		self.radio_button_familia_caixa=tk.Radiobutton(label_frame_moviments_familia, text="Caixa", variable=self.forma_pagament_familia, value=1)
		self.radio_button_familia_banc=tk.Radiobutton(label_frame_moviments_familia, text="Banc", variable=self.forma_pagament_familia, value=2)
		self.radio_button_familia_caixa.grid(row=5, column=2)
		self.radio_button_familia_banc.grid(row=5, column=3)
		self.radio_button_familia_caixa.select()

		self.button_pagar_familia=tk.Button(label_frame_moviments_familia, state="disabled", text="Pagar", command=self.PagarFam)
		self.button_pagar_familia.grid(row=5, column=4, padx=5, sticky="w"+"e")

		# Frame "Assignar".
		self.radio_button_quota=tk.Radiobutton(label_frame_assignar, text="Quota", variable=self.concepte_assignacio, value=1)
		self.radio_button_loteria=tk.Radiobutton(label_frame_assignar, text="Loteria", variable=self.concepte_assignacio, value=2)
		self.radio_button_rifa=tk.Radiobutton(label_frame_assignar, text="Rifa", variable=self.concepte_assignacio, value=3)
		self.radio_button_quota.grid(row=0, column=0)
		self.radio_button_loteria.grid(row=0, column=1)
		self.radio_button_rifa.grid(row=0, column=2)
		self.radio_button_quota.select()

		self.label_descripcio=tk.Label(label_frame_assignar, text="Descripció:")
		self.label_descripcio.grid(row=1, column=0, sticky="e")

		self.entry_descripcio_assignacio=tk.Entry(label_frame_assignar, state="disabled", textvariable=self.descripcio_assignacio)
		self.entry_descripcio_assignacio.grid(row=1, column=1, padx=2)

		self.label_assignar_quantitat=tk.Label(label_frame_assignar, text="Quantitat:")
		self.label_assignar_quantitat.grid(row=2, column=0, sticky="e")

		self.entry_total_assignacio=tk.Entry(label_frame_assignar, state="disabled", textvariable=self.total_assignacio)
		self.entry_total_assignacio.grid(row=2, column=1, padx=2)

		self.button_assignar=tk.Button(label_frame_assignar, state="disabled", text="Assignar", command=self.assignar)
		self.button_assignar.grid(row=2, column=2, padx=5)

		# Frame "Taula".
		self.tree_moviments=ttk.Treeview(label_frame_historial, height=10) # Li indiquem la altura.
		self.tree_moviments.grid(row=0, column=0, padx=10, pady=5)
		self.tree_moviments["columns"]=("uno","dos","tres","quatre","cinc") # Designem les columnes.
		self.tree_moviments.column("#0", width=80) # Designem els diferents amples.
		self.tree_moviments.column("uno", width=80)
		self.tree_moviments.column("dos", width=80)
		self.tree_moviments.column("tres", width=80)
		self.tree_moviments.column("quatre", width=80)
		self.tree_moviments.column("cinc", width=80)
		self.tree_moviments.heading("#0", text="moviment") # Rotulem les columnes.
		self.tree_moviments.heading('uno', text="data")
		self.tree_moviments.heading('dos', text="assignat")
		self.tree_moviments.heading('tres', text="pagat")
		self.tree_moviments.heading('quatre', text="concepte")
		self.tree_moviments.heading('cinc', text="descripció")

		self.scroll_taula=tk.Scrollbar(label_frame_historial, command=self.tree_moviments.yview) # Barra de desplaçament per a la taula.
		self.scroll_taula.grid(row=0, column=1, sticky="nsew") # La fem de l'altura de la taula.

		self.tree_moviments.config(yscrollcommand=self.scroll_taula.set) # Associem la taula a la barra per a que funcione correctament.

		# Bindegem la finestra per a que refresque quan pille el foco al tancar la finestra "modificar".
		self.bind("<FocusIn>", self.manejar_foco)


	def iniciar(self):
		'''
		Inicia la nova finestra omplint automàticament el camp "exercici"
		i ficant el foco en el id per a buscar faller.
		'''
		arxiu=Arxiu("exercici")
		exercici_actual=arxiu.llegir_exercici_actual()
		self.exercici.set(str(exercici_actual-1) + "-" + str(exercici_actual))
		self.entry_id.focus()
		self.grab_set()
		self.transient(self.master)
		self.mainloop()


	def manejar_foco(self, event):
		'''
		Controla el tancament de la finestra "Modificar" de forma que al tancar
		dita finestra, recupera el foco i torna a carregar totes les dades del faller
		ja actualitzades.
		'''
		if self.id.get()!="" and self.modificar_oberta==1:
			self.entry_id.focus()
			self.buscar_per_id('<Return>')
			self.modificar_oberta=0


	def modificar(self):
		''' 
		Crea una nova instància de la classe FinestraModificar
		que obri la finestra "Modificar" des del botó.
		'''
		modificar=FinestraModificar(self)
		self.modificar_oberta=1
		modificar.iniciar(int(self.id.get()))
		

	def canviar_estat(self):
		'''
		Canvia l'estat del faller d'alta a baixa i al revés.
		Es modifica el seu estat en la base de dades i es canvia també l'historial.
		Després es recalcula el descompte familiar depenent dels fallers que queden actius.
		'''
		arxiu=Arxiu("exercici")
		bd=BaseDeDades("falla.db")
		id=self.id.get()
		exercici_actual=arxiu.llegir_exercici_actual()
		faller=bd.llegir_faller(id)
		nom_arxiu="historials"+"/"+str(faller.id)
		arxiu=Arxiu(nom_arxiu)
		historial=arxiu.llegir_historial()
		if faller.alta==1:
			valor=messagebox.askquestion("Baixa","Estàs segur que vols donar de baixa al faller?")
			if valor=="yes":
				faller.alta=0
				bd.actualitzar_faller(faller)
				historial[exercici_actual]=["baixa", ""]
		elif faller.alta==0:
			valor=messagebox.askquestion("Alta","Estàs segur que vols donar d'alta al faller?")
			if valor=="yes":
				edat=faller.calcular_edat(faller.naixement, exercici_actual)
				# Asignem categoria per si ha canviat de tram mentre estava de baixa
				faller.categoria.calcular_categoria(edat)
				faller.categoria=bd.llegir_categoria(faller.categoria.id)
				faller.alta=1
				bd.actualitzar_faller(faller)
				historial[exercici_actual]=["vocal", "Sants Patrons"]				
		llistat_fallers=bd.llegir_fallers_per_familia(faller.familia.id)
		faller.familia.calcular_descompte(llistat_fallers)
		bd.actualitzar_familia(faller.familia)
		arxiu.modificar_historial(historial)
		self.entry_id.focus() # Fica el foco en el camp id.
		self.buscar_per_id('<Return>') # Refresca les dades fent la cerca de nou amb el id del faller.

	
	def buscar_per_id(self, event):
		'''
		Comprova que el faller amb l'id indicat està a la base de dades i, si es així
		llença la funció que ompli el formulari complet. En cas de no ser així mostra
		un error. Utilitza l'atribut "self.id_anterior" per a guardar l'identificador
		de l'últim faller mostrat per a tornar-lo a mostrar en cas d'error.
		Va associat a l'event de pulsar la tecla "Enter" dins del camp "id".
		'''
		bd=BaseDeDades("falla.db")
		id=self.id.get()
		faller=bd.llegir_ultim_faller()
		if faller.id < int(self.id.get()): # Si el id que fiquem es major que el de l'últim faller.
			messagebox.showwarning("Error", "No existeix un faller amb eixa id")
			if self.id_anterior==0: # Si es la primera cerca.
				self.id.set("")
			else:
				self.id.set(self.id_anterior) # Fiquem el id que hem buscat anteriorment.
		else:
			self.id_anterior=id # Guardem l'ultima cerca per si apareix un error en la següent.
			self.omplir_dades(id)
		

	def desplegar_faller(self):
		'''
		Controla el combobox comparant la cadena escrita amb la base de dades i mostrant els resultats en el combobox.
		Utilitza l'atribut "self.identificadors" per a passar el identificador de faller a la funció "seleccionar_faller".
		'''
		bd=BaseDeDades("falla.db")
		cadena=self.combo_box_faller.get()
		llistat_fallers=bd.llegir_fallers_per_cognom(cadena)
		llista=[] # Llista on anem a acumular els valors.
		self.identificadors=[]
		for faller in llistat_fallers:
			self.identificadors=self.identificadors+[faller.id]
			llista=llista + [(faller.cognoms + ", " + faller.nom)]
		self.combo_box_faller["values"]=llista # Insertem cada valor en el desplegable.

	
	def seleccionar_faller(self, event):
		'''
		Controla la selecció del combobox per a guardar el identificador del faller i omplir les dades a partir d'aquest.
		'''
		index=self.combo_box_faller.current()
		self.id.set(self.identificadors[index])
		self.identificadors=[]
		self.omplir_dades(self.id.get())
		

	def desplegar_familia(self):
		'''
		Ompli el combobox amb tots els familiars del faller.
		'''
		bd=BaseDeDades("falla.db")
		faller=bd.llegir_faller(self.id.get())
		llistat_fallers=bd.llegir_fallers_per_familia(faller.familia.id)
		llista=[]
		self.identificadors=[]
		for faller in llistat_fallers:
			self.identificadors=self.identificadors+[faller.id]
			llista=llista + [(faller.cognoms + ", " + faller.nom)]
		self.combo_box_familia["values"]=llista


	def seleccionar_familia(self, event):
		'''
		Controla la selecció del combobox per a guardar el identificador del familiar del faller
		i ompli les dades a partir d'aquest.
		'''
		index=self.combo_box_familia.current()
		self.id.set(self.identificadors[index])
		self.identificadors=[]
		self.omplir_dades(self.id.get())
		self.combo_box_familia.set("") # El borrem per a que no mostre l'últim nom.


	def omplir_dades(self, id):
		'''
		Ompli el formulari complet (dades, pagaments, familia...) a partir de l'id del faller.
		'''
		bd=BaseDeDades("falla.db")
		arxiu=Arxiu("exercici")
		falla=Falla()
		quota=0
		faller=bd.llegir_faller(id)

		# Omplim els camps de dades personals.
		self.combo_box_faller.set(faller.cognoms + ", " + faller.nom)
		self.naixement.set(faller.naixement)
		self.dni.set(faller.dni)
		self.adresa.set(faller.adresa)
		self.telefon.set(faller.telefon)
		self.correu.set(faller.correu)
		self.button_modificar.config(state="normal")

		# En cas de baixa, es mostren en roig els camps de dades personals.
		# Es dehabiliten els camps de pagament i d'assignació i el botó "alta" es fica en "Donar d'alta".
		if faller.alta==0: # Mostrem en verd o en roig els camps segons alta.
			self.button_alta.config(state="normal", text="Donar d'alta")
			self.entry_naixement.configure(disabledbackground="#ff3f3f", disabledforeground="white")
			self.entry_dni.configure(disabledbackground="#ff3f3f", disabledforeground="white")
			self.entry_adresa.configure(disabledbackground="#ff3f3f", disabledforeground="white")
			self.entry_telefon.configure(disabledbackground="#ff3f3f", disabledforeground="white")
			self.entry_correu.configure(disabledbackground="#ff3f3f", disabledforeground="white")
			self.pagar_quota.set("")
			self.entry_pagar_quota.config(state="disabled")
			self.pagar_loteria.set("")
			self.entry_pagar_loteria.config(state="disabled")
			self.pagar_rifa.set("")
			self.entry_pagar_rifa.config(state="disabled")
			self.pagar_total.set("")
			self.button_pagar.config(state="disabled")
			self.entry_descripcio_assignacio.config(state="disabled")
			self.total_assignacio.set("")
			self.entry_total_assignacio.config(state="disabled")
			self.button_assignar.config(state="disabled")
		# En cas de d'alta, es mostren en verd els camps de dades personals.
		# S'habiliten els camps de pagament i d'assignació i el botó "alta" es fica en "Donar de baixa". 
		else:
			self.button_alta.config(state="normal", text="Donar de baixa")
			self.entry_naixement.configure(disabledbackground="#98ff98", disabledforeground="black")
			self.entry_dni.configure(disabledbackground="#98ff98", disabledforeground="black")
			self.entry_adresa.configure(disabledbackground="#98ff98", disabledforeground="black")
			self.entry_telefon.configure(disabledbackground="#98ff98", disabledforeground="black")
			self.entry_correu.configure(disabledbackground="#98ff98", disabledforeground="black")
			self.pagar_quota.set("0") # Fiquem un 0 en el entry per a que no done error l'operació.
			self.entry_pagar_quota.config(state="normal") # Passa a normal per a poder operar.
			self.pagar_loteria.set("0")
			self.entry_pagar_loteria.config(state="normal")
			self.pagar_rifa.set("0")
			self.entry_pagar_rifa.config(state="normal")
			self.pagar_total.set("0 €")
			self.button_pagar.config(state="normal")
			self.entry_descripcio_assignacio.config(state="normal")
			self.total_assignacio.set("0")
			self.entry_total_assignacio.config(state="normal")
			self.button_assignar.config(state="normal")
			# Mostrem en groc als fallers dels quals ens falta la data de naixement com a recordatori de que l'hem de demanar.
			# Gastem la data "01-01-1900" per a quan no sabem la data de naixement però el faller és adult.
			if faller.naixement=="01-01-1900":
				self.entry_naixement.configure(disabledbackground="#ffff00")
				self.entry_dni.configure(disabledbackground="#ffff00")
				self.entry_adresa.configure(disabledbackground="#ffff00")
				self.entry_telefon.configure(disabledbackground="#ffff00")
				self.entry_correu.configure(disabledbackground="#ffff00")

		# Omplim els camps d'assignacions i pagaments del faller.
		quota_base=bd.llegir_quota_faller(faller.id)
		descompte=faller.familia.descompte*quota_base/100
		quota=quota_base-descompte # Busquem la quota corresponent al faller i li restem el descompte familiar.
		exercici_actual=arxiu.llegir_exercici_actual()
		# Busquem tots els moviments del faller en l'exercici i els separem en quotes, loteries o rifes i en assignat o pagat.
		llista_assignacions_pagaments=falla.calcular_assignacions_pagaments(faller.id, exercici_actual)
		# Assignem cada element de la llista a una variable per a que siga més fàcil d'identificar.
		quota_assignada=llista_assignacions_pagaments[0]
		quota_pagada=llista_assignacions_pagaments[1]
		loteria_assignada=llista_assignacions_pagaments[2]
		loteria_pagada=llista_assignacions_pagaments[3]
		rifa_assignada=llista_assignacions_pagaments[4]
		rifa_pagada=llista_assignacions_pagaments[5]
		quota_final=quota+quota_assignada
		self.quota_assignada.set("{0:.2f}".format(quota_final) + " €")
		self.quota_pagada.set("{0:.2f}".format(quota_pagada) + " €")
		self.deute_quota.set("{0:.2f}".format(quota_final-quota_pagada) + " €")
		self.loteria_assignada.set("{0:.2f}".format(loteria_assignada) + " €")
		self.loteria_pagada.set("{0:.2f}".format(loteria_pagada) + " €")
		self.deute_loteria.set("{0:.2f}".format(loteria_assignada-loteria_pagada) + " €")
		self.rifa_assignada.set("{0:.2f}".format(rifa_assignada) + " €")
		self.rifa_pagada.set("{0:.2f}".format(rifa_pagada) + " €")
		self.deute_rifa.set("{0:.2f}".format(rifa_assignada-rifa_pagada) + " €")
		self.total_assignat.set("{0:.2f}".format(quota_final+loteria_assignada+rifa_assignada) + " €")
		self.total_pagat.set("{0:.2f}".format(quota_pagada+loteria_pagada+rifa_pagada) + " €")
		self.deute_total.set("{0:.2f}".format((quota_final+loteria_assignada+rifa_assignada)-(quota_pagada+loteria_pagada+rifa_pagada)) + " €")

		# Omplim els camps d'assignacions i pagaments de la familia completa del faller.
		llistat_fallers=bd.llegir_fallers_per_familia(faller.familia.id)
		membres=0
		for faller in llistat_fallers:
			if faller.alta==1:
				membres=membres + 1
		self.membres_familia.set(membres)
		if faller.alta==1 and membres>1: # Activarem els camps si hi ha membres actius a la familia.
			self.pagar_quota_familia.set("0")
			self.entry_pagar_quota_familia.config(state="normal")
			self.pagar_loteria_familia.set("0")
			self.entry_pagar_loteria_familia.config(state="normal")
			self.pagar_rifa_familia.set("0")
			self.entry_pagar_rifa_familia.config(state="normal")
			self.pagar_total_familia.set("0 €")
			self.button_pagar_familia.config(state="normal")			
		else:
			self.pagar_quota_familia.set("")
			self.entry_pagar_quota_familia.config(state="disabled")
			self.pagar_loteria_familia.set("")
			self.entry_pagar_loteria_familia.config(state="disabled")
			self.pagar_rifa_familia.set("")
			self.entry_pagar_rifa_familia.config(state="disabled")
			self.pagar_total_familia.set("")
			self.button_pagar_familia.config(state="disabled")				
		# Iniciem les variables per a poder iterar.
		quota_familia=0
		quota_assignada_familia=0
		quota_pagada_familia=0
		loteria_assignada_familia=0
		loteria_pagada_familia=0
		rifa_assignada_familia=0
		rifa_pagada_familia=0
		for faller in llistat_fallers:
			if faller.alta==1:
				quota_base=bd.llegir_quota_faller(faller.id)
				descompte=(faller.familia.descompte*quota_base/100)
				quota_familia=quota_familia+quota_base-descompte
				llista_assignacions_pagaments=falla.calcular_assignacions_pagaments(faller.id, exercici_actual)
				# Assignem cada element de la llista a una variable per a que siga més fàcil d'identificar.
				quota_assignada_familia=quota_assignada_familia+llista_assignacions_pagaments[0]
				quota_pagada_familia=quota_pagada_familia+llista_assignacions_pagaments[1]
				loteria_assignada_familia=loteria_assignada_familia+llista_assignacions_pagaments[2]
				loteria_pagada_familia=loteria_pagada_familia+llista_assignacions_pagaments[3]
				rifa_assignada_familia=rifa_assignada_familia+llista_assignacions_pagaments[4]
				rifa_pagada_familia=rifa_pagada_familia+llista_assignacions_pagaments[5]
		quota_final_familia=quota_familia+quota_assignada_familia
		self.quota_assignada_familia.set("{0:.2f}".format(quota_final_familia) + " €") # Mostrem la quota de la familia.
		self.quota_pagada_familia.set("{0:.2f}".format(quota_pagada_familia) + " €") # Mostrem el total pagat de quota de la familia.
		self.deute_quota_familia.set("{0:.2f}".format(quota_final_familia-quota_pagada_familia) + " €")
		self.loteria_assignada_familia.set("{0:.2f}".format(loteria_assignada_familia) + " €")
		self.loteria_pagada_familia.set("{0:.2f}".format(loteria_pagada_familia) + " €")
		self.deute_loteria_familia.set("{0:.2f}".format(loteria_assignada_familia-loteria_pagada_familia) + " €")
		self.rifa_assignada_familia.set("{0:.2f}".format(rifa_assignada_familia) + " €")
		self.rifa_pagada_familia.set("{0:.2f}".format(rifa_pagada_familia) + " €")
		self.deute_rifa_familia.set("{0:.2f}".format(rifa_assignada_familia-rifa_pagada_familia) + " €")
		self.total_assignat_familia.set("{0:.2f}".format(quota_final_familia+loteria_assignada_familia+rifa_assignada_familia) + " €")
		self.total_pagat_familia.set("{0:.2f}".format(quota_pagada_familia+loteria_pagada_familia+rifa_pagada_familia) + " €")
		self.deute_total_familia.set("{0:.2f}".format((quota_final_familia-quota_pagada_familia)+(loteria_assignada_familia-loteria_pagada_familia)+(rifa_assignada_familia-rifa_pagada_familia)) + " €")

		# Reiniciem el valor de descripció de les assignacions.
		self.descripcio_assignacio.set("")	

		# Omplim les dades de la taula.
		self.tree_moviments.delete(*self.tree_moviments.get_children()) # Borrem la taula
		llistat_moviments=bd.llegir_moviments(id, exercici_actual)
		for moviment in llistat_moviments:
			if moviment.concepte==1:
				concepte="quota"
			elif moviment.concepte==2:
				concepte="loteria"
			elif moviment.concepte==3:
				concepte="rifa"
			if moviment.tipo==1: # Segons si es asignació o pagament fiquem la quantitat en una o altra columna
				self.tree_moviments.insert("","end", text=moviment.id, values=(moviment.data, "{0:.2f}".format(moviment.quantitat) + " €", "", concepte, moviment.descripcio))
			elif moviment.tipo==2:
				self.tree_moviments.insert("","end", text=moviment.id, values=(moviment.data, "", "{0:.2f}".format(moviment.quantitat) + " €", concepte, moviment.descripcio))

		
	def fer_seleccio(self, event, entry):
		'''
		Es bindeja a un camp de forma que al fer "FocusIn" en ell es selecciona el contingut
		del camp i es pot sobreescriure sense haver de borrar.

		Paràmetres:
        -----------
        entry : tkinter.Entry
            Camp en el que es fa el foco.
		'''
		entry.select_range(0, tk.END)

	
	def calcular_pagar_total(self, event, entry):
		'''
		Es bindeja a un camp de forma que al fer "FocusOut" en ell es comprova el contingut
		del camp per veure si es un valor correcte. En cas de ser així mostra la suma dels 3 camps
		en el camp total i en cas de que no ho siga el fica a 0, manté el foco per a poder canviar
		el valor i fa la suma però amb el valor del camp a 0.

		Paràmetres:
        -----------
        entry : tkinter.Entry
            Camp en el que es fa el foco.
		'''
		pagar_quota=0
		pagar_loteria=0
		pagar_rifa=0
		pagar_quota_familia=0
		pagar_loteria_familia=0
		pagar_rifa_familia=0
		# Camp "pagar_quota".
		if entry==self.entry_pagar_quota:
			pagar_loteria=float(self.entry_pagar_loteria.get())
			pagar_rifa=float(self.entry_pagar_rifa.get())
			try:
				pagar_quota=float(self.entry_pagar_quota.get())
			except ValueError:
				pagar_quota=0
				self.pagar_quota.set(0)
				messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
				self.entry_pagar_quota.focus()
			self.pagar_total.set("{0:.2f}".format(pagar_quota+pagar_loteria+pagar_rifa) + " €")
		# Camp "pagar_loteria".
		elif entry==self.entry_pagar_loteria:
			pagar_quota=float(self.entry_pagar_quota.get())
			pagar_rifa=float(self.entry_pagar_rifa.get())
			try:
				pagar_loteria=float(self.entry_pagar_loteria.get())
			except ValueError:
				pagar_loteria=0
				self.pagar_loteria.set(0)
				messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
				self.entry_pagar_loteria.focus()
			self.pagar_total.set("{0:.2f}".format(pagar_quota+pagar_loteria+pagar_rifa) + " €")
		# Camp "pagar_rifa".
		elif entry==self.entry_pagar_rifa:
			pagar_quota=float(self.entry_pagar_quota.get())
			pagar_loteria=float(self.entry_pagar_loteria.get())		
			try:
				pagar_rifa=float(self.entry_pagar_rifa.get())
			except ValueError:
				pagar_rifa=0
				self.pagar_rifa.set(0)
				messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
				self.entry_pagar_rifa.focus()
			self.pagar_total.set("{0:.2f}".format(pagar_quota+pagar_loteria+pagar_rifa) + " €")
		# Camp "pagar_quota_familia".
		elif entry==self.entry_pagar_quota_familia:
			pagar_loteria_familia=float(self.entry_pagar_loteria_familia.get())
			pagar_rifa_familia=float(self.entry_pagar_rifa_familia.get())
			try:
				pagar_quota_familia=float(self.entry_pagar_quota_familia.get())
			except ValueError:
				pagar_quota_familia=0
				self.pagar_quota_familia.set(0)
				messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
				self.entry_pagar_quota_familia.focus()
			if float(self.pagar_quota_familia.get())<0:
				pagar_quota_familia=0
				self.pagar_quota_familia.set(0)
				messagebox.showwarning("Error", "Els abonos només es poden fer als fallers per separat")
				self.entry_pagar_quota_familia.focus()
			self.pagar_total_familia.set("{0:.2f}".format(pagar_quota_familia+pagar_loteria_familia+pagar_rifa_familia) + " €")
		# Camp "pagar_loteria_familia".
		elif entry==self.entry_pagar_loteria_familia:
			pagar_quota_familia=float(self.entry_pagar_quota_familia.get())
			pagar_rifa_familia=float(self.entry_pagar_rifa_familia.get())
			try:
				pagar_loteria_familia=float(self.entry_pagar_loteria_familia.get())
			except ValueError:
				pagar_loteria_familia=0
				self.pagar_loteria_familia.set(0)
				messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
				self.entry_pagar_loteria_familia.focus()
			if float(self.pagar_loteria_familia.get())<0:
				pagar_loteria_familia=0
				self.pagar_loteria_familia.set(0)
				messagebox.showwarning("Error", "Els abonos només es poden fer als fallers per separat")
				self.entry_pagar_loteria_familia.focus()
			self.pagar_total_familia.set("{0:.2f}".format(pagar_quota_familia+pagar_loteria_familia+pagar_rifa_familia) + " €")
		# Camp "pagar_rifa_familia".
		elif entry==self.entry_pagar_rifa_familia:
			pagar_quota_familia=float(self.entry_pagar_quota_familia.get())
			pagar_loteria_familia=float(self.entry_pagar_loteria_familia.get())
			try:
				pagar_rifa_familia=float(self.entry_pagar_rifa_familia.get())
			except ValueError:
				pagar_rifa_familia=0
				self.pagar_rifa_familia.set(0)
				messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
				self.entry_pagar_rifa_familia.focus()
			if float(self.pagar_rifa_familia.get())<0:
				pagar_rifa_familia=0
				self.pagar_rifa_familia.set(0)
				messagebox.showwarning("Error", "Els abonos només es poden fer als fallers per separat")
				self.entry_pagar_rifa_familia.focus()
			self.pagar_total_familia.set("{0:.2f}".format(pagar_quota_familia+pagar_loteria_familia+pagar_rifa_familia) + " €")
		
	
	def Pagar(self):

		arxiu=Arxiu('exercici')
		bd=BaseDeDades('falla.db')
		utils=Utils()
		pagquo=0
		paglot=0
		pagrif=0
		if self.pagar_quota.get()=="":
			self.pagar_quota.set(0)
		if self.pagar_loteria.get()=="":
			self.pagar_loteria.set(0)
		if self.pagar_rifa.get()=="":
			self.pagar_rifa.set(0)
		try:
			pagquo=float(self.pagar_quota.get()) #guardem en variables les quantitats a pagar per a mostrar-les al rebut
		except ValueError:
			pagquo=0
			self.pagar_quota.set(0)
			self.pagar_total.set("{0:.2f}".format(paglot+pagrif) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
		try:
			paglot=float(self.pagar_loteria.get())
		except ValueError:
			paglot=0
			self.pagar_loteria.set(0)
			self.pagar_total.set("{0:.2f}".format(pagquo+pagrif) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
		try:
			pagrif=float(self.pagar_rifa.get())
		except ValueError:
			pagrif=0
			self.pagar_rifa.set(0)
			self.pagar_total.set("{0:.2f}".format(paglot+pagrif) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
		opcio=self.forma_pagament.get() #guardem l'opció triada per a la descripció de la base de dades
		descripcio=""
		if opcio=="1":
			descripcio="pagat en caixa"
		if opcio=="2":
			descripcio="pagat pel banc"
			#desc="domiciliació"
		valor=messagebox.askquestion("Pagar","Estàs segur que vols fer el pagament?")
		if valor=="yes":
			if self.pagar_quota.get()=="":
				self.pagar_quota.set("0")
			if self.pagar_loteria.get()=="":
				self.pagar_loteria.set("0")
			if self.pagar_rifa.get()=="":
				self.pagar_rifa.set("0")
			if float(self.pagar_quota.get())==0 and float(self.pagar_loteria.get())==0 and float(self.pagar_rifa.get())==0:
				messagebox.showwarning("Error", "No es pot fer un pagament de 0 euros")
			else:
				rebut=0
				#if opcio=="1":
					#busquem el número que li pertocarà al rebut
					#elRebut=Informe()
					#numrebut=elRebut.AsignarNumRebut()
				exercici_actual=arxiu.llegir_exercici_actual()
				data=utils.calcular_data_actual()
				data_actual=data[0] + "-" + data[1] + "-" + data[2]
				#id=self.idString.get()
				faller=bd.llegir_faller(self.id.get())
				#inserta a la base de dades cada moviment realitzat
				if float(self.pagar_quota.get())!=0:
					moviment=Moviment(0, data_actual, float(self.pagar_quota.get()), 2, 1, exercici_actual, descripcio, rebut, faller)
					bd.crear_moviment(moviment)
					#elMoviment.InsertarPagament(float(self.pagarquotaString.get()), 1, elMoviment.exercici, float(self.idString.get()), desc, numrebut)
				if float(self.pagar_loteria.get())!=0:
					moviment=Moviment(0, data_actual, float(self.pagar_loteria.get()), 2, 2, exercici_actual, descripcio, rebut, faller)
					bd.crear_moviment(moviment)
					#elMoviment.InsertarPagament(float(self.pagarloteriaString.get()), 2, elMoviment.exercici, float(self.idString.get()), desc, numrebut)
				if float(self.pagar_rifa.get())!=0:
					moviment=Moviment(0, data_actual, float(self.pagar_rifa.get()), 2, 3, exercici_actual, descripcio, rebut, faller)
					bd.crear_moviment(moviment)
					#elMoviment.InsertarPagament(float(self.pagarrifaString.get()), 3, elMoviment.exercici, float(self.idString.get()), desc, numrebut)
				#netegem les dades i refresquem per a vore el quadre de pagaments actualitzat
				self.entry_id.focus()
				self.buscar_per_id('<Return>')
				#if opcio=="1":
					#creem el rebut a partir de les dades de les variables dels pagaments i el quadre actualitzat amb el resutat final llevant els 2 últims caràcters ( €) als valors que necessiten un càlcul posterior
					#elRebut=Informe()
					#elRebut.Rebut(0,self.fallerCombo.get(), pagquo, paglot, pagrif, self.quotaString.get()[:-2], self.quotapagString.get()[:-2], self.loteriaString.get()[:-2], self.loteriapagString.get()[:-2], self.rifaString.get()[:-2], self.rifapagString.get()[:-2])			


	def PagarFam(self):

		bd=BaseDeDades("falla.db")
		falla=Falla()
		arxiu=Arxiu("exercici")
		utils=Utils()

		pagquofam=0
		paglotfam=0
		pagriffam=0
		if self.pagar_quota_familia.get()=="":
			self.pagar_quota_familia.set("0")
		if self.pagar_loteria_familia.get()=="":
			self.pagar_loteria_familia.set("0")
		if self.pagar_rifa_familia.get()=="":
			self.pagar_rifa_familia.set("0")
		try:
			pagquofam=float(self.pagar_quota_familia.get()) #guardem en variables les quantitats a pagar per a mostrar-les al rebut
			if float(self.pagar_quota_familia.get())<0:
				pagquofam=0
		except ValueError:
			pagquofam=0
			self.pagar_quota_familia.set(0)
			self.pagar_total_familia.set("{0:.2f}".format(paglotfam+pagriffam) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
		try:
			paglotfam=float(self.pagar_loteria_familia.get())
			if float(self.pagar_loteria_familia.get())<0:
				paglotfam=0
		except ValueError:
			paglotfam=0
			self.pagar_loteria_familia.set(0)
			self.pagar_total_familia.set("{0:.2f}".format(pagquofam+pagriffam) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
		try:
			pagriffam=float(self.pagar_rifa_familia.get())
			if float(self.pagar_rifa_familia.get())<0:
				pagriffam=0
		except ValueError:
			pagriffam=0
			self.pagar_rifa_familia.set(0)
			self.pagar_total_familia.set("{0:.2f}".format(paglotfam+pagriffam) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
		opcio=self.forma_pagament_familia.get()
		descripcio=""
		if opcio=="1":
			descripcio="pagat en caixa"
		if opcio=="2":
			descripcio="pagat pel banc"
		valor=messagebox.askquestion("Pagar","Estàs segur que vols fer el pagament?")
		if valor=="yes":
			if self.pagar_quota_familia.get()=="":
				self.pagar_quota_familia.set("0")
			if self.pagar_loteria_familia.get()=="":
				self.pagar_loteria_familia.set("0")
			if self.pagar_rifa_familia.get()=="":
				self.pagar_rifa_familia.set("0")
			if float(self.pagar_quota_familia.get())==0 and float(self.pagar_loteria_familia.get())==0 and float(self.pagar_rifa_familia.get())==0:
				messagebox.showwarning("Error", "No es pot fer un pagament de 0 euros")						
			else:
				faller=bd.llegir_faller(self.id.get())
				llistat_fallers=bd.llegir_fallers_per_familia(faller.familia.id)
				#falla.llegir_fallers("familia", faller.familia.id)
				membres=0
				idfaller=[]
				for faller in llistat_fallers:
					if faller.alta==1: #si el faller está actiu
						membres=membres + 1
						idfaller=idfaller+[faller.id] #afegim a la llista el id
				quota=0 #les iniciem a 0 perquè després s'autoacumulen
				quotaassignada=0
				quotapagada=0
				loteriaassignada=0
				loteriapagada=0
				rifaassignada=0
				rifapagada=0
				difquota=0
				difloteria=0
				difrifa=0
				pagamentquota=float(self.pagar_quota_familia.get()) #guardem els continguts en variables
				pagamentloteria=float(self.pagar_loteria_familia.get())
				pagamentrifa=float(self.pagar_rifa_familia.get())
				rebut=0
				#if opcio=="1":
					#busquem el número que li pertocarà al rebut
					#elRebut=Informe()
					#numrebut=elRebut.AsignarNumRebut()
				exercici_actual=arxiu.llegir_exercici_actual()
				data=utils.calcular_data_actual()
				data_actual=data[0] + "-" + data[1] + "-" + data[2]
				for faller in llistat_fallers:
					quota_base=bd.llegir_quota_faller(faller.id)
					descompte=(faller.familia.descompte*quota_base/100)
					quota=quota+quota_base-descompte
					llista_assignacions_pagaments=falla.calcular_assignacions_pagaments(faller.id, exercici_actual)
					# Assignem cada element de la llista a una variable per a que siga més fàcil d'identificar.
					quotaassignada=quotaassignada+llista_assignacions_pagaments[0]
					quotapagada=quotapagada+llista_assignacions_pagaments[1]
					loteriaassignada=loteriaassignada+llista_assignacions_pagaments[2]
					loteriapagada=loteriapagada+llista_assignacions_pagaments[3]
					rifaassignada=rifaassignada+llista_assignacions_pagaments[4]
					rifapagada=rifapagada+llista_assignacions_pagaments[5]
					quotafinal=quota+quotaassignada
				#for val in idfaller: #per a cada id de la llista calculem la quota, el descompte i els moviments d'assignació
					#elFaller.BuscarQuotaFaller(str(val))
					#laFamilia.BuscarDescompteFamilia(str(val))
					#quota=elFaller.quota-(laFamilia.descompte*elFaller.quota/100)
					#elMoviment.quotaasignada=0 #com que es va acumulant, s'ha de ficar a 0 en cada iteració
					#elMoviment.quotapagada=0
					#elMoviment.loteriaasignada=0
					#elMoviment.loteriapagada=0
					#elMoviment.rifaasignada=0
					#elMoviment.rifapagada=0
					#elMoviment.BuscarMoviments(str(val),str(elMoviment.exercici))
					#quotaasignada=elMoviment.quotaasignada
					#quotapagada=elMoviment.quotapagada
					difquota=quotafinal-quotapagada
					if pagamentquota!=0 and membres==1:
						moviment=Moviment(0, data_actual, pagamentquota, 2, 1, exercici_actual, descripcio, rebut, faller)
						bd.crear_moviment(moviment)
						#elMoviment.InsertarPagament(pagamentquota, 1, elMoviment.exercici, val, desc, numrebut)
						pagamentquota=0
					if pagamentquota!=0 and pagamentquota<=difquota and membres!=1:
						moviment=Moviment(0, data_actual, pagamentquota, 2, 1, exercici_actual, descripcio, rebut, faller)
						bd.crear_moviment(moviment)
						#elMoviment.InsertarPagament(pagamentquota, 1, elMoviment.exercici, val, desc, numrebut)
						pagamentquota=0
					if pagamentquota!=0 and pagamentquota>difquota and membres!=1:
						if difquota!=0: #per a que no cree moviments a 0
							moviment=Moviment(0, data_actual, difquota, 2, 1, exercici_actual, descripcio, rebut, faller)
							bd.crear_moviment(moviment)
						#elMoviment.InsertarPagament(difquota, 1, elMoviment.exercici, val, desc, numrebut)
						pagamentquota=pagamentquota-difquota
					#loteriaasignada=elMoviment.loteriaasignada
					#loteriapagada=elMoviment.loteriapagada
					difloteria=loteriaassignada-loteriapagada
					if pagamentloteria!=0 and membres==1:
						moviment=Moviment(0, data_actual, pagamentloteria, 2, 2, exercici_actual, descripcio, rebut, faller)
						bd.crear_moviment(moviment)
						#elMoviment.InsertarPagament(pagamentloteria, 2, elMoviment.exercici, val, desc, numrebut)
					if pagamentloteria!=0 and pagamentloteria<=difloteria and membres!=1:
						moviment=Moviment(0, data_actual, pagamentloteria, 2, 2, exercici_actual, descripcio, rebut, faller)
						bd.crear_moviment(moviment)
						#elMoviment.InsertarPagament(pagamentloteria, 2, elMoviment.exercici, val, desc, numrebut)
						pagamentloteria=0
					if pagamentloteria!=0 and pagamentloteria>difloteria and membres!=1:
						if difloteria!=0:
							moviment=Moviment(0, data_actual, difloteria, 2, 2, exercici_actual, descripcio, rebut, faller)
							bd.crear_moviment(moviment)
							#elMoviment.InsertarPagament(difloteria, 2, elMoviment.exercici, val, desc, numrebut)
						pagamentloteria=pagamentloteria-difloteria
					#rifaasignada=elMoviment.rifaasignada
					#rifapagada=elMoviment.rifapagada
					difrifa=rifaassignada-rifapagada
					if pagamentrifa!=0 and membres==1:
						moviment=Moviment(0, data_actual, pagamentrifa, 2, 3, exercici_actual, descripcio, rebut, faller)
						bd.crear_moviment(moviment)
						#elMoviment.InsertarPagament(pagamentrifa, 3, elMoviment.exercici, val, desc, numrebut)
					if pagamentrifa!=0 and pagamentrifa<=difrifa and membres!=1:
						moviment=Moviment(0, data_actual, pagamentrifa, 2, 3, exercici_actual, descripcio, rebut, faller)
						bd.crear_moviment(moviment)
						#elMoviment.InsertarPagament(pagamentrifa, 3, elMoviment.exercici, val, desc, numrebut)
						pagamentrifa=0
					if pagamentrifa!=0 and pagamentrifa>difrifa and membres!=1:
						if difrifa!=0:
							moviment=Moviment(0, data_actual, difrifa, 2, 3, exercici_actual, descripcio, rebut, faller)
							bd.crear_moviment(moviment)
							#elMoviment.InsertarPagament(difrifa, 3, elMoviment.exercici, val, desc, numrebut)
						pagamentrifa=pagamentrifa-difrifa
					membres=membres-1
				self.entry_id.focus()
				self.buscar_per_id('<Return>')
				#if opcio=="1":
					#creem el rebut a partir de les dades de les variables dels pagaments i el quadre actualitzat amb el resutat final llevant els 2 últims caràcters ( €) als valors que necessiten un càlcul posterior
					#elRebut.Rebut(1,self.fallerCombo.get(), pagquofam, paglotfam, pagriffam, self.quotafamString.get()[:-2], self.quotapagadafamString.get()[:-2], self.loteriafamString.get()[:-2], self.loteriapagadafamString.get()[:-2], self.rifafamString.get()[:-2], self.rifapagadafamString.get()[:-2])

	
	def assignar(self):
		'''
		Crea un moviment d'assignació de quota, loteria o rifa amb la descripció que li fiquem.
		'''
		arxiu=Arxiu("exercici")
		bd=BaseDeDades("falla.db")
		utils=Utils()
		exercici_actual=arxiu.llegir_exercici_actual()
		data=utils.calcular_data_actual()
		data_actual=data[0] + "-" + data[1] + "-" + data[2]
		valor=messagebox.askquestion("Asignar","Estàs segur que vols fer l'assignació?")
		if valor=="yes":
			try:
				if float(self.total_assignacio.get())==0:
					messagebox.showwarning("Error", "No es pot fer una assignació de 0 euros")
				else:
					faller=bd.llegir_faller(self.id.get())
					moviment=Moviment(0, data_actual, float(self.total_assignacio.get()), 1, int(self.concepte_assignacio.get()), exercici_actual, self.descripcio_assignacio.get(), 0, faller)
					bd.crear_moviment(moviment)
					self.entry_id.focus()
					self.buscar_per_id('<Return>')
			except ValueError:
				messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
				self.total_assignacio.set(0)