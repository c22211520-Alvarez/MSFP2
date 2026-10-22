"""
Práctica Dos: Sistema Cardiovascular

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Gabriela Gissele Alvarez Garcia
Número de control: C22211520
Correo institucional: c22211520@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas

import numpy as np
import control as ctrl
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt

# Datos de la simulación
u = np.array(pd.read_excel('signal.xlsx', header=None))
x0,t0,tend,dt,w,h = 0,0,15,1E-2,10,5 #tiempo obtenido
N = round((tend-t0)/dt)+1
t= np.linspace(t0,tend,N)
u=np.reshape(signal.resample(u,len(t)),-1)

#Funcion para entregar las funciones de transferencia segun el caso
def casos(Z,L,R,C):
    # Componentes del circuito RLC y función de transferencia
    num = [L*R,R*Z]
    den = [C*L*R*Z,L*(Z+R),R*Z]
    sys = ctrl.tf(num, den)
    # Polos del sistema
    L= np.roots(den)
    return sys,L

#llamar funcion de transferencia del hipotenso
Z,L,R,C= 0.010,0.001,1.00,3.500
syshipo,L = casos(Z,L,R,C)
print(f"Funcion de transferencia del hipotenso (caso 1):{syshipo}")
print(f"Polos del sistema: L1 = {L[0]:.3e}, L2= {L[1]:.3e}\n")
#llamar funcion de transferencia del normotenso
Z,L,R,C= 0.010,0.001,1.00,1.500
sysnormo,L = casos(Z,L,R,C)
print(f"Funcion de transferencia del hipotenso (control):{sysnormo}")
print(f"Polos del sistema: L1 = {L[0]:.3e}, L2= {L[1]:.3e}\n")
#llamar funcion de transferencia del hipertenso
Z,L,R,C= 0.010,0.001,1.00,1.000
syshiper,L= casos(Z,L,R,C)
print(f"Funcion de transferencia del hipotenso (caso 2):{syshiper}")
print(f"Polos del sistema: L1 = {L[0]:.3e}, L2= {L[1]:.3e}\n")


# Componentes del controlador
def controlador(kP,kI,kD,sys):
    Cr = 1e-6
    Re = 1/(kI*Cr)
    Rr = kP*Re
    Ce = kD/Rr
    numPID = [Re*Rr*Ce*Cr,Re*Ce + Rr*Cr]
    denPID = [Re*Cr,0]
    PID = ctrl.tf(numPID, denPID)
    sysPID=ctrl.feedback(ctrl.series(PID,sys),1,sign =-1)
    return sysPID
    
hipoPID = controlador(462.94432652274,1133845.892515,0.0062678328455141,syshipo)
print(f"Funcion de transferencia del hipotenso en lazo cerrado: {hipoPID} \n")
# Sistema de control en lazo cerrado
hiperPID = controlador(135.230473508502,338552.543784993,0.00174865251719904,syshiper)
print(f"Funcion de transferencia del hipertenso en lazo cerrado: {hiperPID} \n")


#Colores
clr1 = np.array([80,3,192])/255
clr2 = np.array([171,3,169])/255
clr3 = np.array([255,213,30])/255
clr4 = np.array([3,252,232])/255

#Funciones del sistema en lazo abierto y lazo cerrado
_,PpN = ctrl.forced_response(sysnormo,t,u,x0) #PpN
_,PpL = ctrl.forced_response(syshipo,t,PpN,x0) #PpL
_,PpH = ctrl.forced_response(syshiper,t,PpN,x0) #PpH


_,PIDL = ctrl.forced_response(hipoPID,t,PpN,x0) #PIDL
_,PIDH = ctrl.forced_response(hiperPID,t,PpN,x0) #PIDH

    
# Respuestas: Simulaciones numéricas
fg1 = plt.figure(1)
fg1.set_size_inches(w,h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.plot(t,PpL,'--',linewidth=0.5,color=clr1,label='Pp(t) Hipotenso')
plt.plot(t,PpN,'-',linewidth=0.5,color=clr2,label='Pp(t) Normotenso')
plt.plot(t,PpH,':',linewidth=0.5,color=clr3,label='Pp(t) Hipertenso')
plt.xlim(0,15); plt.xticks(np.arange(0,16,1))
plt.ylim(-0.4,1.2); plt.yticks(np.arange(-0.4,1.2,0.2))
plt.xlabel('t [s]')
plt.ylabel('Pp(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=3,frameon=False)
plt.show()
fg1.savefig('Individuos_python.pdf',bbox_inches='tight')
    
fg2 = plt.figure(2)  
fg2.set_size_inches(w,h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.plot(t,PpN,'-',linewidth=0.5,color=clr2,label='Pp(t) Normotenso')
plt.plot(t,PpL,'--',linewidth=0.5,color=clr1,label='Pp(t) Hipotenso')
plt.plot(t,PIDL,':',linewidth=0.5,color=clr4,label='PID(t) Hipotenso')
plt.xlim(0,15); plt.xticks(np.arange(0,16,1))
plt.ylim(-0.4,1.2); plt.yticks(np.arange(-0.4,1.2,0.2))
plt.xlabel('t [s]')
plt.ylabel('Pp(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=3,frameon=False)
plt.show()
fg2.savefig('Hipotenso_python.pdf',bbox_inches='tight')

fg3 = plt.figure(3)
fg3.set_size_inches(w,h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.plot(t,PpN,'-',linewidth=0.5,color=clr2,label='Pp(t) Normotenso')
plt.plot(t,PpH,'--',linewidth=0.5,color=clr3,label='Pp(t) Hipertenso')
plt.plot(t,PIDH,':',linewidth=0.5,color=clr4,label='PID(t) Hipertenso')
plt.xlim(0,15); plt.xticks(np.arange(0,16,1))
plt.ylim(-0.4,1.2); plt.yticks(np.arange(-0.4,1.2,0.2))
plt.xlabel('t [s]')
plt.ylabel('Pp(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=3,frameon=False)
plt.show()
fg3.savefig('Hipertenso_python.pdf',bbox_inches='tight')

