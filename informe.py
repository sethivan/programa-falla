from datetime import date
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
import os
import errno
import os.path as path


class Informe():

	def __init__(self):

		pass


	def assignar_numero_rebut(self):

		#intentem crear la carpeta rebuts si no està creada
		try:
			os.mkdir("rebuts")
		except OSError as e:
			if e.errno!=errno.EEXIST:
				raise
		#asignem un nom d'arxiu amb un sumatori des de l'arxiu número 1
		pos=1
		arxiu="rebuts"+"/"+str(pos)
		while path.exists(arxiu+".pdf"):
			pos=pos+1
			arxiu="rebuts"+"/"+str(pos)
		return(pos)


	def crear_rebut(self, familiar, nom, pagquota, pagloteria, pagrifa, quota, quopag, loteria, lotpag, rifa, rifapag):

		#traguem la data actual per a utilitzar-la al rebut
		data=datetime.now()
		anyactual=datetime.strftime(data, '%Y')
		mesactual=datetime.strftime(data, '%m')
		diaactual=datetime.strftime(data, '%d')
		datafinal=diaactual + "-" + mesactual + "-" + anyactual
		#pagament total
		pagament=pagquota+pagloteria+pagrifa
		#pagaments per separat per concepte
		quodif=float(quota)-float(quopag)
		lotdif=float(loteria)-float(lotpag)
		rifadif=float(rifa)-float(rifapag)
		#asignacions totals i pagaments totals
		totalasig=float(quota)+float(loteria)+float(rifa)
		totalpag=float(quopag)+float(lotpag)+float(rifapag)
		total=quodif+lotdif+rifadif
		#intentem crear la carpeta rebuts si no està creada
		try:
			os.mkdir("rebuts")
		except OSError as e:
			if e.errno!=errno.EEXIST:
				raise
		#asignem un nom d'arxiu amb un sumatori des de l'arxiu número 1
		pos=1
		arxiu="rebuts"+"/"+str(pos)
		while path.exists(arxiu+".pdf"):
			pos=pos+1
			arxiu="rebuts"+"/"+str(pos)
		#creem el full i tot el contingut
		w,h=A4
		c=canvas.Canvas(arxiu+".pdf", pagesize=A4)
		c.line(0,h-(h/3),w,h-(h/3))
		c.line(0,h/3,w,h/3)
		c.drawString(w-100, h-30, datafinal)
		c.drawString(50, h-50, nom + " abona la quantitat de " + "{0:.2f}".format(pagament) + " €")
		c.drawString(70, h-80, "{0:.2f}".format(pagquota) + " € en concepte de quota")
		c.drawString(70, h-100, "{0:.2f}".format(pagloteria) + " € en concepte de loteria")
		c.drawString(70, h-120, "{0:.2f}".format(pagrifa) + " € en concepte de rifa")
		if familiar==0: #li passem per variable si ha fet el pagament individual o per bloc familiar
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
		c.drawString(130, h-200, quota + " €")
		c.drawString(200, h-200, quopag + " €")
		c.drawString(270, h-200, "{0:.2f}".format(quodif) + " €")
		c.drawString(55, h-220, "Loteria:")
		c.drawString(130, h-220, loteria + " €")
		c.drawString(200, h-220, lotpag + " €")
		c.drawString(270, h-220, "{0:.2f}".format(lotdif) + " €")
		c.drawString(55, h-240, "Rifa:")
		c.drawString(130, h-240, rifa + " €")
		c.drawString(200, h-240, rifapag + " €")
		c.drawString(270, h-240, "{0:.2f}".format(rifadif) + " €")
		c.drawString(55, h-260, "Totals:")
		c.drawString(130, h-260, "{0:.2f}".format(totalasig) + " €")
		c.drawString(200, h-260, "{0:.2f}".format(totalpag) + " €")
		c.drawString(270, h-260, "{0:.2f}".format(total) + " €")
		c.drawImage("escut.jpg", 360, h-260, height=150, width=200)
		c.showPage()
		c.save()
		#entrem a la carpeta rebuts per a obrir l'arxiu pdf i tornem a la ruta original
		ruta=os.getcwd()
		os.chdir("rebuts")
		os.startfile(str(pos)+".pdf")
		os.chdir(ruta)

'''
	def MovimentsDia(self):

		#traguem la data actual per a utilitzar-la a l'informe
		data=datetime.now()
		anyactual=datetime.strftime(data, '%Y')
		mesactual=datetime.strftime(data, '%m')
		diaactual=datetime.strftime(data, '%d')
		datafinal=diaactual + "-" + mesactual + "-" + anyactual
		elMoviment=Moviment()
		elMoviment.ExerciciActual()
		elFaller=Faller()
		pag=1
		#intentem crear la carpeta moviments dia si no està creada
		try:
			os.mkdir("moviments dia")
		except OSError as e:
			if e.errno!=errno.EEXIST:
				raise
		arxiu="moviments dia"+"/"+str(datafinal)
		#creem el full i tot el contingut
		w,h=A4
		c=canvas.Canvas(arxiu+".pdf", pagesize=A4)
		resmov=elMoviment.MovimentsDia() #recuperem els moviments
		i=0
		total=0
		c.drawString(50, h-30, "FALLER")
		c.drawString(300, h-30, "CONCEPTE")
		c.drawString(w-100, h-30, "QUANTITAT")
		for val in resmov: #distingim el concepte del moviment
			if val[3]==2: #tipo igual a pagament
				elFaller.BuscarFallerPerId(val[6])
				c.drawString(50, h-i-60, elFaller.nom + " " + elFaller.cognoms)
				if val[4]==1:
					concepte="quota"
				if val[4]==2:
					concepte="loteria"
				if val[4]==3:
					concepte="rifa"
				c.drawString(300, h-i-60, concepte)			
				c.drawString(w-100, h-i-60, "{0:.2f}".format(val[2]) + " €")
				i=i+20
				total=total+val[2]
			if i==500:
				pag=pag+1
				c.drawString(20, 20, "moviments del dia")
				c.drawString((w/2)-30, 20, "pàgina "+str(pag))
				c.drawString(w-80, 20, datafinal)
				c.showPage() #mostrem la pàgina feta
				c.drawString(50, h-30, "FALLER") #primera linea de la pàgina següent
				c.drawString(300, h-30, "CONCEPTE")
				c.drawString(w-100, h-30, "QUANTITAT")
				i=0
		c.drawString(300, h-i-80, "TOTAL")
		c.drawString(w-100, h-i-80, "{0:.2f}".format(total) + " €")
		c.drawString(20, 20, "moviments del dia")
		c.drawString((w/2)-30, 20, "pàgina "+str(pag))
		c.drawString(w-80, 20, datafinal)
		c.showPage()
		c.save()
		#entrem a la carpeta rebuts per a obrir l'arxiu pdf i tornem a la ruta original
		ruta=os.getcwd()
		os.chdir("moviments dia")
		os.startfile(str(datafinal)+".pdf")
		os.chdir(ruta)


	def LlistatGeneral(self):

		#traguem la data actual per a utilitzar-la a l'informe
		data=datetime.now()
		anyactual=datetime.strftime(data, '%Y')
		mesactual=datetime.strftime(data, '%m')
		diaactual=datetime.strftime(data, '%d')
		datafinal=diaactual + "-" + mesactual + "-" + anyactual
		elFaller=Faller()
		res=elFaller.BuscarFallerAlta(1)
		elMoviment=Moviment()
		elMoviment.ExerciciActual()
		laFamilia=Familia()
		sumquotafinal=0
		sumquotapagada=0
		sumloteriaasignada=0
		sumloteriapagada=0
		sumrifaasignada=0
		sumrifapagada=0
		pag=0
		#intentem crear la carpeta llistat general si no està creada
		try:
			os.mkdir("llistat general")
		except OSError as e:
			if e.errno!=errno.EEXIST:
				raise
		arxiu="llistat general"+"/"+str(datafinal)
		#creem el full i tot el contingut
		w,h=A4
		c=canvas.Canvas(arxiu+".pdf", pagesize=landscape(A4)) #el creem en horitzontal
		c.setFont("Helvetica", 11)
		i=0
		fallers=0 #per a acumular el total de fallers
		c.drawString(20, w-30, "ID") #la w és el segon parámetre ja que està en horitzontal
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
		for val in res:
			elMoviment.quotaasignada=0 #resetejem a cada iteració per a que no s'acumulen
			elMoviment.quotapagada=0
			elMoviment.loteriaasignada=0
			elMoviment.loteriapagada=0
			elMoviment.rifaasignada=0
			elMoviment.rifapagada=0
			c.drawString(20, w-i-60, str(val[0]))
			c.drawString(50, w-i-60, val[2] + ", " + val[1])
			elFaller.BuscarQuotaFaller(val[0]) #busquem la quota corresponent al faller
			laFamilia.BuscarDescompteFamilia(val[0]) #busquem el descompte familiar del faller
			elMoviment.BuscarMoviments(val[0],str(elMoviment.exercici)) #busquem tots els moviments
			quotafinal=elFaller.quota-(laFamilia.descompte*elFaller.quota/100)+elMoviment.quotaasignada
			totalasig=quotafinal+elMoviment.loteriaasignada+elMoviment.rifaasignada
			totalpag=elMoviment.quotapagada+elMoviment.loteriapagada+elMoviment.rifapagada
			c.drawRightString(295, w-i-60, "{0:.2f}".format(quotafinal) + " €")
			sumquotafinal=sumquotafinal+quotafinal
			c.drawRightString(365, w-i-60, "{0:.2f}".format(elMoviment.quotapagada) + " €")
			sumquotapagada=sumquotapagada+elMoviment.quotapagada
			c.drawRightString(435, w-i-60, "{0:.2f}".format(elMoviment.loteriaasignada) + " €")
			sumloteriaasignada=sumloteriaasignada+elMoviment.loteriaasignada
			c.drawRightString(505, w-i-60, "{0:.2f}".format(elMoviment.loteriapagada) + " €")
			sumloteriapagada=sumloteriapagada+elMoviment.loteriapagada
			c.drawRightString(565, w-i-60, "{0:.2f}".format(elMoviment.rifaasignada) + " €")
			sumrifaasignada=sumrifaasignada+elMoviment.rifaasignada
			c.drawRightString(625, w-i-60, "{0:.2f}".format(elMoviment.rifapagada) + " €")
			sumrifapagada=sumrifapagada+elMoviment.rifapagada
			c.drawRightString(695, w-i-60, "{0:.2f}".format(totalasig) + " €")
			c.drawRightString(765, w-i-60, "{0:.2f}".format(totalpag) + " €")
			c.drawRightString(835, w-i-60, "{0:.2f}".format(totalasig-totalpag) + " €")
			i=i+20
			fallers=fallers+1
			if i==500: #quan arribem a 25 fallers canviem de pàgina
				pag=pag+1
				c.drawString(20, 20, "llistat general")
				c.drawString((h/2)-30, 20, "pàgina "+str(pag))
				c.drawString(h-80, 20, datafinal)
				c.showPage() #mostrem la pàgina feta
				c.setFont("Helvetica", 11)
				c.drawString(20, w-30, "ID") #primera línea de la següent pàgina
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
		c.drawRightString(295,w-i-80, "{0:.2f}".format(sumquotafinal) + " €")
		c.drawRightString(365,w-i-80, "{0:.2f}".format(sumquotapagada) + " €")
		c.drawRightString(435,w-i-80, "{0:.2f}".format(sumloteriaasignada) + " €")
		c.drawRightString(505,w-i-80, "{0:.2f}".format(sumloteriapagada) + " €")
		c.drawRightString(565,w-i-80, "{0:.2f}".format(sumrifaasignada) + " €")
		c.drawRightString(625,w-i-80, "{0:.2f}".format(sumrifapagada) + " €")
		sumasignacions=sumquotafinal+sumloteriaasignada+sumrifaasignada
		c.drawRightString(695,w-i-80, "{0:.2f}".format(sumasignacions) + " €")
		sumpagats=sumquotapagada+sumloteriapagada+sumrifapagada
		c.drawRightString(765,w-i-80, "{0:.2f}".format(sumpagats) + " €")
		c.drawRightString(835,w-i-80, "{0:.2f}".format(sumasignacions-sumpagats) + " €")
		pag=pag+1
		c.drawString(20, 20, "llistat general")
		c.drawString((h/2)-30, 20, "pàgina "+str(pag))
		c.drawString(h-80, 20, datafinal)
		c.showPage() #última pàgina
		c.save()
		#entrem a la carpeta llistat general per a obrir l'arxiu pdf i tornem a la ruta original
		ruta=os.getcwd()
		os.chdir("llistat general")
		os.startfile(str(datafinal)+".pdf")
		os.chdir(ruta)
		

	def LlistatFallers(self):

		#traguem la data actual per a utilitzar-la a l'informe
		data=datetime.now()
		anyactual=datetime.strftime(data, '%Y')
		mesactual=datetime.strftime(data, '%m')
		diaactual=datetime.strftime(data, '%d')
		datafinal=diaactual + "-" + mesactual + "-" + anyactual
		elFaller=Faller()
		res=elFaller.BuscarFallerAlta(1)
		pag=0
		#intentem crear la carpeta llistat fallers si no està creada
		try:
			os.mkdir("llistat fallers")
		except OSError as e:
			if e.errno!=errno.EEXIST:
				raise
		arxiu="llistat fallers"+"/"+str(datafinal)
		#creem el full i tot el contingut
		w,h=A4
		c=canvas.Canvas(arxiu+".pdf", pagesize=landscape(A4)) #el creem en horitzontal
		i=0
		c.drawString(20, w-30, "ID") #la w és el segon parámetre ja que està en horitzontal
		c.drawString(50, w-30, "FALLER")
		c.drawString(250, w-30, "DNI")
		c.drawString(325, w-30, "ADREÇA")
		c.drawString(575, w-30, "TELÈFON")
		c.drawString(650, w-30, "DATA NAIXEMENT")
		c.line(0, w-35, h, w-35)
		for val in res:
			c.drawString(20, w-i-60, str(val[0]))
			c.drawString(50, w-i-60, val[2] + ", " + val[1])
			c.drawString(250, w-i-60, val[5])
			c.drawString(325, w-i-60, val[6])
			c.drawString(575, w-i-60, val[7])
			c.drawString(650, w-i-60, val[3])
			i=i+20
			if i==500: #quan arribem a 25 fallers canviem de pàgina
				pag=pag+1
				c.drawString(20, 20, "llistat de fallers")
				c.drawString((h/2)-30, 20, "pàgina "+str(pag))
				c.drawString(h-80, 20, datafinal)
				c.showPage() #mostrem la pàgina feta
				c.drawString(20, w-30, "ID") #primera línea de la següent pàgina
				c.drawString(50, w-30, "FALLER")
				c.drawString(250, w-30, "DNI")
				c.drawString(325, w-30, "ADREÇA")
				c.drawString(575, w-30, "TELÈFON")
				c.drawString(650, w-30, "DATA NAIXEMENT")
				c.line(0, w-35, h, w-35)
				i=0
		pag=pag+1
		c.drawString(20, 20, "llistat de fallers")
		c.drawString((h/2)-30, 20, "pàgina "+str(pag))
		c.drawString(h-80, 20, datafinal)
		c.showPage() #última pàgina
		c.save()
		#entrem a la carpeta llistat de fallers per a obrir l'arxiu pdf i tornem a la ruta original
		ruta=os.getcwd()
		os.chdir("llistat fallers")
		os.startfile(str(datafinal)+".pdf")
		os.chdir(ruta)


	def LlistatAltesBaixes(self):

		fitxer=open("resum 2022", "rb")
		res=pickle.load(fitxer)
		fitxer.close()
		del(fitxer)
		anterior=[]
		actual=[]
		for val in res:
			anterior.append(val[0])
		elFaller=Faller()
		res2=elFaller.BuscarFallerAlta(1)
		for val in res2:
			actual.append(val[0])
		baixes=set(anterior)-set(actual)
		altes=set(actual)-set(anterior)
		#traguem la data actual per a utilitzar-la a l'informe
		data=datetime.now()
		anyactual=datetime.strftime(data, '%Y')
		mesactual=datetime.strftime(data, '%m')
		diaactual=datetime.strftime(data, '%d')
		datafinal=diaactual + "-" + mesactual + "-" + anyactual
		pag=0
		#intentem crear la carpeta altes i baixes si no està creada
		try:
			os.mkdir("altes i baixes")
		except OSError as e:
			if e.errno!=errno.EEXIST:
				raise
		arxiu="altes i baixes"+"/"+str(datafinal)
		#creem el full i tot el contingut
		w,h=A4
		c=canvas.Canvas(arxiu+".pdf", pagesize=landscape(A4)) #el creem en horitzontal
		i=0
		c.drawString(20, w-30, "ID") #la w és el segon parámetre ja que està en horitzontal
		c.drawString(50, w-30, "FALLER")
		c.drawString(250, w-30, "DNI")
		c.drawString(325, w-30, "ADREÇA")
		c.drawString(575, w-30, "TELÈFON")
		c.drawString(650, w-30, "DATA NAIXEMENT")
		c.line(0, w-35, h, w-35)
		for val in baixes:
			elFaller.BuscarFallerPerId(val)
			c.drawString(20, w-i-60, str(val))
			c.drawString(50, w-i-60, elFaller.cognoms + ", " + elFaller.nom)
			c.drawString(250, w-i-60, elFaller.dni)
			c.drawString(325, w-i-60, elFaller.adresa)
			c.drawString(575, w-i-60, elFaller.telefon)
			c.drawString(650, w-i-60, elFaller.naixement)
			i=i+20
			if i==500: #quan arribem a 25 fallers canviem de pàgina
				pag=pag+1
				c.drawString(20, 20, "baixes")
				c.drawString((h/2)-30, 20, "pàgina "+str(pag))
				c.drawString(h-80, 20, datafinal)
				c.showPage() #mostrem la pàgina feta
				c.drawString(20, w-30, "ID") #primera línea de la següent pàgina
				c.drawString(50, w-30, "FALLER")
				c.drawString(250, w-30, "DNI")
				c.drawString(325, w-30, "ADREÇA")
				c.drawString(575, w-30, "TELÈFON")
				c.drawString(650, w-30, "DATA NAIXEMENT")
				c.line(0, w-35, h, w-35)
				i=0
		pag=pag+1
		c.drawString(20, 20, "baixes")
		c.drawString((h/2)-30, 20, "pàgina "+str(pag))
		c.drawString(h-80, 20, datafinal)
		c.showPage() #última pàgina
		i=0
		c.drawString(20, w-30, "ID") #la w és el segon parámetre ja que està en horitzontal
		c.drawString(50, w-30, "FALLER")
		c.drawString(250, w-30, "DNI")
		c.drawString(325, w-30, "ADREÇA")
		c.drawString(575, w-30, "TELÈFON")
		c.drawString(650, w-30, "DATA NAIXEMENT")
		c.line(0, w-35, h, w-35)
		for val in altes:
			elFaller.BuscarFallerPerId(val)
			c.drawString(20, w-i-60, str(val))
			c.drawString(50, w-i-60, elFaller.cognoms + ", " + elFaller.nom)
			c.drawString(250, w-i-60, elFaller.dni)
			c.drawString(325, w-i-60, elFaller.adresa)
			c.drawString(575, w-i-60, elFaller.telefon)
			c.drawString(650, w-i-60, elFaller.naixement)
			i=i+20
			if i==500: #quan arribem a 25 fallers canviem de pàgina
				pag=pag+1
				c.drawString(20, 20, "altes")
				c.drawString((h/2)-30, 20, "pàgina "+str(pag))
				c.drawString(h-80, 20, datafinal)
				c.showPage() #mostrem la pàgina feta
				c.drawString(20, w-30, "ID") #primera línea de la següent pàgina
				c.drawString(50, w-30, "FALLER")
				c.drawString(250, w-30, "DNI")
				c.drawString(325, w-30, "ADREÇA")
				c.drawString(575, w-30, "TELÈFON")
				c.drawString(650, w-30, "DATA NAIXEMENT")
				c.line(0, w-35, h, w-35)
				i=0
		pag=pag+1
		c.drawString(20, 20, "altes")
		c.drawString((h/2)-30, 20, "pàgina "+str(pag))
		c.drawString(h-80, 20, datafinal)
		c.showPage() #última pàgina
		c.save()
		#entrem a la carpeta llistat de fallers per a obrir l'arxiu pdf i tornem a la ruta original
		ruta=os.getcwd()
		os.chdir("altes i baixes")
		os.startfile(str(datafinal)+".pdf")
		os.chdir(ruta)


	def FallersAmbRifa(self):

		#traguem la data actual per a utilitzar-la a l'informe
		data=datetime.now()
		anyactual=datetime.strftime(data, '%Y')
		mesactual=datetime.strftime(data, '%m')
		diaactual=datetime.strftime(data, '%d')
		datafinal=diaactual + "-" + mesactual + "-" + anyactual
		elFaller=Faller()
		res=elFaller.BuscarFallerAmbRifa()
		pag=0
		#intentem crear la carpeta llistat fallers si no està creada
		try:
			os.mkdir("llistat rifes")
		except OSError as e:
			if e.errno!=errno.EEXIST:
				raise
		arxiu="llistat rifes"+"/"+str(datafinal)
		#creem el full i tot el contingut
		w,h=A4
		c=canvas.Canvas(arxiu+".pdf", pagesize=landscape(A4)) #el creem en horitzontal
		i=0
		c.drawString(20, w-30, "ID") #la w és el segon parámetre ja que està en horitzontal
		c.drawString(50, w-30, "FALLER")
		c.drawString(250, w-30, "DNI")
		c.drawString(325, w-30, "ADREÇA")
		c.drawString(575, w-30, "TELÈFON")
		c.drawString(650, w-30, "DATA NAIXEMENT")
		c.line(0, w-35, h, w-35)
		for val in res:
			c.drawString(20, w-i-60, str(val[0]))
			c.drawString(50, w-i-60, val[2] + ", " + val[1])
			c.drawString(250, w-i-60, val[5])
			c.drawString(325, w-i-60, val[6])
			c.drawString(575, w-i-60, val[7])
			c.drawString(650, w-i-60, val[3])
			i=i+20
			if i==500: #quan arribem a 25 fallers canviem de pàgina
				pag=pag+1
				c.drawString(20, 20, "llistat rifes")
				c.drawString((h/2)-30, 20, "pàgina "+str(pag))
				c.drawString(h-80, 20, datafinal)
				c.showPage() #mostrem la pàgina feta
				c.drawString(20, w-30, "ID") #primera línea de la següent pàgina
				c.drawString(50, w-30, "FALLER")
				c.drawString(250, w-30, "DNI")
				c.drawString(325, w-30, "ADREÇA")
				c.drawString(575, w-30, "TELÈFON")
				c.drawString(650, w-30, "DATA NAIXEMENT")
				c.line(0, w-35, h, w-35)
				i=0
		pag=pag+1
		c.drawString(20, 20, "llistat rifes")
		c.drawString((h/2)-30, 20, "pàgina "+str(pag))
		c.drawString(h-80, 20, datafinal)
		c.showPage() #última pàgina
		c.save()
		#entrem a la carpeta llistat de fallers per a obrir l'arxiu pdf i tornem a la ruta original
		ruta=os.getcwd()
		os.chdir("llistat rifes")
		os.startfile(str(datafinal)+".pdf")
		os.chdir(ruta)
		'''