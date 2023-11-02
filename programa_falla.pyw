'''

PROGRAMA FALLA SANTS PATRONS

Programa de gestió de l'oficina de la Falla Sants Patrons d'Alzira.
Control de fallers, families, quotes, pagaments, rifes, loteries, historials, etc.

Desenvolupat per Ivan Mas Presentación 2020.

'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import platform
from PIL import Image, ImageTk

from finestra_introduir import FinestraIntroduir
from finestra_gestionar import FinestraGestionar
from finestra_historial import FinestraHistorial
from finestra_categories import FinestraCategories
from finestra_llistats import FinestraLlistats

from arxiu import Arxiu
from utils import Utils
from base_de_dades import BaseDeDades

from falla import Falla
from categoria import Categoria
from informe import Informe


class Aplicacio(tk.Frame):
	"""
    Aquesta classe representa l'aplicació principal de la interfície gràfica d'usuari.

    Atributs:
    ---------
    master : tk.Tk
        La instància principal de l'aplicació.
    """
		
		
	def __init__(self, master=None):
		"""
        Inicialitza una nova instància de la classe Aplicacio.

        Paràmetres:
        -----------
        master : tk.Tk, opcional
            La instància principal de l'aplicació. Si no es proporciona,
			es crearà una nova instància de tk.Tk().
        """
		super().__init__(master) # Heretem de la classe Frame.
		self.master=master
		self.sistema_operatiu=platform.system()
		if self.sistema_operatiu=='Windows':
			self.master.state('zoomed') # La finestra s'obri maximitzada.
			self.master.iconbitmap("escut.ico")
		elif self.sistema_operatiu=='Linux':
			self.master.attributes('-zoomed', True)
		self.master.title("Falla Sants Patrons")
		utils=Utils()
		utils.definir_estil_global()
		self.master.configure(bg="#ffffff", pady=5, padx=5)
		
		# Barra de menú.
		self.barra_menu=tk.Menu() # Guardem el menú en una variable.
		self.master.config(menu=self.barra_menu) # Construïm el menú.

		# Submenú Inici.
		self.menu_inici=tk.Menu(self.barra_menu, tearoff=0) # Creem els elements i subelements.
		self.menu_inici.add_command(label="Nou exercici", command=self.nou_exercici)
		self.menu_inici.add_command(label="Modificar categories", command=self.modificar_categories)
		self.menu_inici.add_command(label="Eixir", command=self.eixir)

		# Submenú Faller.
		self.menu_faller=tk.Menu(self.barra_menu, tearoff=0)
		self.menu_faller.add_command(label="Introduir", command=self.introduir_faller, accelerator="Ctrl+I")
		self.master.bind_all("<Control-i>", self.event_introduir)
		self.menu_faller.add_command(label="Gestionar", command=self.gestionar_faller, accelerator="Ctrl+G")
		self.master.bind_all("<Control-g>", self.EventGestionar)
		
		# Submenú Historial.
		self.menu_historial=tk.Menu(self.barra_menu, tearoff=0)
		self.menu_historial.add_command(label="Modificar", command=self.modificar_historial)
		self.menu_historial.add_command(label="Borrar", command=self.borrar_historial)

		# Submenú Sortejos.
		self.menu_sortejos=tk.Menu(self.barra_menu, tearoff=0)
		self.menu_sortejos.add_command(label="Assignar rifa", command=self.assignar_rifa)
		self.menu_sortejos.add_command(label="Assignar loteria", command=self.AssignarLoteria)

		# Submenú Llistats.
		self.menu_imprimir=tk.Menu(self.barra_menu, tearoff=0)
		self.menu_imprimir.add_command(label="Moviments", command=self.MovimentsDia)
		self.menu_imprimir.add_command(label="General", command=self.LlistatGeneral)
		self.menu_imprimir.add_command(label="Fallers", command=self.LlistatFallers)
		self.menu_imprimir.add_command(label="Altes i Baixes", command=self.LlistatAltesBaixes)
		self.menu_imprimir.add_command(label="Rifes", command=self.LlistatRifes)

		# Submenú Ajuda.
		self.menu_ajuda=tk.Menu(self.barra_menu, tearoff=0)
		self.menu_ajuda.add_command(label="Info", command=self.info)

		# Afegim tots els submenús a la barra.
		self.barra_menu.add_cascade(label="Inici", menu=self.menu_inici)
		self.barra_menu.add_cascade(label="Faller", menu=self.menu_faller)
		self.barra_menu.add_cascade(label="Historial", menu=self.menu_historial)
		self.barra_menu.add_cascade(label="Sortejos", menu=self.menu_sortejos)
		self.barra_menu.add_cascade(label="Imprimir", menu=self.menu_imprimir)
		self.barra_menu.add_cascade(label="Ajuda", menu=self.menu_ajuda)

		# Frames en els que dividim la finestra.
		label_frame_portada=tk.LabelFrame(self.master, borderwidth=0, background="#ffffff")
		label_frame_portada.grid(row=0, column=0, padx=20, pady=10, ipady=2, rowspan=3)
		
		label_estil_inici=ttk.Label(self.master, text="Inici", style="Titol.TLabel")
		label_frame_inici=ttk.LabelFrame(self.master, style="Marc.TFrame", labelwidget=label_estil_inici)
		label_frame_inici.grid(row=0, column=1, padx=20, pady=10, ipady=2, sticky="n")

		label_estil_faller=ttk.Label(self.master, text="Faller", style="Titol.TLabel")
		label_frame_faller=ttk.LabelFrame(self.master, style="Marc.TFrame", labelwidget=label_estil_faller)
		label_frame_faller.grid(row=1, column=1, padx=20, pady=10, ipady=2, sticky="n")

		label_estil_historial=ttk.Label(self.master, text="Historial", style="Titol.TLabel")
		label_frame_historial=ttk.LabelFrame(self.master, style="Marc.TFrame", labelwidget=label_estil_historial)
		label_frame_historial.grid(row=2, column=1, padx=20, pady=10, ipady=2, sticky="n")

		label_estil_sortejos=ttk.Label(self.master, text="Sortejos", style="Titol.TLabel")
		label_frame_sortejos=ttk.LabelFrame(self.master, style="Marc.TFrame", labelwidget=label_estil_sortejos)
		label_frame_sortejos.grid(row=0, column=2, padx=20, pady=10, ipady=2, sticky="n")

		label_estil_imprimir=ttk.Label(self.master, text="Imprimir", style="Titol.TLabel")
		label_frame_imprimir=ttk.LabelFrame(self.master, style="Marc.TFrame", labelwidget=label_estil_imprimir)
		label_frame_imprimir.grid(row=1, column=2, padx=20, pady=10, ipady=2, sticky="n")

		# Widgets per a cada frame.

		# Frame portada.
		self.label_falla=ttk.Label(label_frame_portada, text="Falla", style="Portada.TLabel")
		self.label_falla.grid(row=0, column=0, padx=2)

		self.label_sants=ttk.Label(label_frame_portada, text="Sants", style="Portada.TLabel")
		self.label_sants.grid(row=1, column=0, padx=2)

		self.label_patrons=ttk.Label(label_frame_portada, text="Patrons", style="Portada.TLabel")
		self.label_patrons.grid(row=2, column=0, padx=2)

		logo=Image.open("escut.jpg")
		self.image=ImageTk.PhotoImage(logo)
		self.label_image=tk.Label(label_frame_portada, image=self.image, borderwidth=0)
		self.label_image.grid(row=3, column=0)

		# Frame Inici.
		self.button_nou_exercici=ttk.Button(label_frame_inici, width=20, text="Nou exercici", style="Boto.TButton", command=self.nou_exercici)
		self.button_nou_exercici.grid(row=0, column=0, padx=5, pady=5)
		
		self.button_modificar_categories=ttk.Button(label_frame_inici, width=20, text="Modificar categories", style="Boto.TButton", command=self.modificar_categories)
		self.button_modificar_categories.grid(row=1, column=0, padx=5, pady=5)

		# Frame Faller.
		self.button_introduir_faller=ttk.Button(label_frame_faller, width=20, text="Introduir faller", style="Boto.TButton", command=self.introduir_faller)
		self.button_introduir_faller.grid(row=0, column=0, padx=5, pady=5)

		self.button_gestionar_faller=ttk.Button(label_frame_faller, width=20, text="Gestionar faller", style="Boto.TButton", command=self.gestionar_faller)
		self.button_gestionar_faller.grid(row=1, column=0, padx=5, pady=5)

		# Frame Sortejos.
		self.button_rifa=ttk.Button(label_frame_sortejos, width=20, text="Assignar rifa", style="Boto.TButton", command=self.assignar_rifa)
		self.button_rifa.grid(row=0, column=0, padx=5, pady=5)

		self.button_loteria=ttk.Button(label_frame_sortejos, width=20, text="Assignar loteria", style="Boto.TButton", command=self.AssignarLoteria)
		self.button_loteria.grid(row=1, column=0, padx=5, pady=5)

		# Frame Historial.
		self.button_modificar_historial=ttk.Button(label_frame_historial, width=20, text="Modificar historial", style="Boto.TButton", command=self.modificar_historial)
		self.button_modificar_historial.grid(row=0, column=0, padx=5, pady=5)

		self.button_borrar_historial=ttk.Button(label_frame_historial, width=20, text="Borrar historial", style="Boto.TButton", command=self.borrar_historial)
		self.button_borrar_historial.grid(row=1, column=0, padx=5, pady=5)

		#Frame Imprimir.
		self.button_llistats=ttk.Button(label_frame_imprimir, width=20, text="Llistats", style="Boto.TButton", command=self.MovimentsDia)
		self.button_llistats.grid(row=0, column=0, padx=5, pady=5)

		# Comprovació que s'efectua cada vegada que es fica en marxa el programa.
		self.arrancar()


	def arrancar(self):
		'''
		Comprova si existeixen els arxius necessaris per a que funcione el programa i en cas de que falten, els crea.
		Si es crea algún arxiu, avisa a l'usuari de que ho ha fet per a que prenga les mesures necessàries.
		'''
		if not os.path.exists("exercici"):
			llista=[]
			arxiu=Arxiu("exercici")
			utils=Utils()
			data_actual=utils.calcular_data_actual()
			dia_actual=int(data_actual[0])
			mes_actual=int(data_actual[1])
			any_actual=int(data_actual[2])
			if mes_actual>3:
				any_exercici=any_actual+1
			elif mes_actual<2:
				any_exercici=any_actual
			elif mes_actual==3 and dia_actual>19:
				any_exercici=any_actual+1
			elif mes_actual==3 and dia_actual<=19:
				any_exercici=any_actual
			llista.append(any_exercici)
			arxiu.modificar_exercici_actual(llista)
			messagebox.showwarning("Avís", "No hi havia cap arxiu amb l'informació de l'exercici i s'ha creat un nou")
		if not os.path.exists("falla.db"):
			bd=BaseDeDades("falla.db")
			bd.crear_taules()
			categoria=Categoria(0, 475, "adult", "major de 18 anys")
			bd.crear_categoria(categoria)
			categoria=Categoria(0, 300, "cadet", "entre 14 i 17 anys")
			bd.crear_categoria(categoria)
			categoria=Categoria(0, 200, "juvenil", "entre 10 i 13 anys")
			bd.crear_categoria(categoria)
			categoria=Categoria(0, 125, "infantil", "entre 5 i 9 anys")
			bd.crear_categoria(categoria)
			categoria=Categoria(0, 50, "bebè", "menor de 5 anys")
			bd.crear_categoria(categoria)
			bd.tancar_conexio()
			messagebox.showwarning("Avís", "No hi havia cap base de dades del programa i s'ha creat una nova")
	
	
	def modificar_categories(self):
		''' 
		Crea una nova instància de la classe FinestraCategories
		que obri la finestra "Modificar" del menú "Categoria".
		'''
		FinestraCategories(self)
	
	
	def gestionar_faller(self):
		''' 
		Crea una nova instància de la classe FinestraGestionar
		que obri la finestra "Gestionar" del menú "Faller".
		'''
		gestionar_faller=FinestraGestionar(self)
		gestionar_faller.iniciar()


	def EventGestionar(self, event):
		'''
		Bindeig del submenú "Gestionar".
		'''
		self.gestionar_faller()
	

	def introduir_faller(self):
		''' 
		Crea una nova instància de la classe FinestraIntroduir
		que obri la finestra "Introduir" del menú "Faller".
		'''
		introduir_faller = FinestraIntroduir(self)
		introduir_faller.iniciar()

	
	def event_introduir(self, event):
		'''
		Bindeig del submenú "Introduir".
		'''
		self.introduir_faller()


	def AssignarLoteria(self): #funció que obre la finestra "Assignar" del menú "Loteria"

		#FinestraAssignar(self.root)
		pass


	def assignar_rifa(self):
		'''
		Crea una nova instància de la classe Falla per que assigne la rifa corresponent als fallers.
		'''
		falla=Falla()
		falla.assignar_rifa_auto()


	def modificar_historial(self):
		''' 
		Crea una nova instància de la classe FinestraHistorial
		que obri la finestra "Modificar" del menú "Historial".
		'''
		historial = FinestraHistorial(self)
		historial.iniciar()


	def borrar_historial(self):
		'''
		Crea una nova instància e la classe Falla per que borre l'historial de tots els fallers.
		'''
		falla=Falla()
		falla.borrar_historial()


	def MovimentsDia(self): #funció per a traure el llistat en pdf dels moviments del dia

		#elInforme=Informe()
		#elInforme.MovimentsDia()
		llistat = FinestraLlistats(self)
		llistat.iniciar()


	def LlistatGeneral(self): #funció per a traure el llistat en pdf dels comptes actualitzats dels fallers

		#informe=Informe()
		#informe.llistat_general_per_families()
		pass


	def LlistatFallers(self): #funció per a traure el llistat en pdf dels fallers amb les seues dades

		#elInforme=Informe()
		#elInforme.LlistatFallers()
		pass


	def LlistatAltesBaixes(self): #funció per a traure el llistat en pdf de les altes i baixes de fallers respecte a l'exercici anterior

		#elInforme=Informe()
		#elInforme.LlistatAltesBaixes()
		pass


	def LlistatRifes(self): #funció per a traure el llistat en pdf d'aquells fallers a qui els correpon rifa

		informe=Informe()
		informe.llistat_fallers_amb_rifa()
		

	def nou_exercici(self): #funció per a crear un nou exercici faller
		'''
		Crea una nova instància de la classe Falla per a que cree un exercici nou.
		'''
		falla=Falla()
		falla.nou_exercici()

	
	def eixir(self):
		'''
		Tanca la finestra principal de l'aplicació.
		'''
		valor=messagebox.askquestion("Eixir","Vols eixir de l'aplicació?")
		if valor=="yes":
			self.master.destroy()


	def info(self):
		'''
		Mostra una finestra emergent amb informació del programa.
		'''
		messagebox.showinfo("Informació","Aplicació creada per Ivan Mas")


if __name__=='__main__':
	'''
	Inicia l'aplicació.
	'''
	root=tk.Tk()
	app=Aplicacio(root)
	app.mainloop()