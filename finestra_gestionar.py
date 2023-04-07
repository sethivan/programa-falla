import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import LabelFrame

from arxiu import Arxiu
from base_de_dades import BaseDeDades
from utils import Utils

from faller import Faller
from falla import Falla
from familia import Familia
from moviment import Moviment
#from modificar import *
#from informe import *
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import A4
import os
import errno
import os.path as path


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

		self.exerciciString=StringVar() #definim la variable per al exercici
		self.idString=StringVar() #definim la variable per al id
		self.nomString=StringVar() #definim la variable per al nom
		self.naixementString=StringVar() #definim la variable per a la data de naixement
		self.dniString=StringVar() #definim la variable per al dni
		self.adresaString=StringVar() #definim la variable per a l'adreça
		self.telefonString=StringVar() #definim la variable per al telefon
		self.correuString=StringVar() #definim la variable per al correu electrònic
		self.quotaString=StringVar() #definim la variable per a la quota
		self.quotapagString=StringVar() #definim la variable per a la quota pagada
		self.deutequotaString=StringVar() #definim la variable per a mostrar el deute de la quota
		self.pagarquotaString=StringVar() #definim la variable on guardarem el moviment de quota
		self.loteriaString=StringVar()
		self.loteriapagString=StringVar()
		self.deuteloteriaString=StringVar()
		self.pagarloteriaString=StringVar()
		self.rifaString=StringVar()
		self.rifapagString=StringVar()
		self.deuterifaString=StringVar()
		self.pagarrifaString=StringVar()
		self.totalasignatString=StringVar()
		self.totalpagatString=StringVar()
		self.totalString=StringVar()
		self.formapagamentString=StringVar()
		self.pagartotalString=StringVar()
		self.membresString=StringVar() #variable per a guardar els membres actius de la familia
		self.quotafamString=StringVar()
		self.quotapagadafamString=StringVar()
		self.deutequotafamString=StringVar()
		self.pagarquotafamString=StringVar()
		self.loteriafamString=StringVar()
		self.loteriapagadafamString=StringVar()
		self.deuteloteriafamString=StringVar()
		self.pagarloteriafamString=StringVar()
		self.rifafamString=StringVar()
		self.rifapagadafamString=StringVar()
		self.deuterifafamString=StringVar()
		self.pagarrifafamString=StringVar()
		self.totalasignatfamString=StringVar()
		self.totalpagatfamString=StringVar()
		self.totalfamString=StringVar()
		self.formapagamentfamString=StringVar()
		self.pagartotalfamString=StringVar()
		self.asignacioString=StringVar() #variable que controla el element del radiobutton
		self.descripcioString=StringVar() #descripcio del moviment a realitzar
		self.asignarString=StringVar() #variable asignada al entry de asignar
		self.ident=[] #variable per a controlar el camp id de la llista de noms del combo
		self.modificar=0 #variable amb què controlem l'obertura de la finestra de modificar faller
		self.id_anterior=0 #variable on guardem el id anteriorment buscat per a retornar-lo en cas d'error
		
		#Frames en els que dividim la finestra

		frameExercici=LabelFrame(self, text="Exercici") #li diguem en quina finestra va el frame
		frameExercici.grid(row=0, column=0, columnspan=1, pady=5, ipadx=20, ipady=2)

		frameBuscar=LabelFrame(self, text="Faller")
		frameBuscar.grid(row=0, column=1, columnspan=8, ipadx=2, ipady=2)

		frameDades=LabelFrame(self, text="Dades personals")
		frameDades.grid(row=1, column=0, columnspan=4, ipadx=2, ipady=2)

		frameFamilia=LabelFrame(self, text="Familia")
		frameFamilia.grid(row=1, column=4, columnspan=1, ipadx=2, ipady=2)

		frameMoviments=LabelFrame(self, text="Moviments")
		frameMoviments.grid(row=2, column=0, columnspan=4, padx=5, pady=5, ipadx=2, ipady=2)

		frameMovimentsFam=LabelFrame(self, text="Moviments de la familia")
		frameMovimentsFam.grid(row=2, column=4, columnspan=1, padx=5, pady=5, ipadx=2, ipady=2)

		frameAsignar=LabelFrame(self, text="Assignar")
		frameAsignar.grid(row=3, column=0, pady=5, ipady=2, sticky="n")

		frameTaula=LabelFrame(self, text="Historial de moviments")
		frameTaula.grid(row=3, column=1, columnspan=8, pady=5, ipady=2)

		self.pdfBoto=Button(self, width=15, text="crear pdf", command=self.CrearPdf)
		self.pdfBoto.grid(row=4, column=0, padx=5, sticky="w"+"e")

		#Widgets de cada frame

		#Frame Exercici

		self.exerciciEntry=Entry(frameExercici, width=10, state="disabled", disabledforeground="black", textvariable=self.exerciciString)
		self.exerciciEntry.pack()

		arxiu=Arxiu("exercici")
		exercici_actual=arxiu.llegir_exercici_actual()
		self.exerciciString.set(str(exercici_actual-1) + "-" + str(exercici_actual))

		#Frame Buscar Faller

		self.altaBoto=Button(frameBuscar, state="disabled", width=15, text="Donar d'alta", command=self.CanviarEstat)
		self.altaBoto.grid(row=0, column=0, padx=5, sticky="w"+"e")
		
		self.idLabel=Label(frameBuscar, text="ID del faller:")
		self.idLabel.grid(row=0, column=1)

		self.idEntry=Entry(frameBuscar, width=8, textvariable=self.idString)
		self.idEntry.grid(row=0, column=2)
		self.idEntry.focus() #fiquem el foco en el entry
		self.idEntry.bind('<Return>', self.BuscarId) #bindegem el intro a BuscarId

		self.nomLabel=Label(frameBuscar, text="Cognoms i nom:")
		self.nomLabel.grid(row=0, column=3)

		self.fallerCombo=ttk.Combobox(frameBuscar, width=30, postcommand=self.dropdown_opened)
		self.fallerCombo.grid(row=0, column=4)
		self.fallerCombo.bind("<<ComboboxSelected>>", self.selection_changed)

		#Frame Dades Personals

		self.naixementLabel=Label(frameDades, text="Data de naixement:")
		self.naixementLabel.grid(row=0, column=0, sticky="e")

		self.naixementEntry=Entry(frameDades, state="disabled", textvariable=self.naixementString)
		self.naixementEntry.grid(row=0, column=1)

		self.dniLabel=Label(frameDades, text="DNI:")
		self.dniLabel.grid(row=0, column=2, sticky="e")

		self.dniEntry=Entry(frameDades, state="disabled", textvariable=self.dniString)
		self.dniEntry.grid(row=0, column=3)

		self.adresaLabel=Label(frameDades, text="Adreça:")
		self.adresaLabel.grid(row=1, column=0, sticky="e")

		self.adresaEntry=Entry(frameDades, state="disabled", textvariable=self.adresaString)
		self.adresaEntry.grid(row=1, column=1)

		self.telefonLabel=Label(frameDades, text="Telèfon:")
		self.telefonLabel.grid(row=1, column=2, sticky="e")

		self.telefonEntry=Entry(frameDades, state="disabled", textvariable=self.telefonString)
		self.telefonEntry.grid(row=1, column=3)

		self.correuLabel=Label(frameDades, text="Correu electrònic:")
		self.correuLabel.grid(row=2, column=0, sticky="e")

		self.correuEntry=Entry(frameDades, state="disabled", textvariable=self.correuString)
		self.correuEntry.grid(row=2, column=1)

		#self.modificarBoto=Button(frameDades, state="disabled", text="Modificar dades", command=self.Modificar)
		#self.modificarBoto.grid(row=2, column=3)

		#Frame Familia

		self.familiaLabel=Label(frameFamilia, text="Membres de la familia:")
		self.familiaLabel.grid(row=0, column=0)

		self.familiaCombo=ttk.Combobox(frameFamilia, postcommand=self.dropdown_opened_fam)
		self.familiaCombo.grid(row=0, column=1)
		self.familiaCombo.bind("<<ComboboxSelected>>", self.selection_changed_fam)

		self.membresLabel=Label(frameFamilia, text="Membres actius:")
		self.membresLabel.grid(row=0, column=2)

		self.membresEntry=Entry(frameFamilia, width=4, state="disabled", disabledforeground="black", textvariable=self.membresString)
		self.membresEntry.grid(row=0, column=3)

		#Frame Moviments

		self.asignatLabel=Label(frameMoviments, text="Assignat")
		self.asignatLabel.grid(row=0, column=1)

		self.pagatLabel=Label(frameMoviments, text="Pagat")
		self.pagatLabel.grid(row=0, column=2)

		self.diferenciaLabel=Label(frameMoviments, text="Diferència")
		self.diferenciaLabel.grid(row=0, column=3)

		self.quotaLabel=Label(frameMoviments, text="Quota:")
		self.quotaLabel.grid(row=1, column=0, sticky="e")

		self.quotaEntry=Entry(frameMoviments, width=15, state="disabled", disabledforeground="black", textvariable=self.quotaString)
		self.quotaEntry.grid(row=1, column=1)

		self.quotapagEntry=Entry(frameMoviments, width=15, state="disabled", disabledforeground="black", textvariable=self.quotapagString)
		self.quotapagEntry.grid(row=1, column=2)

		self.deutequotaEntry=Entry(frameMoviments, width=15, state="disabled", disabledforeground="black", textvariable=self.deutequotaString)
		self.deutequotaEntry.grid(row=1, column=3)

		self.pagarquotaEntry=Entry(frameMoviments, width=15, state="disabled", textvariable=self.pagarquotaString)
		self.pagarquotaEntry.grid(row=1, column=4)
		self.pagarquotaEntry.bind('<FocusOut>', self.CalcularPagarTotalQuota)
		self.pagarquotaEntry.bind('<FocusIn>', self.LlevarCeroQuota)

		self.loteriaLabel=Label(frameMoviments, text="Loteria:")
		self.loteriaLabel.grid(row=2, column=0, sticky="e")

		self.loteriaEntry=Entry(frameMoviments, width=15, state="disabled", disabledforeground="black", textvariable=self.loteriaString)
		self.loteriaEntry.grid(row=2, column=1)

		self.loteriapagEntry=Entry(frameMoviments, width=15, state="disabled", disabledforeground="black", textvariable=self.loteriapagString)
		self.loteriapagEntry.grid(row=2, column=2)

		self.deuteloteriaEntry=Entry(frameMoviments, width=15, state="disabled", disabledforeground="black", textvariable=self.deuteloteriaString)
		self.deuteloteriaEntry.grid(row=2, column=3)

		self.pagarloteriaEntry=Entry(frameMoviments, width=15, state="disabled", textvariable=self.pagarloteriaString)
		self.pagarloteriaEntry.grid(row=2, column=4)
		self.pagarloteriaEntry.bind('<FocusOut>', self.CalcularPagarTotalLoteria)
		self.pagarloteriaEntry.bind('<FocusIn>', self.LlevarCeroLoteria)

		self.rifaLabel=Label(frameMoviments, text="Rifa:")
		self.rifaLabel.grid(row=3, column=0, sticky="e")

		self.rifaEntry=Entry(frameMoviments, width=15, state="disabled", disabledforeground="black", textvariable=self.rifaString)
		self.rifaEntry.grid(row=3, column=1)

		self.rifapagEntry=Entry(frameMoviments, width=15, state="disabled", disabledforeground="black", textvariable=self.rifapagString)
		self.rifapagEntry.grid(row=3, column=2)

		self.deuterifaEntry=Entry(frameMoviments, width=15, state="disabled", disabledforeground="black", textvariable=self.deuterifaString)
		self.deuterifaEntry.grid(row=3, column=3)

		self.pagarrifaEntry=Entry(frameMoviments, width=15, state="disabled", textvariable=self.pagarrifaString)
		self.pagarrifaEntry.grid(row=3, column=4)
		self.pagarrifaEntry.bind('<FocusOut>', self.CalcularPagarTotalRifa)
		self.pagarrifaEntry.bind('<FocusIn>', self.LlevarCeroRifa)

		self.totalasignatLabel=Label(frameMoviments, text="Totals:")
		self.totalasignatLabel.grid(row=4, column=0, sticky="e")

		self.totalasignatEntry=Entry(frameMoviments, width=15, state="disabled", disabledforeground="black", textvariable=self.totalasignatString)
		self.totalasignatEntry.grid(row=4, column=1)

		self.totalpagatEntry=Entry(frameMoviments, width=15, state="disabled", disabledforeground="black", textvariable=self.totalpagatString)
		self.totalpagatEntry.grid(row=4, column=2)

		self.totalEntry=Entry(frameMoviments, width=15, state="disabled", disabledforeground="black", textvariable=self.totalString)
		self.totalEntry.grid(row=4, column=3)

		self.pagartotalEntry=Entry(frameMoviments, width=15, state="disabled", disabledforeground="black", textvariable=self.pagartotalString)
		self.pagartotalEntry.grid(row=4, column=4)

		self.caixaRadioButton=Radiobutton(frameMoviments, text="Caixa", variable=self.formapagamentString, value=1)
		self.bancRadioButton=Radiobutton(frameMoviments, text="Banc", variable=self.formapagamentString, value=2)
		self.caixaRadioButton.grid(row=5, column=2)
		self.bancRadioButton.grid(row=5, column=3)
		self.caixaRadioButton.select() #seleccionem caixa com a predeterminat

		self.pagarBoto=Button(frameMoviments, state="disabled", text="Pagar", command=self.Pagar)
		self.pagarBoto.grid(row=5, column=4, padx=5, sticky="w"+"e")

		#Frame Moviments de la familia

		self.asignatfamLabel=Label(frameMovimentsFam, text="Assignat")
		self.asignatfamLabel.grid(row=0, column=1)

		self.pagatfamLabel=Label(frameMovimentsFam, text="Pagat")
		self.pagatfamLabel.grid(row=0, column=2)

		self.diferenciafamLabel=Label(frameMovimentsFam, text="Diferència")
		self.diferenciafamLabel.grid(row=0, column=3)

		self.quotafamLabel=Label(frameMovimentsFam, text="Quota:")
		self.quotafamLabel.grid(row=1, column=0, sticky="e")

		self.quotafamEntry=Entry(frameMovimentsFam, width=15, state="disabled", disabledforeground="black", textvariable=self.quotafamString)
		self.quotafamEntry.grid(row=1, column=1)

		self.quotapagadafamEntry=Entry(frameMovimentsFam, width=15, state="disabled", disabledforeground="black", textvariable=self.quotapagadafamString)
		self.quotapagadafamEntry.grid(row=1, column=2)

		self.deutequotafamEntry=Entry(frameMovimentsFam, width=15, state="disabled", disabledforeground="black", textvariable=self.deutequotafamString)
		self.deutequotafamEntry.grid(row=1, column=3)

		self.pagarquotafamEntry=Entry(frameMovimentsFam, width=15, state="disabled", textvariable=self.pagarquotafamString)
		self.pagarquotafamEntry.grid(row=1, column=4)
		self.pagarquotafamEntry.bind('<FocusOut>', self.CalcularPagarFamTotalQuota)
		self.pagarquotafamEntry.bind('<FocusIn>', self.LlevarCeroQuotaFam)

		self.loteriafamLabel=Label(frameMovimentsFam, text="Loteria:")
		self.loteriafamLabel.grid(row=2, column=0, sticky="e")

		self.loteriafamEntry=Entry(frameMovimentsFam, width=15, state="disabled", disabledforeground="black", textvariable=self.loteriafamString)
		self.loteriafamEntry.grid(row=2, column=1)

		self.loteriapagadafamEntry=Entry(frameMovimentsFam, width=15, state="disabled", disabledforeground="black", textvariable=self.loteriapagadafamString)
		self.loteriapagadafamEntry.grid(row=2, column=2)

		self.deuteloteriafamEntry=Entry(frameMovimentsFam, width=15, state="disabled", disabledforeground="black", textvariable=self.deuteloteriafamString)
		self.deuteloteriafamEntry.grid(row=2, column=3)

		self.pagarloteriafamEntry=Entry(frameMovimentsFam, width=15, state="disabled", textvariable=self.pagarloteriafamString)
		self.pagarloteriafamEntry.grid(row=2, column=4)
		self.pagarloteriafamEntry.bind('<FocusOut>', self.CalcularPagarFamTotalLoteria)
		self.pagarloteriafamEntry.bind('<FocusIn>', self.LlevarCeroLoteriaFam)

		self.rifafamLabel=Label(frameMovimentsFam, text="Rifa:")
		self.rifafamLabel.grid(row=3, column=0, sticky="e")

		self.rifafamEntry=Entry(frameMovimentsFam, width=15, state="disabled", disabledforeground="black", textvariable=self.rifafamString)
		self.rifafamEntry.grid(row=3, column=1)

		self.rifapagadafamEntry=Entry(frameMovimentsFam, width=15, state="disabled", disabledforeground="black", textvariable=self.rifapagadafamString)
		self.rifapagadafamEntry.grid(row=3, column=2)

		self.deuterifafamEntry=Entry(frameMovimentsFam, width=15, state="disabled", disabledforeground="black", textvariable=self.deuterifafamString)
		self.deuterifafamEntry.grid(row=3, column=3)

		self.pagarrifafamEntry=Entry(frameMovimentsFam, width=15, state="disabled", textvariable=self.pagarrifafamString)
		self.pagarrifafamEntry.grid(row=3, column=4)
		self.pagarrifafamEntry.bind('<FocusOut>', self.CalcularPagarFamTotalRifa)
		self.pagarrifafamEntry.bind('<FocusIn>', self.LlevarCeroRifaFam)

		self.totalasignatfamLabel=Label(frameMovimentsFam, text="Totals:")
		self.totalasignatfamLabel.grid(row=4, column=0, sticky="e")

		self.totalasignatfamEntry=Entry(frameMovimentsFam, width=15, state="disabled", disabledforeground="black", textvariable=self.totalasignatfamString)
		self.totalasignatfamEntry.grid(row=4, column=1)

		self.totalpagatfamEntry=Entry(frameMovimentsFam, width=15, state="disabled", disabledforeground="black", textvariable=self.totalpagatfamString)
		self.totalpagatfamEntry.grid(row=4, column=2)

		self.totalfamEntry=Entry(frameMovimentsFam, width=15, state="disabled", disabledforeground="black", textvariable=self.totalfamString)
		self.totalfamEntry.grid(row=4, column=3)

		self.pagartotalfamEntry=Entry(frameMovimentsFam, width=15, state="disabled", disabledforeground="black", textvariable=self.pagartotalfamString)
		self.pagartotalfamEntry.grid(row=4, column=4)

		self.caixafamRadioButton=Radiobutton(frameMovimentsFam, text="Caixa", variable=self.formapagamentfamString, value=1)
		self.bancfamRadioButton=Radiobutton(frameMovimentsFam, text="Banc", variable=self.formapagamentfamString, value=2)
		self.caixafamRadioButton.grid(row=5, column=2)
		self.bancfamRadioButton.grid(row=5, column=3)
		self.caixafamRadioButton.select() #seleccionem caixa com a predeterminat

		self.pagarfamBoto=Button(frameMovimentsFam, state="disabled", text="Pagar", command=self.PagarFam)
		self.pagarfamBoto.grid(row=5, column=4, padx=5, sticky="w"+"e")

		#Frame Asignar

		self.quotaRadioButton=Radiobutton(frameAsignar, text="Quota", variable=self.asignacioString, value=1)
		self.loteriaRadioButton=Radiobutton(frameAsignar, text="Loteria", variable=self.asignacioString, value=2)
		self.rifaRadioButton=Radiobutton(frameAsignar, text="Rifa", variable=self.asignacioString, value=3)
		self.quotaRadioButton.grid(row=0, column=0)
		self.loteriaRadioButton.grid(row=0, column=1)
		self.rifaRadioButton.grid(row=0, column=2)
		self.quotaRadioButton.select() #seleccionem quota com a predeterminat

		self.descripcioLabel=Label(frameAsignar, text="Descripció:")
		self.descripcioLabel.grid(row=1, column=0, sticky="e")

		self.descripcioEntry=Entry(frameAsignar, state="disabled", textvariable=self.descripcioString)
		self.descripcioEntry.grid(row=1, column=1, padx=2)

		self.asignarLabel=Label(frameAsignar, text="Quantitat:")
		self.asignarLabel.grid(row=2, column=0, sticky="e")

		self.asignarEntry=Entry(frameAsignar, state="disabled", textvariable=self.asignarString)
		self.asignarEntry.grid(row=2, column=1, padx=2)

		self.asignarBoto=Button(frameAsignar, state="disabled", text="Assignar", command=self.Asignar)
		self.asignarBoto.grid(row=2, column=2, padx=5)

		#Frame Taula

		self.movimentsTree=ttk.Treeview(frameTaula, height=10) #li indiquem la altura 
		self.movimentsTree.grid(row=0, column=0, padx=10, pady=5)
		self.movimentsTree["columns"]=("uno","dos","tres","quatre","cinc") #designem les columnes
		self.movimentsTree.column("#0", width=80) #designem els diferents amples
		self.movimentsTree.column("uno", width=80)
		self.movimentsTree.column("dos", width=80)
		self.movimentsTree.column("tres", width=80)
		self.movimentsTree.column("quatre", width=80)
		self.movimentsTree.column("cinc", width=80)
		self.movimentsTree.heading("#0", text="moviment") #rotulem les columnes
		self.movimentsTree.heading('uno', text="data")
		self.movimentsTree.heading('dos', text="assignat")
		self.movimentsTree.heading('tres', text="pagat")
		self.movimentsTree.heading('quatre', text="concepte")
		self.movimentsTree.heading('cinc', text="descripció")

		self.scrollTaula=Scrollbar(frameTaula, command=self.movimentsTree.yview) #barra de desplaçament per a la taula
		self.scrollTaula.grid(row=0, column=1, sticky="nsew") #la fem de l'altura de la taula

		self.movimentsTree.config(yscrollcommand=self.scrollTaula.set) #associem la taula a la barra per a que funcione correctament

		#Bindegem la finestra per a que refresque quan pille el foco

		self.bind("<FocusIn>", self.handle_focus)


	def iniciar(self):
		'''
		Inicia la nova finestra.
		'''
		self.grab_set()
		self.transient(self.master)
		self.mainloop()


	def CrearPdf(self):

		pass

		#elRebut=Informe()
		#pagquo=0
		#paglot=0
		#pagrif=0
		# elRebut.Rebut(self.fallerCombo.get(), pagquo, paglot, pagrif, self.quotaString.get(), self.quotapagString.get(), self.loteriaString.get(), self.loteriapagString.get(), self.rifaString.get(), self.rifapagString.get())


	def handle_focus(self, event):
		
		if self.idString.get()!="" and self.modificar==1: #si el contingut del idEntry no està buit i s'ha obert la finestra de modificar faller
			self.idEntry.focus()
			self.BuscarId('<Return>') #actualitza el contingut de la finestra
			self.modificar=0


	#def Modificar(self):

		#laModificacio=FinestraModificar(self.fgestionar)
		#laModificacio.OmplirModificar(self.idString.get())
		#self.modificar=1


	def CanviarEstat(self):
		
		arxiu=Arxiu("exercici")
		bd=BaseDeDades("falla.db")
		falla=Falla()
		id=self.idString.get()
		exercici_actual=arxiu.llegir_exercici_actual()
		faller=bd.llegir_faller(id)		
		if faller.alta==1:
			valor=messagebox.askquestion("Baixa","Estàs segur que vols donar de baixa al faller?")
			if valor=="yes":
				faller.alta=0
				bd.actualitzar_faller(faller)
				#accedim a l'historial del faller
				#arxiu="historials"+"/"+str(cadena)
				#fitxer=open(arxiu,"rb")
				#historial=pickle.load(fitxer)
				#fitxer.close()
				#del(fitxer)					
				#historial[exer]=["baixa", ""] #el donem de baixa en l'any de l'exercici
				#arxiu="historials"+"/"+str(cadena)
				#fitxer=open(arxiu,"wb")
				#pickle.dump(historial, fitxer)
				#fitxer.close()
				#del(fitxer)
		if faller.alta==0:
			valor=messagebox.askquestion("Alta","Estàs segur que vols donar d'alta al faller?")
			if valor=="yes":
				edat=faller.calcular_edat(faller.naixement, exercici_actual)
				# Asignem categoria per si ha canviat de tram mentre estava de baixa
				faller.categoria.calcular_categoria(edat)
				faller.categoria=bd.llegir_categoria(faller.categoria.id)
				faller.alta=1
				bd.actualitzar_faller(faller)
				#accedim a l'historial del faller
				#arxiu="historials"+"/"+str(cadena)
				#fitxer=open(arxiu,"rb")
				#historial=pickle.load(fitxer)
				#fitxer.close()
				#del(fitxer)					
				#historial[exer]=["vocal", "Sants Patrons"] #el donem d'alta com a vocal en l'any de l'exercici
				#arxiu="historials"+"/"+str(cadena)
				#fitxer=open(arxiu,"wb")
				#pickle.dump(historial, fitxer)
				#fitxer.close()
				#del(fitxer)
		llistat_fallers=falla.llegir_fallers("familia", faller.familia.id)
		faller.familia.calcular_descompte(llistat_fallers)
		bd.actualitzar_familia(faller.familia)
		self.idEntry.focus() # Fica el foco en el camp id.
		self.BuscarId('<Return>') # Refresca les dades fent la cerca de nou amb el id del faller.

	
	def BuscarId(self, event): #funció que llança el botó quan es pulsa, event fa que funcione el bindeig del intro
		
		bd=BaseDeDades("falla.db")
		id=self.idString.get() # Guardem el contingut del idEntry en una variable.
		faller=bd.llegir_ultim_faller()
		if faller.id < int(id): # Si el id que fiquem es major que el de l'últim faller.
			messagebox.showwarning("Error", "No existeix un faller amb eixa id")
			if self.id_anterior==0: # Si es la primera cerca.
				self.idString.set("")
			else:
				self.idString.set(self.id_anterior) # Fiquem el id que hem buscat anteriorment.
		else:
			self.id_anterior=id # Guardem l'ultima cerca per si apareix un error en la següent.
			self.OmplirBuscar(id)
		

	def dropdown_opened(self):
		'''
		Controla el combobox comparant la cadena escrita amb la base de dades i mostrant els resultats en el combobox.
		Utilitza la variable global "self.ident" per a passar el identificador de faller a la funció "selection_changed"
		'''
		cadena=self.fallerCombo.get()
		falla=Falla()
		llistat_fallers=falla.llegir_fallers("cognoms", cadena)
		llista=[] # Llista on anem a acumular els valors.
		self.ident=[]
		for faller in llistat_fallers:
			self.ident=self.ident+[faller.id]
			llista=llista + [(faller.cognoms + ", " + faller.nom)]
		self.fallerCombo["values"]=llista # Insertem cada valor en el desplegable.

	
	def selection_changed(self, event):
		'''
		Controla la selecció del combobox per a guardar el identificador del faller i omplir les dades a partir d'aquest
		'''
		index=self.fallerCombo.current()
		self.idString.set(self.ident[index])
		cadena=self.idString.get()
		self.ident=[]
		self.OmplirBuscar(cadena)
		

	def dropdown_opened_fam(self):

		bd=BaseDeDades("falla.db")
		falla=Falla()
		faller=bd.llegir_faller(self.idString.get())
		llistat_fallers=falla.llegir_fallers("familia", faller.familia.id)
		llista=[] # Llista on anem a acumular els valors.
		self.ident=[]
		for faller in llistat_fallers:
			self.ident=self.ident+[faller.id]
			llista=llista + [(faller.cognoms + ", " + faller.nom)]
		self.familiaCombo["values"]=llista


	def selection_changed_fam(self, event):

		index=self.familiaCombo.current()
		self.idString.set(self.ident[index])
		cadena=self.idString.get()
		self.ident=[]
		self.OmplirBuscar(cadena)
		self.familiaCombo.set("") # El borrem per a que no mostre l'últim nom.


	def OmplirBuscar(self, id):

		bd=BaseDeDades("falla.db")
		arxiu=Arxiu("exercici")
		falla=Falla()
		quota=0
		faller=bd.llegir_faller(id) # Busquem el faller a partir de la cadena guardada.
		# Omplim els camps de dades personals.
		self.fallerCombo.set(faller.cognoms + ", " + faller.nom) # Mostrem en el combo els cognoms i nom del faller.
		self.naixementString.set(faller.naixement) # Mostrem la data de naixement del faller.
		self.dniString.set(faller.dni) # Mostrem el dni del faller.
		self.adresaString.set(faller.adresa) # Mostrem l'adreça del faller.
		self.telefonString.set(faller.telefon) # Mostrem el telèfon del faller.
		self.correuString.set(faller.correu) # Mostrem el correu electrònic del faller.
		#self.idmod=num
		#self.modificarBoto.config(state="normal")
		if faller.alta==0: # Mostrem en verd o en roig els camps segons alta.
			self.altaBoto.config(state="normal", text="Donar d'alta")
			self.naixementEntry.configure(disabledbackground="#ff3f3f", disabledforeground="white")
			self.dniEntry.configure(disabledbackground="#ff3f3f", disabledforeground="white")
			self.adresaEntry.configure(disabledbackground="#ff3f3f", disabledforeground="white")
			self.telefonEntry.configure(disabledbackground="#ff3f3f", disabledforeground="white")
			self.correuEntry.configure(disabledbackground="#ff3f3f", disabledforeground="white")
			self.pagarquotaString.set("")
			self.pagarquotaEntry.config(state="disabled")
			self.pagarloteriaString.set("")
			self.pagarloteriaEntry.config(state="disabled")
			self.pagarrifaString.set("")
			self.pagarrifaEntry.config(state="disabled")
			self.pagartotalString.set("")
			self.pagarBoto.config(state="disabled")
		else:
			self.altaBoto.config(state="normal", text="Donar de baixa")
			self.naixementEntry.configure(disabledbackground="#98ff98", disabledforeground="black")
			self.dniEntry.configure(disabledbackground="#98ff98", disabledforeground="black")
			self.adresaEntry.configure(disabledbackground="#98ff98", disabledforeground="black")
			self.telefonEntry.configure(disabledbackground="#98ff98", disabledforeground="black")
			self.correuEntry.configure(disabledbackground="#98ff98", disabledforeground="black")
			self.pagarquotaString.set("0") # Fiquem un 0 en el entry per a que no done error l'operació.
			self.pagarquotaEntry.config(state="normal") # Passa a normal per a poder operar.
			self.pagarloteriaString.set("0")
			self.pagarloteriaEntry.config(state="normal")
			self.pagarrifaString.set("0")
			self.pagarrifaEntry.config(state="normal")
			self.pagartotalString.set("0 €")
			self.pagarBoto.config(state="normal")
			if faller.naixement=="01-01-1900": # Mostrem en groc als fallers dels quals ens falta la data de naixement.
				self.naixementEntry.configure(disabledbackground="#ffff00")
				self.dniEntry.configure(disabledbackground="#ffff00")
				self.adresaEntry.configure(disabledbackground="#ffff00")
				self.telefonEntry.configure(disabledbackground="#ffff00")
				self.correuEntry.configure(disabledbackground="#ffff00")
		# Omplim els camps d'assignacions i pagaments del faller.
		quota_base=bd.llegir_quota_faller(faller.id)
		descompte=faller.familia.descompte*quota_base/100
		quota=quota_base-descompte # Busquem la quota corresponent al faller i li restem el descompte familiar.
		exercici_actual=arxiu.llegir_exercici_actual()
		# Busquem tots els moviments del faller en l'exercici i els separem en quotes, loteries o rifes i en assignat o pagat.
		llista_assignacions_pagaments=falla.calcular_assignacions_pagaments(faller.id, exercici_actual)
		# Assignem cada element de la llista a una variable per a que siga més fàcil d'identificar.
		quotaassignada=llista_assignacions_pagaments[0]
		quotapagada=llista_assignacions_pagaments[1]
		loteriaassignada=llista_assignacions_pagaments[2]
		loteriapagada=llista_assignacions_pagaments[3]
		rifaassignada=llista_assignacions_pagaments[4]
		rifapagada=llista_assignacions_pagaments[5]
		quotafinal=quota+quotaassignada
		self.quotaString.set("{0:.2f}".format(quotafinal) + " €") # La quota assignada es la quota total menys el descompte més les assignacions.
		self.quotapagString.set("{0:.2f}".format(quotapagada) + " €") # Mostrem la quota pagada.
		self.deutequotaString.set("{0:.2f}".format(quotafinal-quotapagada) + " €") # Mostrem el deute de la quota.
		self.loteriaString.set("{0:.2f}".format(loteriaassignada) + " €") # El mateix en loteria.
		self.loteriapagString.set("{0:.2f}".format(loteriapagada) + " €")
		self.deuteloteriaString.set("{0:.2f}".format(loteriaassignada-loteriapagada) + " €")
		self.rifaString.set("{0:.2f}".format(rifaassignada) + " €") # El mateix en rifa.
		self.rifapagString.set("{0:.2f}".format(rifapagada) + " €")
		self.deuterifaString.set("{0:.2f}".format(rifaassignada-rifapagada) + " €")
		self.totalasignatString.set("{0:.2f}".format(quotafinal+loteriaassignada+rifaassignada) + " €") #totals
		self.totalpagatString.set("{0:.2f}".format(quotapagada+loteriapagada+rifapagada) + " €")
		self.totalString.set("{0:.2f}".format((quotafinal+loteriaassignada+rifaassignada)-(quotapagada+loteriapagada+rifapagada)) + " €")
		# Omplim els camps d'assignacions i pagaments de la familia completa del faller.
		llistat_fallers=falla.llegir_fallers("familia", faller.familia.id)
		membres=0
		#idfaller=[]
		for faller in llistat_fallers:
			if faller.alta==1:
				membres=membres + 1
				#idfaller=idfaller+faller.id # Afegim a la llista el id.
		self.membresString.set(membres)
		if membres==0: # Activarem els camps si hi ha membres actius a la familia.
			self.pagarquotafamString.set("")
			self.pagarquotafamEntry.config(state="disabled")
			self.pagarloteriafamString.set("")
			self.pagarloteriafamEntry.config(state="disabled")
			self.pagarrifafamString.set("")
			self.pagarrifafamEntry.config(state="disabled")
			self.pagartotalfamString.set("")
			self.pagarfamBoto.config(state="disabled")
		else:
			self.pagarquotafamString.set("0")
			self.pagarquotafamEntry.config(state="normal")
			self.pagarloteriafamString.set("0")
			self.pagarloteriafamEntry.config(state="normal")
			self.pagarrifafamString.set("0")
			self.pagarrifafamEntry.config(state="normal")
			self.pagartotalfamString.set("0 €")
			self.pagarfamBoto.config(state="normal")
		self.descripcioString.set("") # Reiniciem el valor de descripció de les assignacions
		quota=0 # Les iniciem a 0 per què no s'acumulen amb les anteriors.
		quotaassignada=0
		quotapagada=0
		loteriaassignada=0
		loteriapagada=0
		rifaassignada=0
		rifapagada=0
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
		self.quotafamString.set("{0:.2f}".format(quotafinal) + " €") # Mostrem la quota de la familia.
		self.quotapagadafamString.set("{0:.2f}".format(quotapagada) + " €") # Mostrem el total pagat de quota de la familia.
		self.deutequotafamString.set("{0:.2f}".format(quotafinal-quotapagada) + " €")
		self.loteriafamString.set("{0:.2f}".format(loteriaassignada) + " €")
		self.loteriapagadafamString.set("{0:.2f}".format(loteriapagada) + " €")
		self.deuteloteriafamString.set("{0:.2f}".format(loteriaassignada-loteriapagada) + " €")
		self.rifafamString.set("{0:.2f}".format(rifaassignada) + " €")
		self.rifapagadafamString.set("{0:.2f}".format(rifapagada) + " €")
		self.deuterifafamString.set("{0:.2f}".format(rifaassignada-rifapagada) + " €")
		self.totalasignatfamString.set("{0:.2f}".format(quotafinal+loteriaassignada+rifaassignada) + " €")
		self.totalpagatfamString.set("{0:.2f}".format(quotapagada+loteriapagada+rifapagada) + " €")
		self.totalfamString.set("{0:.2f}".format((quotafinal-quotapagada)+(loteriaassignada-loteriapagada)+(rifaassignada-rifapagada)) + " €")	
		if faller.alta==1: # Habilitar o deshabilitem el botó i el entry de l'assignació.
			self.descripcioEntry.config(state="normal")
			self.asignarString.set("0")
			self.asignarEntry.config(state="normal")
			self.asignarBoto.config(state="normal")
		if faller.alta==0:
			self.descripcioEntry.config(state="disabled")
			self.asignarString.set("")
			self.asignarEntry.config(state="disabled")
			self.asignarBoto.config(state="disabled")
		self.movimentsTree.delete(*self.movimentsTree.get_children()) # Borrem la taula
		llistat_moviments=bd.llegir_moviments(id, exercici_actual)
		for moviment in llistat_moviments:
			if moviment.concepte==1:
				concepte="quota"
			elif moviment.concepte==2:
				concepte="loteria"
			elif moviment.concepte==3:
				concepte="rifa"
			if moviment.tipo==1: # Segons si es asignació o pagament fiquem la quantitat en una o altra columna
				self.movimentsTree.insert("","end", text=moviment.id, values=(moviment.data, "{0:.2f}".format(moviment.quantitat) + " €", "", concepte, moviment.descripcio))
			elif moviment.tipo==2:
				self.movimentsTree.insert("","end", text=moviment.id, values=(moviment.data, "", "{0:.2f}".format(moviment.quantitat) + " €", concepte, moviment.descripcio))

		
	def LlevarCeroQuota(self, event): #aquestes 3 funcions lleven el 0 per a deixar espai en blanc per a escriure

		if self.pagarquotaString.get()=="0":
			self.pagarquotaString.set("")


	def LlevarCeroLoteria(self, event):

		if self.pagarloteriaString.get()=="0":
			self.pagarloteriaString.set("")


	def LlevarCeroRifa(self, event):

		if self.pagarrifaString.get()=="0":
			self.pagarrifaString.set("")

	
	def LlevarCeroQuotaFam(self, event):

		if self.pagarquotafamString.get()=="0":
			self.pagarquotafamString.set("")

	
	def LlevarCeroLoteriaFam(self, event):

		if self.pagarloteriafamString.get()=="0":
			self.pagarloteriafamString.set("")

	
	def LlevarCeroRifaFam(self, event):

		if self.pagarrifafamString.get()=="0":
			self.pagarrifafamString.set("")


	def CalcularPagarTotalQuota(self, event): #calcula la suma dels 3 camps de pagament segons el camp en el que estiga

		pq=0
		pl=float(self.pagarloteriaString.get())
		pr=float(self.pagarrifaString.get())
		if self.pagarquotaString.get()=="": #si el camp es queda buit fiquem automàticament un 0
			self.pagarquotaString.set("0")
		try:
			pq=float(self.pagarquotaString.get())
		except ValueError: #si el valor no es vàlid el fiquem a 0 per a que no done error, fem la suma amb els altres camps
			self.pagarquotaString.set(0)
			self.pagartotalString.set("{0:.2f}".format(pl+pr) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
			self.pagarquotaEntry.focus() #li deixem el focus per a ficar el valor vàlid
		self.pagartotalString.set("{0:.2f}".format(pq+pl+pr) + " €")

	
	def CalcularPagarTotalLoteria(self, event):
		
		pl=0
		pq=float(self.pagarquotaString.get())
		pr=float(self.pagarrifaString.get())
		if self.pagarloteriaString.get()=="":
			self.pagarloteriaString.set("0")
		try:
			pl=float(self.pagarloteriaString.get())
		except ValueError:
			self.pagarloteriaString.set(0)
			self.pagartotalString.set("{0:.2f}".format(pq+pr) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
			self.pagarloteriaEntry.focus()
		self.pagartotalString.set("{0:.2f}".format(pq+pl+pr) + " €")

	
	def CalcularPagarTotalRifa(self, event):
		
		pr=0
		pl=float(self.pagarloteriaString.get())
		pq=float(self.pagarquotaString.get())
		if self.pagarrifaString.get()=="":
			self.pagarrifaString.set("0")
		try:
			pr=float(self.pagarrifaString.get())
		except ValueError:
			self.pagarrifaString.set(0)
			self.pagartotalString.set("{0:.2f}".format(pq+pl) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
			self.pagarrifaEntry.focus()
		self.pagartotalString.set("{0:.2f}".format(pq+pl+pr) + " €")

	
	def CalcularPagarFamTotalQuota(self, event):

		pq=0
		pl=float(self.pagarloteriafamString.get())
		pr=float(self.pagarrifafamString.get())
		if self.pagarquotafamString.get()=="":
			self.pagarquotafamString.set("0")
		if float(self.pagarquotafamString.get())<0:
			self.pagarquotafamString.set("0")
			messagebox.showwarning("Error", "Els abonos només es poden fer als fallers per separat")
		try:
			pq=float(self.pagarquotafamString.get())
		except ValueError:
			self.pagarquotafamString.set(0)
			self.pagartotalfamString.set("{0:.2f}".format(pl+pr) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
			self.pagarquotafamEntry.focus()
		self.pagartotalfamString.set("{0:.2f}".format(pq+pl+pr) + " €")

	
	def CalcularPagarFamTotalLoteria(self, event):
		
		pl=0
		pq=float(self.pagarquotafamString.get())
		pr=float(self.pagarrifafamString.get())
		if self.pagarloteriafamString.get()=="":
			self.pagarloteriafamString.set("0")
		if float(self.pagarloteriafamString.get())<0:
			self.pagarloteriafamString.set("0")
			messagebox.showwarning("Error", "Els abonos només es poden fer als fallers per separat")
		try:
			pl=float(self.pagarloteriafamString.get())
		except ValueError:
			self.pagarloteriafamString.set(0)
			self.pagartotalfamString.set("{0:.2f}".format(pq+pr) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
			self.pagarloteriafamEntry.focus()
		self.pagartotalfamString.set("{0:.2f}".format(pq+pl+pr) + " €")
	

	def CalcularPagarFamTotalRifa(self, event):
		
		pr=0
		pl=float(self.pagarloteriafamString.get())
		pq=float(self.pagarquotafamString.get())
		if self.pagarrifafamString.get()=="":
			self.pagarrifafamString.set("0")
		if float(self.pagarrifafamString.get())<0:
			self.pagarrifafamString.set("0")
			messagebox.showwarning("Error", "Els abonos només es poden fer als fallers per separat")
		try:
			pr=float(self.pagarrifafamString.get())
		except ValueError:
			self.pagarrifafamString.set(0)
			self.pagartotalfamString.set("{0:.2f}".format(pq+pl) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
			self.pagarrifafamEntry.focus()
		self.pagartotalfamString.set("{0:.2f}".format(pq+pl+pr) + " €")
	
	
	def Pagar(self):

		arxiu=Arxiu('exercici')
		bd=BaseDeDades('falla.db')
		utils=Utils()
		pagquo=0
		paglot=0
		pagrif=0
		if self.pagarquotaString.get()=="":
			self.pagarquotaString.set(0)
		if self.pagarloteriaString.get()=="":
			self.pagarloteriaString.set(0)
		if self.pagarrifaString.get()=="":
			self.pagarrifaString.set(0)
		try:
			pagquo=float(self.pagarquotaString.get()) #guardem en variables les quantitats a pagar per a mostrar-les al rebut
		except ValueError:
			pagquo=0
			self.pagarquotaString.set(0)
			self.pagartotalString.set("{0:.2f}".format(paglot+pagrif) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
		try:
			paglot=float(self.pagarloteriaString.get())
		except ValueError:
			paglot=0
			self.pagarloteriaString.set(0)
			self.pagartotalString.set("{0:.2f}".format(pagquo+pagrif) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
		try:
			pagrif=float(self.pagarrifaString.get())
		except ValueError:
			pagrif=0
			self.pagarrifaString.set(0)
			self.pagartotalString.set("{0:.2f}".format(paglot+pagrif) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
		opcio=self.formapagamentString.get() #guardem l'opció triada per a la descripció de la base de dades
		descripcio=""
		if opcio=="1":
			descripcio="pagat en caixa"
		if opcio=="2":
			descripcio="pagat pel banc"
			#desc="domiciliació"
		valor=messagebox.askquestion("Pagar","Estàs segur que vols fer el pagament?")
		if valor=="yes":
			if self.pagarquotaString.get()=="":
				self.pagarquotaString.set("0")
			if self.pagarloteriaString.get()=="":
				self.pagarloteriaString.set("0")
			if self.pagarrifaString.get()=="":
				self.pagarrifaString.set("0")
			if float(self.pagarquotaString.get())==0 and float(self.pagarloteriaString.get())==0 and float(self.pagarrifaString.get())==0:
				messagebox.showwarning("Error", "No es pot fer un pagament de 0 euros")
			else:
				rebut=0
				#if opcio=="1":
					#busquem el número que li pertocarà al rebut
					#elRebut=Informe()
					#numrebut=elRebut.AsignarNumRebut()
				exercici_actual=arxiu.llegir_exercici_actual()
				data=utils.calcular_data_actual()
				id=self.idString.get()
				faller=bd.llegir_faller(id)
				#inserta a la base de dades cada moviment realitzat
				if float(self.pagarquotaString.get())!=0:
					moviment=Moviment(0, data, float(self.pagarquotaString.get()), 2, 1, exercici_actual, descripcio, rebut, faller)
					bd.crear_moviment(moviment)
					#elMoviment.InsertarPagament(float(self.pagarquotaString.get()), 1, elMoviment.exercici, float(self.idString.get()), desc, numrebut)
				if float(self.pagarloteriaString.get())!=0:
					moviment=Moviment(0, data, float(self.pagarloteriaString.get()), 2, 2, exercici_actual, descripcio, rebut, faller)
					bd.crear_moviment(moviment)
					#elMoviment.InsertarPagament(float(self.pagarloteriaString.get()), 2, elMoviment.exercici, float(self.idString.get()), desc, numrebut)
				if float(self.pagarrifaString.get())!=0:
					moviment=Moviment(0, data, float(self.pagarrifaString.get()), 2, 3, exercici_actual, descripcio, rebut, faller)
					bd.crear_moviment(moviment)
					#elMoviment.InsertarPagament(float(self.pagarrifaString.get()), 3, elMoviment.exercici, float(self.idString.get()), desc, numrebut)
				#netegem les dades i refresquem per a vore el quadre de pagaments actualitzat
				self.idEntry.focus()
				self.BuscarId('<Return>')
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
		if self.pagarquotafamString.get()=="":
			self.pagarquotafamString.set("0")
		if self.pagarloteriafamString.get()=="":
			self.pagarloteriafamString.set("0")
		if self.pagarrifafamString.get()=="":
			self.pagarrifafamString.set("0")
		try:
			pagquofam=float(self.pagarquotafamString.get()) #guardem en variables les quantitats a pagar per a mostrar-les al rebut
			if float(self.pagarquotafamString.get())<0:
				pagquofam=0
		except ValueError:
			pagquofam=0
			self.pagarquotafamString.set(0)
			self.pagartotalfamString.set("{0:.2f}".format(paglotfam+pagriffam) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
		try:
			paglotfam=float(self.pagarloteriafamString.get())
			if float(self.pagarloteriafamString.get())<0:
				paglotfam=0
		except ValueError:
			paglotfam=0
			self.pagarloteriafamString.set(0)
			self.pagartotalfamString.set("{0:.2f}".format(pagquofam+pagriffam) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
		try:
			pagriffam=float(self.pagarrifafamString.get())
			if float(self.pagarrifafamString.get())<0:
				pagriffam=0
		except ValueError:
			pagriffam=0
			self.pagarrifafamString.set(0)
			self.pagartotalfamString.set("{0:.2f}".format(paglotfam+pagriffam) + " €")
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
		opcio=self.formapagamentfamString.get()
		descripcio=""
		if opcio=="1":
			descripcio="pagat en caixa"
		if opcio=="2":
			descripcio="pagat pel banc"
		valor=messagebox.askquestion("Pagar","Estàs segur que vols fer el pagament?")
		if valor=="yes":
			if self.pagarquotafamString.get()=="":
				self.pagarquotafamString.set("0")
			if self.pagarloteriafamString.get()=="":
				self.pagarloteriafamString.set("0")
			if self.pagarrifafamString.get()=="":
				self.pagarrifafamString.set("0")
			if float(self.pagarquotafamString.get())==0 and float(self.pagarloteriafamString.get())==0 and float(self.pagarrifafamString.get())==0:
				messagebox.showwarning("Error", "No es pot fer un pagament de 0 euros")						
			else:
				faller=bd.llegir_faller(self.idString.get())
				llistat_fallers=falla.llegir_fallers("familia", faller.familia.id)
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
				pagamentquota=float(self.pagarquotafamString.get()) #guardem els continguts en variables
				pagamentloteria=float(self.pagarloteriafamString.get())
				pagamentrifa=float(self.pagarrifafamString.get())
				rebut=0
				#if opcio=="1":
					#busquem el número que li pertocarà al rebut
					#elRebut=Informe()
					#numrebut=elRebut.AsignarNumRebut()
				exercici_actual=arxiu.llegir_exercici_actual()
				data=utils.calcular_data_actual()
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
						moviment=Moviment(0, data, pagamentquota, 2, 1, exercici_actual, descripcio, rebut, faller)
						bd.crear_moviment(moviment)
						#elMoviment.InsertarPagament(pagamentquota, 1, elMoviment.exercici, val, desc, numrebut)
						pagamentquota=0
					if pagamentquota!=0 and pagamentquota<=difquota and membres!=1:
						moviment=Moviment(0, data, pagamentquota, 2, 1, exercici_actual, descripcio, rebut, faller)
						bd.crear_moviment(moviment)
						#elMoviment.InsertarPagament(pagamentquota, 1, elMoviment.exercici, val, desc, numrebut)
						pagamentquota=0
					if pagamentquota!=0 and pagamentquota>difquota and membres!=1:
						if difquota!=0: #per a que no cree moviments a 0
							moviment=Moviment(0, data, difquota, 2, 1, exercici_actual, descripcio, rebut, faller)
							bd.crear_moviment(moviment)
						#elMoviment.InsertarPagament(difquota, 1, elMoviment.exercici, val, desc, numrebut)
						pagamentquota=pagamentquota-difquota
					#loteriaasignada=elMoviment.loteriaasignada
					#loteriapagada=elMoviment.loteriapagada
					difloteria=loteriaassignada-loteriapagada
					if pagamentloteria!=0 and membres==1:
						moviment=Moviment(0, data, pagamentloteria, 2, 2, exercici_actual, descripcio, rebut, faller)
						bd.crear_moviment(moviment)
						#elMoviment.InsertarPagament(pagamentloteria, 2, elMoviment.exercici, val, desc, numrebut)
					if pagamentloteria!=0 and pagamentloteria<=difloteria and membres!=1:
						moviment=Moviment(0, data, pagamentloteria, 2, 2, exercici_actual, descripcio, rebut, faller)
						bd.crear_moviment(moviment)
						#elMoviment.InsertarPagament(pagamentloteria, 2, elMoviment.exercici, val, desc, numrebut)
						pagamentloteria=0
					if pagamentloteria!=0 and pagamentloteria>difloteria and membres!=1:
						if difloteria!=0:
							moviment=Moviment(0, data, difloteria, 2, 2, exercici_actual, descripcio, rebut, faller)
							bd.crear_moviment(moviment)
							#elMoviment.InsertarPagament(difloteria, 2, elMoviment.exercici, val, desc, numrebut)
						pagamentloteria=pagamentloteria-difloteria
					#rifaasignada=elMoviment.rifaasignada
					#rifapagada=elMoviment.rifapagada
					difrifa=rifaassignada-rifapagada
					if pagamentrifa!=0 and membres==1:
						moviment=Moviment(0, data, pagamentrifa, 2, 3, exercici_actual, descripcio, rebut, faller)
						bd.crear_moviment(moviment)
						#elMoviment.InsertarPagament(pagamentrifa, 3, elMoviment.exercici, val, desc, numrebut)
					if pagamentrifa!=0 and pagamentrifa<=difrifa and membres!=1:
						moviment=Moviment(0, data, pagamentrifa, 2, 3, exercici_actual, descripcio, rebut, faller)
						bd.crear_moviment(moviment)
						#elMoviment.InsertarPagament(pagamentrifa, 3, elMoviment.exercici, val, desc, numrebut)
						pagamentrifa=0
					if pagamentrifa!=0 and pagamentrifa>difrifa and membres!=1:
						if difrifa!=0:
							moviment=Moviment(0, data, difrifa, 2, 3, exercici_actual, descripcio, rebut, faller)
							bd.crear_moviment(moviment)
							#elMoviment.InsertarPagament(difrifa, 3, elMoviment.exercici, val, desc, numrebut)
						pagamentrifa=pagamentrifa-difrifa
					membres=membres-1
				self.idEntry.focus()
				self.BuscarId('<Return>')
				#if opcio=="1":
					#creem el rebut a partir de les dades de les variables dels pagaments i el quadre actualitzat amb el resutat final llevant els 2 últims caràcters ( €) als valors que necessiten un càlcul posterior
					#elRebut.Rebut(1,self.fallerCombo.get(), pagquofam, paglotfam, pagriffam, self.quotafamString.get()[:-2], self.quotapagadafamString.get()[:-2], self.loteriafamString.get()[:-2], self.loteriapagadafamString.get()[:-2], self.rifafamString.get()[:-2], self.rifapagadafamString.get()[:-2])

	
	def Asignar(self):

		arxiu=Arxiu("exercici")
		bd=BaseDeDades("falla.db")
		utils=Utils()
		exercici_actual=arxiu.llegir_exercici_actual()
		data=utils.calcular_data_actual()
		descripcio=self.descripcioString.get() #recuperem la descripció per a l'assignació
		opcio=self.asignacioString.get() #recuperem l'opció triada
		valor=messagebox.askquestion("Asignar","Estàs segur que vols fer l'assignació?")
		if valor=="yes":
			try:
				if float(self.asignarString.get())==0:
					messagebox.showwarning("Error", "No es pot fer una assignació de 0 euros")
				else:
					faller=bd.llegir_faller(self.idString.get())
					moviment=Moviment(0, data, float(self.asignarString.get()), 1, int(opcio), exercici_actual, descripcio, 0, faller)
					bd.crear_moviment(moviment)
					#elMoviment.InsertarAsignacio(float(self.asignarString.get()), int(opcio), elMoviment.exercici, int(self.idString.get()), desc)
					self.idEntry.focus()
					self.BuscarId('<Return>')
			except ValueError:
				messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
				self.asignarString.set(0)