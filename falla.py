'''
Proporciona la classe "Falla".
'''
from tkinter import messagebox

from base_de_dades import BaseDeDades
from utils import Utils
from arxiu import Arxiu

from movement import Movement
from database import Database
from family import Family
from member import Member
from category import Category


class Falla():
    '''
	Aquesta classe pot controlar llistats de les classes "Member" i "Movement" i operar amb elles.

	Atributs:
	---------
	members_list : list
        Llistat d'objectes de la classe "Member".
    movements_list : list
        Llistat d'objectes de la classe "Movement".
	'''

    def __init__(self, members_list: list = None, movements_list: list = None, categories_list: list = None):
        '''
		Inicialitza una nova instància de la classe Falla.
        Disposa de dos paràmetres que mostren les relacions que manté amb la classe "Member" i la classe "Movement".

        Atributs:
	    ---------
	    members_list : list
            Llistat d'objectes de la classe "Member".
        movements_list : list
            Llistat d'objectes de la classe "Movement".
        categories_list: list
            Llistat d'objectes de la classe "Category".
		'''
        if members_list is None:
            members_list = []
        self.members_list = members_list
        if movements_list is None:
            movements_list = []
        self.movements_list = movements_list
        if categories_list is None:
            categories_list = []
        self.categories_list = categories_list
        self.falla_year = 0


    def enroll_member(member):
        pass

    def deactivate_member(member):
        pass

    def activate_member(member):
        pass
    
    
    def get_members(self, filter, value):
        db = Database('sp')
        if filter == "surname":
            result = db.select_members_by_surname(value)
        elif filter == "adult":
            result = db.select_adult_members()
        elif filter == "family":
            result = db.select_members_by_family(value)
        db.close_connection()
        for values in result:
            family = Family(values[12], values[13], values[14])
            category = Category(values[15], values[16], values[17], values[18])
            member = Member(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[11], family, category)
            self.members_list.append(member)


    def get_movements(self, id_member, falla_year):
        db = Database('sp')
        result = db.select_movements_by_member(id_member, falla_year)
        db.close_connection()
        for values in result:
            movement = Movement(values[0], values[1], values[2], values[3], values[4], values[5], values[7], values[8])
            self.movements_list.append(movement)


    def get_categories(self):
        db = Database('sp')
        result = db.select_categories()
        db.close_connection()
        for values in result:
            category = Category(values[0], values[1], values[2], values[3])
            self.categories_list.append(category)


    def get_current_falla_year(self):
        db = Database('sp')
        self.falla_year = db.select_current_falla_year()
        db.close_connection()


    def assign_fee(self, transaction_date, amount, falla_year, id_member, description):
        Movement.set_movement(transaction_date, amount, 1, 1, falla_year, id_member, description, 0)


    def assign_lottery(self, transaction_date, amount, falla_year, id_member, description):
        Movement.set_movement(transaction_date, amount, 1, 2, falla_year, id_member, description, 0)

    
    def assign_raffle(self, transaction_date, amount, falla_year, id_member, description):
        '''
        Crida a la classe Movement per a crear una assignació de rifa.
        '''
        Movement.set_movement(transaction_date, amount, 1, 3, falla_year, id_member, description, 0)


    def assign_massive_raffle(self):
        '''
        Crea un moviment per cadascún dels fallers amb obligació de pagar rifa i
        el guarda a la base de dades.
        '''
        answer=messagebox.askquestion("Assignar rifa",
                                     "Estàs segur que vols assignar la rifa als fallers corresponents?")
        if answer == "yes":
            result = self.get_members("adult", "")
            for values in result:
                member = Member(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[11])
                self.members_list.append(member)
            try:
                for member in self.members_list:
                    self.assign_raffle(None, 15, None, "rifa", member.id)
            except TypeError:
                messagebox.showerror("Assignar rifa", "La rifa no s'ha pogut assignar correctament")
            else:
                messagebox.showinfo("Assignar rifa", "La rifa s'ha assignat correctament")


    def calculate_assigned_fee(self, id_member, falla_year):
        db = Database('sp')
        result = db.select_fee_by_member(id_member)
        fee = result[0]
        result = db.select_discount_by_member(id_member)
        discount = result[0]*fee/100
        fee = fee - discount
        result = db.select_fee_assignment_movements_by_member(id_member, falla_year)
        db.close_connection()
        for value in result:
            fee = fee + value[0]
        return fee


    def calculate_payed_fee(self, id_member, falla_year):
        db = Database('sp')
        result = db.select_fee_payment_movements_by_member(id_member, falla_year)
        db.close_connection()
        fee = 0
        for value in result:
            fee = fee + value[0]
        return fee


    def calculate_assigned_lottery(self, id_member, falla_year):
        db = Database('sp')
        result = db.select_lottery_assignment_movements_by_member(id_member, falla_year)
        db.close_connection()
        lottery = 0
        for value in result:
            lottery = lottery + value[0]
        return lottery


    def calculate_payed_lottery(self, id_member, falla_year):
        db = Database('sp')
        result = db.select_lottery_payment_movements_by_member(id_member, falla_year)
        db.close_connection()
        lottery = 0
        for value in result:
            lottery = lottery + value[0]
        return lottery


    def calculate_assigned_raffle(self, id_member, falla_year):
        db = Database('sp')
        result = db.select_raffle_assignment_movements_by_member(id_member, falla_year)
        db.close_connection()
        raffle = 0
        for value in result:
            raffle = raffle + value[0]
        return raffle


    def calculate_payed_raffle(self, id_member, falla_year):
        db = Database('sp')
        result = db.select_raffle_payment_movements_by_member(id_member, falla_year)
        db.close_connection()
        raffle = 0
        for value in result:
            raffle = raffle + value[0]
        return raffle
    

    def nou_exercici(self):
        '''
        Crea un nou exercici seguint els següents passos:
        Es crea un arxiu binari amb la id de cada faller amb alta activa junt amb les dades
        d'assignacions i pagaments finals.
        Es modifica l'arxiu binari "exercici" amb l'any actual del sistema.
        Es repasen les categories de tots els fallers no adults per vore si canvien de categoria.
        Recuperem l'arxiu binari creat anteriorment de forma que assignem els deutes o sobrants
        al nou exercici per a cada faller que no haja acabat l'exercici anterior a 0.
        Finalment afegim l'estat de l'historial per a cada faller en el nou exercici depenent de
        si va acabar l'exercici anterior donat d'alta o no.
        '''
		# Creem una cópia en fitxer binari del resultat de l'exercici.
        bd=BaseDeDades("falla.db")
        arxiu=Arxiu("exercici")
        members_list=bd.llegir_fallers_per_alta(1)
        exercici_actual=arxiu.llegir_exercici_actual()
        llista=[]
        for faller in members_list:
            valors=[]
            quota_assignada=0
            quota_pagada=0
            loteria_assignada=0
            loteria_pagada=0
            rifa_assignada=0
            rifa_pagada=0
            valors.append(faller.id)
            quota_base=bd.llegir_quota_faller(faller.id)
            descompte=(faller.familia.descompte*quota_base/100)
            quota=quota_base-descompte
            llista_assignacions_pagaments=self.calcular_assignacions_pagaments(faller.id, exercici_actual)
            quota_assignada=llista_assignacions_pagaments[0]
            quota_pagada=llista_assignacions_pagaments[1]
            loteria_assignada=llista_assignacions_pagaments[2]
            loteria_pagada=llista_assignacions_pagaments[3]
            rifa_assignada=llista_assignacions_pagaments[4]
            rifa_pagada=llista_assignacions_pagaments[5]
            quota_final=quota+quota_assignada
            total_assignacions=quota_final+loteria_assignada+rifa_assignada
            total_pagaments=quota_pagada+loteria_pagada+rifa_pagada
            valors.append("{0:.2f}".format(quota_final))
            valors.append("{0:.2f}".format(loteria_assignada))
            valors.append("{0:.2f}".format(rifa_assignada))
            valors.append("{0:.2f}".format(total_assignacions))
            valors.append("{0:.2f}".format(quota_pagada))
            valors.append("{0:.2f}".format(loteria_pagada))
            valors.append("{0:.2f}".format(rifa_pagada))
            valors.append("{0:.2f}".format(total_pagaments))
            valors.append("{0:.2f}".format(total_assignacions-total_pagaments))
            llista.append(valors)
        nom_arxiu="resums"+"/"+"resum "+str(exercici_actual)
        arxiu=Arxiu(nom_arxiu)
        arxiu.crear_resum(llista)
        messagebox.showinfo("Exercici nou", "Resum de l'any anterior guardat correctament")

		# Modifiquem l'arxiu binari "exercici" amb l'any actual del sistema.
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
        messagebox.showinfo("Exercici nou", "Nou any assignat correctament")
        
        # Assignem la nova categoria a cada faller que haja canviat.
        exercici_actual=arxiu.llegir_exercici_actual()
        for faller in members_list:
            if faller.category.id>1:
                old_category_id=faller.category.id
                edat=faller.calcular_edat(faller.naixement, exercici_actual)
                category_id=faller.calculate_category(edat)
                if category_id!=old_category_id:
                    category=bd.llegir_categoria(category.id)   #provar en la refactoritzacio a juntar les 2 linies
                    faller.category=category                    #provar en la refactoritzacio a juntar les 2 linies
                    bd.actualitzar_faller(faller)
        messagebox.showinfo("Exercici nou", "Categories de fallers actualitzades")

		# Recuperem l'arxiu binari de l'exercici anterior i assignem els valors distints de 0 a l'exercici actual.
        nom_arxiu="resums"+"/"+"resum "+str(exercici_actual-1)
        arxiu=Arxiu(nom_arxiu)
        llista=arxiu.llegir_resum()
        data=data_actual[0] + "-" + data_actual[1] + "-" + data_actual[2]
        for valor in llista:
             if valor[9]!="0.00":
                faller=bd.llegir_faller(valor[0])
                moviment=Movement(0, data, valor[9], 1, 1, exercici_actual, "any anterior", 0, faller)
                bd.crear_moviment(moviment)
        bd.tancar_conexio()
        messagebox.showinfo("Exercici nou", "Deutes i sobrants de l'exercici anterior actualitzats")

        # Afegim a cada faller l'historial de l'exercici nou.
        members_list=bd.llegir_fallers()
        for faller in members_list:
            nom_arxiu="historials"+"/"+str(faller.id)
            arxiu=Arxiu(nom_arxiu)
            historial=arxiu.llegir_historial()
            if faller.alta==1:
                historial[exercici_actual]=["vocal", "Sants Patrons"]
            else:
                historial[exercici_actual]=["baixa", ""]
            arxiu.modificar_historial(historial)
        messagebox.showinfo("Exercici nou", "Historial faller actualitzat com a vocals. La resta de punts s'han d'assignar manualment")
        messagebox.showinfo("Exercici nou", "El canvi d'exercici s'ha realitzat correctament")


    def borrar_historial(self):
        '''
        Borra tots els arxius d'historial de tots els fallers i els reinicia com si l'exercici
        actual fora el primer any de faller.
        '''
        valor=messagebox.askquestion("Borrar historial",
                                     "Estàs segur que vols reiniciar els historials de tots els fallers?")
        if valor=="yes":
            bd=BaseDeDades("falla.db")
            arxiu=Arxiu("exercici")
            exercici_actual=arxiu.llegir_exercici_actual()
            members_list=bd.llegir_fallers()
            for faller in members_list:
                exercici=faller.calcular_primer_exercici(faller.naixement)
                historial={}
                while exercici < exercici_actual:
                    historial[exercici]=["baixa", ""]
                    exercici=exercici+1
                if faller.alta==1:
                    historial[exercici_actual]=["vocal", "Sants Patrons"]
                else:
                    historial[exercici_actual]=["baixa", ""]
                nom_arxiu="historials"+"/"+str(faller.id)
                arxiu=Arxiu(nom_arxiu)
                arxiu.crear_historial(historial)
            bd.tancar_conexio()
            messagebox.showinfo("Borrar historial", "L'historial de tots els fallers s'ha reiniciat correctament")