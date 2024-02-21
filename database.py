import mysql.connector
from tkinter import messagebox

from utils import Utils

class Database:
    
    def __init__(self, db_name):
        '''
        Conexió MariaDb
        '''
        self.verify_existence_bd(db_name)
        self.mysqlConnection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="hamuclaulo07",
            database=db_name
        )
        if self.mysqlConnection.is_connected():
            self.mysqlCursor=self.mysqlConnection.cursor()
        else:
            messagebox.showerror("Error", "No s'ha pogut establir la conexió amb la base de dades.")


    def verify_existence_bd(self, db_name):
        try:
            self.mysqlConnection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="hamuclaulo07"
            )
            if self.mysqlConnection.is_connected():
                self.mysqlCursor=self.mysqlConnection.cursor()
            else:
                messagebox.showerror("Error", "No s'ha pogut establir la conexió amb la base de dades.")
            query = f"SHOW DATABASES LIKE '{db_name}'"
            self.mysqlCursor.execute(query)
            result = self.mysqlCursor.fetchone()
            self.mysqlCursor.close()
            self.mysqlConnection.close()
            if result:
                pass
            else:
                messagebox.showerror("Error", "La base de dades no existeix. Es va a crear de forma automàtica.")
                self.create_database(db_name)
                self.create_tables(db_name)
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "No s'ha pogut verificar l'existència de la base de dades.")


    
    def create_database(self, db_name):
        '''
        Crea la BBDD
        '''
        self.mysqlConnection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="hamuclaulo07"
            )
        if self.mysqlConnection.is_connected():
            self.mysqlCursor=self.mysqlConnection.cursor()
        else:
            messagebox.showerror("Error", "No s'ha pogut establir la conexió amb la base de dades.")
        query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        try:
            self.mysqlCursor.execute(query)
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "No s'ha pogut crear la base de dades")
        finally:
            self.mysqlCursor.close()
            self.mysqlConnection.close()
       

    def create_tables(self, db_name):
        '''
        Crea les diferents taules
        '''
        self.mysqlConnection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="hamuclaulo07",
                    database=db_name
                )
        if self.mysqlConnection.is_connected():
            self.mysqlCursor=self.mysqlConnection.cursor()
        else:
            messagebox.showerror("Error", "No s'ha pogut establir la conexió amb la base de dades.")

        query="""
        CREATE TABLE IF NOT EXISTS member(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            surname VARCHAR(100) NOT NULL,
            birthdate DATE NOT NULL,
            gender ENUM('M', 'F'),
            dni VARCHAR(10),
            address VARCHAR(100),
            phoneNumber VARCHAR(15),
            isRegistered BOOLEAN,
            idFamily INT,
            idCategory INT,
            email VARCHAR(50)
        )
        """
        try:
            self.mysqlCursor.execute(query)
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "No s'ha pogut crear la taula member")
        
        query = """
        CREATE TABLE IF NOT EXISTS category(
            id INT AUTO_INCREMENT PRIMARY KEY,
            fee DECIMAL(10, 2) NOT NULL,
            name VARCHAR(10),
            description VARCHAR(50)
        )
        """
        try:
            self.mysqlCursor.execute(query)
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "No s'ha pogut crear la taula category")

        query = """
        CREATE TABLE IF NOT EXISTS family(
            id INT AUTO_INCREMENT PRIMARY KEY,
            discount DECIMAL(10, 2) NOT NULL,
            isDirectDebited BOOLEAN
        )
        """
        try:
            self.mysqlCursor.execute(query)
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "No s'ha pogut crear la taula family")
        
        query = """
        CREATE TABLE IF NOT EXISTS movement(
            id INT AUTO_INCREMENT PRIMARY KEY,
            transactionDate DATE NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            idType INT NOT NULL,
            idConcept INT NOT NULL,
            fallaYear INT NOT NULL,
            idMember INT,
            description VARCHAR(100),
            receiptNumber INT
        )
        """
        try:
            self.mysqlCursor.execute(query)
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "No s'ha pogut crear la taula movement")

        query = """
        ALTER TABLE member
            ADD CONSTRAINT member_family_FK
            FOREIGN KEY(idFamily)
            REFERENCES family(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
            ADD CONSTRAINT member_category_FK
            FOREIGN KEY(idCategory)
            REFERENCES category(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
        """
        try:
            self.mysqlCursor.execute(query)
            self.mysqlConnection.commit()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Ha fallat la creació de les FK de la taula member.")

        query = """
        ALTER TABLE movement
            ADD CONSTRAINT movement_member_FK
            FOREIGN KEY(idMember)
            REFERENCES member(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
        """
        try:
            self.mysqlCursor.execute(query)
            self.mysqlConnection.commit()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Ha fallat la creació de la FK de la taula moviment.")
        finally:
            self.mysqlCursor.close()
            self.mysqlConnection.close()


    def export_category_to_mysql(self, result):
        '''
        Exportació taula categoria a sp.category
        '''
        query = "INSERT INTO category (id, fee, name, description) VALUES (%s, %s, %s, %s)"
        try:
            for row in result:
                self.mysqlCursor.execute(query, row)
            self.mysqlConnection.commit()
        except mysql.connector.Error as error:
            self.mysqlConnection.rollback()
            messagebox.showerror("Error", "No s'han pogut insertar les dades a la taula category")


    def export_family_to_mysql(self, result):
        '''
        Exportació taula familia a sp.family
        '''
        query = "INSERT INTO family (id, discount, isDirectDebited) VALUES (%s, %s, %s)"
        try:
            for row in result:
                self.mysqlCursor.execute(query, row)
            self.mysqlConnection.commit()
        except mysql.connector.Error as error:
            self.mysqlConnection.rollback()
            messagebox.showerror("Error", "No s'han pogut insertar les dades a la taula family")


    def export_member_to_mysql(self, result):
        '''
        Exportació taula faller a sp.member
        '''
        utils=Utils()
        query = "INSERT INTO member (id, name, surname, birthdate, gender, dni, address, phoneNumber, isRegistered, idFamily, idCategory, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            for row in result:
                as_list = list(row)
                date=utils.convert_date(as_list[3])
                as_list[3]=date
                self.mysqlCursor.execute(query, as_list)
            self.mysqlConnection.commit()
        except mysql.connector.Error as error:
            self.mysqlConnection.rollback()
            messagebox.showerror("Error", "No s'han pogut insertar les dades a la taula member")


    def export_movements_to_mysql(self, result):
        '''
        Exportació taula moviment a sp.movements
        '''
        utils=Utils()
        query = "INSERT INTO movements (id, transactionDate, amount, idType, idConcept, fallaYear, idMember, description, receiptNumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            for row in result:
                as_list = list(row)
                date=utils.convert_date(as_list[1])
                as_list[1]=date
                self.mysqlCursor.execute(query, as_list)
            self.mysqlConnection.commit()
        except mysql.connector.Error as error:
            self.mysqlConnection.rollback()
            messagebox.showerror("Error", "No s'han pogut insertar les dades a la taula member")

