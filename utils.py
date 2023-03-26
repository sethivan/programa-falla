from datetime import datetime

class Utils():

    def __init__(self):

        pass


    def calcular_data_actual(self):

        data=datetime.now()
        anyactual=datetime.strftime(data,'%Y')
        mesactual=datetime.strftime(data,'%m')
        diaactual=datetime.strftime(data,'%d')
        datafinal=diaactual + "-" + mesactual + "-" + anyactual
        return datafinal

