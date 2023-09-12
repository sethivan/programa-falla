import tkinter as tk
import tkinter.ttk as ttk
import platform

from base_de_dades import BaseDeDades
from utils import Utils


class FinestraCategories(tk.Toplevel):
    '''
	Esta classe representa una nova finestra que depén de la finestra principal.

	Atributs:
	---------
	master : tk.Tk o tk.Toplevel
		La instància principal de l'aplicació o de la finestra que crea esta nova finestra.
	'''


    def __init__(self, master=None):
        '''
		Inicialitza una nova instància de la classe FinestraCategories.

		Parametres:
		-----------
		master : tk.Tk o tk.Toplevel, opcional
			La instància principal de l'aplicació o de la finestra que crea esta nova finestra.
			Si no se proporciona, se creará una nueva instancia de tk.Tk().
		'''
        super().__init__(master)
        self.master=master
        self.sistema_operatiu=platform.system()
        if self.sistema_operatiu=='Windows':
            self.iconbitmap("escut.ico")
        self.resizable(0,0)
        self.title("Modificar Categories")
        utils=Utils()
        utils.definir_estil_global()
        self.configure(bg="#eae9e7", pady=5, padx=5)

        self.quota_adult=tk.StringVar()
        self.quota_cadet=tk.StringVar()
        self.quota_juvenil=tk.StringVar()
        self.quota_infantil=tk.StringVar()
        self.quota_bebe=tk.StringVar()

        # Widgets
        self.label_nom_adult=ttk.Label(self, text="Adult (major d'edat)", style="Etiqueta.TLabel")
        self.label_nom_adult.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.entry_quota_adult=ttk.Entry(self, width=6, justify="right", textvariable=self.quota_adult)
        self.entry_quota_adult.grid(row=0, column=1, padx=5, pady=5)

        self.label_nom_cadet=ttk.Label(self, text="Cadet (entre 14 i 17 anys)", style="Etiqueta.TLabel")
        self.label_nom_cadet.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.entry_quota_cadet=ttk.Entry(self, width=6, justify="right", textvariable=self.quota_cadet)
        self.entry_quota_cadet.grid(row=1, column=1, padx=5, pady=5)

        self.label_nom_juvenil=ttk.Label(self, text="Juvenil (entre 10 i 13 anys)", style="Etiqueta.TLabel")
        self.label_nom_juvenil.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.entry_quota_juvenil=ttk.Entry(self, width=6, justify="right", textvariable=self.quota_juvenil)
        self.entry_quota_juvenil.grid(row=2, column=1, padx=5, pady=5)

        self.label_nom_infantil=ttk.Label(self, text="Infantil (entre 5 i 9 anys)", style="Etiqueta.TLabel")
        self.label_nom_infantil.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.entry_quota_infantil=ttk.Entry(self, width=6, justify="right", textvariable=self.quota_infantil)
        self.entry_quota_infantil.grid(row=3, column=1, padx=5, pady=5)

        self.label_nom_bebe=ttk.Label(self, text="Bebe (menor de 5 anys)", style="Etiqueta.TLabel")
        self.label_nom_bebe.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.entry_quota_bebe=ttk.Entry(self, width=6, justify="right", textvariable=self.quota_bebe)
        self.entry_quota_bebe.grid(row=4, column=1, padx=5, pady=5)

        self.button_modificar=ttk.Button(self, width=15, text="Modificar", style="Boto.TButton", command=self.modificar)
        self.button_modificar.grid(row=5, column=0, columnspan=2, pady=5)



    def iniciar(self):
        '''
		Inicia la nova finestra accedint a la taula "categoria" de la base de dades i omplint tots els camps.
		'''
        bd=BaseDeDades("falla.db")
        categoria=bd.llegir_categoria(1)
        self.quota_adult.set(categoria.quota)
        categoria=bd.llegir_categoria(2)
        self.quota_cadet.set(categoria.quota)
        categoria=bd.llegir_categoria(3)
        self.quota_juvenil.set(categoria.quota)
        categoria=bd.llegir_categoria(4)
        self.quota_infantil.set(categoria.quota)
        categoria=bd.llegir_categoria(5)
        self.quota_bebe.set(categoria.quota)
        bd.tancar_conexio()
        self.grab_set()
        self.transient(self.master)


    def modificar(self):
        '''
        Modifica la taula "categoria" de la base de dades amb les modificacions efectuades.
        '''
        bd=BaseDeDades("falla.db")
        categoria=bd.llegir_categoria(1)
        categoria.quota=self.quota_adult.get()
        bd.actualitzar_categoria(categoria)
        categoria=bd.llegir_categoria(2)
        categoria.quota=self.quota_cadet.get()
        bd.actualitzar_categoria(categoria)
        categoria=bd.llegir_categoria(3)
        categoria.quota=self.quota_juvenil.get()
        bd.actualitzar_categoria(categoria)
        categoria=bd.llegir_categoria(4)
        categoria.quota=self.quota_infantil.get()
        bd.actualitzar_categoria(categoria)
        categoria=bd.llegir_categoria(5)
        categoria.quota=self.quota_bebe.get()
        bd.actualitzar_categoria(categoria)
        bd.tancar_conexio()