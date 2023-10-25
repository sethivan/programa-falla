from datetime import date
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from tkinter import messagebox
import os
import errno
import os.path as path
import subprocess
import platform
import pickle

from base_de_dades import BaseDeDades
from utils import Utils
from arxiu import Arxiu
from falla import Falla
from faller import Faller


class Informe():

	def __init__(self):

		pass


	def assignar_numero_rebut(self):
		'''
		Busca a la carpeta "rebuts" quin és l'últim rebut creat i retorna el número següent.

		Retorna:
		--------
		index : integer.
			Número de rebut disponible per a ser assignat.
		'''
		# Intentem crear la carpeta rebuts si no està creada.
		try:
			os.mkdir("rebuts")
		except OSError as e:
			if e.errno!=errno.EEXIST:
				raise
		# Assignem com a nom d'arxiu el següent número a l'últim creat.
		index=1
		arxiu="rebuts"+"/"+str(index)
		while path.exists(arxiu+".pdf"):
			index=index+1
			arxiu="rebuts"+"/"+str(index)
		return(index)


	def crear_rebut(self, familiar, nom, pagament_quota, pagament_loteria, pagament_rifa, quota_assignada, quota_pagada, loteria_assignada, loteria_pagada, rifa_assignada, rifa_pagada):
		'''
		Crea un .pdf amb la informació de pagament del faller en format rebut.

		Paràmetres:
		-----------
		familiar : boolean.
			Indica si el pagament ha segut personal o familiar.
		nom : string.
			Nom complet del faller.
		pagament_quota : real.
			Quantitat pagada pel faller en concepte de quota en el moviment actual.
		pagament_loteria : real.
			Quantitat pagada pel faller en concepte de loteria en el moviment actual.
		pagament_rifa : real.
			Quantitat pagada pel faller en concepte de rifa en el moviment actual.
		quota_assignada : real.
			Quantitat total assignada al faller en concepte de quota.
		quota_pagada : real.
			Quantitat total pagada pel faller en concepte de quota.
		loteria_assignada : real.
			Quantitat total assignada al faller en concepte de loteria.
		loteria_pagada : real.
			Quantitat total pagada pel faller en concepte de loteria.
		rifa_assignada : real.
			Quantitat total assignada al faller en concepte de rifa.
		rifa_pagada : real.
			Quantitat total pagada pel faller en concepte de rifa.
		'''
		# Traguem la data actual per a utilitzar-la al rebut.
		utils=Utils()
		data=utils.calcular_data_actual()
		data_actual=data[0] + "-" + data[1] + "-" + data[2]
		# Calculem el pagament total.
		pagament_total=pagament_quota+pagament_loteria+pagament_rifa
		# Calculem els deutes per concepte.
		deute_quota=float(quota_assignada)-float(quota_pagada)
		deute_loteria=float(loteria_assignada)-float(loteria_pagada)
		deute_rifa=float(rifa_assignada)-float(rifa_pagada)
		# Calculem els totals.
		total_assignat=float(quota_assignada)+float(loteria_assignada)+float(rifa_assignada)
		total_pagat=float(quota_pagada)+float(loteria_pagada)+float(rifa_pagada)
		deute_total=deute_quota + deute_loteria + deute_rifa
		# Intentem crear la carpeta rebuts si no està creada.
		try:
			os.mkdir("rebuts")
		except OSError as e:
			if e.errno!=errno.EEXIST:
				raise
		# Assignem com a nom d'arxiu el següent número a l'últim creat.
		index=self.assignar_numero_rebut()
		#index=1
		#arxiu="rebuts"+"/"+str(index)
		#while path.exists(arxiu+".pdf"):
			#index=index+1
			#arxiu="rebuts"+"/"+str(index)
		arxiu="rebuts"+"/"+str(index)

		# Creem el full i tot el contingut.
		w,h=A4
		c=canvas.Canvas(arxiu+".pdf", pagesize=A4)
		# Encapçalament.
		c.line(0,h-(h/3),w,h-(h/3))
		c.line(0,h/3,w,h/3)
		c.drawString(w-100, h-30, data_actual)
		# Informació de la part superior.
		c.drawString(50, h-50, nom + " abona la quantitat de " + "{0:.2f}".format(pagament_total) + " €")
		c.drawString(70, h-80, "{0:.2f}".format(pagament_quota) + " € en concepte de quota")
		c.drawString(70, h-100, "{0:.2f}".format(pagament_loteria) + " € en concepte de loteria")
		c.drawString(70, h-120, "{0:.2f}".format(pagament_rifa) + " € en concepte de rifa")
		# Informació de la taula.
		if familiar==0: # Li passem per variable si ha fet el pagament individual o per bloc familiar.
			c.drawString(50, h-150, "RESUM DEL PENDENT DE PAGAMENT:")
		else:
			c.drawString(50, h-150, "RESUM DEL PENDENT DE PAGAMENT DE LA FAMILIA COMPLETA:")
		xlist=[50,120,190,260,330]
		ylist=[h-165,h-185,h-205,h-225,h-245,h-265]
		c.grid(xlist,ylist)
		c.drawString(130, h-180, "Assignat")
		c.drawString(208, h-180, "Pagat")
		c.drawString(272, h-180, "Pendent")
		c.drawString(55, h-200, "Quota:")
		c.drawString(130, h-200, quota_assignada + " €")
		c.drawString(200, h-200, quota_pagada + " €")
		c.drawString(270, h-200, "{0:.2f}".format(deute_quota) + " €")
		c.drawString(55, h-220, "Loteria:")
		c.drawString(130, h-220, loteria_assignada + " €")
		c.drawString(200, h-220, loteria_pagada + " €")
		c.drawString(270, h-220, "{0:.2f}".format(deute_loteria) + " €")
		c.drawString(55, h-240, "Rifa:")
		c.drawString(130, h-240, rifa_assignada + " €")
		c.drawString(200, h-240, rifa_pagada + " €")
		c.drawString(270, h-240, "{0:.2f}".format(deute_rifa) + " €")
		c.drawString(55, h-260, "Totals:")
		c.drawString(130, h-260, "{0:.2f}".format(total_assignat) + " €")
		c.drawString(200, h-260, "{0:.2f}".format(total_pagat) + " €")
		c.drawString(270, h-260, "{0:.2f}".format(deute_total) + " €")
		c.drawImage("escut.jpg", 360, h-260, height=150, width=200)
		c.showPage()
		c.save()
		# Entrem a la carpeta "rebuts" per a obrir l'arxiu pdf i tornem a la ruta original.
		ruta=os.getcwd()
		os.chdir("rebuts")
		arxiu=str(index)+".pdf"
		sistema_operatiu=platform.system()
		if sistema_operatiu=='Windows':
			os.startfile(arxiu)
		elif sistema_operatiu=='Linux':
			ruta_completa=os.path.join(os.path.dirname(__file__), arxiu)
			subprocess.run(["xdg-open", ruta_completa])
		os.chdir(ruta)


	def llistat_moviments(self, data, efectiu, banc):
		'''
		Crea un .pdf amb un llistat de tots els moviments de la data indicada segons el tipus de pagament.

		Paràmetres:
		-----------
		data : string.
			Data en la que volem llistar els moviments.
		efectiu : boolean.
			Marca si volem traure els moviments fets en efectiu .
		banc : boolean.
			Marca si volem traure els moviments fets pel banc.
		'''
		bd=BaseDeDades("falla.db")
		pagina=0
		try:
			os.mkdir("moviments dia")
		except OSError as e:
			if e.errno!=errno.EEXIST:
				raise
		arxiu="moviments dia"+"/"+str(data)
		# Creem el full i tot el contingut.
		w,h=A4
		c=canvas.Canvas(arxiu+".pdf", pagesize=A4)
		if efectiu==1 and banc==1:
			llistat_moviments=bd.llegir_moviments_per_data_tipo(data, 2)
		elif efectiu==1 and banc==0:
			llistat_moviments=bd.llegir_moviments_per_data_tipo_descripcio(data, 2, "pagat en caixa")
		else:
			llistat_moviments=bd.llegir_moviments_per_data_tipo_descripcio(data, 2, "pagat pel banc")
		i=0
		total=0
		c.drawString(50, h-30, "FALLER")
		c.drawString(300, h-30, "CONCEPTE")
		c.drawString(w-100, h-30, "QUANTITAT")
		for moviment in llistat_moviments:
			c.drawString(50, h-i-60, moviment.faller.nom + " " + moviment.faller.cognoms)
			if moviment.concepte==1:
				concepte="quota"
			if moviment.concepte==2:
				concepte="loteria"
			if moviment.concepte==3:
				concepte="rifa"
			c.drawString(300, h-i-60, concepte)
			c.drawString(w-100, h-i-60, "{0:.2f}".format(moviment.quantitat) + " €")
			i=i+20
			total=total + moviment.quantitat
			if i==700:
				pagina=pagina+1
				c.drawString(20, 20, "moviments del dia")
				c.drawString((w/2)-30, 20, "pàgina "+str(pagina))
				c.drawString(w-80, 20, data)
				c.showPage() # Mostrem la pàgina creada.
				c.drawString(50, h-30, "FALLER") # Primera linea de la pàgina següent.
				c.drawString(300, h-30, "CONCEPTE")
				c.drawString(w-100, h-30, "QUANTITAT")
				i=0
		c.drawString(300, h-i-80, "TOTAL")
		c.drawString(w-100, h-i-80, "{0:.2f}".format(total) + " €")
		c.drawString(20, 20, "moviments del dia")
		c.drawString((w/2)-30, 20, "pàgina "+str(pagina+1))
		c.drawString(w-80, 20, data)
		c.showPage()
		c.save()
		# Entrem a la carpeta "moviments dia" per a obrir l'arxiu pdf i tornem a la ruta original.
		ruta=os.getcwd()
		os.chdir("moviments dia")
		arxiu=str(data)+".pdf"
		sistema_operatiu=platform.system()
		if sistema_operatiu=='Windows':
			os.startfile(arxiu)
		elif sistema_operatiu=='Linux':
			ruta_completa=os.path.join(os.path.dirname(__file__), arxiu)
			subprocess.run(["xdg-open", ruta_completa])
		os.chdir(ruta)


	def llistat_general(self):
		'''
		Crea un .pdf amb un llistat amb l'estat actual de comptes de tots els fallers actius
		i, en conseqüència, de la falla al complet.
		'''
		# Traguem la data actual per a utilitzar-la al rebut.
		utils=Utils()
		data=utils.calcular_data_actual()
		data_actual=data[0] + "-" + data[1] + "-" + data[2]
		bd=BaseDeDades('falla.db')
		llistat_fallers=bd.llegir_fallers_per_alta(1)
		arxiu=Arxiu('exercici')
		exercici_actual=arxiu.llegir_exercici_actual()
		falla=Falla()
		suma_quotes_assignades=0
		suma_quotes_pagades=0
		suma_loteries_assignades=0
		suma_loteries_pagades=0
		suma_rifes_assignades=0
		suma_rifes_pagades=0
		pagina=0
		# Intentem crear la carpeta "llistat general" si no està creada.
		try:
			os.mkdir("llistat general")
		except OSError as e:
			if e.errno!=errno.EEXIST:
				raise
		arxiu="llistat general"+"/"+str(data_actual)
		# Creem el full i tot el contingut.
		w,h=A4
		c=canvas.Canvas(arxiu+".pdf", pagesize=landscape(A4)) # El creem en horitzontal.
		c.setFont("Helvetica", 11)
		i=0
		fallers=0 # Per a acumular el total de fallers.
		c.drawString(20, w-30, "ID") # La w és el segon parámetre ja que està en horitzontal.
		c.drawString(50, w-30, "FALLER")
		c.drawRightString(295, w-30, "QUOTA A.")
		c.drawRightString(365, w-30, "QUOTA P.")
		c.drawRightString(435, w-30, "LOTER. A.")
		c.drawRightString(505, w-30, "LOTER. P.")
		c.drawRightString(565, w-30, "RIFA A.")
		c.drawRightString(625, w-30, "RIFA P.")
		c.drawRightString(695, w-30, "TOTAL A.")
		c.drawRightString(765, w-30, "TOTAL P.")
		c.drawRightString(835, w-30, "DIFERÈNC.")
		c.line(0, w-35, h, w-35)
		for faller in llistat_fallers:
			quota_assignada=0 # Resetejem a cada iteració per a que no s'acumulen
			quota_pagada=0
			loteria_assignada=0
			loteria_pagada=0
			rifa_assignada=0
			rifa_pagada=0
			c.drawString(20, w-i-60, str(faller.id))
			c.drawString(50, w-i-60, faller.cognoms + ", " + faller.nom)
			quota_base=bd.llegir_quota_faller(faller.id)
			descompte=(faller.familia.descompte*quota_base/100)
			quota=quota_base-descompte
			llista_assignacions_pagaments=falla.calcular_assignacions_pagaments(faller.id, exercici_actual)
			quota_assignada=llista_assignacions_pagaments[0]
			quota_pagada=llista_assignacions_pagaments[1]
			loteria_assignada=llista_assignacions_pagaments[2]
			loteria_pagada=llista_assignacions_pagaments[3]
			rifa_assignada=llista_assignacions_pagaments[4]
			rifa_pagada=llista_assignacions_pagaments[5]
			quota_final=quota+quota_assignada
			total_assignat=quota_final+loteria_assignada+rifa_assignada
			total_pagat=quota_pagada+loteria_pagada+rifa_pagada
			c.drawRightString(295, w-i-60, "{0:.2f}".format(quota_final) + " €")
			suma_quotes_assignades=suma_quotes_assignades+quota_final
			c.drawRightString(365, w-i-60, "{0:.2f}".format(quota_pagada) + " €")
			suma_quotes_pagades=suma_quotes_pagades+quota_pagada
			c.drawRightString(435, w-i-60, "{0:.2f}".format(loteria_assignada) + " €")
			suma_loteries_assignades=suma_loteries_assignades+loteria_assignada
			c.drawRightString(505, w-i-60, "{0:.2f}".format(loteria_pagada) + " €")
			suma_loteries_pagades=suma_loteries_pagades+loteria_pagada
			c.drawRightString(565, w-i-60, "{0:.2f}".format(rifa_assignada) + " €")
			suma_rifes_assignades=suma_rifes_assignades+rifa_assignada
			c.drawRightString(625, w-i-60, "{0:.2f}".format(rifa_pagada) + " €")
			suma_rifes_pagades=suma_rifes_pagades+rifa_pagada
			c.drawRightString(695, w-i-60, "{0:.2f}".format(total_assignat) + " €")
			c.drawRightString(765, w-i-60, "{0:.2f}".format(total_pagat) + " €")
			c.drawRightString(835, w-i-60, "{0:.2f}".format(total_assignat-total_pagat) + " €")
			i=i+20
			fallers=fallers+1
			if i==500: # Quan arribem a 25 fallers canviem de pàgina.
				pagina=pagina+1
				c.drawString(20, 20, "llistat general")
				c.drawString((h/2)-30, 20, "pàgina "+str(pagina))
				c.drawString(h-80, 20, data_actual)
				c.showPage() # Mostrem la pàgina feta.
				c.setFont("Helvetica", 11)
				c.drawString(20, w-30, "ID") # Primera línea de la següent pàgina.
				c.drawString(50, w-30, "FALLER")
				c.drawRightString(295, w-30, "QUOTA A.")
				c.drawRightString(365, w-30, "QUOTA P.")
				c.drawRightString(435, w-30, "LOTER. A.")
				c.drawRightString(505, w-30, "LOTER. P.")
				c.drawRightString(565, w-30, "RIFA A.")
				c.drawRightString(625, w-30, "RIFA P.")
				c.drawRightString(695, w-30, "TOTAL A.")
				c.drawRightString(765, w-30, "TOTAL P.")
				c.drawRightString(835, w-30, "DIFERÈNC.")
				c.line(0, w-35, h, w-35)
				i=0
		c.line(0, w-i-60, h, w-i-60)
		c.drawRightString(50,w-i-80, "TOTALS")
		c.drawRightString(200,w-i-80, "FALLERS = " + str(fallers))
		c.drawRightString(295,w-i-80, "{0:.2f}".format(suma_quotes_assignades) + " €")
		c.drawRightString(365,w-i-80, "{0:.2f}".format(suma_quotes_pagades) + " €")
		c.drawRightString(435,w-i-80, "{0:.2f}".format(suma_loteries_assignades) + " €")
		c.drawRightString(505,w-i-80, "{0:.2f}".format(suma_loteries_pagades) + " €")
		c.drawRightString(565,w-i-80, "{0:.2f}".format(suma_rifes_assignades) + " €")
		c.drawRightString(625,w-i-80, "{0:.2f}".format(suma_rifes_pagades) + " €")
		total_assignacions=suma_quotes_assignades+suma_loteries_assignades+suma_rifes_assignades
		c.drawRightString(695,w-i-80, "{0:.2f}".format(total_assignacions) + " €")
		total_pagaments=suma_quotes_pagades+suma_loteries_pagades+suma_rifes_pagades
		c.drawRightString(765,w-i-80, "{0:.2f}".format(total_pagaments) + " €")
		c.drawRightString(835,w-i-80, "{0:.2f}".format(total_assignacions-total_pagaments) + " €")
		pagina=pagina+1
		c.drawString(20, 20, "llistat general")
		c.drawString((h/2)-30, 20, "pàgina "+str(pagina))
		c.drawString(h-80, 20, data_actual)
		c.showPage() # Última pàgina.
		c.save()
		# Entrem a la carpeta llistat general per a obrir l'arxiu pdf i tornem a la ruta original.
		ruta=os.getcwd()
		os.chdir("llistat general")
		os.startfile(str(data_actual)+".pdf")
		os.chdir(ruta)


	def llistat_altes_baixes(self):
		'''
		Crea un .pdf amb un llistat de les altes i les baixes de la falla al comparar
		els actuals fallers amb el resum de l'any anterior.
		'''
		arxiu=Arxiu('exercici')
		exercici_actual=arxiu.llegir_exercici_actual()
		any_anterior=exercici_actual-1
		try:
			fitxer=open("resum "+str(any_anterior), "rb")
		except IOError:
			messagebox.showerror("Informe", "No existeix l'arxiu resum de l'any anterior")
		else:
			llistat_fallers_anteriors=pickle.load(fitxer)
			fitxer.close()
			del(fitxer)
			ids_anteriors=[]
			ids_actuals=[]
			for faller in llistat_fallers_anteriors:
				ids_anteriors.append(faller[0])
			bd=BaseDeDades('falla.db')
			llistat_fallers_actuals=bd.llegir_fallers_per_alta(1)
			for faller in llistat_fallers_actuals:
				ids_actuals.append(faller.id)
			llistat_ids_baixes=set(ids_anteriors)-set(ids_actuals)
			llistat_ids_altes=set(ids_actuals)-set(ids_anteriors)
			# Calculem la data actual per a utilitzar-la a l'informe.
			utils=Utils()
			data=utils.calcular_data_actual()
			data_actual=data[0] + "-" + data[1] + "-" + data[2]
			pagina=0
			# Intentem crear la carpeta altes i baixes si no està creada.
			try:
				os.mkdir("altes i baixes")
			except OSError as e:
				if e.errno!=errno.EEXIST:
					raise
			arxiu="altes i baixes"+"/"+str(data_actual)
			# Creem el full i tot el contingut.
			w,h=A4
			c=canvas.Canvas(arxiu+".pdf", pagesize=landscape(A4)) # El creem en horitzontal.
			i=0
			c.drawString(20, w-30, "ID") # La w és el segon parámetre ja que està en horitzontal.
			c.drawString(50, w-30, "FALLER")
			c.drawString(250, w-30, "DNI")
			c.drawString(325, w-30, "ADREÇA")
			c.drawString(575, w-30, "TELÈFON")
			c.drawString(650, w-30, "DATA NAIXEMENT")
			c.line(0, w-35, h, w-35)
			bd=BaseDeDades('falla.db')
			for id in llistat_ids_baixes:
				faller=bd.llegir_faller(id)
				c.drawString(20, w-i-60, str(id))
				c.drawString(50, w-i-60, faller.cognoms + ", " + faller.nom)
				c.drawString(250, w-i-60, faller.dni)
				c.drawString(325, w-i-60, faller.adresa)
				c.drawString(575, w-i-60, faller.telefon)
				c.drawString(650, w-i-60, faller.naixement)
				i=i+20
				if i==500: # Quan arribem a 25 fallers canviem de pàgina.
					pagina=pagina+1
					c.drawString(20, 20, "baixes")
					c.drawString((h/2)-30, 20, "pàgina "+str(pagina))
					c.drawString(h-80, 20, data_actual)
					c.showPage() # Mostrem la pàgina feta.
					c.drawString(20, w-30, "ID") # Primera línea de la següent pàgina.
					c.drawString(50, w-30, "FALLER")
					c.drawString(250, w-30, "DNI")
					c.drawString(325, w-30, "ADREÇA")
					c.drawString(575, w-30, "TELÈFON")
					c.drawString(650, w-30, "DATA NAIXEMENT")
					c.line(0, w-35, h, w-35)
					i=0
			pagina=pagina+1
			c.drawString(20, 20, "baixes")
			c.drawString((h/2)-30, 20, "pàgina "+str(pagina))
			c.drawString(h-80, 20, data_actual)
			c.showPage() # Última pàgina.
			i=0
			c.drawString(20, w-30, "ID") # La w és el segon parámetre ja que està en horitzontal.
			c.drawString(50, w-30, "FALLER")
			c.drawString(250, w-30, "DNI")
			c.drawString(325, w-30, "ADREÇA")
			c.drawString(575, w-30, "TELÈFON")
			c.drawString(650, w-30, "DATA NAIXEMENT")
			c.line(0, w-35, h, w-35)
			for id in llistat_ids_altes:
				faller=bd.llegir_faller(id)
				c.drawString(20, w-i-60, str(id))
				c.drawString(50, w-i-60, faller.cognoms + ", " + faller.nom)
				c.drawString(250, w-i-60, faller.dni)
				c.drawString(325, w-i-60, faller.adresa)
				c.drawString(575, w-i-60, faller.telefon)
				c.drawString(650, w-i-60, faller.naixement)
				i=i+20
				if i==500: # Quan arribem a 25 fallers canviem de pàgina.
					pagina=pagina+1
					c.drawString(20, 20, "altes")
					c.drawString((h/2)-30, 20, "pàgina "+str(pagina))
					c.drawString(h-80, 20, data_actual)
					c.showPage() # Mostrem la pàgina feta.
					c.drawString(20, w-30, "ID") # Primera línea de la següent pàgina.
					c.drawString(50, w-30, "FALLER")
					c.drawString(250, w-30, "DNI")
					c.drawString(325, w-30, "ADREÇA")
					c.drawString(575, w-30, "TELÈFON")
					c.drawString(650, w-30, "DATA NAIXEMENT")
					c.line(0, w-35, h, w-35)
					i=0
			pagina=pagina+1
			c.drawString(20, 20, "altes")
			c.drawString((h/2)-30, 20, "pàgina "+str(pagina))
			c.drawString(h-80, 20, data_actual)
			c.showPage() # Última pàgina.
			c.save()
			# Entrem a la carpeta "altes i baixes" per a obrir l'arxiu pdf i tornem a la ruta original.
			ruta=os.getcwd()
			os.chdir("altes i baixes")
			os.startfile(str(data_actual)+".pdf")
			os.chdir(ruta)


	def llistat_fallers_amb_rifa(self):
		'''
		Crea un .pdf amb un llistat dels fallers amb obligació de rifa.
		'''
		# Traguem la data actual per a utilitzar-la a l'informe.
		utils=Utils()
		data=utils.calcular_data_actual()
		data_actual=data[0] + "-" + data[1] + "-" + data[2]
		bd=BaseDeDades('falla.db')
		llistat_fallers=bd.llegir_fallers_adults()
		pagina=0
		# Intentem crear la carpeta "llistat rifes" si no està creada.
		try:
			os.mkdir("llistat rifes")
		except OSError as e:
			if e.errno!=errno.EEXIST:
				raise
		arxiu="llistat rifes"+"/"+str(data_actual)
		# Creem el full i tot el contingut.
		w,h=A4
		c=canvas.Canvas(arxiu+".pdf", pagesize=A4)
		c.drawString(20, h-30, "ID")
		c.drawString(50, h-30, "FALLER")
		c.drawString(300, h-30, "ID")
		c.drawString(330, h-30, "FALLER")
		c.line(0, h-35, w, h-35)
		fila=0
		columna=0
		for faller in llistat_fallers:
			if fila<35 and columna==0:
				c.drawString(20, h-(fila*20)-60, str(faller.id))
				c.drawString(50, h-(fila*20)-60, faller.cognoms + ", " + faller.nom)
				fila=fila+1
			elif fila==35 and columna==0:
				columna=1
				fila=0
			elif fila<35 and columna==1:
				c.drawString(300, h-(fila*20)-60, str(faller.id))
				c.drawString(330, h-(fila*20)-60, faller.cognoms + ", " + faller.nom)
				fila=fila+1
			elif fila==35 and columna==1: # Quan arribem a 70 fallers canviem de pàgina
				pagina=pagina+1
				c.drawString(20, 20, "llistat rifes")
				c.drawString((w/2)-30, 20, "pàgina "+str(pagina))
				c.drawString(w-80, 20, data_actual)
				c.showPage() # Mostrem la pàgina feta.
				c.drawString(20, h-30, "ID") # Primera línea de la següent pàgina.
				c.drawString(50, h-30, "FALLER")
				c.drawString(300, h-30, "ID")
				c.drawString(330, h-30, "FALLER")
				c.line(0, h-35, w, h-35)
				columna=0
				fila=0
		pagina=pagina+1
		c.drawString(20, 20, "llistat rifes")
		c.drawString((w/2)-30, 20, "pàgina "+str(pagina))
		c.drawString(w-80, 20, data_actual)
		c.showPage() # Última pàgina.
		c.save()
		# Entrem a la carpeta llistat rifes per a obrir l'arxiu pdf i tornem a la ruta original.
		ruta=os.getcwd()
		os.chdir("llistat rifes")
		os.startfile(str(data_actual)+".pdf")
		os.chdir(ruta)
		

	def llistat_fallers(self, llistat_dades):
		'''
		Crea un .pdf amb el llistat de dades dels fallers actius.
		'''
		# Traguem la data actual per a utilitzar-la a l'informe.
		utils=Utils()
		data=utils.calcular_data_actual()
		data_actual=data[0] + "-" + data[1] + "-" + data[2]
		bd=BaseDeDades('falla.db')
		llistat_fallers=bd.llegir_fallers_per_alta(1)
		pagina=0
		# Intentem crear la carpeta "llistat fallers" si no està creada.
		try:
			os.mkdir("llistat fallers")
		except OSError as e:
			if e.errno!=errno.EEXIST:
				raise
		arxiu="llistat fallers"+"/"+str(data_actual)
		# Creem el full i tot el contingut.
		w,h=A4
		c=canvas.Canvas(arxiu+".pdf", pagesize=landscape(A4)) # El creem en horitzontal.
		i=0
		j=20
		c.drawString(j, w-30, "ID") # La w és el segon parámetre ja que està en horitzontal.
		j=j+30
		if "nom" in llistat_dades:
			c.drawString(j, w-30, "FALLER")
			j=j+200
		if "dni" in llistat_dades:
			c.drawString(j, w-30, "DNI")
			j=j+75
		if "adreça" in llistat_dades:
			c.drawString(j, w-30, "ADREÇA")
			j=j+250
		if "telefon" in llistat_dades:
			c.drawString(j, w-30, "TELÈFON")
			j=j+75
		if "naixement" in llistat_dades:
			c.drawString(j, w-30, "NAIXEMENT")
			j=j+75
		if "correu" in llistat_dades:
			c.drawString(j, w-30, "E-MAIL")
		c.line(0, w-35, h, w-35)
		for faller in llistat_fallers:
			j=20
			c.drawString(j, w-i-60, str(faller.id))
			j=j+30
			if "nom" in llistat_dades:
				c.drawString(j, w-i-60, faller.cognoms + ", " + faller.nom)
				j=j+200
			if "dni" in llistat_dades:
				c.drawString(j, w-i-60, faller.dni)
				j=j+75
			if "adreça" in llistat_dades:
				c.drawString(j, w-i-60, faller.adresa)
				j=j+250
			if "telefon" in llistat_dades:
				c.drawString(j, w-i-60, faller.telefon)
				j=j+75
			if "naixement" in llistat_dades:
				c.drawString(j, w-i-60, faller.naixement)
				j=j+75
			if "correu" in llistat_dades:
				c.drawString(j, w-i-60, faller.correu)
			i=i+20
			if i==500: # Quan arribem a 25 fallers canviem de pàgina.
				pagina=pagina+1
				c.drawString(20, 20, "llistat de fallers")
				c.drawString((h/2)-30, 20, "pàgina "+str(pagina))
				c.drawString(h-80, 20, data_actual)
				c.showPage() # Mostrem la pàgina feta.
				# Primera línea de la següent pàgina.
				j=20
				c.drawString(j, w-30, "ID") # La w és el segon parámetre ja que està en horitzontal.
				j=j+30
				if "nom" in llistat_dades:
					c.drawString(j, w-30, "FALLER")
					j=j+200
				if "dni" in llistat_dades:
					c.drawString(j, w-30, "DNI")
					j=j+75
				if "adreça" in llistat_dades:
					c.drawString(j, w-30, "ADREÇA")
					j=j+250
				if "telefon" in llistat_dades:
					c.drawString(j, w-30, "TELÈFON")
					j=j+75
				if "naixement" in llistat_dades:
					c.drawString(j, w-30, "NAIXEMENT")
					j=j+75
				if "correu" in llistat_dades:
					c.drawString(j, w-30, "E-MAIL")
				c.line(0, w-35, h, w-35)
				i=0
		pagina=pagina+1
		c.drawString(20, 20, "llistat de fallers")
		c.drawString((h/2)-30, 20, "pàgina "+str(pagina))
		c.drawString(h-80, 20, data_actual)
		c.showPage() # Última pàgina.
		c.save()
		# Entrem a la carpeta "llistat fallers" per a obrir l'arxiu pdf i tornem a la ruta original.
		ruta=os.getcwd()
		os.chdir("llistat fallers")
		os.startfile(str(data_actual)+".pdf")
		os.chdir(ruta)


	def llistat_fallers_per_categories(self, llistat_categories, llistat_dades):
		'''
		Crea un .pdf amb el llistat de dades dels fallers actius de les categories passades.

		Paràmetres:
		-----------
		llistat_categories : llista.
			Llistat de categories per a les quals volem treure el llistat.
		'''
		# Traguem la data actual per a utilitzar-la a l'informe.
		utils=Utils()
		data=utils.calcular_data_actual()
		data_actual=data[0] + "-" + data[1] + "-" + data[2]
		bd=BaseDeDades('falla.db')
		llistat_fallers=[]
		for categoria in llistat_categories:
			llistat_fallers.extend(bd.llegir_fallers_per_categoria(categoria))
		llistat_fallers=sorted(llistat_fallers, key=lambda faller:faller.cognoms)
		pagina=0
		# Intentem crear la carpeta "llistat fallers" si no està creada.
		try:
			os.mkdir("llistat fallers")
		except OSError as e:
			if e.errno!=errno.EEXIST:
				raise
		arxiu="llistat fallers"+"/"+"categories " + str(data_actual)
		# Creem el full i tot el contingut.
		w,h=A4
		c=canvas.Canvas(arxiu+".pdf", pagesize=landscape(A4)) # El creem en horitzontal.
		i=0
		j=20
		c.drawString(j, w-30, "ID") # La w és el segon parámetre ja que està en horitzontal.
		j=j+30
		if "nom" in llistat_dades:
			c.drawString(j, w-30, "FALLER")
			j=j+200
		if "dni" in llistat_dades:
			c.drawString(j, w-30, "DNI")
			j=j+75
		if "adreça" in llistat_dades:
			c.drawString(j, w-30, "ADREÇA")
			j=j+250
		if "telefon" in llistat_dades:
			c.drawString(j, w-30, "TELÈFON")
			j=j+75
		if "naixement" in llistat_dades:
			c.drawString(j, w-30, "NAIXEMENT")
			j=j+75
		if "correu" in llistat_dades:
			c.drawString(j, w-30, "E-MAIL")
		c.line(0, w-35, h, w-35)
		for faller in llistat_fallers:
			j=20
			c.drawString(j, w-i-60, str(faller.id))
			j=j+30
			if "nom" in llistat_dades:
				c.drawString(j, w-i-60, faller.cognoms + ", " + faller.nom)
				j=j+200
			if "dni" in llistat_dades:
				c.drawString(j, w-i-60, faller.dni)
				j=j+75
			if "adreça" in llistat_dades:
				c.drawString(j, w-i-60, faller.adresa)
				j=j+250
			if "telefon" in llistat_dades:
				c.drawString(j, w-i-60, faller.telefon)
				j=j+75
			if "naixement" in llistat_dades:
				c.drawString(j, w-i-60, faller.naixement)
				j=j+75
			if "correu" in llistat_dades:
				c.drawString(j, w-i-60, faller.correu)
			i=i+20
			if i==500: # Quan arribem a 25 fallers canviem de pàgina.
				pagina=pagina+1
				c.drawString(20, 20, "llistat de fallers per categories")
				c.drawString((h/2)-30, 20, "pàgina "+str(pagina))
				c.drawString(h-80, 20, data_actual)
				c.showPage() # Mostrem la pàgina feta.
				# Primera línea de la següent pàgina.
				j=20
				c.drawString(j, w-30, "ID") # La w és el segon parámetre ja que està en horitzontal.
				j=j+30
				if "nom" in llistat_dades:
					c.drawString(j, w-30, "FALLER")
					j=j+200
				if "dni" in llistat_dades:
					c.drawString(j, w-30, "DNI")
					j=j+75
				if "adreça" in llistat_dades:
					c.drawString(j, w-30, "ADREÇA")
					j=j+250
				if "telefon" in llistat_dades:
					c.drawString(j, w-30, "TELÈFON")
					j=j+75
				if "naixement" in llistat_dades:
					c.drawString(j, w-30, "NAIXEMENT")
					j=j+75
				if "correu" in llistat_dades:
					c.drawString(j, w-30, "E-MAIL")
				c.line(0, w-35, h, w-35)
				i=0
		pagina=pagina+1
		c.drawString(20, 20, "llistat de fallers per categories")
		c.drawString((h/2)-30, 20, "pàgina "+str(pagina))
		c.drawString(h-80, 20, data_actual)
		c.showPage() # Última pàgina.
		c.save()
		# Entrem a la carpeta "llistat fallers" per a obrir l'arxiu pdf i tornem a la ruta original.
		ruta=os.getcwd()
		os.chdir("llistat fallers")
		os.startfile("categories " + str(data_actual)+".pdf")
		os.chdir(ruta)


	def llistat_fallers_per_edat(self, edat_inicial, edat_final, llistat_dades):
		'''
		Crea un .pdf amb el llistat de dades dels fallers actius amb edats compreses
		entre els paràmetres d'entrada.

		Paràmetres:
		-----------
		edat_inicial : int.
			Mínima edat dels fallers del llistat.
		edat_final : int
			Màxima edat dels fallers del llistat.
		'''
		# Traguem la data actual per a utilitzar-la a l'informe.
		utils=Utils()
		data=utils.calcular_data_actual()
		data_actual=data[0] + "-" + data[1] + "-" + data[2]
		arxiu=Arxiu('exercici')
		exercici_actual=arxiu.llegir_exercici_actual()
		bd=BaseDeDades('falla.db')
		llistat_fallers=bd.llegir_fallers_per_alta(1)
		llistat_fallers_per_edat=[]
		for faller in llistat_fallers:
			edat=faller.calcular_edat(faller.naixement, exercici_actual)
			if (edat>=edat_inicial) and (edat<=edat_final):
				llistat_fallers_per_edat.append(faller)
		pagina=0
		# Intentem crear la carpeta "llistat fallers" si no està creada.
		try:
			os.mkdir("llistat fallers")
		except OSError as e:
			if e.errno!=errno.EEXIST:
				raise
		arxiu="llistat fallers"+"/"+"edat " + str(data_actual)
		# Creem el full i tot el contingut.
		w,h=A4
		c=canvas.Canvas(arxiu+".pdf", pagesize=landscape(A4)) # El creem en horitzontal.
		i=0
		j=20
		c.drawString(j, w-30, "ID") # La w és el segon parámetre ja que està en horitzontal.
		j=j+30
		if "nom" in llistat_dades:
			c.drawString(j, w-30, "FALLER")
			j=j+200
		if "dni" in llistat_dades:
			c.drawString(j, w-30, "DNI")
			j=j+75
		if "adreça" in llistat_dades:
			c.drawString(j, w-30, "ADREÇA")
			j=j+250
		if "telefon" in llistat_dades:
			c.drawString(j, w-30, "TELÈFON")
			j=j+75
		if "naixement" in llistat_dades:
			c.drawString(j, w-30, "NAIXEMENT")
			j=j+75
		if "correu" in llistat_dades:
			c.drawString(j, w-30, "E-MAIL")
		c.line(0, w-35, h, w-35)
		for faller in llistat_fallers_per_edat:
			j=20
			c.drawString(j, w-i-60, str(faller.id))
			j=j+30
			if "nom" in llistat_dades:
				c.drawString(j, w-i-60, faller.cognoms + ", " + faller.nom)
				j=j+200
			if "dni" in llistat_dades:
				c.drawString(j, w-i-60, faller.dni)
				j=j+75
			if "adreça" in llistat_dades:
				c.drawString(j, w-i-60, faller.adresa)
				j=j+250
			if "telefon" in llistat_dades:
				c.drawString(j, w-i-60, faller.telefon)
				j=j+75
			if "naixement" in llistat_dades:
				c.drawString(j, w-i-60, faller.naixement)
				j=j+75
			if "correu" in llistat_dades:
				c.drawString(j, w-i-60, faller.correu)
			i=i+20
			if i==500: # Quan arribem a 25 fallers canviem de pàgina.
				pagina=pagina+1
				c.drawString(20, 20, "llistat de fallers per edat")
				c.drawString((h/2)-30, 20, "pàgina "+str(pagina))
				c.drawString(h-80, 20, data_actual)
				c.showPage() # Mostrem la pàgina feta.
				# Primera línea de la següent pàgina.
				j=20
				c.drawString(j, w-30, "ID") # La w és el segon parámetre ja que està en horitzontal.
				j=j+30
				if "nom" in llistat_dades:
					c.drawString(j, w-30, "FALLER")
					j=j+200
				if "dni" in llistat_dades:
					c.drawString(j, w-30, "DNI")
					j=j+75
				if "adreça" in llistat_dades:
					c.drawString(j, w-30, "ADREÇA")
					j=j+250
				if "telefon" in llistat_dades:
					c.drawString(j, w-30, "TELÈFON")
					j=j+75
				if "naixement" in llistat_dades:
					c.drawString(j, w-30, "NAIXEMENT")
					j=j+75
				if "correu" in llistat_dades:
					c.drawString(j, w-30, "E-MAIL")
				c.line(0, w-35, h, w-35)
				i=0
		pagina=pagina+1
		c.drawString(20, 20, "llistat de fallers per edat")
		c.drawString((h/2)-30, 20, "pàgina "+str(pagina))
		c.drawString(h-80, 20, data_actual)
		c.showPage() # Última pàgina.
		c.save()
		# Entrem a la carpeta "llistat fallers" per a obrir l'arxiu pdf i tornem a la ruta original.
		ruta=os.getcwd()
		os.chdir("llistat fallers")
		os.startfile("edat " + str(data_actual)+".pdf")
		os.chdir(ruta)