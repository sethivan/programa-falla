from datetime import datetime
import tkinter.ttk as ttk

class Utils():

    def __init__(self):

        pass


    def define_global_style(self):
        '''
		Definició dels estils per als widgets ttk de la finestra.
		'''
        self.estil=ttk.Style()
        self.estil.theme_use('clam')
        self.estil.configure(".", font=("Ubuntu", 10))
        self.estil.configure("Marc.TFrame", background="#ffffff", relief="groove")
        self.estil.configure("Titol.TLabel", background="#ffffff", foreground="#e95420", font=("Ubuntu", 11))
        self.estil.configure("Portada.TLabel", background="#ffffff", foreground="#e95420", font=("Ubuntu", 40))
        self.estil.configure("Etiqueta.TLabel", background="#ffffff")
        self.estil.map("Entrada.TEntry", foreground=[('disabled','black')])
        self.estil.configure("Check.TCheckbutton", background="#ffffff")
        self.estil.map("Check.TCheckbutton", background=[('disabled', '#eae9e7')])
        self.estil.configure("Radio.TRadiobutton", background="#ffffff")
        self.estil.map("Radio.TRadiobutton", background=[('active', '#e95420')], foreground=[('active', '#ffffff')])
        self.estil.configure("Boto.TButton", background="#ffffff", foreground="#000000", font=("Ubuntu", 11))
        self.estil.map("Boto.TButton", background=[('active', '#e95420')], foreground=[('active', '#ffffff'), ('disabled', '#aea79f')])
                

    def calcular_data_actual(self):
        '''
		Llegim la data actual del sistema i la tornem en format llista.

		Retorna:
        --------
        data_final : llista
            Llistat amb el dia, mes i any actuals.
		'''
        data=datetime.now()
        any_actual=datetime.strftime(data,'%Y')
        mes_actual=datetime.strftime(data,'%m')
        dia_actual=datetime.strftime(data,'%d')
        data_final=[]
        data_final.append(dia_actual)
        data_final.append(mes_actual)
        data_final.append(any_actual)
        return data_final
    

    def convert_date(self, spanish_date):
        date = datetime.strptime(spanish_date, '%d-%m-%Y')
        mariadb_date = date.strftime('%Y-%m-%d')
        return mariadb_date
    

    def english_to_spanish_date(self, english_date):
        spanish_date = english_date.strftime('%d-%m-%Y')
        return spanish_date

