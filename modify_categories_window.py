import tkinter as tk
import tkinter.ttk as ttk
import platform

from utils import Utils

from falla import Falla
from category import Category


class ModifyCategoriesWindow(tk.Toplevel):
    '''
	Esta classe representa una nova finestra que depén de la finestra principal.

	Atributs:
	---------
	master : tk.Tk o tk.Toplevel
		La instància principal de l'aplicació o de la finestra que crea esta nova finestra.
	'''


    def __init__(self, master = None):
        '''
		Inicialitza una nova instància de la classe ModifyCategoriesWindow.

		Parametres:
		-----------
		master : tk.Tk o tk.Toplevel, opcional
			La instància principal de l'aplicació o de la finestra que crea esta nova finestra.
			Si no se proporciona, se creará una nueva instancia de tk.Tk().
		'''
        super().__init__(master)
        self.master = master
        self.sistema_operatiu = platform.system()
        if self.sistema_operatiu == 'Windows':
            self.iconbitmap("escut.ico")
        self.resizable(0,0)
        self.title("Modificar Categories")
        utils=Utils()
        utils.define_global_style()
        self.configure(bg = "#ffffff", pady = 5, padx = 5)

        self.adult_fee = tk.StringVar()
        self.cadet_fee = tk.StringVar()
        self.youth_fee = tk.StringVar()
        self.childish_fee = tk.StringVar()
        self.baby_fee = tk.StringVar()

        # Widgets
        self.label_adult_name = ttk.Label(self, text = "Adult (major d'edat)", style = "Etiqueta.TLabel")
        self.label_adult_name.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "w")

        self.entry_adult_fee = ttk.Entry(self, width = 6, justify = "right", textvariable = self.adult_fee)
        self.entry_adult_fee.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.label_cadet_name = ttk.Label(self, text = "Cadet (entre 14 i 17 anys)", style = "Etiqueta.TLabel")
        self.label_cadet_name.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "w")

        self.entry_cadet_fee = ttk.Entry(self, width = 6, justify = "right", textvariable = self.cadet_fee)
        self.entry_cadet_fee.grid(row = 1, column = 1, padx = 5, pady = 5)

        self.label_youth_name = ttk.Label(self, text = "Juvenil (entre 10 i 13 anys)", style = "Etiqueta.TLabel")
        self.label_youth_name.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "w")

        self.entry_youth_fee = ttk.Entry(self, width = 6, justify = "right", textvariable = self.youth_fee)
        self.entry_youth_fee.grid(row = 2, column = 1, padx = 5, pady = 5)

        self.label_childish_name = ttk.Label(self, text = "Infantil (entre 5 i 9 anys)", style = "Etiqueta.TLabel")
        self.label_childish_name.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "w")

        self.entry_childish_fee = ttk.Entry(self, width = 6, justify = "right", textvariable = self.childish_fee)
        self.entry_childish_fee.grid(row = 3, column = 1, padx = 5, pady = 5)

        self.label_baby_name = ttk.Label(self, text = "Bebe (menor de 5 anys)", style = "Etiqueta.TLabel")
        self.label_baby_name.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = "w")

        self.entry_baby_fee=ttk.Entry(self, width = 6, justify = "right", textvariable = self.baby_fee)
        self.entry_baby_fee.grid(row = 4, column = 1, padx = 5, pady = 5)

        self.button_modify=ttk.Button(self, width=15, text="Modificar", style="Boto.TButton", command=self.modify_categories)
        self.button_modify.grid(row=5, column=0, columnspan=2, pady=5)
        
		# Inicia la nova finestra accedint a la taula "category" de la base de dades i omplint tots els camps.
        falla = Falla()
        falla.get_categories()
        for category in falla.categories_list:
            if category.id == 1:
                self.adult_fee.set(category.fee)
            elif category.id == 2:
                self.cadet_fee.set(category.fee)
            elif category.id == 3:
                self.youth_fee.set(category.fee)
            elif category.id == 4:
                self.childish_fee.set(category.fee)
            elif category.id == 5:
                self.baby_fee.set(category.fee)
        self.grab_set()
        self.transient(self.master)


    def modify_categories(self):
        '''
        Modifica la taula "category" de la base de dades amb les modificacions efectuades.
        '''
        falla = Falla()
        falla.get_categories()
        for category in falla.categories_list:
            if category.id == 1:
                category.fee = self.adult_fee.get()
            elif category.id == 2:
                category.fee = self.cadet_fee.get()
            elif category.id == 3:
                category.fee = self.youth_fee.get()
            elif category.id == 4:
                category.fee = self.childish_fee.get()
            elif category.id == 5:
                category.fee = self.baby_fee.get()
            category.modify_category(category.id, category.fee, category.name, category.description)