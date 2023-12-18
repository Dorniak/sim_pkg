from matplotlib import pyplot as plt
from utils.Performance import Performance
from utils.Controller import Controller
fig, ax = plt.subplots()
fig, ax2 = plt.subplots()

P = Performance()    
# Crear una instancia del controlador
controller = Controller()
#Kp=0.2
#Ki=0.004
#Kd=0.0
Kp=0.1#0.1#0.5
Ki=7#0.008#0.004
Kd=0.6#0.0#0.0
velocidad=[]
ut=[]
coordenadax=[]

Velocidad_de_referencia = 50.0
# Inicializar el controlador con los valores de ganancia
controller.Init(Kp, Ki, Kd)

# Establecer la velocidad de referencia
controller.Set_reference(Velocidad_de_referencia)

# Ejecutar 320 ciclos del controlador
for ite in range(320):
    x,y = controller.Exec_controller_cycleJE()
    velocidad.append(x)
    ut.append(y)
    coordenadax.append(ite)
ax.plot(coordenadax, velocidad, linewidth=2.0)
ax.grid(axis='x', color='0.95')
ax.grid(axis='y', color='0.95')
ax2.plot(coordenadax, ut, linewidth=2.0)
ax2.grid(axis='x', color='0.95')
ax2.grid(axis='y', color='0.95')

P.Init(velocidad, Velocidad_de_referencia)
o, d, Ess, Ts = P.Calcula_indexes()
print("Overshoot: ",o)
print("d: ",d)
print("Ess: ",Ess)
print("Ts:", Ts)