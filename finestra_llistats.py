import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import platform

from utils import Utils
from base_de_dades import BaseDeDades
from informe import Informe


class FinestraLlistats(tk.Toplevel):
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
        self.sistema_operatiu=platform.system()
        if self.sistema_operatiu=='Windows':
            self.iconbitmap("escut.ico")
        self.resizable(0,0)
        self.title("Llistats")
        utils=Utils()
        utils.definir_estil_global()
        self.configure(bg="#ffffff", pady=5, padx=5)

        self.data_moviments_dia=tk.StringVar()
        self.efectiu=tk.IntVar()
        self.banc=tk.IntVar()
        self.nom_complet=tk.IntVar()
        self.dni=tk.IntVar()
        self.adresa=tk.IntVar()
        self.telefon=tk.IntVar()
        self.data_naixement=tk.IntVar()
        self.correu_electronic=tk.IntVar()
        self.adult=tk.IntVar()
        self.cadet=tk.IntVar()
        self.juvenil=tk.IntVar()
        self.infantil=tk.IntVar()
        self.bebe=tk.IntVar()
        self.opcio=tk.IntVar()
        self.edat_inicial=tk.StringVar()
        self.edat_final=tk.StringVar()

        # Frames en els que dividim la finestra.
        label_estil_moviments_dia=ttk.Label(self, text="Moviments dia", style="Titol.TLabel")
        label_frame_moviments_dia=ttk.LabelFrame(self, style="Marc.TFrame", labelwidget=label_estil_moviments_dia)
        label_frame_moviments_dia.grid(row=0, column=0, padx=5, pady=5, ipadx=2, ipady=3)

        label_estil_fallers=ttk.Label(self, text="Llistat fallers", style="Titol.TLabel")
        label_frame_fallers=ttk.LabelFrame(self, style="Marc.TFrame", labelwidget=label_estil_fallers)
        label_frame_fallers.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5)

        label_estil_altres_llistats=ttk.Label(self, text="Altres llistats", style="Titol.TLabel")
        label_frame_altres_llistats=ttk.LabelFrame(self, style="Marc.TFrame", labelwidget=label_estil_altres_llistats)
        label_frame_altres_llistats.grid(row=2, column=0, padx=5, pady=5, ipadx=2, ipady=3)

        # Widgets per a cada frame.

        # Frame "Moviments dia".
        self.label_data_moviments_dia=ttk.Label(label_frame_moviments_dia, text="Data", style="Etiqueta.TLabel")
        self.label_data_moviments_dia.grid(row=0, column=0, padx=5, pady=5)

        self.entry_data_moviments_dia=ttk.Entry(label_frame_moviments_dia, width=10, textvariable=self.data_moviments_dia)
        self.entry_data_moviments_dia.grid(row=0, column=1, padx=5, pady=5)

        self.check_button_efectiu=ttk.Checkbutton(label_frame_moviments_dia, text="Efectiu", style="Check.TCheckbutton", variable=self.efectiu)
        self.check_button_efectiu.grid(row=0, column=2, padx=5, pady=5)
        self.check_button_banc=ttk.Checkbutton(label_frame_moviments_dia, text="Banc", style="Check.TCheckbutton", variable=self.banc)
        self.check_button_banc.grid(row=0, column=3, padx=5, pady=5)

        self.button_moviments_dia=ttk.Button(label_frame_moviments_dia, text="Llistat moviments", style="Boto.TButton", command=self.crear_llistat_moviments)
        self.button_moviments_dia.grid(row=0, column=4, padx=5, pady=5)

        # Frame "Llistat fallers".
        self.check_button_nom_complet=ttk.Checkbutton(label_frame_fallers, text="Nom complet", style="Check.TCheckbutton", variable=self.nom_complet)
        self.check_button_nom_complet.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        self.check_button_dni=ttk.Checkbutton(label_frame_fallers, text="DNI", style="Check.TCheckbutton", variable=self.dni)
        self.check_button_dni.grid(row=1, column=0, padx=5, pady=2, sticky="w")

        self.check_button_adresa=ttk.Checkbutton(label_frame_fallers, text="Adreça", style="Check.TCheckbutton", variable=self.adresa)
        self.check_button_adresa.grid(row=2, column=0, padx=5, pady=2, sticky="w")

        self.check_button_telefon=ttk.Checkbutton(label_frame_fallers, text="Telèfon", style="Check.TCheckbutton", variable=self.telefon)
        self.check_button_telefon.grid(row=3, column=0, padx=5, pady=2, sticky="w")

        self.check_button_data_naixement=ttk.Checkbutton(label_frame_fallers, text="Data de naixement", style="Check.TCheckbutton", variable=self.data_naixement)
        self.check_button_data_naixement.grid(row=4, column=0, padx=5, pady=2, sticky="w")

        self.check_button_correu_electronic=ttk.Checkbutton(label_frame_fallers, text="Correu electrònic", style="Check.TCheckbutton", variable=self.correu_electronic)
        self.check_button_correu_electronic.grid(row=5, column=0, padx=5, pady=2, sticky="w")

        self.radio_button_complet=ttk.Radiobutton(label_frame_fallers, text="Complet", style="Radio.TRadiobutton", variable=self.opcio, value=1, command=self.deshabilitar_opcions)
        self.radio_button_categories=ttk.Radiobutton(label_frame_fallers, text="Per categories", style="Radio.TRadiobutton", variable=self.opcio, value=2, command=self.habilitar_categories)
        self.radio_button_edats=ttk.Radiobutton(label_frame_fallers, text="Per edats", style="Radio.TRadiobutton", variable=self.opcio, value=3, command=self.habilitar_edats)
        self.radio_button_complet.grid(row=0, column=3, padx=5, pady=2, sticky="w")
        self.radio_button_categories.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.radio_button_edats.grid(row=0, column=2, padx=5, pady=2, sticky="w")

        self.check_button_adult=ttk.Checkbutton(label_frame_fallers, state="disabled", text="Adult", style="Check.TCheckbutton", variable=self.adult)
        self.check_button_adult.grid(row=1, column=1, padx=5, sticky="w")

        self.check_button_cadet=ttk.Checkbutton(label_frame_fallers, state="disabled", text="Cadet", style="Check.TCheckbutton", variable=self.cadet)
        self.check_button_cadet.grid(row=2, column=1, padx=5, sticky="w")

        self.check_button_juvenil=ttk.Checkbutton(label_frame_fallers, state="disabled", text="Juvenil", style="Check.TCheckbutton", variable=self.juvenil)
        self.check_button_juvenil.grid(row=3, column=1, padx=5, sticky="w")

        self.check_button_infantil=ttk.Checkbutton(label_frame_fallers, state="disabled", text="Infantil", style="Check.TCheckbutton", variable=self.infantil)
        self.check_button_infantil.grid(row=4, column=1, padx=5, sticky="w")

        self.check_button_bebe=ttk.Checkbutton(label_frame_fallers, state="disabled", text="Bebè", style="Check.TCheckbutton", variable=self.bebe)
        self.check_button_bebe.grid(row=5, column=1, padx=5, sticky="w")

        self.label_edat_inicial=ttk.Label(label_frame_fallers, text="edat inicial", style="Etiqueta.TLabel")
        self.label_edat_inicial.grid(row=1, column=2, padx=5, sticky="w")

        self.entry_edat_inicial=ttk.Entry(label_frame_fallers, width=5, state="disabled", textvariable=self.edat_inicial)
        self.entry_edat_inicial.grid(row=2, column=2, padx=5, sticky="w")

        self.label_edat_final=ttk.Label(label_frame_fallers, text="edat final", style="Etiqueta.TLabel")
        self.label_edat_final.grid(row=3, column=2, padx=5, sticky="w")

        self.entry_edat_final=ttk.Entry(label_frame_fallers, width=5, state="disabled", textvariable=self.edat_final)
        self.entry_edat_final.grid(row=4, column=2, padx=5, sticky="w")

        self.button_fallers=ttk.Button(label_frame_fallers, text="Llistat fallers", style="Boto.TButton", command=self.crear_llistat_fallers)
        self.button_fallers.grid(row=4, column=3, rowspan=2, sticky="s")

        # Frame "Altres llistats"
        self.button_general=ttk.Button(label_frame_altres_llistats, text="Llistat general", style="Boto.TButton", command=self.crear_llistat_general)
        self.button_general.grid(row=0, column=0, padx=5, pady=3)

        self.button_altes_baixes=ttk.Button(label_frame_altres_llistats, text="Llistat altes i baixes", style="Boto.TButton", command=self.crear_llistat_altes_baixes)
        self.button_altes_baixes.grid(row=0, column=1, padx=5, pady=3)


    def iniciar(self):
        '''
        Inicia la nova finestra.
        '''
        utils=Utils()
        data_actual=utils.calcular_data_actual()
        self.data_moviments_dia.set(data_actual[0]+"-"+data_actual[1]+"-"+data_actual[2])
        self.efectiu.set(1)
        self.banc.set(1)
        self.nom_complet.set(1)
        self.dni.set(1)
        self.adresa.set(1)
        self.telefon.set(1)
        self.data_naixement.set(1)
        self.correu_electronic.set(1)
        self.adult.set(1)
        self.opcio.set(1)
        self.grab_set()
        self.transient(self.master)

    
    def deshabilitar_opcions(self):
        self.check_button_adult.configure(state="disabled")
        self.check_button_cadet.configure(state="disabled")
        self.check_button_juvenil.configure(state="disabled")
        self.check_button_infantil.configure(state="disabled")
        self.check_button_bebe.configure(state="disabled")
        self.entry_edat_inicial.configure(state="disabled")
        self.entry_edat_final.configure(state="disabled")


    def habilitar_categories(self):
        self.check_button_adult.configure(state="normal")
        self.check_button_cadet.configure(state="normal")
        self.check_button_juvenil.configure(state="normal")
        self.check_button_infantil.configure(state="normal")
        self.check_button_bebe.configure(state="normal")
        self.entry_edat_inicial.configure(state="disabled")
        self.entry_edat_final.configure(state="disabled")


    def habilitar_edats(self):
        self.check_button_adult.configure(state="disabled")
        self.check_button_cadet.configure(state="disabled")
        self.check_button_juvenil.configure(state="disabled")
        self.check_button_infantil.configure(state="disabled")
        self.check_button_bebe.configure(state="disabled")
        self.entry_edat_inicial.configure(state="normal")
        self.entry_edat_final.configure(state="normal")

    
    def crear_llistat_moviments(self):
        informe=Informe()
        if self.efectiu.get()==0 and self.banc.get()==0:
            messagebox.showwarning("Error", "Has de marcar com a mínim una de les opcions per a fer el llistat")
        else:
            informe.llistat_moviments(self.data_moviments_dia.get(), self.efectiu.get(), self.banc.get())


    def crear_llistat_fallers(self):
        bd=BaseDeDades('falla.db')
        informe=Informe()
        # Guardem en un llistat les dades marcades a mostrar.
        llistat_dades=[]
        if self.nom_complet.get()==1:
            llistat_dades.append("nom")
        if self.dni.get()==1:
            llistat_dades.append("dni")
        if self.adresa.get()==1:
            llistat_dades.append("adreça")
        if self.telefon.get()==1:
            llistat_dades.append("telefon")
        if self.data_naixement.get()==1:
            llistat_dades.append("naixement")
        if self.correu_electronic.get()==1:
            llistat_dades.append("correu")
        if len(llistat_dades)==6:
            messagebox.showwarning("Error", "Marca 5 opcions de dades com a màxim")
        else:
            # Cridem a la funció corresponent segons l'opció marcada.
            if self.opcio.get()==1:
                informe.llistat_fallers(llistat_dades)
            elif self.opcio.get()==2:
                llistat_categories=[]
                if self.adult.get()==1:
                    llistat_categories.append(1)
                if self.cadet.get()==1:
                    llistat_categories.append(2)
                if self.juvenil.get()==1:
                    llistat_categories.append(3)
                if self.infantil.get()==1:
                    llistat_categories.append(4)
                if self.bebe.get()==1:
                    llistat_categories.append(5)
                informe.llistat_fallers_per_categories(llistat_categories, llistat_dades)
            elif self.opcio.get()==3:
                informe.llistat_fallers_per_edat(int(self.edat_inicial.get()), int(self.edat_final.get()), llistat_dades)


    def crear_llistat_general(self):
        informe=Informe()
        informe.llistat_general()


    def crear_llistat_altes_baixes(self):
        informe=Informe()
        informe.llistat_altes_baixes()
