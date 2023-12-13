import numpy as np
import statistics as stat


class Performance:
    def __init__(self):
        self.Overshoot = 0.0
        self.d = 0.0
        self.Ess = 0.0
        self.Ts = 0.0
        self.v = []
        self.VR = 0.0

    def Init(self, velocidades, Velocidad_de_referencia):
        self.Overshoot = 0.0
        self.d = 0.0
        self.Ess = 0.0
        self.Ts = 0.0
        self.v = velocidades
        self.VR = Velocidad_de_referencia

    def Calcula_Ts(self):
        for i in range(len(self.v) - 20):
            self.sub_v_ts = np.array(self.v[i:i + 20])
            # calcula si todos los valores están por debajo del 2% de la moda
            self.debajo = np.all(np.less(abs(self.sub_v_ts - self.moda), self.moda * 0.01))
            # print(self.debajo)
            # calcula si todos los valores están por encima del 2%
            # self.encima = np.all(np.less(abs(self.sub_v_ts- self.VR),self.VR*0.02))
            # print(self.encima)
            if (self.debajo == True):
                # print(self.sub_v_ts)
                return i
        return 1000

    def Calcula_indexes(self):
        self.Overshoot = max(self.v)
        self.indice_d = self.v.index(self.Overshoot)
        # self.Overshoot = max(self.v)-self.VR
        self.sub_v = self.v[self.indice_d:]
        # print(self.sub_v)
        self.b = self.VR - min(self.sub_v)
        self.d = self.b / self.Overshoot
        self.moda = stat.mode(np.round(self.v, 2))
        self.Overshoot = max(self.v) - self.moda
        self.Ess = self.VR - self.moda
        self.Ts = self.Calcula_Ts()
        return self.Overshoot, self.d, self.Ess, self.Ts