import math

class CoordenadasUTM:
    semiejeMayor = 6378137
    semiejeMenor = 6356752.314

    def __init__(self, hemisferio, cordEste, cordNorte):
        self.hemisferio = hemisferio
        self.cordEste = cordEste
        self.cordNorte = cordNorte
    
    @classmethod
    def calcularExcentricidad(cls):
        return math.sqrt(cls.semiejeMayor**2 - cls.semiejeMenor**2) / cls.semiejeMayor
    
    @classmethod
    def calcular_parametros_excentricidad(cls):
        return math.sqrt(cls.semiejeMayor**2 - cls.semiejeMenor**2) / cls.semiejeMenor
    
    @classmethod
    def calcular_excentricidad_y_radio_curvatura(cls, parametroExcentricidad):
        return parametroExcentricidad**2
    
    @classmethod
    def calcular_radioPolar(cls):
        return (cls.semiejeMayor**2) / cls.semiejeMenor
    
    @classmethod
    def calcular_variables_principales(cls, hemisferio, cordEste, cordNorte, radio_curvatura, radioPolar):
        y_sur_ecuador = 0
        if hemisferio == 'S':
            y_sur_ecuador = cordNorte - 10000000
        else:
            y_sur_ecuador = cordNorte
        fi = y_sur_ecuador / (6366197.724 * 0.9996)
        ni = radioPolar / (1 + radio_curvatura * (math.cos(fi) ** 2))**(1 / 2) * 0.9996
        meridiano_central = -81
        a = (cordEste - 500000) / ni
        a1 =  math.sin(2 * fi)
        a2 = a1 * math.cos(fi)**2
        j2 = fi + (a1 / 2)
        j4 = (3 * j2 + a2) / 4
        j6 = (5 * j4 + a2 * (math.cos(fi))**2) / 3
        alfa = (3 / 4) * radio_curvatura
        beta = (5 / 3) * (alfa)**2
        gamma = (35 / 27) * (alfa)**3
        bFi = 0.9996 * radioPolar * (fi - (alfa * j2) + (beta * j4) - (gamma * j6))  
        b = (y_sur_ecuador - bFi) / ni
        zeta = ((radio_curvatura * a**2) / 2) * (math.cos(fi))**2
        xi = b * (1 - zeta) + fi
        eta = a * (1 - (zeta / 3))
        sen_h_xi = (math.exp(eta) - math.exp(-eta)) / 2
        delta_lambda = math.atan(sen_h_xi / math.cos(xi))
        tau = math.atan(math.cos(delta_lambda) * math.tan(xi))
        fi_radianes = fi + (1 + radio_curvatura * (math.cos(fi) ** 2) - (3 / 2) * radio_curvatura * math.sin(fi) * math.cos(fi) * (tau - fi)) * (tau - fi)
        return fi_radianes, delta_lambda, meridiano_central
    
    @staticmethod
    def calcularLatitud(fi_radianes):
        return (fi_radianes / math.pi) * 180
    
    @staticmethod
    def calcularLongitud(acordEste, meridiano_central):
        return (acordEste / math.pi) * 180 + meridiano_central


#Usos del codigo
"""
# Crear objeto CoordenadasUTM
coord_utm = CoordenadasUTM('N', 500000, 4649776.820)

# Calcular parámetros de la elipsoide
excentricidad = CoordenadasUTM.calcularExcentricidad()
param_excentricidad = CoordenadasUTM.calcular_parametros_excentricidad()
radio_curvatura = CoordenadasUTM.calcular_excentricidad_y_radio_curvatura(param_excentricidad)
radio_polar = CoordenadasUTM.calcular_radioPolar()

# Calcular variables principales
latitud, longitud, meridiano = CoordenadasUTM.calcular_variables_principales('N', 500000, 4649776.820, radio_curvatura, radio_polar)

# Convertir latitud y longitud a grados
latitud_grados = CoordenadasUTM.calcularLatitud(latitud)
longitud_grados = CoordenadasUTM.calcularLongitud(longitud, meridiano)

"""