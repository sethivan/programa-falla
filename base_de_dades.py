import sqlite3
from tkinter import messagebox
import traceback

from member import Member
from family import Family
from movement import Movement
from category import Category
from loteria import Loteria

class BaseDeDades:
    
    def __init__(self, nom_db):
        self.conexio = sqlite3.connect(nom_db)
        self.cursor = self.conexio.cursor()

    
    def import_categoria_from_sqlite(self):

        self.cursor.execute("SELECT * FROM CATEGORIA")
        result = self.cursor.fetchall()
        return result
    

    def import_familia_from_sqlite(self):

        self.cursor.execute("SELECT * FROM FAMILIA")
        result = self.cursor.fetchall()
        return result
    

    def import_faller_from_sqlite(self):

        self.cursor.execute("SELECT * FROM FALLER")
        result = self.cursor.fetchall()
        return result
    

    def import_moviment_from_sqlite(self):

        self.cursor.execute("SELECT * FROM MOVIMENT")
        result = self.cursor.fetchall()
        return result


    def crear_taules(self):
        '''
        Crea totes les taules necessàries per al correcte funcionament de la base de dades.
        '''
        # Taula faller.
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS faller
                            (id INTEGER PRIMARY KEY,
                            nom TEXT NOT NULL,
                            cognoms TEXT NOT NULL,
                            naixement TEXT NOT NULL,
                            sexe INTEGER NOT NULL,
                            dni TEXT,
                            adreça TEXT,
                            telefon TEXT,
                            alta INTEGER NOT NULL,
                            idfamilia INTEGER NOT NULL,
                            idcategoria INTEGER NOT NULL,
                            correu TEXT,
                            FOREIGN KEY (idfamilia) REFERENCES familia(id),
                            FOREIGN KEY (idcategoria) REFERENCES categoria(id))''')

        # Taula familia.
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS familia
                            (id INTEGER PRIMARY KEY,
                            descompte INTEGER NOT NULL,
                            domiciliacio INTEGER NOT NULL)''')

        # Taula categoria.
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS categoria
                            (id INTEGER PRIMARY KEY,
                            quota REAL NOT NULL,
                            nom TEXT NOT NULL,
                            descripcio TEXT NOT NULL)''')

        # Taula moviments.
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS moviments
                            (id INTEGER PRIMARY KEY,
                            data TEXT NOT NULL,
                            quantitat REAL NOT NULL,
                            tipo INTEGER NOT NULL,
                            concepte INTEGER NOT NULL,
                            exercici INTEGER NOT NULL,
                            idfaller INTEGER NOT NULL,
                            descripcio TEXT,
                            rebut INTEGER,
                            FOREIGN KEY (idfaller) REFERENCES faller(id))''')

        self.conexio.commit()
    

    def tancar_conexio(self):

        self.conexio.close()


    # Mètodes per a operacions CRUD en la taula faller.

    def crear_faller(self, faller):
        '''
        Escriu a la base de dades el faller que se li passa com a paràmetre a la taula "faller".

        Paràmetres:
        -----------
        faller : Faller
            Objecte de la classe Faller.
        '''
        dades=faller.nom, faller.cognoms, faller.naixement, faller.sexe, faller.dni, faller.adresa, faller.telefon, faller.alta, faller.familia.id, faller.category.id, faller.correu
        try:
            self.cursor.execute("INSERT INTO faller VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (dades))
        except sqlite3.Error:
            messagebox.showerror("Error", "Hi ha un problema amb la base de dades al crear el faller")
        else:
            self.conexio.commit()


    def llegir_faller(self, id):
        '''
        Llig de la taula "faller" aquell faller amb l'id que se li passa per paràmetre.

        Paràmetres:
        -----------
        id : integer
            Identificador del faller.

        Retorna:
        --------
        faller : Faller
            Objecte de la classe Faller complet amb els atributs "familia" i "category".
        '''
        query_params=(id,)
        try:
            self.cursor.execute("SELECT * FROM faller INNER JOIN familia ON faller.idfamilia = familia.id INNER JOIN categoria ON faller.idcategoria = categoria.id WHERE faller.id=?", query_params)
            resultat = self.cursor.fetchone()
            if resultat is not None:
                # Crear objecte Faller a partir de la fila obtinguda a la base de dades
                familia= Family(resultat[12], resultat[13], resultat[14])
                category= Category(resultat[15], resultat[16], resultat[17], resultat[18])
                faller = Member(resultat[0], resultat[1], resultat[2], resultat[3], resultat[4], resultat[5], resultat[6], resultat[7], resultat[8], resultat[11], familia, category)
                return faller
            else:
                return None
        except (sqlite3.Error, TypeError, ValueError) as e:
            print("Error al llegir el faller de la base de dades:", e)
            return None
        

    def llegir_ultim_faller(self):
        '''
        Llig l'últim registre de la taula "faller".

        Retorna:
        --------
        faller : Faller
            Objecte de la classe Faller.
        '''
        try:
            self.cursor.execute("SELECT * FROM faller INNER JOIN familia ON faller.idfamilia = familia.id INNER JOIN categoria ON faller.idcategoria = categoria.id ORDER BY faller.id DESC LIMIT 1")
            resultat = self.cursor.fetchone()
            if resultat is not None:
                # Crear objecte Faller a partir de la fila obtinguda a la base de dades
                familia= Family(resultat[12], resultat[13], resultat[14])
                categoria= Category(resultat[15], resultat[16], resultat[17], resultat[18])
                faller = Member(resultat[0], resultat[1], resultat[2], resultat[3], resultat[4], resultat[5], resultat[6], resultat[7], resultat[8], resultat[11], familia, categoria)
                return faller
            else:
                return None
        except (sqlite3.Error, TypeError, ValueError) as e:
            print("Error al llegir el faller de la base de dades:", e)
            return None

    
    def llegir_fallers(self):
        '''
        Llig de la taula "faller" tots els fallers
        i els afegeix a una llista d'objectes de la classe Faller.

        Retorna:
        --------
        llista_fallers : llista
            Llistat d'objectes de la classe Faller.
        '''
        try:
            self.cursor.execute("SELECT * FROM faller INNER JOIN familia ON faller.idfamilia = familia.id INNER JOIN categoria ON faller.idcategoria = categoria.id")
            resultat = self.cursor.fetchall()
            llistat_fallers=[]
            for valors in resultat:
                familia= Family(valors[12], valors[13], valors[14])
                categoria= Category(valors[15], valors[16], valors[17], valors[18])
                faller = Member(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[6], valors[7], valors[8], valors[11], familia, categoria)
                llistat_fallers.append(faller)
            return llistat_fallers
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
            return None
        except ConnectionError as e:
            messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
            return None
    
    
    def llegir_fallers_adults(self):
        '''
        Llig de la taula "faller" tots aquells fallers amb 14 anys o més (categories 1 i 2)
        i els afegeix a una llista d'objectes de la classe Faller.

        Retorna:
        --------
        llista_fallers : llista
            Llistat d'objectes de la classe Faller.
        '''
        try:
            self.cursor.execute("SELECT * FROM faller INNER JOIN familia ON faller.idfamilia = familia.id INNER JOIN categoria ON faller.idcategoria = categoria.id WHERE faller.alta=1 and (faller.idcategoria=1 or faller.idcategoria=2) ORDER BY faller.cognoms")
            resultat = self.cursor.fetchall()
            llistat_fallers=[]
            for valors in resultat:
                familia= Family(valors[12], valors[13], valors[14])
                categoria= Category(valors[15], valors[16], valors[17], valors[18])
                faller = Member(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[6], valors[7], valors[8], valors[11], familia, categoria)
                llistat_fallers.append(faller)
            return llistat_fallers
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
            return None
        except ConnectionError as e:
            messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
            return None
        
        
    def llegir_fallers_per_cognom(self, cadena):
        '''
        Llig de la taula "faller" tots aquells fallers amb un cognom que conté la cadena
        passada per paràmetre.

        Paràmetres:
        -----------
        cadena : string
            Cadena de caràcters a la que s'ha de pareixer el cognom dels fallers.

        Retorna:
        --------
        llistat_fallers : llista
            Llistat d'objectes de la classe Faller.
        '''
        valor="%" + cadena + "%"
        query_params=(valor,)
        try:
            self.cursor.execute("SELECT * FROM faller INNER JOIN familia ON faller.idfamilia = familia.id INNER JOIN categoria ON faller.idcategoria = categoria.id WHERE faller.cognoms LIKE ?", query_params)
            resultat = self.cursor.fetchall()
            llistat_fallers=[]
            for valors in resultat:
                familia= Family(valors[12], valors[13], valors[14])
                categoria= Category(valors[15], valors[16], valors[17], valors[18])
                faller = Member(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[6], valors[7], valors[8], valors[11], familia, categoria)
                llistat_fallers.append(faller)
            return llistat_fallers
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
            return None
        except ConnectionError as e:
            messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
            return None
        
   
    def llegir_fallers_per_familia(self, id_familia):
        '''
        Llig de la taula "faller" tots aquells fallers amb l'identificador de familia
        passat per paràmetre.

        Paràmetres:
        -----------
        id_familia : integer
            Identificador de la familia del faller.

        Retorna:
        --------
        llistat_fallers : llista
            Llistat d'objectes de la classe Faller.
        '''
        query_params=(id_familia,)
        try:
            self.cursor.execute("SELECT * FROM faller INNER JOIN familia ON faller.idfamilia = familia.id INNER JOIN categoria ON faller.idcategoria = categoria.id WHERE faller.idfamilia=?", query_params)
            resultat = self.cursor.fetchall()
            llistat_fallers=[]
            for valors in resultat:
                familia= Family(valors[12], valors[13], valors[14])
                categoria= Category(valors[15], valors[16], valors[17], valors[18])
                faller = Member(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[6], valors[7], valors[8], valors[11], familia, categoria)
                llistat_fallers.append(faller)
            return llistat_fallers
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
            return None
        except ConnectionError as e:
            messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
            return None
        

    def llegir_fallers_per_familia_i_alta(self, id_familia, alta):
        '''
        Llig de la taula "faller" tots aquells fallers amb l'identificador de familia
        passat per paràmetre.

        Paràmetres:
        -----------
        id_familia : integer
            Identificador de la familia del faller.
        alta : integer
            Identificador de l'estat d'alta del faller.

        Retorna:
        --------
        llistat_fallers : llista
            Llistat d'objectes de la classe Faller.
        '''
        dades=id_familia, alta
        try:
            self.cursor.execute("SELECT * FROM faller INNER JOIN familia ON faller.idfamilia = familia.id INNER JOIN categoria ON faller.idcategoria = categoria.id WHERE faller.idfamilia=? and faller.alta=?", (dades))
            resultat = self.cursor.fetchall()
            llistat_fallers=[]
            for valors in resultat:
                familia= Family(valors[12], valors[13], valors[14])
                categoria= Category(valors[15], valors[16], valors[17], valors[18])
                faller = Member(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[6], valors[7], valors[8], valors[11], familia, categoria)
                llistat_fallers.append(faller)
            return llistat_fallers
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
            return None
        except ConnectionError as e:
            messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
            return None
        
        
    def llegir_fallers_per_alta(self, alta):
        '''
        Llig de la taula "faller" tots aquells fallers amb l'estat d'alta del faller
        passat per paràmetre.

        Paràmetres:
        -----------
        alta : integer
            Identificador de l'estat d'alta del faller.

        Retorna:
        --------
        llistat_fallers : llista
            Llistat d'objectes de la classe Faller.
        '''
        query_params=(alta,)
        try:
            self.cursor.execute("SELECT * FROM faller INNER JOIN familia ON faller.idfamilia = familia.id INNER JOIN categoria ON faller.idcategoria = categoria.id WHERE faller.alta=? ORDER BY faller.cognoms", query_params)
            resultat = self.cursor.fetchall()
            llistat_fallers=[]
            for valors in resultat:
                familia= Family(valors[12], valors[13], valors[14])
                categoria= Category(valors[15], valors[16], valors[17], valors[18])
                faller = Member(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[6], valors[7], valors[8], valors[11], familia, categoria)
                llistat_fallers.append(faller)
            return llistat_fallers
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
            return None
        except ConnectionError as e:
            messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
            return None


    def llegir_fallers_per_categoria(self, categoria):
        '''
        Llig de la taula "faller" tots aquells fallers amb la categoria del faller
        passada per paràmetre.

        Paràmetres:
        -----------
        categoria : integer
            Identificador de la categoria del faller.

        Retorna:
        --------
        llistat_fallers : llista
            Llistat d'objectes de la classe Faller.
        '''
        query_params=(categoria,)
        try:
            self.cursor.execute("SELECT * FROM faller INNER JOIN familia ON faller.idfamilia = familia.id INNER JOIN categoria ON faller.idcategoria = categoria.id WHERE faller.alta=1 and faller.idcategoria=? ORDER BY faller.cognoms", query_params)
            resultat = self.cursor.fetchall()
            llistat_fallers=[]
            for valors in resultat:
                familia= Family(valors[12], valors[13], valors[14])
                categoria= Category(valors[15], valors[16], valors[17], valors[18])
                faller = Member(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[6], valors[7], valors[8], valors[11], familia, categoria)
                llistat_fallers.append(faller)
            return llistat_fallers
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
            return None
        except ConnectionError as e:
            messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
            return None
        

    def llegir_quota_faller(self, id):
        '''
        Llig de la taula "categoria" en combinació amb la taula "faller" la quota de la categoria a la que pertany el faller.

        Paràmetres:
        -----------
        id : integer
            Identificador del faller.

        Retorna:
        --------
        quota : integer
            Quota assignada al faller per la categoria a la que correspon.
        '''
        query_params=(id,)
        self.cursor.execute("SELECT * FROM categoria INNER JOIN faller ON categoria.id=faller.idcategoria WHERE faller.id=?", query_params)
        resultat=self.cursor.fetchone()
        quota=resultat[1]
        return quota


    def actualitzar_faller(self, faller):
        '''
        Actualitza la taula "faller" amb l'objecte de la classe Faller que se li passa per paràmetre.

        Paràmetres:
        -----------
        faller : Faller
            Objecte de la classe Faller.
        '''
        dades=faller.nom, faller.cognoms, faller.naixement, faller.sexe, faller.dni, faller.adresa, faller.telefon, faller.alta, faller.familia.id, faller.category.id, faller.correu, faller.id
        try:
            self.cursor.execute("UPDATE faller SET nom=?, cognoms=?, naixement=?, sexe=?, dni=?, adreça=?, telefon=?, alta=?, idfamilia=?, idcategoria=?, correu=? WHERE id=?", (dades))
        except sqlite3.Error as error:
            traceback.print_exc()
            messagebox.showerror("Error", "Hi ha un problema amb la base de dades")
        else:
            self.conexio.commit()


    # Mètodes per a operacions CRUD en la taula familia

    def crear_familia(self, familia):
        '''
        Escriu a la base de dades la familia que se li passa com a paràmetre a la taula "familia".

        Paràmetres:
        -----------
        familia : Familia
            Objecte de la classe Familia.
        '''
        dades=familia.descompte, familia.domiciliacio
        try:
            self.cursor.execute("INSERT INTO familia VALUES (null, ?, ?)", (dades))
        except sqlite3.Error:
            messagebox.showerror("Error", "Hi ha un problema amb la base de dades")
        else:
            self.conexio.commit()


    def llegir_familia(self, id):
        '''
        Llig de la taula "familia" aquella familia amb l'id que se li passa per paràmetre.

        Paràmetres:
        -----------
        id : integer
            Identificador de la familia.

        Retorna:
        --------
        familia : Familia
            Objecte de la classe Familia.
        '''
        query_params=(id,)
        try:
            self.cursor.execute("SELECT * FROM familia WHERE id=?", query_params)
            resultat = self.cursor.fetchone()
            if resultat is not None:
                familia = Family(resultat[0], resultat[1], resultat[2])
                return familia
            else:
                return None
        except (sqlite3.Error, TypeError, ValueError) as e:
            print("Error al llegir la familia de la base de dades:", e)
            return None

    
    def llegir_ultima_familia(self):
        '''
        Llig l'últim registre de la taula "familia".

        Retorna:
        --------
        familia : Family
            Objecte de la classe Familia.
        '''
        try:
            self.cursor.execute("SELECT * FROM familia ORDER BY id DESC LIMIT 1")
            resultat = self.cursor.fetchone()
            if resultat is not None:
                familia = Family(resultat[0], resultat[1], resultat[2])
                return familia
            else:
                return None
        except (sqlite3.Error, TypeError, ValueError) as e:
            print("Error al llegir la familia de la base de dades:", e)
            return None
        
    
    def llegir_families(self):
        '''
        Llig de la taula "familia" totes les families
        i les afegeix a una llista d'objectes de la classe Familia.

        Retorna:
        --------
        llista_families : llista
            Llistat d'objectes de la classe Familia.
        '''
        try:
            self.cursor.execute("SELECT * FROM familia")
            resultat = self.cursor.fetchall()
            llistat_families=[]
            for valors in resultat:
                familia= Family(valors[0], valors[1], valors[2])
                llistat_families.append(familia)
            return llistat_families
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
            return None
        except ConnectionError as e:
            messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
            return None
        
        
    def actualitzar_familia(self, familia):
        '''
        Actualitza la taula "familia" amb l'objecte de la classe Familia que se li passa per paràmetre.

        Paràmetres:
        -----------
        familia : Familia
            Objecte de la classe Familia.
        '''
        dades=familia.descompte, familia.domiciliacio, familia.id
        try:
            self.cursor.execute("UPDATE familia SET descompte=?, domiciliacio=? WHERE id=?", (dades))
        except sqlite3.Error:
            messagebox.showerror("Error", "Hi ha un problema amb la base de dades")
        else:
            self.conexio.commit()


    def eliminar_familia(self, id):
        '''
        Elimina de la base de dades la familia el id de la qual se li passa per paràmetre

        Paràmetres:
        -----------
        id : integer
            Identificador de la familia a eliminar.
        '''
        self.cursor.execute("DELETE FROM familia WHERE id=?", (id,))
        self.conexio.commit()
       
    
    # Mètodes per a operacions CRUD en la taula moviment.

    def crear_moviment(self, moviment):
        '''
        Escriu a la base de dades el moviment que se li passa com a paràmetre a la taula "moviment".

        Paràmetres:
        -----------
        moviment : Moviment
            Objecte de la classe Moviment.
        '''
        dades=moviment.data, moviment.quantitat, moviment.tipo, moviment.concepte, moviment.exercici, moviment.faller.id, moviment.descripcio, moviment.rebut
        self.cursor.execute("INSERT INTO moviment VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?)",(dades))
        self.conexio.commit()
    

    def llegir_moviments(self, id_faller, exercici):#REPASAAAAAAAAAAAAAAAAAAAR
        '''
        Llig de la taula "moviments" tots aquells moviments amb l'identificador de faller i l'exercici
        passats per paràmetre.

        Paràmetres:
        -----------
        id_faller : integer
            Identificador del faller.
        exercici : integer
            Exercici per al qual es volen recuperar les dades.

        Retorna:
        --------
        llistat_moviments : list
            Llistat d'objectes de la classe Moviment.
        '''
        query_params=(id_faller, exercici,)
        try:
            self.cursor.execute("SELECT * FROM moviment WHERE idfaller=? and exercici=?", query_params)
            resultat = self.cursor.fetchall()
            llistat_moviments=[]
            for valors in resultat:
                moviment=Movement(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[7], valors[8])
                llistat_moviments.append(moviment)
            return llistat_moviments
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
            return None
        except ConnectionError as e:
            messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
            return None
        

    def llegir_moviments_per_data_tipo(self, data, tipo):
        query_params=(data, tipo,)
        try:
            self.cursor.execute("SELECT * FROM moviment INNER JOIN faller ON moviment.idfaller=faller.id WHERE moviment.data=? and moviment.tipo=?", query_params)
            resultat=self.cursor.fetchall()
            llistat_moviments=[]
            for valors in resultat:
                faller=Member(valors[9], valors[10], valors[11], valors[12], valors[13], valors[14], valors[15], valors[16], valors[17], valors[18])
                moviment=Movement(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[7], valors[8], faller)
                llistat_moviments.append(moviment)
            return llistat_moviments
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
            return None
        except ConnectionError as e:
            messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
            return None
    
    
    def llegir_moviments_per_data_tipo_descripcio(self, data, tipo, descripcio):
        query_params=(data, tipo, descripcio)
        try:
            self.cursor.execute("SELECT * FROM moviment INNER JOIN faller ON moviment.idfaller=faller.id WHERE moviment.data=? and moviment.tipo=? and moviment.descripcio=?", query_params)
            resultat=self.cursor.fetchall()
            llistat_moviments=[]
            for valors in resultat:
                faller=Member(valors[9], valors[10], valors[11], valors[12], valors[13], valors[14], valors[15], valors[16], valors[17], valors[18])
                moviment=Movement(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[7], valors[8], faller)
                llistat_moviments.append(moviment)
            return llistat_moviments
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
            return None
        except ConnectionError as e:
            messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
            return None
        

    # Mètodes per a operacions CRUD en la taula categoria.
        
    def crear_categoria(self, categoria):
        '''
        Escriu a la base de dades la categoria que se li passa com a paràmetre a la taula "categoria".

        Paràmetres:
        -----------
        categoria : Categoria
            Objecte de la classe Categoria.
        '''
        dades=categoria.fee, categoria.name, categoria.description
        self.cursor.execute("INSERT INTO categoria VALUES (null, ?, ?, ?)",(dades))
        self.conexio.commit()
    
    
    
    def llegir_categoria(self, id):
        '''
        Llig de la taula "categoria" aquella categoria amb l'id que se li passa per paràmetre.

        Paràmetres:
        -----------
        id : integer
            Identificador de la categoria.

        Retorna:
        --------
        categoria : Categoria
            Objecte de la classe Categoria
        '''
        query_params=(id,)
        try:
            self.cursor.execute("SELECT * FROM categoria WHERE id=?", query_params)
            resultat = self.cursor.fetchone()
            if resultat is not None:
                categoria = Category(resultat[0], resultat[1], resultat[2], resultat[3])
                return categoria
            else:
                return None
        except (sqlite3.Error, TypeError, ValueError) as e:
            print("Error al llegir la categoria de la base de dades:", e)
            return None
        

    def actualitzar_categoria(self, categoria):
        '''
        Actualitza la taula "categoria" amb l'objecte de la classe Categoria que se li passa per paràmetre.

        Paràmetres:
        -----------
        categoria : Categoria
            Objecte de la classe Categoria.
        '''
        dades=categoria.fee, categoria.name, categoria.description, categoria.id
        try:
            self.cursor.execute("UPDATE categoria SET quota=?, nom=?, descripcio=? WHERE id=?", (dades))
        except sqlite3.Error:
            messagebox.showerror("Error", "Hi ha un problema amb la base de dades")
        else:
            self.conexio.commit()


    # Mètodes per a operacions CRUD en la taula loteria.

    def crear_loteria(self, loteria):
        '''
        Escriu a la base de dades la loteria que se li passa com a paràmetre a la taula "loteria".

        Paràmetres:
        -----------
        loteria : Loteria
            Objecte de la classe Loteria.
        '''
        dades=loteria.sorteig, loteria.data, loteria.paperetes_masculina, loteria.paperetes_femenina, loteria.paperetes_infantil, loteria.decims_masculina, loteria.decims_femenina, loteria.decims_infantil, loteria.assignada, loteria.faller.id
        self.cursor.execute("INSERT INTO categoria VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(dades))
        self.conexio.commit()

    def llegir_loteries_per_sorteig(self, sorteig):
        query_params=(sorteig,)
        try:
            self.cursor.execute("SELECT * FROM loteria INNER JOIN faller ON loteria.idfaller = faller.id WHERE loteria.sorteig=?", query_params)
            resultat = self.cursor.fetchall()
            llistat_loteries=[]
            for valors in resultat:
                faller=Member(valors[10], valors[11], valors[12], valors[13], valors[14], valors[15], valors[16], valors[17], valors[18], valors[19])
                loteria= Loteria(valors[0], valors[1], valors[2], valors[3], valors[4], valors[5], valors[6], valors[7], valors[8], valors[9], faller)
                llistat_loteries.append(loteria)
            return llistat_loteries
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
            return None
        except ConnectionError as e:
            messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
            return None
        

    def llegir_sortejos(self):
        try:
            self.cursor.execute("SELECT DISTINCT sorteig FROM loteria")
            llistat_sortejos = self.cursor.fetchall()
            return llistat_sortejos
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la consulta a la base de dades: {str(e)}")
            return None
        except ConnectionError as e:
            messagebox.showerror("Error", f"No s'ha pogut conectar a la base de dades: {str(e)}")
            return None


    def llegir_ultim_id_loteria(self):
        try:
            self.cursor.execute("SELECT * FROM loteria ORDER BY id DESC LIMIT 1")
            resultat = self.cursor.fetchone()
            if resultat is not None:
                return resultat
            else:
                return None
        except (sqlite3.Error, TypeError, ValueError) as e:
            print("Error al llegir la loteria de la base de dades:", e)
            return None


    def actualitzar_loteria(self, loteria):
        '''
        Actualitza la taula "loteria" amb l'objecte de la classe Loteria que se li passa per paràmetre.

        Paràmetres:
        -----------
        loteria : Loteria
            Objecte de la classe Loteria.
        '''
        dades=loteria.paperetes_masculina, loteria.paperetes_femenina, loteria.paperetes_infantil, loteria.decims_masculina, loteria.decims_femenina, loteria.decims_infantil, loteria.id
        try:
            self.cursor.execute("UPDATE loteria SET paperetes_masculina=?, paperetes_femenina=?, paperetes_infantil=?, decims_masculina=?, decims_femenina=?, decims_infantil=? WHERE id=?", (dades))
        except sqlite3.Error:
            messagebox.showerror("Error", "Hi ha un problema amb la base de dades")
        else:
            self.conexio.commit()


    def actualitzar_assignada_loteria(self, id):
        assignada=1
        dades=assignada, id
        try:
            self.cursor.execute("UPDATE loteria SET assignada=? WHERE id=?", (dades))
        except sqlite3.Error:
            messagebox.showerror("Error", "Hi ha un problema amb la base de dades")
        else:
            self.conexio.commit()


    def eliminar_loteria(self, id):
        '''
        Elimina de la base de dades la loteria el id de la qual se li passa per paràmetre

        Paràmetres:
        -----------
        id : integer
            Identificador de la loteria a eliminar.
        '''
        self.cursor.execute("DELETE FROM loteria WHERE id=?", (id,))
        self.conexio.commit()