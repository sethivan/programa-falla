import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import LabelFrame
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
        sistema_operatiu=platform.system()
        if sistema_operatiu=='Windows':
            self.iconbitmap("escut.ico")
        self.resizable(0,0)
        self.title("Llistats")

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
        label_frame_moviments_dia=LabelFrame(self, text="Moviments dia")
        label_frame_moviments_dia.grid(row=0, column=0)

        label_frame_fallers=LabelFrame(self, text="Llistat fallers")
        label_frame_fallers.grid(row=1, column=0)

        label_frame_altres_llistats=LabelFrame(self, text="Altres llistats")
        label_frame_altres_llistats.grid(row=2, column=0)

        # Widgets per a cada frame.

        # Frame "Moviments dia".
        self.label_data_moviments_dia=ttk.Label(label_frame_moviments_dia, text="Data: ")
        self.label_data_moviments_dia.grid(row=0, column=0)

        self.entry_data_moviments_dia=ttk.Entry(label_frame_moviments_dia, textvariable=self.data_moviments_dia)
        self.entry_data_moviments_dia.grid(row=0, column=1)

        self.check_button_efectiu=tk.Checkbutton(label_frame_moviments_dia, text="Efectiu", variable=self.efectiu)
        self.check_button_efectiu.grid(row=0, column=2)
        self.check_button_efectiu.select()
        self.check_button_banc=tk.Checkbutton(label_frame_moviments_dia, text="Banc", variable=self.banc)
        self.check_button_banc.grid(row=0, column=3)
        self.check_button_banc.select()

        self.button_moviments_dia=ttk.Button(label_frame_moviments_dia, text="Llistat moviments", command=self.crear_llistat_moviments)
        self.button_moviments_dia.grid(row=0, column=4)

        # Frame "Llistat fallers".
        self.label_dades_fallers=ttk.Label(label_frame_fallers, text="Dades a mostrar: ")
        self.label_dades_fallers.grid(row=0, column=0)
        
        self.check_button_nom_complet=tk.Checkbutton(label_frame_fallers, text="Nom complet", variable=self.nom_complet)
        self.check_button_nom_complet.grid(row=0, column=1)
        self.check_button_nom_complet.select()

        self.check_button_dni=tk.Checkbutton(label_frame_fallers, text="DNI", variable=self.dni)
        self.check_button_dni.grid(row=0, column=2)
        self.check_button_dni.select()

        self.check_button_adresa=tk.Checkbutton(label_frame_fallers, text="Adreça", variable=self.adresa)
        self.check_button_adresa.grid(row=0, column=3)
        self.check_button_adresa.select()

        self.check_button_telefon=tk.Checkbutton(label_frame_fallers, text="Telèfon", variable=self.telefon)
        self.check_button_telefon.grid(row=0, column=4)
        self.check_button_telefon.select()

        self.check_button_data_naixement=tk.Checkbutton(label_frame_fallers, text="Data de naixement", variable=self.data_naixement)
        self.check_button_data_naixement.grid(row=0, column=5)
        self.check_button_data_naixement.select()

        self.check_button_correu_electronic=tk.Checkbutton(label_frame_fallers, text="Correu electrònic", variable=self.correu_electronic)
        self.check_button_correu_electronic.grid(row=0, column=6)
        self.check_button_correu_electronic.select()

        self.label_opcions_fallers=ttk.Label(label_frame_fallers, text="Opcions: ")
        self.label_opcions_fallers.grid(row=1, column=0)

        self.radio_button_complet=tk.Radiobutton(label_frame_fallers, text="Complet", variable=self.opcio, value=1, command=self.deshabilitar_opcions)
        self.radio_button_categories=tk.Radiobutton(label_frame_fallers, text="Per categories", variable=self.opcio, value=2, command=self.habilitar_categories)
        self.radio_button_edats=tk.Radiobutton(label_frame_fallers, text="Per edats", variable=self.opcio, value=3, command=self.habilitar_edats)
        self.radio_button_complet.grid(row=1, column=1)
        self.radio_button_categories.grid(row=1, column=2)
        self.radio_button_edats.grid(row=1, column=3)
        self.radio_button_complet.select()

        self.label_categories_fallers=ttk.Label(label_frame_fallers, text="Categories: ")
        self.label_categories_fallers.grid(row=2,column=0)

        self.check_button_adult=tk.Checkbutton(label_frame_fallers, state="disabled", text="Adult", variable=self.adult)
        self.check_button_adult.grid(row=2, column=1)
        self.check_button_adult.select()

        self.check_button_cadet=tk.Checkbutton(label_frame_fallers, state="disabled", text="Cadet", variable=self.cadet)
        self.check_button_cadet.grid(row=2, column=2)

        self.check_button_juvenil=tk.Checkbutton(label_frame_fallers, state="disabled", text="Juvenil", variable=self.juvenil)
        self.check_button_juvenil.grid(row=2, column=3)

        self.check_button_infantil=tk.Checkbutton(label_frame_fallers, state="disabled", text="Infantil", variable=self.infantil)
        self.check_button_infantil.grid(row=2, column=4)

        self.check_button_bebe=tk.Checkbutton(label_frame_fallers, state="disabled", text="Bebè", variable=self.bebe)
        self.check_button_bebe.grid(row=2, column=5)

        self.label_edats_fallers=ttk.Label(label_frame_fallers, text="Edats: ")
        self.label_edats_fallers.grid(row=3,column=0)

        self.label_edat_inicial=ttk.Label(label_frame_fallers, text="Edat inicial: ")
        self.label_edat_inicial.grid(row=3,column=1)

        self.entry_edat_inicial=ttk.Entry(label_frame_fallers, state="disabled", textvariable=self.edat_inicial)
        self.entry_edat_inicial.grid(row=3, column=2)

        self.label_edat_final=ttk.Label(label_frame_fallers, text="Edat final: ")
        self.label_edat_final.grid(row=3, column=3)

        self.entry_edat_final=ttk.Entry(label_frame_fallers, state="disabled", textvariable=self.edat_final)
        self.entry_edat_final.grid(row=3, column=4)

        self.button_fallers=ttk.Button(label_frame_fallers, text="Llistat fallers", command=self.crear_llistat_fallers)
        self.button_fallers.grid(row=3, column=5)

        # Frame "Altres llistats"
        self.button_general=ttk.Button(label_frame_altres_llistats, text="Llistat general", command=self.crear_llistat_general)
        self.button_general.grid(row=0, column=0)

        self.button_altes_baixes=ttk.Button(label_frame_altres_llistats, text="Llistat altes i baixes", command=self.crear_llistat_altes_baixes)
        self.button_altes_baixes.grid(row=0, column=1)


    def iniciar(self):
        '''
        Inicia la nova finestra.
        '''
        utils=Utils()
        data_actual=utils.calcular_data_actual()
        self.data_moviments_dia.set(data_actual[0]+"-"+data_actual[1]+"-"+data_actual[2])
        self.grab_set()
        self.transient(self.master)

    
    def deshabilitar_opcions(self):
        self.check_button_adult.configure(state="disabled")
        self.check_button_cadet.configure(state="disabled")
        self.check_button_juvenil.configure(state="disabled")
        self.check_button_infantil.configure(state="disabled")
        self.check_button_bebe.configure(state="disabled")
        self.entry_edat_final.configure(state="disabled")
        self.entry_edat_final.configure(state="disabled")


    def habilitar_categories(self):
        self.check_button_adult.configure(state="normal")
        self.check_button_cadet.configure(state="normal")
        self.check_button_juvenil.configure(state="normal")
        self.check_button_infantil.configure(state="normal")
        self.check_button_bebe.configure(state="normal")
        self.entry_edat_final.configure(state="disabled")
        self.entry_edat_final.configure(state="disabled")


    def habilitar_edats(self):
        self.check_button_adult.configure(state="disabled")
        self.check_button_cadet.configure(state="disabled")
        self.check_button_juvenil.configure(state="disabled")
        self.check_button_infantil.configure(state="disabled")
        self.check_button_bebe.configure(state="disabled")
        self.entry_edat_final.configure(state="normal")
        self.entry_edat_final.configure(state="normal")

    
    def crear_llistat_moviments(self):
        informe=Informe()
        if self.efectiu.get()==0 and self.banc.get()==0:
            messagebox.showwarning("Error", "Has de marcar com a mínim una de les opcions per a fer el llistat")
        else:
            informe.llistat_moviments(self.data_moviments_dia.get(), self.efectiu.get(), self.banc.get())


    def crear_llistat_fallers(self):
        pass


    def crear_llistat_general(self):
        pass


    def crear_llistat_altes_baixes(self):
        pass
