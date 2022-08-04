import sqlite3


class Familia():

	def __init__(self):

		self.id=0
		self.descompte=0


	def BuscarDescompteFamilia(self, num):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		query_params=(num,)
		elCursor.execute("SELECT * FROM familia INNER JOIN faller ON familia.id=faller.idfamilia WHERE faller.id=?", query_params)
		resultat=elCursor.fetchall()
		for valors in resultat:
			self.descompte=valors[1]
		laConexio.commit()
		laConexio.close()


	def AsignarDescompteFamilia(self, num, desc):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		query_params=(desc,num)
		elCursor.execute("UPDATE familia SET descompte=? WHERE id=?", query_params)
		laConexio.commit()
		laConexio.close()


	def RecuperarUltimaFamilia(self):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		elCursor.execute("SELECT * FROM familia ORDER BY id DESC LIMIT 1")
		resultat=elCursor.fetchall()
		for valors in resultat:
			self.id=valors[0]
		laConexio.commit()
		laConexio.close()


	def InsertarFamilia(self):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		elCursor.execute("INSERT INTO familia VALUES (null,0,0)")
		laConexio.commit()
		laConexio.close()


	def BorrarFamilia(self, num):

		laConexio=sqlite3.connect("falla.db")
		elCursor=laConexio.cursor()
		query_params=(num,)
		elCursor.execute("DELETE FROM familia WHERE id=?", query_params)
		laConexio.commit()
		laConexio.close()