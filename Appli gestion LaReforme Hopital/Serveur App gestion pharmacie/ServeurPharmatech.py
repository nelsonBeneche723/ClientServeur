#::::::Serveur Pharmatech::::::::::::::::
#::::Code Source::::::::::::::
# ING Beneche Nelson:::::::::::::::::::::
# *-* coding:utf-8 *-*
#Creation du serveur
import Pyro4,Pyro5
import socket
from PIL import Image,ImageTk
from pystray import MenuItem,Icon
import pystray
from Utilisateur import Utilisateur
from Patient import Patient
from Consultation import Consultation
from Medicament import Medicament
from Achat import Achat
from Vente import Vente
from Employe import Employe
from Absence import Absence
import tkinter   
from tkinter import messagebox
import win10toast,pickle
import os
#Couleur en arriere plan
os.system('Color b')

## Demarrer automatiquement le demon(un programme qui rend service).
os.startfile('naming.exe')
#os.startfile('naming.exe')
name=socket.gethostname() #le nom hote de la machine client
ip=socket.gethostbyname(name) # Afficher l'adresse ip de la machine du client

#1-Creation de demon (ce demon va ren)
daemon=Pyro4.Daemon(host=ip,port=1234) #l'adresse ip et le port d'ecoute du serveur d'application. passerelle par defaut du routeur :192.168.10.1
#2-Passer la classe au demon, nom du serveur
uri=daemon.register(Utilisateur)
uripat=daemon.register(Patient)
uriconsul=daemon.register(Consultation)
urimedic=daemon.register(Medicament)
uriach=daemon.register(Achat)
urivt=daemon.register(Vente)
uriemp=daemon.register(Employe)
uriab=daemon.register(Absence)
#3-Nom du serveur
ns=Pyro4.locateNS()
ns.register('pharmaut',uri) # ce nom de pharma permet de faire la liaison entre l'application client et l'application serveur.
ns.register('pharmapat',uripat)
ns.register('pharmaconsul',uriconsul)
ns.register('pharmaMedic',urimedic)
ns.register('pharmaAch',uriach)
ns.register('pharmavt',urivt)
ns.register('pharmaEmp',uriemp)
ns.register('pharmaAbs',uriab)

#5-Attente de l'appel du client
print("-------------Demarrage du serveur de l'Hopital La Reforme------------------")
print("--------------------Rapport des utilisateurs--------------------------------")
daemon.requestLoop()









#os.system('python -m Pyro4.naming --host=10.12.31.204')















#def Stopper():
    #if messagebox.askyesnocancel('Message','Voulez-vous arreter le serveur?'):
        #fen.destroy()

#lbtit.grid(row=0,column=1)
#lb.grid(row=1,column=0)
#butdem.grid(row=2,column=0)


##def notification():
##wm=win10toast.LoadIcon('')
##wm.show_toast('hello')
#fen.protocol('WM_DELETE_WINDOW',Stopper)    

    
#img=Image.open('Images/pha1.ico')    
#menu=(MenuItem('Demarrage du serveur',Demarrer),MenuItem('Stopper',Stopper))
#icon=Icon('name',img,'name',menu)
#icon.run()

#if __name__=='__main__':
    #Demarrer()
#fen.mainloop()