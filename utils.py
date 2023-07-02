from datetime import datetime

class Utils():

    def __init__(self):

        pass


    def calcular_data_actual(self):

        data=datetime.now()
        any_actual=datetime.strftime(data,'%Y')
        mes_actual=datetime.strftime(data,'%m')
        dia_actual=datetime.strftime(data,'%d')
        data_final=[]
        data_final.append(dia_actual)
        data_final.append(mes_actual)
        data_final.append(any_actual)
        #data_final=dia_actual + "-" + mes_actual + "-" + any_actual
        return data_final

