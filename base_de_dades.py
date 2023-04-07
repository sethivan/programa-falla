import sqlite3
from tkinter import messagebox

from faller import Faller
from familia import Familia
from moviment import Moviment
from categoria import Categoria

class BaseDeDades:
    
    def __init__(self, nom_db):
        self.conexio = sqlite3.connect(nom_db)
        self.cursor = self.conexio.cursor()


    def crear_taules(self):
        
        #taula faller
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Socio
                            (id INTEGER PRIMARY KEY,
                            nombre TEXT NOT NULL,
                            apellido TEXT NOT NULL,
                            fecha_nacimiento TEXT NOT NULL,
                            dni TEXT NOT NULL,
                            alta INTEGER NOT NULL,
                            id_familia INTEGER NOT NULL,
                            id_categoria INTEGER NOT NULL,
                            FOREIGN KEY (id_familia) REFERENCES Familia(id),
                            FOREIGN KEY (id_categoria) REFERENCES Categoria(id))''')

        #taula familia
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Familia
                            (id INTEGER PRIMARY KEY,
                            descuento REAL NOT NULL)''')

        #taula categoria
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Categoria
                            (id INTEGER PRIMARY KEY,
                            cuota REAL NOT NULL,
                            descripcion TEXT NOT NULL)''')

        #taula moviments
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Movimientos
                            (id INTEGER PRIMARY KEY,
                            fecha TEXT NOT NULL,
                            cantidad REAL NOT NULL,
                            tipo TEXT NOT NULL,
                            concepto TEXT NOT NULL,
                            id_socio INTEGER NOT NULL,
                            FOREIGN KEY (id_socio) REFERENCES Socio(id))''')

        self.conexion.commit()
    

    def tancar_conexio(self):

        self.conexio.close()


    #mètodes per a operacions CRUD en la taula faller

    def crear_faller(self, faller):

        dades=faller.nom, faller.cognoms, faller.naixement, faller.sexe, faller.dni, faller.adresa, faller.telefon, faller.alta, faller.familia.id, faller.categoria.id, faller.correu
        try:
            self.cursor.execute("INSERT INTO faller VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (dades))
        except sqlite3.Error:
            messagebox.showerror("Error", "Hi ha un problema amb la base de dades al crear el faller")
        else:
            self.conexio.commit()





    def llegir_faller(self, id):
        try:
            self.cursor.execute("SELECT * FROM faller WHERE id=?", (id,))
            resultat = self.cursor.fetchone()
            if resultat is not None:
                # Crear objecte Faller a partir de la fila obtinguda a la base de dades
                familia=self.llegir_familia(resultat[9])
                categoria=self.llegir_categoria(resultat[10])
                faller = Faller(resultat[0], resultat[1], resultat[2], resultat[3], resultat[4], resultat[5], resultat[6], resultat[7], resultat[8], resultat[11], familia, categoria)
                return faller
            else:
                return None
        except (sqlite3.Error, TypeError, ValueError) as e:
            print("Error al leer el socio de la base de datos:", e)
            return None
        

    def llegir_ultim_faller(self):

        try:
            self.cursor.execute("SELECT * FROM faller ORDER BY id DESC LIMIT 1")
            resultat = self.cursor.fetchone()
            if resultat is not None:
                # Crear objecte Faller a partir de la fila obtinguda a la base de dades
                familia=self.llegir_familia(resultat[9])
                categoria=self.llegir_categoria(resultat[10])
                faller = Faller(resultat[0], resultat[1], resultat[2], resultat[3], resultat[4], resultat[5], resultat[6], resultat[7], resultat[8], resultat[11], familia, categoria)
                return faller
            else:
                return None
        except (sqlite3.Error, TypeError, ValueError) as e:
            print("Error al leer el socio de la base de datos:", e)
            return None


    def llegir_fallers_adults(self):

        try:
            self.cursor.execute("SELECT * FROM faller WHERE alta=1 and (idcategoria=1 or idcategoria=2) ORDER BY cognoms")
            resultat = self.cursor.fetchall()
            llistat_fallers=[]
            for valors in resultat:
                familia=self.llegir_familia(valors[9])
                categoria=self.llegir_categoria(valors[10])
                faller = Faller(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[6], valors[7], valors[8], valors[11], familia, categoria)
                llistat_fallers.append(faller)
            return llistat_fallers
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
            return None
        except ConnectionError as e:
            messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
            return None
        
        
    def llegir_fallers_per_cognom(self, cadena):
        
        valor="%" + cadena + "%"
        query_params=(valor,)
        try:
            self.cursor.execute("SELECT * FROM faller WHERE cognoms LIKE ?", query_params)
            resultat = self.cursor.fetchall()
            llistat_fallers=[]
            for valors in resultat:
                familia=self.llegir_familia(valors[9])
                categoria=self.llegir_categoria(valors[10])
                faller = Faller(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[6], valors[7], valors[8], valors[11], familia, categoria)
                llistat_fallers.append(faller)
            return llistat_fallers
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
            return None
        except ConnectionError as e:
            messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
            return None
        
   
    def llegir_fallers_per_familia(self, id_familia):
        
        query_params=(id_familia,)
        try:
            self.cursor.execute("SELECT * FROM faller WHERE idfamilia=?", query_params)
            resultat = self.cursor.fetchall()
            llistat_fallers=[]
            for valors in resultat:
                familia=self.llegir_familia(valors[9])
                categoria=self.llegir_categoria(valors[10])
                faller = Faller(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[6], valors[7], valors[8], valors[11], familia, categoria)
                llistat_fallers.append(faller)
            return llistat_fallers
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
            return None
        except ConnectionError as e:
            messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
            return None
        

    def llegir_quota_faller(self, id):

        query_params=(id,)
        self.cursor.execute("SELECT * FROM categoria INNER JOIN faller ON categoria.id=faller.idcategoria WHERE faller.id=?", query_params)
        resultat=self.cursor.fetchall()
        for valors in resultat:
            return valors[1]


    def actualitzar_faller(self, faller):

        query_params=(faller.nom, faller.cognoms, faller.naixement, faller.sexe, faller.dni, faller.adresa, faller.telefon, faller.alta, faller.familia.id, faller.categoria.id, faller.correu, faller.id,)
        try:
            self.cursor.execute("UPDATE faller SET nom=?, cognoms=?, naixement=?, sexe=?, dni=?, adresa=?, telefon=?, alta=?, id_familia=?, id_categoria=?, correu=? WHERE id=?", query_params)
        except sqlite3.Error:
            messagebox.showerror("Error", "Hi ha un problema amb la base de dades")
        else:
            self.conexio.commit()

    
    
    def eliminar_socio(self, id):
        self.cursor.execute("DELETE FROM Socio WHERE id=?", (id,))
        self.conexion.commit()




    #mètodes per a operacions CRUD en la taula familia

    def crear_familia(self, familia):

        dades=familia.descompte, familia.domiciliacio
        try:
            self.cursor.execute("INSERT INTO familia VALUES (null, ?, ?)", (dades))
        except sqlite3.Error:
            messagebox.showerror("Error", "Hi ha un problema amb la base de dades")
        else:
            self.conexio.commit()


    def llegir_familia(self, id):
    
        query_params=(id,)
        try:
            self.cursor.execute("SELECT * FROM familia WHERE id=?", query_params)
            resultat = self.cursor.fetchone()
            if resultat is not None:
                familia = Familia(resultat[0], resultat[1], resultat[2])
                return familia
            else:
                return None
        except (sqlite3.Error, TypeError, ValueError) as e:
            print("Error al llegir la familia de la base de dades:", e)
            return None
        
    
    def llegir_ultima_familia(self):

        try:
            self.cursor.execute("SELECT * FROM familia ORDER BY id DESC LIMIT 1")
            resultat = self.cursor.fetchone()
            if resultat is not None:
                familia = Familia(resultat[0], resultat[1], resultat[2])
                return familia
            else:
                return None
        except (sqlite3.Error, TypeError, ValueError) as e:
            print("Error al llegir la familia de la base de dades:", e)
            return None
        
        
    def actualitzar_familia(self, familia):

        query_params=(familia.descompte, familia.domiciliacio, familia.id,)
        try:
            self.cursor.execute("UPDATE familia SET descompte=?, domiciliacio=? WHERE id=?", query_params)
        except sqlite3.Error:
            messagebox.showerror("Error", "Hi ha un problema amb la base de dades")
        else:
            self.conexio.commit()


    

    #def BuscarDescompteFamilia(self, num):

		#laConexio=sqlite3.connect("falla.db")
		#elCursor=laConexio.cursor()
		#query_params=(num,)
		#elCursor.execute("SELECT * FROM familia INNER JOIN faller ON familia.id=faller.idfamilia WHERE faller.id=?", query_params)
		#resultat=elCursor.fetchall()
		#for valors in resultat:
			#self.descompte=valors[1]
		#laConexio.commit()
		#laConexio.close()

        
    
    #mètodes per a operacions CRUD en la taula moviment

    def crear_moviment(self, moviment):

        dades=moviment.data, moviment.quantitat, moviment.tipo, moviment.concepte, moviment.exercici, moviment.faller.id, moviment.descripcio, 0
        self.cursor.execute("INSERT INTO moviment VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?)",(dades))
        self.conexio.commit()
    

    def llegir_moviments(self, id, exercici):
    
        query_params=(id, exercici,)
        try:
            self.cursor.execute("SELECT * FROM moviment WHERE idfaller=? and exercici=?", query_params)
            resultat = self.cursor.fetchall()
            llistat_moviments=[]
            for valors in resultat:
                faller=self.llegir_faller(valors[6])
                moviment=Moviment(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[7], valors[8], faller)
                llistat_moviments.append(moviment)
            return llistat_moviments
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
            return None
        except ConnectionError as e:
            messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
            return None
        

    #mètodes per a operacions CRUD en la taula categoria
        
    def llegir_categoria(self, id):

        query_params=(id,)
        try:
            self.cursor.execute("SELECT * FROM categoria WHERE id=?", query_params)
            resultat = self.cursor.fetchone()
            if resultat is not None:
                categoria = Categoria(resultat[0], resultat[1], resultat[2], resultat[3])
                return categoria
            else:
                return None
        except (sqlite3.Error, TypeError, ValueError) as e:
            print("Error al llegir la categoria de la base de dades:", e)
            return None

