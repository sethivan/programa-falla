import tkinter as tk
import tkinter.ttk as ttk

from base_de_dades import BaseDeDades


class FinestraCategories(tk.Toplevel):

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
        self.resizable(0,0)
        self.title("Modificar Categories")
        self.iconbitmap("escut.ico")

        self.quota_adult=tk.StringVar()
        self.quota_cadet=tk.StringVar()
        self.quota_juvenil=tk.StringVar()
        self.quota_infantil=tk.StringVar()
        self.quota_bebe=tk.StringVar()

        # Widgets
        self.label_nom_adult=ttk.Label(self, text="Adult")
        self.label_nom_adult.grid(row=0, column=0, padx=2, pady=5, sticky="w")

        self.label_descripcio_adult=ttk.Label(self, text="(Major de 18 anys):")
        self.label_descripcio_adult.grid(row=0, column=1, padx=2, pady=5, sticky="w")

        self.entry_quota_adult=tk.Entry(self, width=8, textvariable=self.quota_adult)
        self.entry_quota_adult.grid(row=0, column=2, padx=2, pady=5, sticky="w")

        self.label_nom_cadet=ttk.Label(self, text="Cadet")
        self.label_nom_cadet.grid(row=1, column=0, padx=2, pady=5, sticky="w")

        self.label_descripcio_cadet=ttk.Label(self, text="(Entre 14 i 17 anys):")
        self.label_descripcio_cadet.grid(row=1, column=1, padx=2, pady=5, sticky="w")

        self.entry_quota_cadet=tk.Entry(self, width=8, textvariable=self.quota_cadet)
        self.entry_quota_cadet.grid(row=1, column=2, padx=2, pady=5, sticky="w")

        self.label_nom_juvenil=ttk.Label(self, text="Juvenil")
        self.label_nom_juvenil.grid(row=2, column=0, padx=2, pady=5, sticky="w")

        self.label_descripcio_juvenil=ttk.Label(self, text="(Entre 10 i 13 anys):")
        self.label_descripcio_juvenil.grid(row=2, column=1, padx=2, pady=5, sticky="w")

        self.entry_quota_juvenil=tk.Entry(self, width=8, textvariable=self.quota_juvenil)
        self.entry_quota_juvenil.grid(row=2, column=2, padx=2, pady=5, sticky="w")

        self.label_nom_infantil=ttk.Label(self, text="Infantil")
        self.label_nom_infantil.grid(row=3, column=0, padx=2, pady=5, sticky="w")

        self.label_descripcio_infantil=ttk.Label(self, text="(Entre 5 i 9 anys):")
        self.label_descripcio_infantil.grid(row=3, column=1, padx=2, pady=5, sticky="w")

        self.entry_quota_infantil=tk.Entry(self, width=8, textvariable=self.quota_infantil)
        self.entry_quota_infantil.grid(row=3, column=2, padx=2, pady=5, sticky="w")

        self.label_nom_bebe=ttk.Label(self, text="Bebe")
        self.label_nom_bebe.grid(row=4, column=0, padx=2, pady=5, sticky="w")

        self.label_descripcio_bebe=ttk.Label(self, text="(Menor de 5 anys):")
        self.label_descripcio_bebe.grid(row=4, column=1, padx=2, pady=5, sticky="w")

        self.entry_quota_bebe=tk.Entry(self, width=8, textvariable=self.quota_bebe)
        self.entry_quota_bebe.grid(row=4, column=2, padx=2, pady=5, sticky="w")

        self.button_modificar=tk.Button(self, width=15, text="Modificar", command=self.modificar)
        self.button_modificar.grid(row=5, column=1, pady=5)



    def iniciar(self):
        '''
		Inicia la nova finestra.
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
        self.mainloop()


    def modificar(self):

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