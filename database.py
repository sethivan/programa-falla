import mysql.connector
from decimal import Decimal
from tkinter import messagebox

from utils import Utils

class Database:
    
    def __init__(self, db_name):
        '''
        Conexió MariaDb
        '''
        self.verify_existence_db(db_name)
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

    def close_connection(self):
        self.mysqlCursor.close()
        self.mysqlConnection.close()


    def verify_existence_db(self, db_name):
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
            self.close_connection()
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
        query=f"CREATE DATABASE IF NOT EXISTS {db_name}"
        try:
            self.mysqlCursor.execute(query)
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "No s'ha pogut crear la base de dades")
       

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
            self.close_connection()


    def export_category_to_mysql(self, result):
        '''
        Exportació taula categoria a sp.category
        '''
        query="INSERT INTO category (id, fee, name, description) VALUES (%s, %s, %s, %s)"
        try:
            for row in result:
                self.mysqlCursor.execute(query, row)
            self.mysqlConnection.commit()
        except mysql.connector.Error as error:
            self.mysqlConnection.rollback()
            messagebox.showerror("Error", "No s'han pogut insertar les dades a la taula category")
        finally:
            self.close_connection()


    def export_family_to_mysql(self, result):
        '''
        Exportació taula familia a sp.family
        '''
        query="INSERT INTO family (id, discount, isDirectDebited) VALUES (%s, %s, %s)"
        try:
            for row in result:
                self.mysqlCursor.execute(query, row)
            self.mysqlConnection.commit()
        except mysql.connector.Error as error:
            self.mysqlConnection.rollback()
            messagebox.showerror("Error", "No s'han pogut insertar les dades a la taula family")
        finally:
            self.close_connection()


    def export_member_to_mysql(self, result):
        '''
        Exportació taula faller a sp.member
        '''
        utils=Utils()
        query="INSERT INTO member (id, name, surname, birthdate, gender, dni, address, phoneNumber, isRegistered, idFamily, idCategory, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
        finally:
            self.close_connection()


    def export_movements_to_mysql(self, result):
        '''
        Exportació taula moviment a sp.movement
        '''
        utils=Utils()
        query="INSERT INTO movement (id, transactionDate, amount, idType, idConcept, fallaYear, idMember, description, receiptNumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            for row in result:
                as_list = list(row)
                date=utils.convert_date(as_list[1])
                as_list[1]=date
                self.mysqlCursor.execute(query, as_list)
            self.mysqlConnection.commit()
        except mysql.connector.Error as error:
            self.mysqlConnection.rollback()
            messagebox.showerror("Error", "No s'han pogut insertar les dades a la taula movement")
        finally:
            self.close_connection()


    def insert_member(self, name, surname, birthdate, gender, dni, address, phone_number, is_registered, email, id_family, id_category):
        query = "INSERT INTO member (name, surname, birthdate, gender, dni, address, phoneNumber, isRegistered, email, idFamily, idCategory) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = name, surname, birthdate, gender, dni, address, phone_number, is_registered, email, id_family, id_category
        try:
            self.mysqlCursor.execute(query, data)
            self.mysqlConnection.commit()
        except mysql.connector.Error as error:
             messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_member(self, id):
        query = "SELECT * FROM member INNER JOIN family ON member.idFamily = family.id INNER JOIN category ON member.idCategory = category.id where member.id = %s"
        try:
            self.mysqlCursor.execute(query, (id,))
            member = self.mysqlCursor.fetchone()
            return member
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_last_member(self):
        query = "SELECT * FROM member ORDER BY id DESC LIMIT 1"
        try:
            self.mysqlCursor.execute(query)
            member = self.mysqlCursor.fetchone()
            return member
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_members_by_surname(self, surname):
        query = "SELECT * FROM member INNER JOIN family ON member.idFamily = family.id INNER JOIN category ON member.idCategory = category.id WHERE member.surname LIKE %s"
        try:
            self.mysqlCursor.execute(query, (f"%{surname}%",))
            members_list = self.mysqlCursor.fetchall()
            return members_list
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_adult_members(self):
        query = "SELECT * FROM member INNER JOIN family ON member.idFamily = family.id INNER JOIN category ON member.idCategory = category.id WHERE member.isRegistered and (member.idCategory=1 or member.idCategory=2) ORDER BY member.surname"
        try:
            self.mysqlCursor.execute(query)
            members_list = self.mysqlCursor.fetchall()
            return members_list
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_members_by_family(self, id_family):
        query = "SELECT * FROM member INNER JOIN family ON member.idFamily = family.id INNER JOIN category ON member.idCategory = category.id WHERE member.idFamily = %s"
        try:
            self.mysqlCursor.execute(query, (id_family,))
            members_list = self.mysqlCursor.fetchall()
            return members_list
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_membership_history(self, id):
        query = "SELECT * FROM membership_history Where id = %s"
        try:
            self.mysqlCursor.execute(query, (id,))
            membership_history = self.mysqlCursor.fetchall()
            return membership_history
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def update_member(self, id, name, surname, birthdate, gender, dni, address, phone_number, is_registered, email, id_family, id_category):
        query = "UPDATE member SET name = %s, surname = %s, birthdate = %s, gender = %s, dni = %s, address = %s, phoneNumber = %s, isRegistered = %s, email = %s, idFamily = %s, idCategory = %s WHERE id = %s"
        data = name, surname, birthdate, gender, dni, address, phone_number, is_registered, email, id_family, id_category, id
        try:
            self.mysqlCursor.execute(query, data)
            self.mysqlConnection.commit()
        except mysql.connector.Error as error:
             messagebox.showerror("Error", str(error))


    def insert_family(self, discount, is_direct_debited):
        query = "INSERT INTO family (discount, isDirectDebited) VALUES (%s, %s)"
        data = discount, is_direct_debited
        try:
            self.mysqlCursor.execute(query, data)
            self.mysqlConnection.commit()
        except mysql.connector.Error as error:
             messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_family(self, id):
        query = "SELECT * FROM family where id = %s"
        try:
            self.mysqlCursor.execute(query, (id,))
            family = self.mysqlCursor.fetchone()
            return family
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_last_family(self):
        query = "SELECT * FROM family ORDER BY id DESC LIMIT 1"
        try:
            self.mysqlCursor.execute(query)
            family = self.mysqlCursor.fetchone()
            return family
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_discount_by_member(self, id_member):
        query = "SELECT discount FROM family INNER JOIN member ON family.id = member.idFamily WHERE member.id = %s"
        try:
            self.mysqlCursor.execute(query, (id_member,))
            discount = self.mysqlCursor.fetchone()
            return discount
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def update_family(self, id, discount, is_direct_debited):
        query = "UPDATE family SET discount = %s, isDirectDebited = %s WHERE id = %s"
        data = discount, is_direct_debited, id
        try:
            self.mysqlCursor.execute(query, data)
            self.mysqlConnection.commit()
        except mysql.connector.Error as error:
             messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_fee_assignment_movements_by_member(self, id_member, falla_year):
        query = "SELECT amount FROM movement WHERE idMember = %s and idType = 1 and idConcept = 1 and fallaYear = %s"
        try:
            self.mysqlCursor.execute(query, (id_member, falla_year))
            movements_list = self.mysqlCursor.fetchall()
            return movements_list
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_lottery_assignment_movements_by_member(self, id_member, falla_year):
        query = "SELECT amount FROM movement WHERE idMember = %s and idType = 1 and idConcept = 2 and fallaYear = %s"
        try:
            self.mysqlCursor.execute(query, (id_member, falla_year))
            movements_list = self.mysqlCursor.fetchall()
            return movements_list
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_raffle_assignment_movements_by_member(self, id_member, falla_year):
        query = "SELECT amount FROM movement WHERE idMember = %s and idType = 1 and idConcept = 3 and fallaYear = %s"
        try:
            self.mysqlCursor.execute(query, (id_member, falla_year))
            movements_list = self.mysqlCursor.fetchall()
            return movements_list
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_fee_payment_movements_by_member(self, id_member, falla_year):
        query = "SELECT amount FROM movement WHERE idMember = %s and idType = 2 and idConcept = 1 and fallaYear = %s"
        try:
            self.mysqlCursor.execute(query, (id_member, falla_year))
            movements_list = self.mysqlCursor.fetchall()
            return movements_list
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_lottery_payment_movements_by_member(self, id_member, falla_year):
        query = "SELECT amount FROM movement WHERE idMember = %s and idType = 2 and idConcept = 2 and fallaYear = %s"
        try:
            self.mysqlCursor.execute(query, (id_member, falla_year))
            movements_list = self.mysqlCursor.fetchall()
            return movements_list
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_raffle_payment_movements_by_member(self, id_member, falla_year):
        query = "SELECT amount FROM movement WHERE idMember = %s and idType = 2 and idConcept = 3 and fallaYear = %s"
        try:
            self.mysqlCursor.execute(query, (id_member, falla_year))
            movements_list = self.mysqlCursor.fetchall()
            return movements_list
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))

    
    def select_fee_by_member(self, id_member):
        query = "SELECT fee FROM category INNER JOIN member ON category.id = member.idCategory WHERE member.id = %s"
        try:
            self.mysqlCursor.execute(query, (id_member,))
            fee = self.mysqlCursor.fetchone()
            return fee
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def insert_movement(self, transaction_date, amount, id_type, id_concept, falla_year, id_member, description, receipt_number):
        query = "INSERT INTO movement (transactionDate, amount, idType, idConcept, fallaYear, idMember, description, receiptNumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = transaction_date, amount, id_type, id_concept, falla_year, id_member, description, receipt_number
        try:
            self.mysqlCursor.execute(query, data)
            self.mysqlConnection.commit()
        except mysql.connector.Error as error:
             messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))

    
    def select_movements_by_member(self, id_member, falla_year):
        query = "SELECT * FROM movement WHERE idMember = %s AND fallaYear = %s"
        try:
            self.mysqlCursor.execute(query, (id_member, falla_year))
            movements_list = self.mysqlCursor.fetchall()
            return movements_list
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_category(self, id):
        query = "SELECT * FROM category where id = %s"
        try:
            self.mysqlCursor.execute(query, (id,))
            category = self.mysqlCursor.fetchone()
            return category
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_categories(self):
        query = "SELECT * FROM category"
        try:
            self.mysqlCursor.execute(query)
            categories_list = self.mysqlCursor.fetchall()
            return categories_list
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def update_category(self, id, fee, name, description):
        query = "UPDATE category SET fee = %s, name = %s, description = %s WHERE id = %s"
        data = fee, name, description, id
        try:
            self.mysqlCursor.execute(query, data)
            self.mysqlConnection.commit()
        except mysql.connector.Error as error:
             messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))


    def select_current_falla_year(self):
        query = "SELECT code FROM falla_year ORDER BY code DESC LIMIT 1"
        try:
            self.mysqlCursor.execute(query)
            falla_year = self.mysqlCursor.fetchone()
            return falla_year[0]
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error al conectar a la base de dades" + str(error))