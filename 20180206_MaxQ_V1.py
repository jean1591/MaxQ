import pprint, time, matplotlib.pyplot as plt


def pression_altitude(alt):
    """
    Fonction calculant la pression par rapport a l'altitude
    :param alt: int, altitude
    :return: float, pression a l'altitude
    """
    return round(1013.25*(1-(0.0065*alt)/288.15)**5.255, 2)


def acceleration_masse(acceleration_prec, poussee, masse):
    """
    Fonction calculant l'acceleration subie par la fusee
    :param poussee: int, force produite par les moteurs en Newton
    :param masse: int, masse totale de la fusee avec ses reservoirs pleins
    :return: int, acceleration produite en m/s²
    """
    # 9.8 reprensentant la gravite
    return round(acceleration_prec + (poussee - 9.8 * masse) / masse, 2)


def masse_fusee_seconde(masse_fusee_initiale, debit_massique, sec):
    """
    Fonction calculant la masse de la fusee apres x secondes
    :param masse_combustible_initiale: int, masse totale de la fusee avec reservoirs pleins en kg
    :param debit_massique: int, masse expulsee par seconde en kg/s
    :param sec: int, nombre de secondes ecoulees
    :return: int, masse en kg de la fusee apres sec secondes
    """
    masse_fusee = masse_fusee_initiale * 0.2
    masse_combustible_initiale = masse_fusee_initiale * 0.8
    return int(masse_fusee + masse_combustible_initiale-(debit_massique*sec))


def vitesse_actuelle(temps_init, position_actuelle):
    """
    Fonction calculant la vitesse d'un objet a un moment donne
    :param position_actuelle: int, distance de l'bjet en metre
    :param temps_init: float, marqueur du debut de la mission
    :return: int, vitesse en km/h de l'objet
    """
    return round(position_actuelle / (time.time() - temps_init), 0)


# Initialise la mission
# Valeurs basees sur la Falcon 9
altitude = 0
pression_actuelle = pression_altitude(altitude)
poussee = 7607000
masse_fusee_initiale = 549000
masse_combustible_initiale = masse_fusee_initiale * 0.8
masse_revisee = masse_fusee_initiale*0.2 + masse_combustible_initiale
debit_massique = 2500
vitesse = 0
acceleration_actuelle = 0
debut_mission = time.time()
duree = 0

data = {}

while duree < 129:
    try:
        pression_actuelle = pression_altitude(altitude)
    except TypeError:
        pression_actuelle = 0
    altitude += acceleration_actuelle
    masse_revisee = masse_fusee_seconde(masse_fusee_initiale, debit_massique, duree)
    acceleration_actuelle = acceleration_masse(acceleration_actuelle, 7607000, masse_revisee)
    data.setdefault(duree, {"Altitude": round(altitude, 2),
                            "Pression": pression_actuelle,
                            "Masse": masse_revisee,
                            "Acceleration": acceleration_actuelle,
                            "Vitesse": round(acceleration_actuelle * 3.6, 2),
                            "Q": 1/2 * round((acceleration_actuelle**2) * 3.6 * pression_actuelle, 2)
                            }
                    )
    duree += 1


pprint.pprint(data)


list_vitesse = []
list_pression = []
list_masse = []
list_Q = []
list_acceleration = []

for element in data:
    list_vitesse.append(data[element]["Vitesse"])
    list_pression.append(data[element]["Pression"])
    list_masse.append(data[element]["Masse"])
    # if len(list_Q) > 0 and data[element]["Q"] < list_Q[-1]:
    #     print(element, "MAX Q:", list_Q[-1], "Pa")
    #     break
    list_Q.append(data[element]["Q"])
    list_acceleration.append(data[element]["Acceleration"])


# MAX Q
plt.plot(list_Q)
plt.title("MAX Q")
plt.ylabel("Pression (Pa)")
plt.xlabel("Temps (secondes)")
plt.show()
