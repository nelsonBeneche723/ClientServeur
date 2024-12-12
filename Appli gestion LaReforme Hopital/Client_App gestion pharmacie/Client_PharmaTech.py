# *-* coding: utf-8 *-*
import Pyro4
import sqlite3
import random
import os,re
import time, io
import pickle
import base64
import hashlib
import webbrowser
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A0,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10, letter,landscape,inch
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY,TA_LEFT,TA_RIGHT

#import pymysql
global ut,pat

#Connection client au serveur d'application de pharmatech
ns=Pyro4.locateNS()
uri=ns.lookup('pharmaut') #nom du serveur permet de faire la liaison avec les methodes exposes pour les utilisateurs a distantes.
uripat=ns.lookup('pharmapat') #pour le patient 
uriconsult=ns.lookup('pharmaconsul')
urimedic=ns.lookup('pharmaMedic')
uriach=ns.lookup('pharmaAch')
urivt=ns.lookup('pharmavt')
uriemp=ns.lookup('pharmaEmp')
uriab=ns.lookup('pharmaAbs')

ut=Pyro4.Proxy(uri) #Objet distant pour l'utilisateur
pat=Pyro4.Proxy(uripat) #objet distant pour le patient
consul=Pyro4.Proxy(uriconsult) #objet distant pour la consultation
medic=Pyro4.Proxy(urimedic) #objet distant pour la classe medicament
ach=Pyro4.Proxy(uriach) #objet distant pour la classe achat
vent=Pyro4.Proxy(urivt) #objet distant pour la classe de vente
emp=Pyro4.Proxy(uriemp)
abs=Pyro4.Proxy(uriab)

# importation des modules
import tkinter
from PIL import Image,ImageTk,ImageFile
from tkinter import messagebox
from tkcalendar import DateEntry,Calendar
from tkinter import ttk
import sqlite3
import random
import datetime
from tkinter import filedialog

class FenPrincipalePharmatech:
    def __init__(self):
        #self.master=master
                
        app=tkinter.Tk()
        app.title('Connexion au Système Hopital la Reforme')
        app.iconbitmap('Images/pharmacie.ico')
        
        #declaration de menu
        main=tkinter.Menu(app)
        menu1=tkinter.Menu(main,tearoff=0)
        def fenconnection():
            global txtnomut,txtmot,butc
            fen=tkinter.Toplevel(app) #fenetre fille
            fen.title('Fenetre de connexion')
            fen.iconbitmap('Images/Admin-icon.ico')
            larg=300
            haut=110
            largecran=fen.winfo_screenwidth()
            hautecran=fen.winfo_screenheight()
            x=(largecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fen.geometry('%dx%d+%d+%d'%(larg,haut,x,y))
            fen.resizable(height=False,width=False)
            fen.transient(app)# rendre modale la fenetre
            lb=tkinter.Label(fen,text='Connexion au systeme')
            lbnomut=tkinter.Label(fen,text='Nom utilisateur:')
            nomu=tkinter.StringVar()
            motp=tkinter.StringVar()
            txtnomut=tkinter.Entry(fen,textvariable=nomu,width=30)
            lbmot=tkinter.Label(fen,text='Mot de passe:')
            txtmot=tkinter.Entry(fen,textvariable=motp,width=30,show='*') 
            butc=tkinter.Button(fen,text='Connecter',command=lambda:Connexion())
            buta=tkinter.Button(fen,text='Annuler')
            txtnomut.focus()
            lb.grid(row=0,column=1,padx=2,pady=2)
            lbnomut.grid(row=1,column=0,padx=2,pady=2)
            txtnomut.grid(row=1,column=1,padx=2,pady=2)
            lbmot.grid(row=2,column=0,padx=2,pady=2)
            txtmot.grid(row=2,column=1,padx=2,pady=2)  
            butc.grid(row=3,column=0)
            buta.grid(row=3,column=1)
            fen.mainloop()
        
        def Connexion():
            global txtnomut,txtmot
            global ut
            nomutilisateur=txtnomut.get()
            motpas=txtmot.get()
            motpas=motpas.encode()
            motpasse=hashlib.sha1(motpas).hexdigest()
            try:
                if nomutilisateur=='':
                    messagebox.showerror('Echec','le champ nom utilisateur est vide')
                elif motpasse=='':
                    messagebox.showerror('Echec','le champ mot de passe est vide.')
                else:
                    uti=ut.ConnexionUtilisateur(nomutilisateur,motpasse) #methode de connexion de l'utilisateur
                    if uti!=0: #Si la methode contient des donnees..
                        if uti[0][6]=='administrateur système':
                            app.withdraw()
                            FenGestionUtilisateur()
                        elif uti[0][6]=="administrateur d'entreprise":
                            app.withdraw()
                            Fenprincipale()
                        elif uti[0][6]=='Docteur':
                            app.withdraw()
                            #ajouter la methode principale

                            #messagebox.showerror('Info','pas encore disponible')
                    else:
                        tkinter.messagebox.showerror('Echec de connexion','compte utilisateur refusé')
            except Pyro4.core.errors.ConnectionClosedError:
                messagebox.showerror('Echec de connexion','Le serveur est eteint.')

                               
        def Fenprincipale():
            global fenp
            fenp=tkinter.Tk()
            fenp.title('Hopital-La REFORME')
            fenp.iconbitmap('Images/784072.ico')
            #creation du menu de la fenetre principale
            mainmenu=tkinter.Menu(fenp)
            menu1=tkinter.Menu(mainmenu,tearoff=0)
            menu2=tkinter.Menu(mainmenu,tearoff=0)
            menu3=tkinter.Menu(mainmenu,tearoff=0)
            menu4=tkinter.Menu(mainmenu,tearoff=0)
            menu5=tkinter.Menu(mainmenu,tearoff=0)
            menu6=tkinter.Menu(mainmenu,tearoff=0)
            menu7=tkinter.Menu(mainmenu,tearoff=0)
            menu8=tkinter.Menu(mainmenu,tearoff=0)
            
            imgg=Image.open('Images/img_43443.png')
            im2=ImageTk.PhotoImage(imgg.resize((12,12)),master=fenp) 
            imgg3=Image.open('Images/Doctor3-512.png')
            im3=ImageTk.PhotoImage(imgg3.resize((12,12)),master=fenp) 
            imgg4=Image.open('Images/ba31d0bd9e.png')
            im4=ImageTk.PhotoImage(imgg4.resize((12,12)),master=fenp)
            imgg5=Image.open('Images/pngtree-elemental-design-of-nurse-care-for-patients-in-cartoon-hospital-png-image_4011893.jpg')
            im5=ImageTk.PhotoImage(imgg5.resize((12,12)),master=fenp)            
            imgg6=Image.open('Images/8c8b3766126753c6d098cdb2e42cff49.png')
            im6=ImageTk.PhotoImage(imgg6.resize((12,12)),master=fenp)            
            imgg7=Image.open('Images/Pharmacie-logo.jpg')
            im7=ImageTk.PhotoImage(imgg7.resize((12,12)),master=fenp)            
            imgg8=Image.open('Images/unnamed.png')
            im8=ImageTk.PhotoImage(imgg8.resize((12,12)),master=fenp)                       
            imgg9=Image.open('Images/784072.png')
            im9=ImageTk.PhotoImage(imgg9.resize((15,15)),master=fenp)            
            imgg10=Image.open('Images/acroread.png')
            im10=ImageTk.PhotoImage(imgg10.resize((15,15)),master=fenp) 
            imgg11=Image.open('Images/PinClipart.com_exhaust-pipe-clipart_1505094(2).png')
            im11=ImageTk.PhotoImage(imgg11.resize((15,15)),master=fenp) 
            imgg12=Image.open('Images/kdict2.png')
            im12=ImageTk.PhotoImage(imgg12.resize((15,15)),master=fenp) 
             
            
            menu1.add_command(label='Creer dossier',command=lambda: FenCreerPatient(),image=im2,compound='left',accelerator="Ctrl+C")
            menu1.add_command(label='Rechercher',command=lambda:FenRechercherPatient(),image=im3,compound='left',accelerator="Ctrl+R")
            menu1.add_command(label='Modifier',command=lambda:ModifierPatient(),image=im4,compound='left',accelerator="Ctrl+M")
            menu1.add_separator()
            menu1.add_command(label='Lister',image=im5,compound='left',command=lambda:FenListPatient(),accelerator="Ctrl+L")
            
            menu2.add_command(label='Consulter',command=lambda:Consultation(),image=im6,compound='left')
            menu2.add_command(label='Modifier',image=im7,compound='left',command=lambda:FenModifierConsul())
            menu2.add_separator()
            #menu2.
            #Sous menu dans le menu 2----
            sub=tkinter.Menu(menu2,tearoff=0)
            sub.add_command(label='Afficher tout de la journée',underline=0,command=lambda:FenListToutConsul())
            menu2.add_cascade(label='Afficher',menu=sub,image=im11,compound='left')

            menu3.add_command(label='Embaucher',command=lambda:FenEmbaucherEmp())
            menu3.add_command(label='Rechercher',command=lambda:FenRechercherEmp())
            menu3.add_command(label='Modifier',command=lambda:FenModifierEmp())
            menu3.add_separator()
            menu3.add_command(label="Revoquer",command=lambda:FenrevocationEmploye())
            #menu2.add_command(label='Rechercher info sur un patient')
            menu4.add_command(label='Effectuer',command=lambda:FenEffectuerAchat())
            # menu4.add_command(label='Rechercher',command='')
            menu4.add_command(label='Lister',command=lambda:FenListeAchat())
            menu5.add_command(label='Effectuer',command=lambda:FenEffectuerVente())
            menu6.add_command(label='Mentionner',command=lambda:FenMentionAbs())
            # menu6.add_command(label='Ajouter une evenement')
            menu7.add_command(label='Enregistrer nouveau',command=lambda:FenEnregistrerMedicament(),image=im8,compound='left',accelerator="Ctrl+E")
            menu7.add_command(label='Rechercher',command=lambda:FenRechercherMedicament(),accelerator="Ctrl+S",image=im12,compound='left')
            menu8.add_command(label='A propos du logiciel',command=lambda:AideLog(),image=im9,compound='left')
            #def LireDocument(event):
                #os.startfile('GuideUtilisateur.pdf')            
                #fen=tkinter.Tk()
                #fen.mainloop()
                
            #menu8.add_command(label='Documentation',image=im10,compound='left',command=lambda :LireDocument)
            
            mainmenu.add_cascade(label='Patient',menu=menu1)
            mainmenu.add_cascade(label='Medicament',menu=menu7)
            mainmenu.add_cascade(label='Consultation',menu=menu2)
            mainmenu.add_cascade(label='Employe',menu=menu3)
            mainmenu.add_cascade(label='Achat',menu=menu4)
            mainmenu.add_cascade(label='Vente',menu=menu5)
            mainmenu.add_cascade(label='Absence',menu=menu6)
            mainmenu.add_cascade(label='Aide',menu=menu8)
            #Menu raccourci
            lbmenu=tkinter.Label(fenp,text='Menu raccourci',fg='Green',font=('',12,'bold'))
            butcr=tkinter.Button(fenp,text='Creer un patient',bg='white',width=35,cursor='hand2',command=lambda:FenCreerPatient())
            butr=tkinter.Button(fenp,text='Rechercher un patient',bg='white',width=35,cursor='hand2',command=lambda:FenRechercherPatient())
            butc=tkinter.Button(fenp,text='Consulter un patient',bg='white',width=35,cursor='hand2',command=lambda:Consultation())
            buta=tkinter.Button(fenp,text='Effectuer un achat',bg='white',width=35,cursor='hand2',command=lambda:FenEffectuerAchat())
            bute=tkinter.Button(fenp,text='Effectuer une vente',bg='white',width=35,cursor='hand2',command=lambda:FenEffectuerVente())
            butm=tkinter.Button(fenp,text='Mentionner une absence',bg='white',width=35,cursor='hand2',command=lambda:FenMentionAbs())
            # butcr=tkinter.Button(fenp,text='Creer un patient')
            # butcr=tkinter.Button(fenp,text='Creer un patient')
            # butcr=tkinter.Button(fenp,text='Creer un patient')
            # butcr=tkinter.Button(fenp,text='Creer un patient')

            #Image en arriere-plan
            img=Image.open('Images/784072.png')
            im=ImageTk.PhotoImage(img.resize((1200,800)),master=fenp)
            lb=tkinter.Label(fenp,image=im)
            lb.im=im
            lbmenu.grid(row=0, column=0, padx=5, pady=5)
            butcr.grid(row=1, column=0, padx=5, pady=5)
            butr.grid(row=2, column=0, padx=5, pady=5)
            butc.grid(row=3, column=0, padx=5, pady=5)
            buta.grid(row=4, column=0, padx=5, pady=5)
            bute.grid(row=5, column=0, padx=5, pady=5)
            butm.grid(row=6, column=0, padx=5, pady=5)
            lb.grid(row=0, column=1, rowspan=35, columnspan=35, sticky=('N','W','E','S'))
            
            fenp.config(menu=mainmenu)
            fenp.state('zoomed')
            def Fermerapp():
                if messagebox.askyesnocancel('Quitter',"Voulez-vous fermer l'application Hopital la REFORME? \n Sauvegarder tout votre travail avant de cliquer sur oui."):
                    fenp.destroy()
                    print('Deconnexion du systeme:')
            fenp.protocol("WM_DELETE_WINDOW",lambda:Fermerapp())
            #Les Touches de combinaison#
            fenp.bind('<Control-c>',FenCreerPatt) #1
            fenp.bind('<Control-r>',FenRechercherPatt) #2
            fenp.bind('<Control-m>',ModifierPatt) #3
            fenp.bind('<Control-l>',FenListPatt) #4
            fenp.bind('<Control-s>',FenRechercherMedic) #5
            fenp.bind('<Control-e>',FenEnregistrerMedic) #6
            fenp.mainloop()
        
        def FenGestionUtilisateur():
            appli=tkinter.Tk()
            appli.title('Gestion des utilisateurs')
            tabcontrol=tkinter.ttk.Notebook(appli) #creation d'une tab de control pour va permet des ajouter des elements
            tab1=tkinter.Frame(tabcontrol)
            tab2=tkinter.Frame(tabcontrol)
            tab3=tkinter.Frame(tabcontrol)
            tabcontrol.add(tab1,text='Enregistrer')
            
            lbtit=tkinter.Label(tab1,text='Nouveau Utilisateur',font=('',11,'bold'))
            lbnom=tkinter.Label(tab1,text='Nom')
            txtnom=tkinter.Entry(tab1,width=30)
            lbprenom=tkinter.Label(tab1,text='Prenom')
            txtprenom=tkinter.Entry(tab1,width=30)
            lbsexe=tkinter.Label(tab1,text='Sexe')
            cmbsexe=tkinter.ttk.Combobox(tab1,values=("Masculin",'Feminin'),width=27)
            lbnomut=tkinter.Label(tab1,text='Nom utilisateur')
            txtnomut=tkinter.Entry(tab1,width=30)
            lbmot=tkinter.Label(tab1,text='Mot de passe')
            txtmot=tkinter.Entry(tab1,width=30,show="*")
            lbfonc=tkinter.Label(tab1,text='Fonction')
            cmbfon=tkinter.ttk.Combobox(tab1,values=("Administrateur","Administrateur d'entreprise","Secretaire","Docteur","Technicien(ne) de laboratoire","Infirmier(e)"),width=27)
            lbph=tkinter.Label(tab1,text='Photo')
            def parcourir():
                chemin=filedialog.askopenfilename(initialdir='/',filetypes=(('jpeg files','*.jpg'),('All files','*.*')))
                im=Image.open(chemin)
                imj=ImageTk.PhotoImage(im.resize((320,290)),master=appli)
                lb=tkinter.Label(tab1,image=imj)
                lb.imj=imj
                lb.grid(row=5,column=3)
                
            butparc=tkinter.Button(tab1,text='Selectionner une photo',command=lambda:parcourir())
            buten=tkinter.Button(tab1,text='Enregistrer')
            butann=tkinter.Button(tab1,text='Annuler')
            
            tabcontrol.add(tab2,text='Rechercher')
            lbcode=tkinter.Label(tab2,text="Code de l'utilisateur")
            txtcode=tkinter.Entry(tab2,width=30)
            butrech=tkinter.Button(tab2,text='Rechercher',command=lambda:RecherchUt())
            lbno=tkinter.Label(tab2)
            txtlbnom=tkinter.Label(tab2)
            lbpreno=tkinter.Label(tab2)
            txtlbpreno=tkinter.Label(tab2)   
            lbsex=tkinter.Label(tab2)
            txtlbsex=tkinter.Label(tab2)  
            lbnomutt=tkinter.Label(tab2)
            txtlbnomutt=tkinter.Label(tab2)  
            lbmotp=tkinter.Label(tab2)
            txtlbmotp=tkinter.Label(tab2)   
            lbfonct=tkinter.Label(tab2)
            txtlbfonc=tkinter.Label(tab2) 
            lbphot=tkinter.Label(tab2)
            txtlbpho=tkinter.Label(tab2)    
            lbda=tkinter.Label(tab2)
            txtlbda=tkinter.Label(tab2)                
            def RecherchUt():
                codeut=txtcode.get()
                rech=ut.RechercherUt(codeut)
                if rech!=0:
                    lbno.configure(text='Nom:',font=('',9,'bold'))
                    lbno.grid(row=1,column=0)
                    txtlbnom.configure(text=rech[0][1].upper())
                    txtlbnom.grid(row=1,column=1)                    
                    lbpreno.configure(text='Prenom:',font=('',9,'bold'))
                    lbpreno.grid(row=1,column=2)
                    txtlbpreno.configure(text=rech[0][2])
                    txtlbpreno.grid(row=1,column=3)
                    lbsex.configure(text='Sexe:',font=('',9,'bold'))
                    lbsex.grid(row=2,column=0)
                    txtlbsex.configure(text=rech[0][3])
                    txtlbsex.grid(row=2,column=1)
                    lbnomutt.configure(text='Nom-utilisateur:',font=('',9,'bold'))
                    lbnomutt.grid(row=2,column=2)
                    txtlbnomutt.configure(text=rech[0][4])
                    txtlbnomutt.grid(row=2,column=3)
                    lbmotp.configure(text='Mot de passe:',font=('',9,'bold'))                    
                    lbmotp.grid(row=3,column=0)
                    txtlbmotp.configure(text='*********************')
                    txtlbmotp.grid(row=3,column=1)
                    lbfonct.configure(text='Fonction:',font=('',9,'bold'))                    
                    lbfonct.grid(row=3,column=2)
                    txtlbfonc.configure(text=rech[0][6])
                    txtlbfonc.grid(row=3,column=3)
                    lbphot.configure(text='Photo',font=('',9,'bold'))
                    lbphot.grid(row=4,column=0)
                    lbda.configure(text='Date creation:',font=('',9,'bold'))
                    lbda.grid(row=4,column=2)
                    txtlbda.configure(text=rech[0][8])
                    txtlbda.grid(row=4,column=3)                    
                    os.chdir('./') #repertoire courant
                    phot=rech[0][7].encode('utf-8') #prendre le chaine de caractere et coder la valeur en binaire
                    with open('{}.png'.format(rech[0][1]),'wb') as file:
                        file_photo=base64.decodebytes(phot)
                        file.write(file_photo)
                        file.flush() # permet d'ecrire et de lire un fichier binaire en meme temps
                        ImageFile.LOAD_TRUNCATED_IMAGES=True # Pour lire les images de plus que 7 bytes de taille
                        n_im=rech[0][1]+'.png'
                        imgg=Image.open(n_im)
                        imm=ImageTk.PhotoImage(imgg.resize((300,200)),master=tab2)
                        txtlbpho.configure(image=imm)
                        txtlbpho.imm=imm
                        txtlbpho.grid(row=4,column=1)
                        file.close()
                        os.remove(n_im) #supprimer le fichier
                    
                    
                    
            
            lbcode.grid(row=0,column=0)
            txtcode.grid(row=0,column=1)
            butrech.grid(row=0,column=2)
              
             
            tabcontrol.add(tab3,text='Lister')
            
            lbtitr=tkinter.Label(tab3,text='Liste de tous les utilisateurs du systeme')
            tr=tkinter.ttk.Treeview(tab3,columns=('Identifiant','Nom','Prenom','Sexe','Nom-utilisateur','Mot de passe','Fonction','Date-creation'),show='headings')
            tr.heading('Identifiant',text='Identifiant')
            tr.heading('Nom',text='Nom')
            tr.heading('Prenom',text='Prenom')
            tr.heading('Sexe',text='Sexe')
            tr.heading('Nom-utilisateur',text='Nom-utilisateur')
            tr.heading('Mot de passe',text='Mot de passe')
            tr.heading('Fonction',text='Fonction')
            tr.heading('Date-creation',text='Date-creation')
            
            tr.column('Identifiant',width=100)
            tr.column('Nom',width=100)
            tr.column('Prenom',width=100)
            tr.column('Sexe',width=100)
            tr.column('Nom-utilisateur',width=100)
            tr.column('Mot de passe',width=200)
            tr.column('Fonction',width=150)
            tr.column('Date-creation',width=100)  
            #Remplir le champ treeview avec les donnees utilisateurs
            lis=ut.ListerUtilisateur()
            # l'objet lis retourne les valeurs sous multiples tuples, dans ce cas on doit recuperer les valeurs dans chaque tuple, selon la position de l'attribut...
            code=[x[0] for x in lis] # on recupere ses donnees sous forme de liste
            nom=[x[1] for x in lis]
            prenom=[x[2] for x in lis]
            sexe=[x[3]for x in lis]
            nomutilisateur=[x[4] for x in lis]
            motpasse='********************'
            fonction=[x[6] for x in lis]
            datecreation=[x[7] for x in lis]
            #boucle qui va permet d'afficher les valeurs dans le treeview
            for c,n,p,s,nomut,fonc,dtec in zip(code,nom,prenom,sexe,nomutilisateur,fonction,datecreation): #zip permet de fusionner deux listes et l'afficher en colonne
              
                tr.insert('','end',values=(c,n,p,s,nomut,motpasse,fonc,dtec)) #inserer les valeurs dans le treeview
            
            tabcontrol.grid(row=0,column=0)
            lbtit.grid(row=1,column=3)
            lbnom.grid(row=2,column=0,padx=6,pady=6)
            txtnom.grid(row=2,column=1,padx=6,pady=6)
            lbprenom.grid(row=3,column=0,padx=6,pady=6)
            txtprenom.grid(row=3,column=1,padx=6,pady=6)
            lbsexe.grid(row=4,column=0,padx=6,pady=6)
            cmbsexe.grid(row=4,column=1,padx=6,pady=6)
            lbnomut.grid(row=2,column=3,padx=6,pady=6)
            txtnomut.grid(row=2,column=4,padx=6,pady=6)
            lbmot.grid(row=3,column=3,padx=6,pady=6)
            txtmot.grid(row=3,column=4,padx=6,pady=6)
            lbfonc.grid(row=4,column=3,padx=6,pady=6)
            cmbfon.grid(row=4,column=4,padx=6,pady=6)
            lbph.grid(row=5,column=2)
            img=Image.open('Images/Admin-icon.png')
            im=ImageTk.PhotoImage(img.resize((320,290)),master=appli)
            lb=tkinter.Label(tab1,image=im)
            lb.grid(row=5,column=3)
            
            butparc.grid(row=5,column=4)
            buten.grid(row=6,column=2)
            butann.grid(row=6,column=4)
            
            tr.grid(row=1,column=0)
            
            appli.state('zoomed')
            appli.mainloop()
        def FenCreerPatient():
            global fenp,fen,txtnom,txtprenom,cmbsexe,txtadr,txttel,txtass,txtass1,txtdate,txtetat,txtnumpers,txtpers,txtprof,txttyp,txtent,cmbgr,chemin,lbpho,assure
            fen=tkinter.Toplevel(fenp)
            fen.title("Enregistrer nouveau patient")
            fen.iconbitmap('Images/img_43443.ico')
            larg=910
            haut=520
            largeecran=fen.winfo_screenwidth()
            hautecran=fen.winfo_screenheight()
            x=(largeecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fen.geometry('%dx%d+%d+%d' % (larg,haut,x,y))     
            
            lb=tkinter.Label(fen,text='Enregistrer Information Patient',font=('arial',16,'bold'),foreground='green')
            lbnom=tkinter.Label(fen,text='Nom')
            lbprenom=tkinter.Label(fen,text='Prenom')
            lbsexe=tkinter.Label(fen,text='Sexe')
            lbdate=tkinter.Label(fen,text='Date de naissance')
            lbad=tkinter.Label(fen,text='Adresse')
            lbtel=tkinter.Label(fen,text='Telephone')
            lbetat=tkinter.Label(fen,text='Etat matrimonial')
            lbgr=tkinter.Label(fen,text='Groupe sanguin')
            lbpers=tkinter.Label(fen,text='Personne responsable')
            lbnumper=tkinter.Label(fen,text='Numero du responsable')
            lbprofes=tkinter.Label(fen,text='Profession') 
            lbtypass=tkinter.Label(fen,text='Type assurance')
            lbass=tkinter.Label(fen,text='Assuré')
            lba=tkinter.Label(fen,text='Entreprise assurée')
            
            lbphoto=tkinter.Label(fen,text='Photo',font=('arial',8,'bold'))
            imgg=Image.open('Images/img_43443.png')
            im=ImageTk.PhotoImage(imgg.resize((300,240)),master=fenp)
            lbpho=tkinter.Label(fen,image=im,background='white')
            lbpho.im=im
            
            #lbnom=tkinter.Label(fen,text='')
            txtnom=tkinter.Entry(fen,width=30)
            txtprenom=tkinter.Entry(fen,width=30)
            cmbsexe=tkinter.ttk.Combobox(fen,values=('Masculin','Feminin'),width=27)
            cmbsexe.configure(state='readonly')
            txtdate=DateEntry(fen,background='green',foreground='black',borderwidth=2,locale="fr_FR",width=27)
            txtadr=tkinter.Entry(fen,width=30)
            txttel=tkinter.Entry(fen,width=30)
            txttel.insert(tkinter.INSERT,'(+509)-')
            txtetat=tkinter.ttk.Combobox(fen,values=('Celibataire','Fiancé(e)','Veuf(ve)','Marie(e)','Divorcé'),width=27)
            txtetat.configure(state='readonly')
            cmbgr=tkinter.ttk.Combobox(fen,values=('A+','A-','B','B+','B-','O-','O+'),width=27)
            cmbgr.configure(state='readonly')
            txtpers=tkinter.Entry(fen,width=30) 
            txtnumpers=tkinter.Entry(fen,width=30)
            txtnumpers.insert(tkinter.INSERT,'(+509)-')
            assure=tkinter.StringVar()
            txtass=tkinter.ttk.Radiobutton(fen,value='Oui',text='Oui',variable=assure)
            txtass1=tkinter.ttk.Radiobutton(fen,value='Non',text='Non',variable=assure)
            txttyp=tkinter.ttk.Combobox(fen,width=27)
            txttyp.insert(0,'Assurance maladie')
            txttyp.configure(state='readonly')
            txtprof=tkinter.Entry(fen,width=30)
            txtent=tkinter.Entry(fen,width=30)
            txtasR=tkinter.Entry(fen,width=30)
            
            butpar=tkinter.Button(fen,text='Parcourir',command=lambda:Parcourir())
            butEn=tkinter.Button(fen,text='Enregistrer',command=lambda:Enregistrerpatient())
            butA=tkinter.Button(fen,text='Annuler')
            
            def Parcourir():
                global chemin,lbpho
                chemin=filedialog.askopenfilename(initialdir='/',title='Ajouter un photo pour le patient',filetype=(('jpeg files','*.jpg'),('All files','*.*')))
                im=Image.open(chemin)
                imm=ImageTk.PhotoImage(im.resize((300,240)),master=fen)
                lbpho=tkinter.Label(fen,image=imm)
                lbpho.imm=imm
                lbpho.grid(row=9,column=3,rowspan=10,columnspan=10)
                
            lb.grid(row=0,column=3)
            lbnom.grid(row=1,column=0,padx=3,pady=3)
            txtnom.grid(row=1,column=1,padx=3,pady=3)
            lbprenom.grid(row=1,column=3,padx=3,pady=3)
            txtprenom.grid(row=1,column=4,padx=3,pady=3)
            lbsexe.grid(row=2,column=0,padx=3,pady=3)
            cmbsexe.grid(row=2,column=1,padx=3,pady=3)
            lbdate.grid(row=2,column=3,padx=3,pady=3)
            txtdate.grid(row=2,column=4,padx=3,pady=3)
            lbad.grid(row=3,column=0,padx=3,pady=3)
            txtadr.grid(row=3,column=1,padx=3,pady=3)
            lbtel.grid(row=3,column=3,padx=3,pady=3)
            txttel.grid(row=3,column=4,padx=3,pady=3)  
            lbetat.grid(row=4,column=0,padx=3,pady=3)
            txtetat.grid(row=4,column=1,padx=3,pady=3)
            lbgr.grid(row=4,column=3,padx=3,pady=3)
            cmbgr.grid(row=4,column=4,padx=3,pady=3)
            lbpers.grid(row=5,column=0,padx=3,pady=3)
            txtpers.grid(row=5,column=1,padx=3,pady=3)
            lbnumper.grid(row=5,column=3,padx=3,pady=3)
            txtnumpers.grid(row=5,column=4,padx=3,pady=3)
            lbtypass.grid(row=8,column=0,padx=3,pady=3)
            txttyp.grid(row=8,column=1,padx=3,pady=3)
            lbprofes.grid(row=8,column=3,padx=3,pady=3)
            txtprof.grid(row=8,column=4,padx=15,pady=15)
            lbphoto.grid(row=11,column=1)
            lba.grid(row=9,column=0,padx=5,pady=5)
            txtent.grid(row=9,column=1,padx=5,pady=5)
            lbpho.grid(row=9,column=3,rowspan=10,columnspan=10)
            butpar.grid(row=9,column=5,rowspan=7,columnspan=7)
            butEn.grid(row=22,column=0,rowspan=21,columnspan=21)
            butA.grid(row=22,column=4,rowspan=21,columnspan=21)
            #fen.configure(background='white')
            fen.transient(fenp)
            fen.resizable(height=False,width=False)
            fen.mainloop()
        def FenCreerPatt(event):
        
            global fenp,fen,txtnom,txtprenom,cmbsexe,txtadr,txttel,txtass,txtass1,txtdate,txtetat,txtnumpers,txtpers,txtprof,txttyp,txtent,cmbgr,chemin,lbpho,assure
            fen=tkinter.Toplevel(fenp)
            fen.title("Enregistrer nouveau patient")
            fen.iconbitmap('Images/img_43443.ico')
            larg=910
            haut=520
            largeecran=fen.winfo_screenwidth()
            hautecran=fen.winfo_screenheight()
            x=(largeecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fen.geometry('%dx%d+%d+%d' % (larg,haut,x,y))     
            
            lb=tkinter.Label(fen,text='Enregistrer Information Patient',font=('arial',16,'bold'),foreground='green')
            lbnom=tkinter.Label(fen,text='Nom')
            lbprenom=tkinter.Label(fen,text='Prenom')
            lbsexe=tkinter.Label(fen,text='Sexe')
            lbdate=tkinter.Label(fen,text='Date de naissance')
            lbad=tkinter.Label(fen,text='Adresse')
            lbtel=tkinter.Label(fen,text='Telephone')
            lbetat=tkinter.Label(fen,text='Etat matrimonial')
            lbgr=tkinter.Label(fen,text='Groupe sanguin')
            lbpers=tkinter.Label(fen,text='Personne responsable')
            lbnumper=tkinter.Label(fen,text='Numero du responsable')
            lbprofes=tkinter.Label(fen,text='Profession') 
            lbtypass=tkinter.Label(fen,text='Type assurance')
            lbass=tkinter.Label(fen,text='Assuré')
            lba=tkinter.Label(fen,text='Entreprise assurée')
            
            lbphoto=tkinter.Label(fen,text='Photo',font=('arial',8,'bold'))
            imgg=Image.open('Images/img_43443.png')
            im=ImageTk.PhotoImage(imgg.resize((300,240)),master=fenp)
            lbpho=tkinter.Label(fen,image=im,background='white')
            lbpho.im=im
            
            #lbnom=tkinter.Label(fen,text='')
            txtnom=tkinter.Entry(fen,width=30)
            txtprenom=tkinter.Entry(fen,width=30)
            cmbsexe=tkinter.ttk.Combobox(fen,values=('Masculin','Feminin'),width=27)
            cmbsexe.configure(state='readonly')
            txtdate=DateEntry(fen,background='green',foreground='black',borderwidth=2,locale="fr_FR",width=27)
            txtadr=tkinter.Entry(fen,width=30)
            txttel=tkinter.Entry(fen,width=30)
            txttel.insert(tkinter.INSERT,'(+509)-')
            txtetat=tkinter.ttk.Combobox(fen,values=('Celibataire','Fiancé(e)','Veuf(ve)','Marie(e)','Divorcé'),width=27)
            txtetat.configure(state='readonly')
            cmbgr=tkinter.ttk.Combobox(fen,values=('A+','A-','B','B+','B-','O-','O+'),width=27)
            cmbgr.configure(state='readonly')
            txtpers=tkinter.Entry(fen,width=30) 
            txtnumpers=tkinter.Entry(fen,width=30)
            txtnumpers.insert(tkinter.INSERT,'(+509)-')
            assure=tkinter.StringVar()
            txtass=tkinter.ttk.Radiobutton(fen,value='Oui',text='Oui',variable=assure)
            txtass1=tkinter.ttk.Radiobutton(fen,value='Non',text='Non',variable=assure)
            txttyp=tkinter.ttk.Combobox(fen,width=27)
            txttyp.insert(0,'Assurance maladie')
            txttyp.configure(state='readonly')
            txtprof=tkinter.Entry(fen,width=30)
            txtent=tkinter.Entry(fen,width=30)
            txtasR=tkinter.Entry(fen,width=30)
            
            butpar=tkinter.Button(fen,text='Parcourir',command=lambda:Parcourir())
            butEn=tkinter.Button(fen,text='Enregistrer',command=lambda:Enregistrerpatient())
            butA=tkinter.Button(fen,text='Annuler')
            
            def Parcourir():
                global chemin,lbpho
                chemin=filedialog.askopenfilename(initialdir='/',title='Ajouter un photo pour le patient',filetype=(('jpeg files','*.jpg'),('All files','*.*')))
                im=Image.open(chemin)
                imm=ImageTk.PhotoImage(im.resize((300,240)),master=fen)
                lbpho=tkinter.Label(fen,image=imm)
                lbpho.imm=imm
                lbpho.grid(row=9,column=3,rowspan=10,columnspan=10)
                
            lb.grid(row=0,column=3)
            lbnom.grid(row=1,column=0,padx=3,pady=3)
            txtnom.grid(row=1,column=1,padx=3,pady=3)
            lbprenom.grid(row=1,column=3,padx=3,pady=3)
            txtprenom.grid(row=1,column=4,padx=3,pady=3)
            lbsexe.grid(row=2,column=0,padx=3,pady=3)
            cmbsexe.grid(row=2,column=1,padx=3,pady=3)
            lbdate.grid(row=2,column=3,padx=3,pady=3)
            txtdate.grid(row=2,column=4,padx=3,pady=3)
            lbad.grid(row=3,column=0,padx=3,pady=3)
            txtadr.grid(row=3,column=1,padx=3,pady=3)
            lbtel.grid(row=3,column=3,padx=3,pady=3)
            txttel.grid(row=3,column=4,padx=3,pady=3)  
            lbetat.grid(row=4,column=0,padx=3,pady=3)
            txtetat.grid(row=4,column=1,padx=3,pady=3)
            lbgr.grid(row=4,column=3,padx=3,pady=3)
            cmbgr.grid(row=4,column=4,padx=3,pady=3)
            lbpers.grid(row=5,column=0,padx=3,pady=3)
            txtpers.grid(row=5,column=1,padx=3,pady=3)
            lbnumper.grid(row=5,column=3,padx=3,pady=3)
            txtnumpers.grid(row=5,column=4,padx=3,pady=3)
            lbtypass.grid(row=8,column=0,padx=3,pady=3)
            txttyp.grid(row=8,column=1,padx=3,pady=3)
            lbprofes.grid(row=8,column=3,padx=3,pady=3)
            txtprof.grid(row=8,column=4,padx=15,pady=15)
            lbphoto.grid(row=11,column=1)
            lba.grid(row=9,column=0,padx=5,pady=5)
            txtent.grid(row=9,column=1,padx=5,pady=5)
            lbpho.grid(row=9,column=3,rowspan=10,columnspan=10)
            butpar.grid(row=9,column=5,rowspan=7,columnspan=7)
            butEn.grid(row=22,column=0,rowspan=21,columnspan=21)
            butA.grid(row=22,column=4,rowspan=21,columnspan=21)
            #fen.configure(background='white')
            fen.transient(fenp)
            fen.resizable(height=False,width=False)
            fen.mainloop()     
        def Enregistrerpatient():
            global chemin,lbpho
            numerocarte=random.randint(0000000000,1000000000)
            nom=txtnom.get()
            prenom=txtprenom.get()
            sexe=cmbsexe.get()
            daten=txtdate.get()
            #conversion la date francaise en format anglaise
            datenaiss=datetime.datetime.strptime(daten,'%d/%m/%Y')
            datenaissance=datenaiss.date()
            ##############
            adresse=txtadr.get()
            telephone=txttel.get()
            etat_matrimoniale=txtetat.get()
            groupesanguin=cmbgr.get()
            personneresponsable=txtpers.get()
            numeropersonneresponsable=txtnumpers.get()
            asl=assure.get()
            profession=txtprof.get()
            typeassurance=txttyp.get()
            entreprise_assuree=txtent.get()
            d=datetime.date.today()
            dateenregistrer=d.strftime('%Y-%m-%d')
            datemodification=''
            
            #condition sur le bouton enregistrer patient
            if nom=='':
                messagebox.showerror('Avertissement','champ nom vide.')
            elif prenom=='':
                messagebox.showerror('Avertissement','champ prenom vide.')
            else:
                #Recuperer le chemin de la photo ,converti la photo en format de bytes en chaine de caracteres afin de stocker le fichier sous forme de blob dans une base de donnees..
                with open(chemin,'rb') as f: 
                    ph=base64.b64encode(f.read()) # encoder l'image de format bytes en binaire
                    photo=ph.decode('utf-8') # Retirer le format binaire pour la stocker dans une base de donnees sous forme chaine de caracteres.
                    #Appeler la methode creation de nouveau patient       
                    patie=pat.CreerPatient(numerocarte,nom,prenom,sexe,datenaissance,adresse,telephone,etat_matrimoniale,groupesanguin,personneresponsable,numeropersonneresponsable,typeassurance,entreprise_assuree,profession,photo,dateenregistrer,datemodification)
                    if patie!=0:
                        messagebox.showinfo('Information','Un patient a été enregistrée avec succès.\n Code du patient: '+str(numerocarte))
                    else:
                        messagebox.showerror('Avertissement',"echec d'enregistrement de patient.")
                        
        def FenRechercherPatient():
            global fenp,fen,txtnumcarte,txtnomR,txtprenomR,cmbsexeR,txtadrR,txttelR,txtassR,txtass1R,txtdateR,txtetatR,txtnumpersR,txtpersR,txtprofR,txttypR,txtasR,cmbgrR,chemin,lbphoR,assureR
            global fenrech
            fenrech=tkinter.Toplevel(fenp)
            fenrech.title("Fenetre de recherche sur patient")
            fenrech.iconbitmap('Images/doctoress.ico')
            larg=880
            haut=520
            largeecran=fenrech.winfo_screenwidth()
            hautecran=fenrech.winfo_screenheight()
            x=(largeecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fenrech.geometry('%dx%d+%d+%d' % (larg,haut,x,y))     
            
            lb=tkinter.Label(fenrech,text='Rechercher Information Patient',font=('arial',16,'bold'),foreground='green')
            lbnum=tkinter.Label(fenrech,text='Numero de carte')
            lbnom=tkinter.Label(fenrech,text='Nom')
            lbprenom=tkinter.Label(fenrech,text='Prenom')
            lbsexe=tkinter.Label(fenrech,text='Sexe')
            lbdate=tkinter.Label(fenrech,text='Date de naissance')
            lbad=tkinter.Label(fenrech,text='Adresse')
            lbtel=tkinter.Label(fenrech,text='Telephone')
            lbetat=tkinter.Label(fenrech,text='Etat matrimonial')
            lbgr=tkinter.Label(fenrech,text='Groupe sanguin')
            lbpers=tkinter.Label(fenrech,text='Personne responsable')
            lbnumper=tkinter.Label(fenrech,text='Numero du responsable')
            lbprofes=tkinter.Label(fenrech,text='Profession') 
            lbtypass=tkinter.Label(fenrech,text='Type assurance')
            lbentass=tkinter.Label(fenrech,text='Entreprise assurée')
            lbass=tkinter.Label(fenrech,text='Assure:')
            lbphoto=tkinter.Label(fenrech,text='Photo',font=('arial',8,'bold'))
            imgg=Image.open('Images/img_43443.png')
            im=ImageTk.PhotoImage(imgg.resize((300,240)),master=fenp)
            lbphoR=tkinter.Label(fenrech,image=im,background='white')
            lbphoR.im=im
            
            txtnomR=tkinter.Entry(fenrech,width=30)
            txtnumcarte=tkinter.Entry(fenrech,width=30)
            txtnumcarte.bind('<Return>',Rechercpatient) # ASSOCIER LA METHODE RECHERCHER QUAND ON PRESSE LA TOUCHE ENTER....
            txtprenomR=tkinter.Entry(fenrech,width=30)
            cmbsexeR=tkinter.ttk.Entry(fenrech,width=30)
            txtdateR=tkinter.ttk.Entry(fenrech,width=30)
            txtadrR=tkinter.Entry(fenrech,width=30)
            txttelR=tkinter.Entry(fenrech,width=30)
            txtetatR=tkinter.ttk.Entry(fenrech,width=30)
            cmbgrR=tkinter.ttk.Entry(fenrech,width=30)
            txtpersR=tkinter.Entry(fenrech,width=30) 
            txtnumpersR=tkinter.Entry(fenrech,width=30)
            assure=tkinter.StringVar()
            txtass=tkinter.ttk.Radiobutton(fenrech,value='Oui',text='Oui',variable=assure)
            txtass1=tkinter.ttk.Radiobutton(fenrech,value='Non',text='Non',variable=assure)
            txttypR=tkinter.ttk.Entry(fenrech,width=30)
            txtprofR=tkinter.Entry(fenrech,width=30)
            txtasR=tkinter.Entry(fenrech,width=30)
            
            butR=tkinter.Button(fenrech,text='Rechercher',command=lambda:Recherpatient())
            butAR=tkinter.Button(fenrech,text='Annuler')
                
            lb.grid(row=0,column=2)
            lbnum.grid(row=1,column=0,padx=3,pady=3)
            txtnumcarte.grid(row=1,column=1,padx=3,pady=3)
            butR.grid(row=1,column=2)
            #butAR.grid(row=1,column=3)
            lbnom.grid(row=2,column=0,padx=3,pady=3)
            txtnomR.grid(row=2,column=1,padx=3,pady=3)
            lbprenom.grid(row=2,column=2,padx=3,pady=3)
            txtprenomR.grid(row=2,column=3,padx=3,pady=3)
            lbsexe.grid(row=3,column=0,padx=3,pady=3)
            cmbsexeR.grid(row=3,column=1,padx=3,pady=3)
            lbdate.grid(row=3,column=2,padx=3,pady=3)
            txtdateR.grid(row=3,column=3,padx=3,pady=3)
            lbad.grid(row=4,column=0,padx=3,pady=3)
            txtadrR.grid(row=4,column=1,padx=3,pady=3)
            lbtel.grid(row=4,column=2,padx=3,pady=3)
            txttelR.grid(row=4,column=3,padx=3,pady=3)  
            lbetat.grid(row=5,column=0,padx=3,pady=3)
            txtetatR.grid(row=5,column=1,padx=3,pady=3)
            lbgr.grid(row=5,column=2,padx=3,pady=3)
            cmbgrR.grid(row=5,column=3,padx=3,pady=3)
            lbpers.grid(row=6,column=0,padx=3,pady=3)
            txtpersR.grid(row=6,column=1,padx=3,pady=3)
            lbnumper.grid(row=6,column=2,padx=3,pady=3)
            txtnumpersR.grid(row=6,column=3,padx=3,pady=3)
            lbtypass.grid(row=7,column=0,padx=3,pady=3)
            txttypR.grid(row=7,column=1,padx=3,pady=3)
            lbprofes.grid(row=7,column=2,padx=3,pady=3)
            txtprofR.grid(row=7,column=3,padx=15,pady=15)
            lbentass.grid(row=8,column=0,padx=3,pady=3)
            txtasR.grid(row=8,column=1,padx=15,pady=15)
            lbphoR.grid(row=8,column=2,rowspan=10,columnspan=10)
            #fenrech.configure(background='white')
            fenrech.transient(fenp)
            fenrech.resizable(height=False,width=False)
            fenrech.mainloop() 
        
        
        def FenRechercherPatt(event):
            global fenp,fen,txtnumcarte,txtnomR,txtprenomR,cmbsexeR,txtadrR,txttelR,txtassR,txtass1R,txtdateR,txtetatR,txtnumpersR,txtpersR,txtprofR,txttypR,txtasR,cmbgrR,chemin,lbphoR,assureR
            global fenrech
            fenrech = tkinter.Toplevel(fenp)
            fenrech.title("Fenetre de recherche sur patient")
            fenrech.iconbitmap('Images/doctoress.ico')
            larg=880
            haut=520
            largeecran=fenrech.winfo_screenwidth()
            hautecran=fenrech.winfo_screenheight()
            x=(largeecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fenrech.geometry('%dx%d+%d+%d' % (larg,haut,x,y))     
            
            lb=tkinter.Label(fenrech,text='Rechercher Information Patient',font=('arial',16,'bold'),foreground='green')
            lbnum=tkinter.Label(fenrech,text='Numero de carte')
            lbnom=tkinter.Label(fenrech,text='Nom')
            lbprenom=tkinter.Label(fenrech,text='Prenom')
            lbsexe=tkinter.Label(fenrech,text='Sexe')
            lbdate=tkinter.Label(fenrech,text='Date de naissance')
            lbad=tkinter.Label(fenrech,text='Adresse')
            lbtel=tkinter.Label(fenrech,text='Telephone')
            lbetat=tkinter.Label(fenrech,text='Etat matrimonial')
            lbgr=tkinter.Label(fenrech,text='Groupe sanguin')
            lbpers=tkinter.Label(fenrech,text='Personne responsable')
            lbnumper=tkinter.Label(fenrech,text='Numero du responsable')
            lbprofes=tkinter.Label(fenrech,text='Profession') 
            lbtypass=tkinter.Label(fenrech,text='Type assurance')
            lbentass=tkinter.Label(fenrech,text='Entreprise assurée')
            lbass=tkinter.Label(fenrech,text='Assure:')
            lbphoto=tkinter.Label(fenrech,text='Photo',font=('arial',8,'bold'))
            imgg=Image.open('Images/img_43443.png')
            im=ImageTk.PhotoImage(imgg.resize((300,240)),master=fenp)
            lbphoR=tkinter.Label(fenrech,image=im,background='white')
            lbphoR.im=im
            
            txtnomR=tkinter.Entry(fenrech,width=30)
            txtnumcarte=tkinter.Entry(fenrech,width=30)
            txtnumcarte.bind('<Return>',Rechercpatient) #ASSOCIER LA METHODE RECHERCHER QUAND ON PRESSE LA TOUCHE ENTER....
            txtprenomR=tkinter.Entry(fenrech,width=30)
            cmbsexeR=tkinter.ttk.Entry(fenrech,width=30)
            txtdateR=tkinter.ttk.Entry(fenrech,width=30)
            txtadrR=tkinter.Entry(fenrech,width=30)
            txttelR=tkinter.Entry(fenrech,width=30)
            txtetatR=tkinter.ttk.Entry(fenrech,width=30)
            cmbgrR=tkinter.ttk.Entry(fenrech,width=30)
            txtpersR=tkinter.Entry(fenrech,width=30) 
            txtnumpersR=tkinter.Entry(fenrech,width=30)
            assure=tkinter.StringVar()
            txtass=tkinter.ttk.Radiobutton(fenrech,value='Oui',text='Oui',variable=assure)
            txtass1=tkinter.ttk.Radiobutton(fenrech,value='Non',text='Non',variable=assure)
            txttypR=tkinter.ttk.Entry(fenrech,width=30)
            txtprofR=tkinter.Entry(fenrech,width=30)
            txtasR=tkinter.Entry(fenrech,width=30)
            
            butR=tkinter.Button(fenrech,text='Rechercher',command=lambda:Recherpatient())
            butAR=tkinter.Button(fenrech,text='Annuler')
                
            lb.grid(row=0,column=2)
            lbnum.grid(row=1,column=0,padx=3,pady=3)
            txtnumcarte.grid(row=1,column=1,padx=3,pady=3)
            butR.grid(row=1,column=2)
            #butAR.grid(row=1,column=3)
            lbnom.grid(row=2,column=0,padx=3,pady=3)
            txtnomR.grid(row=2,column=1,padx=3,pady=3)
            lbprenom.grid(row=2,column=2,padx=3,pady=3)
            txtprenomR.grid(row=2,column=3,padx=3,pady=3)
            lbsexe.grid(row=3,column=0,padx=3,pady=3)
            cmbsexeR.grid(row=3,column=1,padx=3,pady=3)
            lbdate.grid(row=3,column=2,padx=3,pady=3)
            txtdateR.grid(row=3,column=3,padx=3,pady=3)
            lbad.grid(row=4,column=0,padx=3,pady=3)
            txtadrR.grid(row=4,column=1,padx=3,pady=3)
            lbtel.grid(row=4,column=2,padx=3,pady=3)
            txttelR.grid(row=4,column=3,padx=3,pady=3)  
            lbetat.grid(row=5,column=0,padx=3,pady=3)
            txtetatR.grid(row=5,column=1,padx=3,pady=3)
            lbgr.grid(row=5,column=2,padx=3,pady=3)
            cmbgrR.grid(row=5,column=3,padx=3,pady=3)
            lbpers.grid(row=6,column=0,padx=3,pady=3)
            txtpersR.grid(row=6,column=1,padx=3,pady=3)
            lbnumper.grid(row=6,column=2,padx=3,pady=3)
            txtnumpersR.grid(row=6,column=3,padx=3,pady=3)
            lbtypass.grid(row=7,column=0,padx=3,pady=3)
            txttypR.grid(row=7,column=1,padx=3,pady=3)
            lbprofes.grid(row=7,column=2,padx=3,pady=3)
            txtprofR.grid(row=7,column=3,padx=15,pady=15)
            lbentass.grid(row=8,column=0,padx=3,pady=3)
            txtasR.grid(row=8,column=1,padx=15,pady=15)
            lbphoR.grid(row=8,column=2,rowspan=10,columnspan=10)
            #fenrech.configure(background='white')
            fenrech.transient(fenp)
            fenrech.resizable(height=False,width=False)
            fenrech.mainloop() 
          
            
        def FenListPatient():
            global tage,trr,butrr,butlr,butlrr,tnom,tprenom,cmbsex,lcompt
            fen=tkinter.Toplevel(fenp)
            larg=1310
            haut=600
            largecran=fen.winfo_screenwidth()
            hautecran=fen.winfo_screenheight()
            x=(largecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fen.geometry('%dx%d+%d+%d' %(larg,haut,x,y))
            fen.title('Liste des patients')
            fen.iconbitmap('Images/pngtree-elemental-design-of-nurse-care-for-patients-in-cartoon-hospital-png-image_4011893.ico')
           
            legend=tkinter.ttk.LabelFrame(fen,text='Dossier du patient')
            tabcontrol=tkinter.ttk.Notebook(legend)
            tab1=tkinter.Frame(tabcontrol)
            tab2=tkinter.Frame(tabcontrol)
            tab3=tkinter.Frame(tabcontrol)            
            tabcontrol.add(tab1,text='Lister par nom')
            tabcontrol.add(tab2,text='Lister par sexe')
            tabcontrol.add(tab3,text='Lister par age')
            
            
            lnom=tkinter.Label(tab1,text='Nom')
            lprenom=tkinter.Label(tab1,text='Prenom')
            tnom=tkinter.Entry(tab1,width=30)
            tprenom=tkinter.Entry(tab1,width=30)
            butrr=tkinter.Button(tab1,text='Lister',command=lambda:ListerParNom())
            butlr=tkinter.Button(tab2,text='Lister',command=lambda:ListerParSexe())
            butlrr=tkinter.Button(tab3,text='Lister',command=lambda:ListerParAge())
            lsex=tkinter.Label(tab2,text='Sexe')
            cmbsex=tkinter.ttk.Combobox(tab2,values=('Masculin','Feminin'))
            cmbsex.configure(state='readonly')
            lage=tkinter.Label(tab3,text='Age')
            #tage=tkinter.Spinbox(tab3,from_=0,to=100)
            tage=tkinter.Entry(tab3,width=30)
            lcompt=tkinter.Label(legend)
            
            trr=tkinter.ttk.Treeview(legend,columns=('Identifiant','Nom','Prenom','Sexe','Date-naissance','Adresse','Telephone'),show='headings',height=20)
            trr.heading('Identifiant',text='Identifiant')
            trr.heading('Nom',text='Nom')
            trr.heading('Prenom',text='Prenom')
            trr.heading('Sexe',text='Sexe')
            #trr.column('Sexe',width=100)
            trr.heading('Date-naissance',text='Date-naissance')
            #trr.column('Date-naissance',width=30)
            trr.heading('Adresse',text='Adresse')
            trr.heading('Telephone',text='Telephone')
            trr.column('Telephone',width=100)
            butimp=tkinter.Button(tab1,text='Imprimer')
            legend.grid(row=0,column=0)
            tabcontrol.grid(row=0,column=0)
            lnom.grid(row=0,column=0,padx=5,pady=5)
            tnom.grid(row=0,column=1,padx=5,pady=5)
            #lprenom.grid(row=0,column=2,padx=5,pady=5)
            #tprenom.grid(row=0,column=3,padx=5,pady=5)
            butrr.grid(row=0,column=4)
            lsex.grid(row=1,column=0)
            cmbsex.grid(row=1,column=1,padx=5,pady=5)
            butlr.grid(row=1,column=2)            
            lage.grid(row=2,column=0)
            tage.grid(row=2,column=1,padx=5,pady=5)
            butlrr.grid(row=2,column=2)
           
            trr.grid(row=1,column=0)
            lcompt.grid(row=3,column=0)
            fen.transient(fenp)
            fen.resizable(height=False,width=False)
            
            fen.mainloop()
        
        def FenListPatt(event):
            global tage,trr,butrr,butlr,butlrr,tnom,tprenom,cmbsex,lcompt
            fen=tkinter.Toplevel(fenp)
            larg=1310
            haut=600
            largecran=fen.winfo_screenwidth()
            hautecran=fen.winfo_screenheight()
            x=(largecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fen.geometry('%dx%d+%d+%d' %(larg,haut,x,y))
            fen.title('Liste des patients')
            fen.iconbitmap('Images/pngtree-elemental-design-of-nurse-care-for-patients-in-cartoon-hospital-png-image_4011893.ico')
           
            legend=tkinter.ttk.LabelFrame(fen,text='Dossier du patient')
            tabcontrol=tkinter.ttk.Notebook(legend)
            tab1=tkinter.Frame(tabcontrol)
            tab2=tkinter.Frame(tabcontrol)
            tab3=tkinter.Frame(tabcontrol)            
            tabcontrol.add(tab1,text='Lister par nom')
            tabcontrol.add(tab2,text='Lister par sexe')
            tabcontrol.add(tab3,text='Lister par age')
            
            
            lnom=tkinter.Label(tab1,text='Nom')
            lprenom=tkinter.Label(tab1,text='Prenom')
            tnom=tkinter.Entry(tab1,width=30)
            tprenom=tkinter.Entry(tab1,width=30)
            butrr=tkinter.Button(tab1,text='Lister',command=lambda:ListerParNom())
            butlr=tkinter.Button(tab2,text='Lister',command=lambda:ListerParSexe())
            butlrr=tkinter.Button(tab3,text='Lister',command=lambda:ListerParAge())
            lsex=tkinter.Label(tab2,text='Sexe')
            cmbsex=tkinter.ttk.Combobox(tab2,values=('Masculin','Feminin'))
            cmbsex.configure(state='readonly')
            lage=tkinter.Label(tab3,text='Age')
            #tage=tkinter.Spinbox(tab3,from_=0,to=100)
            tage=tkinter.Entry(tab3,width=30)
            lcompt=tkinter.Label(legend)
            
            trr=tkinter.ttk.Treeview(legend,columns=('Identifiant','Nom','Prenom','Sexe','Date-naissance','Adresse','Telephone'),show='headings',height=20)
            trr.heading('Identifiant',text='Identifiant')
            trr.heading('Nom',text='Nom')
            trr.heading('Prenom',text='Prenom')
            trr.heading('Sexe',text='Sexe')
            #trr.column('Sexe',width=100)
            trr.heading('Date-naissance',text='Date-naissance')
            #trr.column('Date-naissance',width=30)
            trr.heading('Adresse',text='Adresse')
            trr.heading('Telephone',text='Telephone')
            trr.column('Telephone',width=100)
            butimp=tkinter.Button(tab1,text='Imprimer')
            legend.grid(row=0,column=0)
            tabcontrol.grid(row=0,column=0)
            lnom.grid(row=0,column=0,padx=5,pady=5)
            tnom.grid(row=0,column=1,padx=5,pady=5)
            #lprenom.grid(row=0,column=2,padx=5,pady=5)
            #tprenom.grid(row=0,column=3,padx=5,pady=5)
            butrr.grid(row=0,column=4)
            lsex.grid(row=1,column=0)
            cmbsex.grid(row=1,column=1,padx=5,pady=5)
            butlr.grid(row=1,column=2)            
            lage.grid(row=2,column=0)
            tage.grid(row=2,column=1,padx=5,pady=5)
            butlrr.grid(row=2,column=2)
           
            trr.grid(row=1,column=0)
            lcompt.grid(row=3,column=0)
            fen.transient(fenp)
            fen.resizable(height=False,width=False)
            
            fen.mainloop()
        
            
        def ListerParNom(): 
            #Recuperer la valeur du champ nom
            nom=tnom.get()
            if nom=='':
                messagebox.showerror('Information','le champ nom est vide.')
            elif nom.isnumeric():
                #methode lister par nom
                messagebox.showwarning('','Le champ nom accepte seulement les caractères alphabétiques.')
            else:
                listparnom=pat.ListerPatientNom(nom)
                trr.delete(*trr.get_children())
                identifiant=[x[0] for x in listparnom] #Recuperer tous les valeurs dans la premiere position dans les differentes tuples.
                nom=[x[1] for x in listparnom] #Recuperation de valeur dans les tuples qui se positionne en deuxieme element.
                prenom=[x[2] for x in listparnom]
                sexe=[x[3] for x in listparnom]
                datenaissance=[x[4] for x in listparnom]
                adresse=[x[5] for x in listparnom]
                telephone=[x[6] for x in listparnom] # on recupere tous les valeurs de l'indice 6
                
                trr.delete(*trr.get_children())
                # Fusionner les valeurs de plusieurs tuples
                for i,no,pre,se,da,ad,tel in zip(identifiant,nom,prenom,sexe,datenaissance,adresse,telephone):#fusionner plusieurs listes en une seule
                        trr.insert('','end',values=(i,no,pre,se,da,ad,tel))
                # Afficher le nombre de colonne du treeview
                lcompt.configure(text='Remarque: '+str(len(trr.get_children()))+" patient(s) possédant le nom de famille '"+tnom.get()+"'.")
        
        def ListerParSexe():
            #Recuperer la valeur du combo sexe
            sexe=cmbsex.get()
            if sexe=='':
                messagebox.showerror('Information','le champ sexe est vide.')
            elif sexe.isnumeric():
                messagebox.showwarning('','Le champ sexe accepte seulement les caractères alphabétiques.')
            else:
                listparsexe=pat.ListerPatientSexe(sexe)
                identifiant=[x[0] for x in listparsexe] #Recuperer tous les valeurs dans la premiere position dans les differentes tuples.
                nom=[x[1] for x in listparsexe] #Recuperation de valeur dans les tuples qui se positionne en deuxieme element.
                prenom=[x[2] for x in listparsexe]
                sexe=[x[3] for x in listparsexe]
                datenaissance=[x[4] for x in listparsexe]
                adresse=[x[5] for x in listparsexe]
                telephone=[x[6] for x in listparsexe]
                
                trr.delete(*trr.get_children())
                #Fusionner les valeurs de plusieurs tuples
                for i,no,pre,se,da,ad,tel in zip(identifiant,nom,prenom,sexe,datenaissance,adresse,telephone):#fusionner plusieurs listes en une seule
                        trr.insert('','end',values=(i,no,pre,se,da,ad,tel))
                #Afficher le nombre de colonne du treeview
                lcompt.configure(text='Remarque: '+str(len(trr.get_children()))+" patient(s) de sexe "+cmbsex.get()+".")
                 
                 
                
        def ListerParAge():
            age=tage.get()
            if age=='':
                messagebox.showerror('Information',"Le champ age est vide.")
            elif age=='0':
                messagebox.showwarning('Information',"D'abord il faut selectionner une catégorie d'age.\nLa catégorie d'age commence par 1.")
            else:
                datejour=datetime.date.today()# date du jour
                datesys=datejour.strftime('%Y') #Annee en cours
                patie=pat.ListerPatientAge(age,datesys)  #methode lister de patient par age.
                identifiant=[x[0] for x in patie] #Recuperer tous les valeurs dans la premiere position dans les differentes tuples.
                nom=[x[1] for x in patie] #Recuperation de valeur dans les tuples qui se positionne en deuxieme element.
                prenom=[x[2] for x in patie]
                sexe=[x[3] for x in patie]
                datenaissance=[x[4] for x in patie]
                adresse=[x[5] for x in patie]
                telephone=[x[6] for x in patie]
                
                #Nettoyer le treeview
                trr.delete(*trr.get_children())
                #Remplir le champ treeview
                for i,no,pre,se,da,ad,tel in zip(identifiant,nom,prenom,sexe,datenaissance,adresse,telephone):#fusionner plusieurs listes en une seule
                        trr.insert('','end',values=(i,no,pre,se,da,ad,tel))
                #Afficher le nombre de colonne du treeview
                lcompt.configure(text='Remarque: '+str(len(trr.get_children()))+" patient(s) agé de "+age+" ans.")
           
        def ModifierPatient():
            global txtc,tnom,tprenom,tsexe,tadresse,tdate,ttel,tetat,tpers,tnumpers,cmgr,ttyp,tent,tprof,chemin,fen
            fen=tkinter.Toplevel(fenp)
            fen.title('Modifier information sur un patient')
            fen.iconbitmap('Images/rech.ico')
            larg=1020 #largeur de la fenetre modifier patient
            haut=350 #la hauteur de la fenetre
            largecran=fen.winfo_screenwidth()
            hautecran=fen.winfo_screenheight()
            x=(largecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fen.geometry('%dx%d+%d+%d' %(larg,haut,x,y))
            titr=tkinter.Label(fen,text='Modifier un patient',font=('',16,'bold'),foreground='Green')
            lbc=tkinter.Label(fen,text='Identifiant du patient')
            txtc=tkinter.Entry(fen,width=30)
            butrech=tkinter.Button(fen,text='Rechercher',command=lambda:RecherchPat())
            lnom=tkinter.Label(fen,text='Nom')
            tnom=tkinter.Entry(fen,width=30,fg='green')
            lprenom=tkinter.Label(fen,text='Prenom')
            tprenom=tkinter.Entry(fen,width=30,fg='green')
            lsexe=tkinter.Label(fen,text='Sexe')
            tsexe=tkinter.ttk.Combobox(fen,values=('Masculin','Feminin'),width=27)
            tsexe.configure(state='readonly')
            ladresse=tkinter.Label(fen,text='Adresse')
            tadresse=tkinter.Entry(fen,width=30)
            ldate=tkinter.Label(fen,text='Date de naissance')
            lad=tkinter.Label(fen,text='Adresse')
            ltel=tkinter.Label(fen,text='Telephone')
            letat=tkinter.Label(fen,text='Etat matrimonial')
            lgr=tkinter.Label(fen,text='Groupe sanguin')
            lpers=tkinter.Label(fen,text='Personne responsable')
            lnumper=tkinter.Label(fen,text='Numero du responsable')
            lprofes=tkinter.Label(fen,text='Profession') 
            ltypass=tkinter.Label(fen,text='Type assurance')
            lass=tkinter.Label(fen,text='Assure:')
            la=tkinter.Label(fen,text='Entreprise assurée:')            
            tdate=DateEntry(fen,background='green',foreground='black',borderwidth=2,locale="fr_FR",width=27)
            #print(tdate.strftime('%Y')
            tadr=tkinter.Entry(fen,width=30)
            ttel=tkinter.Entry(fen,width=30)
            ttel.insert(tkinter.INSERT,'(+509)-')
            tetat=tkinter.ttk.Combobox(fen,values=('Celibataire','Fiancé(e)','Veuf(ve)','Marié(e)','Divorcé'),width=27)
            tetat.configure(state='readonly')
            cmgr=tkinter.ttk.Combobox(fen,values=('A+','A-','B','B+','B-','O-','O+'),width=27)
            cmgr.configure(state='readonly')
            tpers=tkinter.Entry(fen,width=30) 
            tnumpers=tkinter.Entry(fen,width=30)
            tnumpers.insert(tkinter.INSERT,'(+509)-')
            #assure=tkinter.StringVar()
            #txtass=tkinter.ttk.Radiobutton(fen,value='Oui',text='Oui',variable=assure)
            #txtass1=tkinter.ttk.Radiobutton(fen,value='Non',text='Non',variable=assure)
            butpar=tkinter.Button(fen,text='Parcourir',command=lambda:Parcourir())
            
            def Parcourir():
                global chemin
                chemin=filedialog.askopenfilename(initialdir='/',title='Choisir une photo',filetype=(('jpeg files','*.jpg'),('All files','*.*')))
                img=Image.open(chemin)
                im=ImageTk.PhotoImage(img.resize((300,240)),master=fenp)
                lbph=tkinter.Label(fen,image=im,background='white')
                lbph.im=im                        
                lbph.grid(row=3,column=10,sticky=('N','S','W','E'),rowspan=10,columnspan=10)                
                
            butM=tkinter.Button(fen,text='Modifier',command=lambda:ModPatient())
            butAnn=tkinter.Button(fen,text='Annuler')
            lphot=tkinter.Label(fen,text='Photo')
            #image en arriere plan
            img=Image.open('Images/img_43443.png')
            im=ImageTk.PhotoImage(img.resize((300,240)),master=fenp)
            lim=tkinter.Label(fen,image=im)
            lim.im=im
            lim.grid(row=3,column=10,sticky=('N','E','W','S'),rowspan=12,columnspan=12)
            
            limg=tkinter.Label(fen)
            ttyp=tkinter.ttk.Combobox(fen,values=('Assurance maladie','Veilleisse'),width=27)
            #ttyp.insert(0,'Assurance maladie')
            ttyp.configure(state='readonly')
            tprof=tkinter.Entry(fen,width=30)
            tent=tkinter.Entry(fen,width=30)
            tasR=tkinter.Entry(fen,width=30)
            
            #positionner les elements dans la fenetre fille
            titr.grid(row=0,column=3)
            lbc.grid(row=1,column=0)
            txtc.grid(row=1,column=1)
            butrech.grid(row=1, column=2)
            lphot.grid(row=1,column=5)
            lnom.grid(row=2,column=0,padx=5,pady=5)
            tnom.grid(row=2,column=1,padx=5,pady=5)
            lprenom.grid(row=2,column=2,padx=5,pady=5)
            tprenom.grid(row=2,column=3,padx=5,pady=5)
            lsexe.grid(row=3,column=0,padx=5,pady=5)
            tsexe.grid(row=3,column=1,padx=5,pady=5)
            ladresse.grid(row=3,column=2,padx=5,pady=5)
            tadresse.grid(row=3,column=3,padx=5,pady=5)
            ldate.grid(row=4,column=0,padx=5,pady=5)
            tdate.grid(row=4,column=1,padx=5,pady=5)
            ltel.grid(row=4,column=2,padx=5,pady=5)
            ttel.grid(row=4,column=3,padx=5,pady=5)
            lgr.grid(row=5,column=0,padx=5,pady=5)
            cmgr.grid(row=5,column=1,padx=5,pady=5)
            letat.grid(row=5,column=2,padx=5,pady=5)
            tetat.grid(row=5,column=3,padx=5,pady=5)
            lpers.grid(row=6,column=0,padx=5,pady=5)
            tpers.grid(row=6,column=1,padx=5,pady=5)
            lnumper.grid(row=6,column=2,padx=5,pady=5)
            tnumpers.grid(row=6,column=3,padx=5,pady=5)
            ltypass.grid(row=7,column=0,padx=5,pady=5)
            ttyp.grid(row=7,column=1,padx=5,pady=5)
            la.grid(row=7,column=2,padx=5,pady=5)
            tent.grid(row=7,column=3,padx=5,pady=5)
            lprofes.grid(row=8,column=0,padx=5,pady=5)
            tprof.grid(row=8,column=1,padx=5,pady=5)
            butpar.grid(row=9,column=3,padx=5,pady=5)
            butM.grid(row=12,column=1)
            butAnn.grid(row=12,column=3)            
            
            #fen.configure(background='white')
            fen.transient(fenp)
            fen.resizable(width=False,height=False)
            fen.mainloop()
            
        def ModifierPatt(event):
            global txtc,tnom,tprenom,tsexe,tadresse,tdate,ttel,tetat,tpers,tnumpers,cmgr,ttyp,tent,tprof,chemin,fen
            fen=tkinter.Toplevel(fenp)
            fen.title('Modifier information sur un patient')
            larg=1020 #largeur de la fenetre modifier patient
            haut=350 #la hauteur de la fenetre
            largecran=fen.winfo_screenwidth()
            hautecran=fen.winfo_screenheight()
            x=(largecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fen.geometry('%dx%d+%d+%d' %(larg,haut,x,y))
            titr=tkinter.Label(fen,text='Modifier un patient',font=('',16,'bold'),foreground='Green')
            lbc=tkinter.Label(fen,text='Identifiant du patient')
            txtc=tkinter.Entry(fen,width=30)
            butrech=tkinter.Button(fen,text='Rechercher',command=lambda:RecherchPat())
            lnom=tkinter.Label(fen,text='Nom')
            tnom=tkinter.Entry(fen,width=30,fg='green')
            lprenom=tkinter.Label(fen,text='Prenom')
            tprenom=tkinter.Entry(fen,width=30,fg='green')
            lsexe=tkinter.Label(fen,text='Sexe')
            tsexe=tkinter.ttk.Combobox(fen,values=('Masculin','Feminin'),width=27)
            tsexe.configure(state='readonly')
            ladresse=tkinter.Label(fen,text='Adresse')
            tadresse=tkinter.Entry(fen,width=30)
            ldate=tkinter.Label(fen,text='Date de naissance')
            lad=tkinter.Label(fen,text='Adresse')
            ltel=tkinter.Label(fen,text='Telephone')
            letat=tkinter.Label(fen,text='Etat matrimonial')
            lgr=tkinter.Label(fen,text='Groupe sanguin')
            lpers=tkinter.Label(fen,text='Personne responsable')
            lnumper=tkinter.Label(fen,text='Numero du responsable')
            lprofes=tkinter.Label(fen,text='Profession') 
            ltypass=tkinter.Label(fen,text='Type assurance')
            lass=tkinter.Label(fen,text='Assure:')
            la=tkinter.Label(fen,text='Entreprise assurée:')            
            tdate=DateEntry(fen,background='green',foreground='black',borderwidth=2,locale="fr_FR",width=27)
            #print(tdate.strftime('%Y')
            tadr=tkinter.Entry(fen,width=30)
            ttel=tkinter.Entry(fen,width=30)
            ttel.insert(tkinter.INSERT,'(+509)-')
            tetat=tkinter.ttk.Combobox(fen,values=('Celibataire','Fiancé(e)','Veuf(ve)','Marié(e)','Divorcé'),width=27)
            tetat.configure(state='readonly')
            cmgr=tkinter.ttk.Combobox(fen,values=('A+','A-','B','B+','B-','O-','O+'),width=27)
            cmgr.configure(state='readonly')
            tpers=tkinter.Entry(fen,width=30) 
            tnumpers=tkinter.Entry(fen,width=30)
            tnumpers.insert(tkinter.INSERT,'(+509)-')
            #assure=tkinter.StringVar()
            #txtass=tkinter.ttk.Radiobutton(fen,value='Oui',text='Oui',variable=assure)
            #txtass1=tkinter.ttk.Radiobutton(fen,value='Non',text='Non',variable=assure)
            butpar=tkinter.Button(fen,text='Parcourir',command=lambda:Parcourir())
            
            def Parcourir():
                global chemin
                chemin=filedialog.askopenfilename(initialdir='/',title='Choisir une photo',filetype=(('jpeg files','*.jpg'),('All files','*.*')))
                img=Image.open(chemin)
                im=ImageTk.PhotoImage(img.resize((300,240)),master=fenp)
                lbph=tkinter.Label(fen,image=im,background='white')
                lbph.im=im                        
                lbph.grid(row=3,column=10,sticky=('N','S','W','E'),rowspan=10,columnspan=10)                
                
            butM=tkinter.Button(fen,text='Modifier',command=lambda:ModPatient())
            butAnn=tkinter.Button(fen,text='Annuler')
            lphot=tkinter.Label(fen,text='Photo')
            #image en arriere plan
            img=Image.open('Images/img_43443.png')
            im=ImageTk.PhotoImage(img.resize((300,240)),master=fenp)
            lim=tkinter.Label(fen,image=im)
            lim.im=im
            lim.grid(row=3,column=10,sticky=('N','E','W','S'),rowspan=12,columnspan=12)
            
            limg=tkinter.Label(fen)
            ttyp=tkinter.ttk.Combobox(fen,values=('Assurance maladie','Veilleisse'),width=27)
            #ttyp.insert(0,'Assurance maladie')
            ttyp.configure(state='readonly')
            tprof=tkinter.Entry(fen,width=30)
            tent=tkinter.Entry(fen,width=30)
            tasR=tkinter.Entry(fen,width=30)
            
            #positionner les elements dans la fenetre fille
            titr.grid(row=0,column=3)
            lbc.grid(row=1,column=0)
            txtc.grid(row=1,column=1)
            butrech.grid(row=1, column=2)
            lphot.grid(row=1,column=5)
            lnom.grid(row=2,column=0,padx=5,pady=5)
            tnom.grid(row=2,column=1,padx=5,pady=5)
            lprenom.grid(row=2,column=2,padx=5,pady=5)
            tprenom.grid(row=2,column=3,padx=5,pady=5)
            lsexe.grid(row=3,column=0,padx=5,pady=5)
            tsexe.grid(row=3,column=1,padx=5,pady=5)
            ladresse.grid(row=3,column=2,padx=5,pady=5)
            tadresse.grid(row=3,column=3,padx=5,pady=5)
            ldate.grid(row=4,column=0,padx=5,pady=5)
            tdate.grid(row=4,column=1,padx=5,pady=5)
            ltel.grid(row=4,column=2,padx=5,pady=5)
            ttel.grid(row=4,column=3,padx=5,pady=5)
            lgr.grid(row=5,column=0,padx=5,pady=5)
            cmgr.grid(row=5,column=1,padx=5,pady=5)
            letat.grid(row=5,column=2,padx=5,pady=5)
            tetat.grid(row=5,column=3,padx=5,pady=5)
            lpers.grid(row=6,column=0,padx=5,pady=5)
            tpers.grid(row=6,column=1,padx=5,pady=5)
            lnumper.grid(row=6,column=2,padx=5,pady=5)
            tnumpers.grid(row=6,column=3,padx=5,pady=5)
            ltypass.grid(row=7,column=0,padx=5,pady=5)
            ttyp.grid(row=7,column=1,padx=5,pady=5)
            la.grid(row=7,column=2,padx=5,pady=5)
            tent.grid(row=7,column=3,padx=5,pady=5)
            lprofes.grid(row=8,column=0,padx=5,pady=5)
            tprof.grid(row=8,column=1,padx=5,pady=5)
            butpar.grid(row=9,column=3,padx=5,pady=5)
            butM.grid(row=12,column=1)
            butAnn.grid(row=12,column=3)            
            
            #fen.configure(background='white')
            fen.transient(fenp)
            fen.resizable(width=False,height=False)
            fen.mainloop()   
            
            
        def RecherchPat():
            numerocarte=txtc.get()
            patient=pat.RechercherPatient(numerocarte)
            
            if numerocarte=='':
                messagebox.showerror('Message','Le numéro de carte du patient est recommandé.')
            else:
                if patient!=0:
                    tnom.delete(0,'end')
                    tnom.insert(tkinter.END,patient[0][1].upper())
                    tprenom.delete(0,'end')  
                    tprenom.insert(tkinter.END,patient[0][2])
                    tsexe.set(patient[0][3])                    
                    tdate.delete(0,'end')  
                    tdate.insert(tkinter.END,patient[0][4])
                    tadresse.delete(0,'end')  
                    tadresse.insert(tkinter.END,patient[0][5])
                    ttel.delete(0,'end')  
                    ttel.insert(tkinter.END,patient[0][6])                      
                    #tetat.delete(0,'end')  
                    tetat.set(patient[0][7])  
                    #cmgr.delete(0,'end')  
                    cmgr.set(patient[0][8])   
                    tpers.delete(0,'end')  
                    tpers.insert(tkinter.END,patient[0][9])  
                    tnumpers.delete(0,'end')  
                    tnumpers.insert(tkinter.END,patient[0][10])     
                    #ttyp.delete(0,'end')  
                    ttyp.set(patient[0][11])
                    tent.delete(0,'end')  
                    tent.insert(tkinter.END,patient[0][12])  
                    tprof.delete(0,'end')  
                    tprof.insert(tkinter.END,patient[0][13])   
                    pho=str(patient[0][14]).encode('utf-8')
                    with open("{}.png".format(patient[0][2]),"wb")as f:
                        os.chdir('./')# repertoire courant pour stocker l'image
                        phot=base64.decodebytes(pho)
                        f.write(phot)
                        f.flush()#pour lire et ecrire en meme temps.
                        ImageFile.LOAD_TRUNCATED_IMAGES=True # pour la taille
                        nomim=patient[0][2]+".png"
                        img=Image.open(nomim)
                        im1=ImageTk.PhotoImage(img.resize((300,240)),master=fenp)
                        limg=tkinter.Label(fen,image=im1)
                        limg.im1=im1
                        limg.grid(row=3,column=10,sticky=('N','E','W','S'),rowspan=12,columnspan=12)
                    
                    
                    
        def Rechercpatient(event):
            #global fenrech,fenp
            #programmation du bouton rechercher
            numerocarte=txtnumcarte.get()
            patient=pat.RechercherPatient(numerocarte)
            
            if numerocarte=='':
                messagebox.showerror('Message','Un numero de carte est recommande pour continuer la recherche.')
            else:
                if patient!=0:
                    txtnomR.delete(0,'end')
                    txtnomR.insert(tkinter.END,patient[0][1].upper())
                    txtprenomR.delete(0,'end')
                    txtprenomR.insert(tkinter.END,patient[0][2])
                    cmbsexeR.delete(0,'end')
                    cmbsexeR.insert(tkinter.END,patient[0][3])
                    txtdateR.delete(0,'end')
                    txtdateR.insert(tkinter.END,patient[0][4])
                    txtadrR.delete(0,'end')
                    txtadrR.insert(tkinter.END,patient[0][5])
                    txttelR.delete(0,'end')
                    txttelR.insert(tkinter.END,patient[0][6])
                    txtetatR.delete(0,'end')
                    txtetatR.insert(tkinter.END,patient[0][7])
                    cmbgrR.delete(0,'end')
                    cmbgrR.insert(tkinter.END,patient[0][8])
                    txtnumpersR.delete(0,'end')
                    txtnumpersR.insert(tkinter.END,patient[0][10])
                    txttypR.delete(0,'end')                    
                    txttypR.insert(tkinter.END,patient[0][11])
                    txtpersR.delete(0,'end')
                    txtpersR.insert(tkinter.END,patient[0][9])
                    txtprofR.delete(0,'end')
                    txtprofR.insert(tkinter.END,patient[0][13])
                    txtasR.delete(0,'end')
                    txtasR.insert(tkinter.END,patient[0][12])
                     
                    photo=str(patient[0][14]).encode('utf-8') #Encodage la chaine en binaire
                    with open("{}.png".format(patient[0][1]),'wb') as f:
                        
                    
                        os.chdir('./') #stocker l'image dans le repertoire racine de l'application 
                        #convertit la valeur coder en chaine sous forme de bytes
                        fichphoto=base64.decodebytes(photo) #decoder la chaine
                        f.write(fichphoto) #ecrire le fichier dans le repertoire
                        f.flush() #prendre le temps avant de lire a cause de l'ecriture
                        nomfichier=patient[0][1]+'.png' # format du fichier= nomfichier.png
                        ImageFile.LOAD_TRUNCATED_IMAGES=True # permet de prendre une image de grande taille plus que 7 octets.
                        #Ouvrir le fichier image 
                        img=Image.open(nomfichier)
                        im=ImageTk.PhotoImage(img.resize((300,240)),master=fenp)
                        lbphoR=tkinter.Label(fenrech,image=im,background='white')
                        lbphoR.im=im                        
                        lbphoR.grid(row=8,column=2,rowspan=10,columnspan=10)
                        f.close()
                        os.remove(nomfichier) #Supprimer le fichier image qui a ete cree dans le repertoire precise pour l'ecriture de l'image.
                    
                else:
                    messagebox.showerror('Message','le numero de carte est invalide.')
                    #txttelR,txtassR,txtass1R,txtdateR,txtetatR,txtnumpersR,txtpersR,txtprofR,txttypR,cmbgrR,
        
        def ModPatient():
            numerocarte=txtc.get()
            nom=tnom.get()
            prenom=tprenom.get()
            sexe=tsexe.get()
            adresse=tadresse.get()
            daten=tdate.get() # Date en format francaise
            datenaiss=datetime.datetime.strptime(daten,'%d/%m/%Y') # Transformer la date en anglaise
            datenaissance=datenaiss.date() #format anglaise : YYYY-MM-AA            
            telephone=ttel.get()
            groupesanguin=cmgr.get()
            etat_matrimoniale=tetat.get()
            personneresponsable=tpers.get()
            numeropersonneresponsable=tnumpers.get()
            typeassurance=ttyp.get()
            profession=tprof.get()
            entreprise_assuree=tent.get()
            datemodif=datetime.date.today()
            datemodification=datemodif.strftime('%d-%m-%Y')
                        
         
            if numerocarte=='':
                messagebox.showerror('Message','le champ numero de carte est vide.')
            elif nom=='':
                messagebox.showerror('Message','le champ de nom du patient est vide.')
            else:
                
                with open(chemin,'rb') as f:
                    if messagebox.askyesnocancel('Message de confirmation','Voulez-vous continuer la modification?'):
                            
                        pht=base64.b64encode(f.read())# lire la photo
                        photo=pht.decode('utf-8') #l'image sous forme de chaine de caracteres..
                        pat.ModifierPatient(numerocarte,nom,prenom,sexe,datenaissance,adresse,telephone,etat_matrimoniale,groupesanguin,personneresponsable,numeropersonneresponsable,typeassurance,entreprise_assuree,profession,photo,datemodification)
                        messagebox.showinfo('Message','Un patient a été modifiée avec succès..')                    
                    else:
                        messagebox.showerror('Message','Echec de modification.')
                
                    
        def Recherpatient():
            
            global fenrech,fenp
            #programmation de la bouton rechercher
            numerocarte=txtnumcarte.get()
            patient=pat.RechercherPatient(numerocarte)
            
            if numerocarte=='':
                messagebox.showerror('Message','Un numero de carte est recommande pour continuer la recherche.')
            else:
                if patient!=0:
                    txtnomR.delete(0,'end')
                    txtnomR.insert(tkinter.END,patient[0][1].upper())
                    txtprenomR.delete(0,'end')
                    txtprenomR.insert(tkinter.END,patient[0][2])
                    cmbsexeR.delete(0,'end')
                    cmbsexeR.insert(tkinter.END,patient[0][3])
                    txtdateR.delete(0,'end')
                    txtdateR.insert(tkinter.END,patient[0][4])
                    txtadrR.delete(0,'end')
                    txtadrR.insert(tkinter.END,patient[0][5])
                    txttelR.delete(0,'end')
                    txttelR.insert(tkinter.END,patient[0][6])
                    txtetatR.delete(0,'end')
                    txtetatR.insert(tkinter.END,patient[0][7])
                    cmbgrR.delete(0,'end')
                    cmbgrR.insert(tkinter.END,patient[0][8])
                    txtnumpersR.delete(0,'end')
                    txtnumpersR.insert(tkinter.END,patient[0][10])
                    txttypR.delete(0,'end')                    
                    txttypR.insert(tkinter.END,patient[0][11])
                    txtpersR.delete(0,'end')
                    txtpersR.insert(tkinter.END,patient[0][9])
                    txtprofR.delete(0,'end')
                    txtprofR.insert(tkinter.END,patient[0][13])
                    txtasR.delete(0,'end')
                    txtasR.insert(tkinter.END,patient[0][12])
                    photo=str(patient[0][14]).encode('utf-8') #Encoder la chaine de caractere en binaire
                    with open("{}.png".format(patient[0][1]),'wb') as f:
                        
                    
                        os.chdir('./') #stocker l'image dans le repertoire racine de l'application 
                        #convertit la valeur coder en chaine sous forme de bytes
                        fichphoto=base64.decodebytes(photo) #decoder la chaine
                        f.write(fichphoto) #ecrire le fichier dans le repertoire
                        f.flush() #prendre le temps avant de lire a cause de l'ecriture
                        nomfichier=patient[0][1]+'.png' # format du fichier= nomfichier.png
                        ImageFile.LOAD_TRUNCATED_IMAGES=True # permet de lire une image de petite taille.
                        #Ouvrir le fichier image 
                        img=Image.open(nomfichier)
                        im=ImageTk.PhotoImage(img.resize((300,240)),master=fenp)
                        lbphoR=tkinter.Label(fenrech,image=im,background='white')
                        lbphoR.im=im                        
                        lbphoR.grid(row=8,column=2,rowspan=10,columnspan=10)
                        os.remove(nomfichier) #Supprimer le fichier image qui a ete cree dans le repertoire precise pour l'ecriture de l'image.
                    
                else:
                    messagebox.showerror('Message','le numero de carte du patient est invalide.')
                    #txttelR,txtassR,txtass1R,txtdateR,txtetatR,txtnumpersR,txtpersR,txtprofR,txttypR,cmbgrR,
             
        def Consultation():
            global fenp,txtcodepat,tr,chmotif,chres,chprescription,txttemp,txtten
            fen=tkinter.Toplevel(fenp)
            larg=1280
            haut=630
            largeecran=fen.winfo_screenwidth()
            hautecran=fen.winfo_screenheight()
            x=(largeecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fen.geometry('%dx%d+%d+%d' % (larg,haut,x,y))
            fen.title('Fenetre de consultation')
            lbtit=tkinter.Label(fen,text='Consultation',font=('arial',16,'bold'),foreground='green')
            lbcodepat=tkinter.Label(fen, text='Numero de carte du patient')
            lbmotif=tkinter.Label(fen, text='Motif:')
            lbpres=tkinter.Label(fen, text='Prescription:')
            lbres=tkinter.Label(fen, text='Resultat-examen:')
            lbten=tkinter.Label(fen,text='Tension-arteriel')#label de tension arteriel
            lbtemp=tkinter.Label(fen,text='Temperature')
            txtcodepat=tkinter.Entry(fen,width=30)
            txtten=tkinter.Text(fen,width=10,height=8,font=('arial',9,''))
            txttemp=tkinter.Text(fen,width=10,height=8,font=('arial',9,''))
            sctemp=tkinter.Scrollbar(fen,orient='vertical',command=txttemp.yview)
            txttemp.configure(yscrollcommand=sctemp.set)
            #txttens=tkinter.Text(fen,width=10,height=8)
            sctens=tkinter.Scrollbar(fen,orient='vertical',command=txtten.yview)
            txtten.configure(yscrollcommand=sctens.set)            
            style=ttk.Style()
            style.theme_use('clam')
            
            
            tr=tkinter.ttk.Treeview(fen,style="Treeview",columns=('Nom','Prenom','Age','Poids','Date-consultation'),show='headings',height=25)
            style.configure("Treeview",foreground='gray',background='green')
            tr.heading('Nom',text='Nom')
            tr.heading('Prenom',text='Prenom')
            tr.heading('Age',text='Age')
            #tr.heading('Adresse',text='Adresse')
            #tr.heading('Motif',text='Motif')
            #tr.heading('Prescription',text='Prescription')
            tr.heading('Poids',text='Poids')
            #tr.heading('Resultat-examen',text='Resultat-examen')
            #tr.heading('Date premiere consultation',text='Date premiere consultation')
            tr.heading('Date-consultation',text='Date-consultation')
            
            tr.column('Nom',width=100)
            tr.column('Prenom',width=100)
            tr.column('Age',width=100)
            #tr.column('Adresse',width=100)
            #tr.column('Motif',width=130)
            #tr.column('Prescription',width=130)
            tr.column('Poids',width=100)
            #tr.column('Resultat-examen',width=100)
            #tr.column('Date premiere consultation',width=160)
            tr.column('Date-consultation',width=170)
            
           
                
                
            chmotif=tkinter.Text(fen,width=50,height=10,font=('arial',9,''))
            #chmotif.
            sc=tkinter.Scrollbar(fen,orient='vertical',command=chmotif.yview)
            chmotif.configure(yscrollcommand=sc.set)
            chres=tkinter.Text(fen,width=50,height=10,font=('arial',9,''))
            sc1=tkinter.Scrollbar(fen,orient='vertical',command=chres.yview)
            chres.configure(yscrollcommand=sc1.set)
            chprescription=tkinter.Text(fen,width=50,height=10,font=('arial',9,''))
            sc2=tkinter.Scrollbar(fen,orient='vertical',command=chprescription.yview)
            chprescription.configure(yscrollcommand=sc2.set)
            
            #sctens=tkinter.Scrollbar(fen,orient='vertical',command=txttens.yview)
            #txttens.configure(yscrollcommand=sctens.set)
            sctemp=tkinter.Scrollbar(fen,orient='vertical',command=txttemp.yview)
            txttemp.configure(yscrollcommand=sctemp.set)
            bout=tkinter.Button(fen,text='Rechercher',command=lambda:RechPatientConsulter())
            boutaj=tkinter.Button(fen,text='Nouvelle consultation',command=lambda:FenNouveauConsultation())
            lbtit.grid(row=0,column=3)
            lbcodepat.grid(row=1,column=0)
            txtcodepat.grid(row=1,column=1)
            bout.grid(row=1,column=2)
            boutaj.grid(row=1,column=3)
            tr.grid(row=2,column=0,rowspan=12,columnspan=12,sticky=('N','S','W','E'))
            lbtemp.grid(row=3,column=19)
            txttemp.grid(row=3,column=20)
            sctemp.grid(row=3,column=21)
            lbmotif.grid(row=3,column=14)
            chmotif.grid(row=3,column=15,padx=5,pady=5)
            sc.grid(row=3,column=17)
            lbpres.grid(row=4,column=14)
            chprescription.grid(row=4,column=15)
            sc2.grid(row=4,column=17)
            lbres.grid(row=5,column=14)
            chres.grid(row=5,column=15,padx=5,pady=5)
            sc1.grid(row=5,column=17)
            lbten.grid(row=4,column=19)
            txtten.grid(row=4,column=20)
            sctens.grid(row=4,column=21)
            fen.transient(app)
            fen.resizable(height=False,width=False)
            #fen.configure(background='white')
            fen.mainloop()
        def FenNouveauConsultation():
            global txtident,txtage,txtdate,txtpoids,txtmotiff,txtpresc,txtresulta,txttens,txttempp
            fenaj=tkinter.Toplevel(fenp)
            fenaj.transient(fenp)
            #fenaj.configure(background='white')            
            larg=910
            haut=560
            largeecran=fenaj.winfo_screenwidth()
            hautecran=fenaj.winfo_screenheight()
            x=(largeecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fenaj.geometry('%dx%d+%d+%d' % (larg,haut,x,y))     
            fenaj.title('Enregistrer nouvelle consultation')
            lbtit=tkinter.Label(fenaj,text='Enregistrer nouvelle consultation',font=('arial','12','bold'),fg='green')
            lbtit.grid(row=0,column=3)
            lbident=tkinter.Label(fenaj,text='Numero de la carte')
            txtident=tkinter.Entry(fenaj,width=30)
            lbage=tkinter.Label(fenaj,text='Age')
            txtage=tkinter.Entry(fenaj)
            lbpoids=tkinter.Label(fenaj,text='Poids')
            txtpoids=tkinter.Entry(fenaj)
            lbmotif=tkinter.Label(fenaj,text='Motif')
            txtmotiff=tkinter.Text(fenaj,width=30,height=10,font=('arial',8,''))
            lbpres=tkinter.Label(fenaj,text='Prescription')
            txtpresc=tkinter.Text(fenaj,width=30,height=8,font=('arial',8,''))
            lbresult=tkinter.Label(fenaj,text='Resultat examen')
            txtresulta=tkinter.Text(fenaj,width=30,height=10,font=('arial',8,''))   
            lbtemp=tkinter.Label(fenaj,text='Temperature du corps')
            txttempp=tkinter.Entry(fenaj,width=30) 
            lbtens=tkinter.Label(fenaj,text='Tension arteriel')
            txttens=tkinter.Entry(fenaj,width=30)               
            dt=datetime.date.today()
            dat=dt.strftime('%d/%m/%Y')
            hr=time.strftime('%I:%M:%S') # dans l'intervalle de 12 hres
            lbdate=tkinter.Label(fenaj,text='Date de consultation')
            txtdate=tkinter.Entry(fenaj)
            lbhr=tkinter.Label(fenaj,text='Heure de consultation')
            txthr=tkinter.Entry(fenaj)           
            txthr.insert(tkinter.END,hr)
            txthr.configure(state='disabled')
            txtdate.insert(tkinter.END,dat)
            txtdate.configure(state='disabled')            
            #Retrouver la date
            
            butaj=tkinter.Button(fenaj,text='Ajouter',command=lambda:AjouterNouvelleConsultation())
            butann=tkinter.Button(fenaj,text='Annuler')
            lbtit.grid(row=0,column=2)
            lbident.grid(row=1,column=0,padx=5,pady=5)
            txtident.grid(row=1,column=1,padx=5,pady=5)
            lbage.grid(row=1,column=2,padx=5,pady=5)
            txtage.grid(row=1,column=3,padx=5,pady=5)
            lbpoids.grid(row=2,column=0,padx=5,pady=5)
            txtpoids.grid(row=2,column=1,padx=5,pady=5)
            lbmotif.grid(row=2,column=2,padx=5,pady=5)
            txtmotiff.grid(row=2,column=3,padx=5,pady=5)
            lbtemp.grid(row=3,column=0,padx=5,pady=5)
            txttempp.grid(row=3,column=1,padx=5,pady=5)
            lbtens.grid(row=3,column=2,padx=5,pady=5)
            txttens.grid(row=3,column=3,padx=5,pady=5)
            #sctens.grid(row=3,column=4,padx=5,pady=5)
            lbpres.grid(row=4,column=0,padx=5,pady=5)
            txtpresc.grid(row=4,column=1,padx=5,pady=5)
            lbresult.grid(row=4,column=2,padx=5,pady=5)
            txtresulta.grid(row=4,column=3,padx=5,pady=5)
            lbdate.grid(row=5,column=0,padx=5,pady=5)
            txtdate.grid(row=5,column=1,padx=5,pady=5)
            lbhr.grid(row=5,column=2,padx=5,pady=5)
            txthr.grid(row=5,column=3,padx=5,pady=5)            
            butaj.grid(row=6,column=1)
            butann.grid(row=6,column=2)
            
            fenaj.transient(fenp)
            #fenaj.configure(background='white')            
            fenaj.resizable(width=False,height=False)
            fenaj.mainloop()
            
        def FenModifierConsul():
            global txtident,txtdatecons,txtdate,txtage,txthr,txtmotiff,txtpoids,txtpresc,txtresulta,txttempp,txttens
            fenm=tkinter.Toplevel(fenp)
            fenm.title('Modifier les informations sur une consultation')
            larg=830
            haut=640
            largeecran=fenm.winfo_screenwidth()
            hautecran=fenm.winfo_screenheight()
            x=(largeecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fenm.geometry('%dx%d+%d+%d' % (larg,haut,x,y))                 
            fenm.transient(fenp)
            #lbtit=tkinter.Label(fenaj,text='Enregistrer nouvelle consultation',font=('arial','12','bold'),fg='green')
            legend=tkinter.LabelFrame(fenm,text='Modifier les informations du patient')
            #lbtit.grid(row=0,column=3)
            lbident=tkinter.Label(legend,text='Numero de la carte')
            txtident=tkinter.Entry(legend,width=30)
            lbdatecons=tkinter.Label(legend,text='Date de consultation')
            txtdatecons=DateEntry(legend,borderwidth=2,background='green',foreground='white',locale='fr_FR',width=27)
            lbage=tkinter.Label(legend,text='Age')
            txtage=tkinter.Entry(legend,width=20)
            lbpoids=tkinter.Label(legend,text='Poids')
            txtpoids=tkinter.Entry(legend)
            lbmotif=tkinter.Label(legend,text='Motif')
            txtmotiff=tkinter.Text(legend,width=30,height=10,font=('arial',8,''))
            lbpres=tkinter.Label(legend,text='Prescription')
            txtpresc=tkinter.Text(legend,width=30,height=8,font=('arial',8,''))
            lbresult=tkinter.Label(legend,text='Resultat examen')
            txtresulta=tkinter.Text(legend,width=30,height=10,font=('arial',8,''))   
            lbtemp=tkinter.Label(legend,text='Temperature du corps')
            txttempp=tkinter.Entry(legend,width=30) 
            lbtens=tkinter.Label(legend,text='Tension arteriel')
            txttens=tkinter.Entry(legend,width=30)               
            dt=datetime.date.today()
            dat=dt.strftime('%d/%m/%Y')
            hr=time.strftime('%I:%M:%S') # dans l'intervalle de 12 heures
            lbdate=tkinter.Label(legend,text='Date de modification')
            txtdate=tkinter.Entry(legend)
            lbhr=tkinter.Label(legend,text='Heure de modification')
            txthr=tkinter.Entry(legend)           
            txthr.insert(tkinter.END,hr)
            txthr.configure(state='disabled')
            txtdate.insert(tkinter.END,dat)
            txtdate.configure(state='disabled')   
            
            butr=tkinter.Button(legend,text='Rechercher',command=lambda:RechMoConsul())
            butm=tkinter.Button(legend,text='Modifier',command=lambda:ModifConsul())
            butann=tkinter.Button(legend,text='Annuler')
            #lbtit.grid(row=0,column=2)
            legend.grid(row=0,column=0)
            lbident.grid(row=1,column=0,padx=5,pady=5)
            txtident.grid(row=1,column=1,padx=5,pady=5)
            lbdatecons.grid(row=1,column=2,padx=5,pady=5)
            txtdatecons.grid(row=1,column=3,padx=5,pady=5)
            butr.grid(row=1,column=4,padx=5,pady=5)
            lbage.grid(row=2,column=0,padx=5,pady=5)
            txtage.grid(row=2,column=1,padx=5,pady=5)
            lbpoids.grid(row=2,column=2,padx=5,pady=5)
            txtpoids.grid(row=2,column=3,padx=5,pady=5)
            lbmotif.grid(row=3,column=0,padx=5,pady=5)
            txtmotiff.grid(row=3,column=1,padx=5,pady=5)
            lbtemp.grid(row=3,column=2,padx=5,pady=5)
            txttempp.grid(row=3,column=3,padx=5,pady=5)
            lbtens.grid(row=4,column=0,padx=5,pady=5)
            txttens.grid(row=4,column=1,padx=5,pady=5)
            #sctens.grid(row=3,column=4,padx=5,pady=5)
            lbpres.grid(row=4,column=2,padx=5,pady=5)
            txtpresc.grid(row=4,column=3,padx=5,pady=5)
            lbresult.grid(row=5,column=0,padx=5,pady=5)
            txtresulta.grid(row=5,column=1,padx=5,pady=5)
            lbdate.grid(row=5,column=2,padx=5,pady=5)
            txtdate.grid(row=5,column=3,padx=5,pady=5)
            lbhr.grid(row=6,column=0,padx=5,pady=5)
            txthr.grid(row=6,column=1,padx=5,pady=5)            
            butm.grid(row=7,column=1)
            butann.grid(row=7,column=2)
             
            fenm.resizable(width=False,height=False)
            fenm.mainloop() 
            
        def RechMoConsul():  
            numerocarte=txtident.get()
            dateconsultation=txtdatecons.get()
            if numerocarte=='':
                messagebox.showerror('Information','le champ numero de carte vide.')
            elif dateconsultation=='':
                messagebox.showerror('Information','le champ date de consultation est vide.')
            else:
                rech=consul.RechMoConsul(numerocarte,dateconsultation)
                txtage.delete(0,'end')
                txtage.insert(tkinter.END,rech[0][1])
                txtpoids.delete(0,'end')
                txtpoids.insert(tkinter.END,rech[0][2])
                txtmotiff.delete('1.0','end')
                txtmotiff.insert(tkinter.END,rech[0][3])
                txttempp.delete(0,'end')
                txttempp.insert(tkinter.END,rech[0][4])
                txttens.delete(0,'end')
                txttens.insert(tkinter.END,rech[0][5])
                txtpresc.delete('1.0','end')
                txtpresc.insert(tkinter.END,rech[0][6])
                txtresulta.delete('1.0','end')
                txtresulta.insert(tkinter.END,rech[0][7])
               
        def ModifConsul():
            numerocarte=txtident.get()
            motif=txtmotiff.get('1.0','end')
            age=txtage.get()
            poids=txtpoids.get()
            prescription=txtpresc.get('1.0','end')
            temperature=txttempp.get()
            tensionarteriel=txttens.get()
            resultatexamen=txtresulta.get('1.0','end')
            dateconsultation=txtdatecons.get()
            dt=datetime.date.today()
            datemodification=dt.strftime('%d/%m/%Y') #0/00/0000 #date francaise
            if numerocarte=='':
                messagebox.showerror('Information','le champ numero de carte vide.')
            elif dateconsultation=='':
                messagebox.showerror('Information','le champ date de consultation est vide.')
            else:      
                #Methode distant qui va modifier les infos du consulation#
                modif=consul.ModifierConsultation(age,poids,motif,temperature,tensionarteriel,prescription,resultatexamen,datemodification,numerocarte,dateconsultation)
                if modif!=0:
                    messagebox.showinfo('Information','Le dossier du patient '+numerocarte+' a été modifié avec succès.') #Message de succes
                else:
                    messagebox.showerror('Message Echec','Echec de modification.')
                    
                     
        def RechPatientConsulter():
            #insertion de donnees dans le treeview
            numerocarte=txtcodepat.get()
            listconsult=consul.RechercherDossierPatientConsulter(numerocarte)
            nom=[x[0] for x in listconsult] #Retrouver la premiere valeur dans chaque tuple
            prenom=[x[1] for x in listconsult]
            age=[x[2] for x in listconsult]
            poids=[x[3] for x in listconsult]
            chmotif.delete('1.0','end')
            chmotif.insert(tkinter.END,[x[4] for x in listconsult])
            chmotif.insert(tkinter.END,'\n')
            #chmotif.strip('{}')
            txttemp.delete('1.0','end')
            txttemp.insert(tkinter.END,[x[5] for x in listconsult])
            txttemp.insert(tkinter.END,'\n')
            txtten.delete('1.0','end')
            txtten.insert(tkinter.END,[x[6] for x in listconsult])
            txtten.insert(tkinter.END,'\n')
            chprescription.delete('1.0','end')
            chprescription.insert(tkinter.END,[x[7] for x in listconsult])
            chprescription.insert(tkinter.END,'\n')
            #chprescription.strip('{}')
            chres.delete('1.0','end')
            chres.insert(tkinter.END,[x[8] for x in listconsult])
            chres.insert(tkinter.END,'\n')
            #chres.strip('{}')
            dte=[x[9] for x in listconsult]
            #Iterer differentes listes de meme taille
            tr.delete(*tr.get_children()) #Suppression de la liste
            for n,p,a,po,dte in zip (nom,prenom,age,poids,dte):
                tr.insert('','end',values=(n,p,a,po,dte))
                
        def AjouterNouvelleConsultation():
            numerocarte=txtident.get()
            age=txtage.get()
            poids=txtpoids.get()
            motif=txtmotiff.get('1.0','end-1c')
            prescription=txtpresc.get('1.0','end-1c')
            tensionarteriel=txttens.get()
            resultatexamen=txtresulta.get('1.0','end-1c')
            temperature=txttempp.get()
            Heure=time.strftime('%I:%M:%S') #Heure, minute,seconde
            dateco=datetime.date.today()
            dateconsultation=dateco.strftime('%d/%m/%Y')
            datemodification='' #la date de modification doit laisser vide.
            
            if numerocarte=='':
                messagebox.showerror('Message','Il faut entrer le numero de la carte du patient.')
            elif age=='':
                messagebox.showerror('Message',"Il faut entrer l'age du patient.")
            elif poids=='':
                messagebox.showerror('Message','Il faut entrer le poids du patient.')
            elif len(motif)==0:
                messagebox.showerror('Message','Il faut entrer le motif.')
            elif temperature=='':
                messagebox.showerror('Message','Il faut remplir le champ temperature.')
            elif tensionarteriel=='':
                messagebox.showerror('Message','Il faut remplir le champ tension du patient.')
            elif len(prescription)==0:
                messagebox.showerror('Message','Il faut remplir le champ prescription.')
            elif len(resultatexamen)==0:
                messagebox.showerror('Message','Il faut remplir le champ resultat examen.')
              
            else:
                
                p=pat.RechercherIdPatient(numerocarte)
                if p:  # si on trouve le numero du patient.
                    #appel a la methode ajout
                    ajout=consul.EffectuerConsultation(numerocarte,age,poids,motif,temperature,tensionarteriel,prescription,resultatexamen,Heure,dateconsultation,datemodification)
                    messagebox.showinfo('Message','Le dossier du patient '+numerocarte+' a été sauvegardé avec succès.')
                    #Nettoyer les champs
                    txtident.delete(0,'end')
                    txtage.delete(0,'end')
                    txtpoids.delete(0,'end')
                    txtmotiff.delete('1.0','end')                    
                else:
                    messagebox.showerror('Message',"Veuillez entrer un numero de carte valide.")
        
        
        def FenListToutConsul():
            fen=tkinter.Toplevel(fenp)
            fen.title('Liste des patients consulter pendant la journée')
            fen.iconbitmap('Images/pl.ico')
            larg=1390
            haut=600
            largecran=fen.winfo_screenwidth()
            hautecran=fen.winfo_screenheight()
            x=(largecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fen.geometry('%dx%d+%d+%d' % (larg,haut,x,y))
            legend=tkinter.LabelFrame(fen,text='Liste des patients consulter pendant la journée')
            tr=tkinter.ttk.Treeview(legend,columns=('Identifiant','Age','Poids','Motif','Temperature','Tension-arteriel','Prescription','Resultat-Examen','Heure'),show='headings',height=25)
            tr.heading('Identifiant',text='Identifiant')
            tr.heading('Age',text='Age')
            tr.column('Age',width=50)
            tr.heading('Poids',text='Poids')
            tr.column('Poids',width=50)
            tr.heading('Motif',text='Motif')
            tr.column('Age',width=150)
            tr.heading('Temperature',text='Temperature') 
            tr.column('Temperature',width=78)
            tr.heading('Tension-arteriel',text='tension-arteriel')
            tr.column('Tension-arteriel',width=90)
            tr.heading('Prescription',text='Prescription')
            tr.column('Prescription',width=200)
            tr.heading('Resultat-Examen',text='Resultat-Examen')
            tr.column('Resultat-Examen',width=200)
            tr.heading('Heure',text='Heure')
            tr.column('Heure',width=200)
            #Ajouter la barre de defilement horizontale
            sc=tkinter.Scrollbar(legend,orient='horizontal',command=tr.yview)
            tr.config(yscrollcommand=sc.set)
            lbinfo=tkinter.Label(legend)
            #Placement du methode qui va remplir la grille de donnees.
            datejour=datetime.date.today()
            dateconsultation=datejour.strftime('%d/%m/%Y') #la date sous le format 00/00/0000
            rempl=consul.ListerToutJournee(dateconsultation)
            identifiant=[x[0] for x in rempl]
            age=[x[1] for x in rempl]
            poids=[x[2] for x in rempl]
            motif=[x[3] for x in rempl]
            temperature=[x[4] for x in rempl]
            tensionarteriel=[x[5] for x in rempl]
            prescription=[x[6] for x in rempl]
            resultatexamen=[x[7] for x in rempl]
            heure=[x[8] for x in rempl]
            #Fusionner ou iterer les listes de meme taille
            for i,a,p,m,temp,ten,pr,res,hr in zip(identifiant,age,poids,motif,temperature,tensionarteriel,prescription,resultatexamen,heure):
                tr.insert('','end',values=(i,a,p,m,temp,ten,pr,res,hr))
            lbinfo.configure(text='Nombre de patient consulté: '+str(len(tr.get_children()))+' personne(s).')    # Compter le nombre de ligne d'enregistrement existe dans la grille 
                
            legend.grid(row=0,column=0)
            tr.grid(row=1,column=0)
            sc.grid(row=2,column=0)
            lbinfo.grid(row=3,column=0)
            fen.resizable(width=False,height=False)
            fen.transient(fenp)
            fen.mainloop()
                   
        def FenEnregistrerMedicament():
            global txtdesc,txtyp,txtpr,txtquant,txtdatf,txtdatP,cmbunit,cmbcomp,txtrem
            fen=tkinter.Toplevel(fenp)
            fen.title('Enregistrer Nouveau Medicament')
            fen.iconbitmap('Images/unnamed.ico')
            large=410
            haut=470
            largecran=fen.winfo_screenwidth()
            hautecran=fen.winfo_screenheight()
            x=(largecran/2)-(large/2)
            y=(hautecran/2)-(haut/2)
            fen.geometry('%dx%d+%d+%d' % (large,haut,x,y))
            legend=tkinter.ttk.Labelframe(fen,text='Informations sur le medicament')
            #legend.configure(bg='white')
            desc=tkinter.Label(legend,text='Description')
            txtdesc=tkinter.Entry(legend,width=44)
            typel=tkinter.Label(legend,text='Categorie')
            txtyp=tkinter.ttk.Combobox(legend,width=41,values=('Antitussif,pectorant','Analgesique','Antibiotique','Antitiberculeux,anti-pertileux','Anti-mycosiques','Antiviraux','Antiacide,antiflatulent','Antianemique','Anti-Allergique','Antagoniste de calcium','Antiagregants-Plaquettaire','AntiArythmique','Anticholinergique','Antiépileptiques','Anticoagulants circulants','Anticoagulants de type AVK','Antidiarrhéiques','Antihistaminiques H1','Antihistaminiques H2','Antihypertenseurs','Antipsychotiques','Antispasmodiques','Antithyroïdiens de synthèse','Anxiolytiques','Bêta-bloquants','Cardiotoniques','Hypnotiques','Hypoglycémiants injectables','Hypoglycémiants oraux','Hypolipémiants',"Inhibiteurs de l'enzyme de conversion","Inhibiteurs de l'angiotensine II",'Mucolytiques','Nootropiques','Phényléthylamines',"Sartans,Antagonistes de l'angiotensine II",'Triptans'))
            txtyp.configure(state='readonly')
            pr=tkinter.Label(legend,text='Prix par unité')
            txtpr=tkinter.Entry(legend,width=44)
            quant=tkinter.Label(legend,text='Quantité')
            txtquant=tkinter.Entry(legend,width=44)
            datf=tkinter.Label(legend,text="Date d'entrée")
            txtdatf=DateEntry(legend,borderwidth=2,background='white',foreground='black',locale='fr_FR',width=41)
            datP=tkinter.Label(legend,text='Date de peremption')
            txtdatP=DateEntry(legend,borderwidth=2,background='white',foreground='black',locale='fr_FR',width=41)   
            #nomfournisseur=tkinter.Label(legend,text='Nom du fournisseur')
            #txtnomf=tkinter.Entry(legend,width=30)
            lunit=tkinter.Label(legend,text='Unité')
            cmbunit=tkinter.ttk.Combobox(legend,values=('tube','comprimé','sirop','ml','gramme','nombre'),width=41)
            cmbunit.configure(state='readonly')
            lcomp=tkinter.Label(legend,text='Composition')
            cmbcomp=tkinter.ttk.Combobox(legend,values=('50 ml','120 ml','160 ml','200 ml','260 ml','300 ml','320 ml','360 ml','443 ml','1 l','1.5 l','10 comprimés','20 comprimés','30 comprimés','50 comprimés','60 comprimés','65 comprimés','100 comprimés','150 comprimés','200 comprimés','250 comprimés','300 comprimés','350 comprimés','500 comprimés'),width=41)
            cmbcomp.configure(state='readonly')
            rem=tkinter.Label(legend,text='Remarque')
            txtrem=tkinter.Text(legend,width=40,height=10,font=('arial',8,''))
            butE=tkinter.Button(legend,text='Enregistrer',command=lambda:AjouterMedicament())
            butAnn=tkinter.Button(legend,text='Annuler')
            legend.grid(row=0,column=0)
            desc.grid(row=1,column=0,padx=5,pady=5)
            txtdesc.grid(row=1,column=1,padx=5,pady=5)
            #nomfournisseur.grid(row=1,column=2,padx=5,pady=5)
            #txtnomf.grid(row=1,column=3,padx=5,pady=5)
            typel.grid(row=2,column=0,padx=5,pady=5)
            txtyp.grid(row=2,column=1,padx=5,pady=5)
            pr.grid(row=3,column=0,padx=5,pady=5)
            txtpr.grid(row=3,column=1,padx=5,pady=5)
            quant.grid(row=4,column=0,padx=5,pady=5)
            txtquant.grid(row=4,column=1,padx=5,pady=5)
            lunit.grid(row=5,column=0,padx=5,pady=5)
            cmbunit.grid(row=5,column=1)
            datf.grid(row=6,column=0,padx=5,pady=5)
            txtdatf.grid(row=6,column=1,padx=5,pady=5)
            datP.grid(row=7,column=0,padx=5,pady=5)
            txtdatP.grid(row=7,column=1,padx=5,pady=5)
            lcomp.grid(row=8,column=0,padx=5,pady=5)
            cmbcomp.grid(row=8,column=1,padx=5,pady=5)
            rem.grid(row=9,column=0,padx=5,pady=5)
            txtrem.grid(row=9,column=1,padx=5,pady=5)
            butE.grid(row=10,column=0,padx=5,pady=5)
            butAnn.grid(row=10,column=1,padx=5,pady=5)
            fen.configure(background='white')
            fen.transient(fenp)
            fen.resizable(width=False,height=False)
            fen.mainloop()
         
         
        def FenEnregistrerMedic(event):
            global txtdesc,txtyp,txtpr,txtquant,txtdatf,txtdatP,cmbunit,cmbcomp,txtrem
             
            fen=tkinter.Toplevel(fenp)
            fen.title('Enregistrer Nouveau Medicament')
            fen.iconbitmap('Images/unnamed.ico')
            large=410
            haut=470
            largecran=fen.winfo_screenwidth()
            hautecran=fen.winfo_screenheight()
            x=(largecran/2)-(large/2)
            y=(hautecran/2)-(haut/2)
            fen.geometry('%dx%d+%d+%d' % (large,haut,x,y))
            legend=tkinter.ttk.Labelframe(fen,text='Informations sur le medicament')
            #legend.configure(bg='white')
            desc=tkinter.Label(legend,text='Description')
            txtdesc=tkinter.Entry(legend,width=44)
            typel=tkinter.Label(legend,text='Categorie')
            txtyp=tkinter.ttk.Combobox(legend,width=41,values=('Antitussif,pectorant','Analgesique','Antibiotique','Antitiberculeux,anti-pertileux','Anti-mycosiques','Antiviraux','Antiacide,antiflatulent','Antianemique','Anti-Allergique','Antagoniste de calcium','Antiagregants-Plaquettaire','AntiArythmique','Anticholinergique','Antiépileptiques','Anticoagulants circulants','Anticoagulants de type AVK','Antidiarrhéiques','Antihistaminiques H1','Antihistaminiques H2','Antihypertenseurs','Antipsychotiques','Antispasmodiques','Antithyroïdiens de synthèse','Anxiolytiques','Bêta-bloquants','Cardiotoniques','Hypnotiques','Hypoglycémiants injectables','Hypoglycémiants oraux','Hypolipémiants',"Inhibiteurs de l'enzyme de conversion","Inhibiteurs de l'angiotensine II",'Mucolytiques','Nootropiques','Phényléthylamines',"Sartans,Antagonistes de l'angiotensine II",'Triptans'))
            txtyp.configure(state='readonly')
            pr=tkinter.Label(legend,text='Prix par unité')
            txtpr=tkinter.Entry(legend,width=44)
            quant=tkinter.Label(legend,text='Quantité')
            txtquant=tkinter.Entry(legend,width=44)
            datf=tkinter.Label(legend,text="Date d'entrée")
            txtdatf=DateEntry(legend,borderwidth=2,background='white',foreground='black',locale='fr_FR',width=41)
            datP=tkinter.Label(legend,text='Date de peremption')
            txtdatP=DateEntry(legend,borderwidth=2,background='white',foreground='black',locale='fr_FR',width=41)   
            #nomfournisseur=tkinter.Label(legend,text='Nom du fournisseur')
            #txtnomf=tkinter.Entry(legend,width=30)
            lunit=tkinter.Label(legend,text='Unité')
            cmbunit=tkinter.ttk.Combobox(legend,values=('tube','comprimé','sirop','ml','gramme','nombre'),width=41)
            cmbunit.configure(state='readonly')
            lcomp=tkinter.Label(legend,text='Composition')
            cmbcomp=tkinter.ttk.Combobox(legend,values=('50 ml','120 ml','160 ml','200 ml','260 ml','300 ml','320 ml','360 ml','443 ml','1 l','1.5 l','10 comprimés','20 comprimés','30 comprimés','50 comprimés','60 comprimés','65 comprimés','100 comprimés','150 comprimés','200 comprimés','250 comprimés','300 comprimés','350 comprimés','500 comprimés'),width=41)
            cmbcomp.configure(state='readonly')
            cmbcomp.configure(state='readonly')
            rem=tkinter.Label(legend,text='Remarque')
            txtrem=tkinter.Text(legend,width=40,height=10,font=('arial',8,''))
            butE=tkinter.Button(legend,text='Enregistrer',command=lambda:AjouterMedicament())
            butAnn=tkinter.Button(legend,text='Annuler')
            legend.grid(row=0,column=0)
            desc.grid(row=1,column=0,padx=5,pady=5)
            txtdesc.grid(row=1,column=1,padx=5,pady=5)
            #nomfournisseur.grid(row=1,column=2,padx=5,pady=5)
            #txtnomf.grid(row=1,column=3,padx=5,pady=5)
            typel.grid(row=2,column=0,padx=5,pady=5)
            txtyp.grid(row=2,column=1,padx=5,pady=5)
            pr.grid(row=3,column=0,padx=5,pady=5)
            txtpr.grid(row=3,column=1,padx=5,pady=5)
            quant.grid(row=4,column=0,padx=5,pady=5)
            txtquant.grid(row=4,column=1,padx=5,pady=5)
            lunit.grid(row=5,column=0,padx=5,pady=5)
            cmbunit.grid(row=5,column=1)
            datf.grid(row=6,column=0,padx=5,pady=5)
            txtdatf.grid(row=6,column=1,padx=5,pady=5)
            datP.grid(row=7,column=0,padx=5,pady=5)
            txtdatP.grid(row=7,column=1,padx=5,pady=5)
            lcomp.grid(row=8,column=0,padx=5,pady=5)
            cmbcomp.grid(row=8,column=1,padx=5,pady=5)
            rem.grid(row=9,column=0,padx=5,pady=5)
            txtrem.grid(row=9,column=1,padx=5,pady=5)
            butE.grid(row=10,column=0,padx=5,pady=5)
            butAnn.grid(row=10,column=1,padx=5,pady=5)
            fen.configure(background='white')
            fen.transient(fenp)
            fen.resizable(width=False,height=False)
            fen.mainloop()   
            
        def FenRechercherMedicament():
            global txtcod,txtdes,txtypc,txtp,txtquan,txtdatff,txtdatPP,cmbunitt,cmbcompp,txtremm
            fen=tkinter.Toplevel(fenp)
            fen.title('Rechercher un medicament')
            fen.iconbitmap('Images/kdict2.ico')
            larg=850
            haut=410
            largeecran=fen.winfo_screenwidth()
            hautecran=fen.winfo_screenheight()
            x=(largeecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fen.geometry('%dx%d+%d+%d' % (larg,haut,x,y))   
            #legend=tkinter.ttk.Notebook()
            legend=tkinter.LabelFrame(fen,text="Rechercher l'information sur un medicament")
            lbc=tkinter.Label(legend,text='code de medicament')
            txtcod=tkinter.Entry(legend,width=44)
            desc=tkinter.Label(legend,text='Description')
            txtdes=tkinter.Entry(legend,width=44)
            typel=tkinter.Label(legend,text='Categorie')
            txtypc=tkinter.Entry(legend,width=44)
            #txtypc.configure(state='readonly')
            pr=tkinter.Label(legend,text='Prix par unité')
            txtp=tkinter.Entry(legend,width=44)
            quant=tkinter.Label(legend,text='Quantité')
            txtquan=tkinter.Entry(legend,width=44)
            datf=tkinter.Label(legend,text="Date d'entrée")
            txtdatff=tkinter.Entry(legend,width=44)
            datP=tkinter.Label(legend,text='Date de peremption')
            txtdatPP=tkinter.Entry(legend,width=44) 
            #nomfournisseur=tkinter.Label(legend,text='Nom du fournisseur')
            #txtnomf=tkinter.Entry(legend,width=30)
            lunit=tkinter.Label(legend,text='Unité')
            cmbunitt=tkinter.ttk.Combobox(legend,values=('tube','comprimé','sirop','ml','gramme','nombre'),width=41)
            cmbunitt.configure(state='readonly')
            lcomp=tkinter.Label(legend,text='Composition')
            cmbcompp=tkinter.ttk.Combobox(legend,values=('50 ml','120 ml','160 ml','200 ml','260 ml','300 ml','320 ml','360 ml','443 ml','1 l','1.5 l','10 comprimés','20 comprimés','30 comprimés','50 comprimés','60 comprimés','65 comprimés','100 comprimés','150 comprimés','200 comprimés','250 comprimés','300 comprimés','350 comprimés','500 comprimés'),width=41)
            cmbcompp.configure(state='readonly')
            rem=tkinter.Label(legend,text='Remarque')
            txtremm=tkinter.Text(legend,width=40,height=10,font=('arial',8,''))
            butR=tkinter.Button(legend,text='Rechercher',command=lambda:RechercherMedic())
            butAn=tkinter.Button(legend, text='Annuler')
            legend.grid(row=0,column=0)
            lbc.grid(row=1, column=0, padx=5, pady=5)
            txtcod.grid(row=1, column=1, padx=5, pady=5)
            butR.grid(row=1, column=2, padx=5, pady=5)
            butAn.grid(row=1, column=3, padx=5, pady=5)
            desc.grid(row=2, column=0, padx=5, pady=5)
            txtdes.grid(row=2, column=1, padx=5, pady=5)
            lunit.grid(row=2, column=2, padx=5, pady=5)
            cmbunitt.grid(row=2, column=3)
            lcomp.grid(row=4, column=0, padx=5, pady=5)
            cmbcompp.grid(row=4, column=1, padx=5, pady=5)
            typel.grid(row=4, column=2, padx=5, pady=5)
            txtypc.grid(row=4, column=3, padx=5, pady=5)
            pr.grid(row=5, column=0, padx=5, pady=5)
            txtp.grid(row=5, column=1, padx=5, pady=5)
            quant.grid(row=5, column=2, padx=5, pady=5)
            txtquan.grid(row=5, column=3, padx=5, pady=5)
            datf.grid(row=6, column=0, padx=5, pady=5)
            txtdatff.grid(row=6, column=1, padx=5, pady=5)
            datP.grid(row=6, column=2, padx=5, pady=5)
            txtdatPP.grid(row=6, column=3, padx=5, pady=5)

            rem.grid(row=7, column=2, padx=5, pady=5)
            txtremm.grid(row=7, column=3, padx=5, pady=5)

            fen.resizable(width=False,height=False)
            fen.transient(fenp)
            fen.mainloop()
            
        def FenRechercherMedic(event):
            global txtcod,txtdes,txtypc,txtp,txtquan,txtdatff,txtdatPP,cmbunitt,cmbcompp,txtremm
            fen=tkinter.Toplevel(fenp)
            fen.title('Rechercher un medicament')
            fen.iconbitmap('Images/kdict2.ico')
            larg=850
            haut=410
            largeecran=fen.winfo_screenwidth()
            hautecran=fen.winfo_screenheight()
            x=(largeecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fen.geometry('%dx%d+%d+%d' % (larg,haut,x,y))   
            #legend=tkinter.ttk.Notebook()
            legend=tkinter.LabelFrame(fen,text="Rechercher l'information sur un medicament")
            lbc = tkinter.Label(legend, text='Code de medicament')
            txtcod = tkinter.Entry(legend, width=44)
            desc=tkinter.Label(legend,text='Description')
            txtdes=tkinter.Entry(legend,width=44)
            typel=tkinter.Label(legend,text='Categorie')
            txtypc=tkinter.Entry(legend,width=44)
            pr=tkinter.Label(legend,text='Prix par unité')
            txtp=tkinter.Entry(legend,width=44)
            quant=tkinter.Label(legend,text='Quantité')
            txtquan=tkinter.Entry(legend,width=44)
            datf=tkinter.Label(legend,text="Date d'entrée")
            txtdatff=tkinter.Entry(legend,width=44)
            datP=tkinter.Label(legend,text='Date de peremption')
            txtdatPP=tkinter.Entry(legend,width=44)   
            lunit=tkinter.Label(legend,text='Unité')
            cmbunitt=tkinter.ttk.Combobox(legend,values=('tube','comprimé','sirop','ml','gramme','nombre'),width=41)
            cmbunitt.configure(state='readonly')
            lcomp=tkinter.Label(legend,text='Composition')
            cmbcompp=tkinter.ttk.Combobox(legend,values=('50 ml','120 ml','160 ml','200 ml','260 ml','300 ml','320 ml','360 ml','443 ml','1 l','1.5 l','10 comprimés','20 comprimés','30 comprimés','50 comprimés','60 comprimés','65 comprimés','100 comprimés','150 comprimés','200 comprimés','250 comprimés','300 comprimés','350 comprimés','500 comprimés'),width=41)
            cmbcompp.configure(state='readonly')
            rem=tkinter.Label(legend,text='Remarque')
            txtremm=tkinter.Text(legend,width=40,height=10,font=('arial',8,''))
            butR=tkinter.Button(legend,text='Rechercher',command=lambda:RechercherMedic())
            butAn=tkinter.Button(legend, text='Annuler')  #
            legend.grid(row=0,column=0)

            lbc.grid(row=1, column=0, padx=5, pady=5)
            txtcod.grid(row=1, column=1, padx=5, pady=5)
            butR.grid(row=1, column=2, padx=5, pady=5)
            butAn.grid(row=1, column=3, padx=5, pady=5)
            desc.grid(row=2,column=0,padx=5,pady=5)
            txtdes.grid(row=2,column=1,padx=5,pady=5)
            lunit.grid(row=2,column=2,padx=5,pady=5)
            cmbunitt.grid(row=2,column=3)
            lcomp.grid(row=4,column=0,padx=5,pady=5)
            cmbcompp.grid(row=4,column=1,padx=5,pady=5)
            typel.grid(row=4,column=2,padx=5,pady=5)
            txtypc.grid(row=4,column=3,padx=5,pady=5)
            pr.grid(row=5,column=0,padx=5,pady=5)
            txtp.grid(row=5,column=1,padx=5,pady=5)
            quant.grid(row=5,column=2,padx=5,pady=5)
            txtquan.grid(row=5,column=3,padx=5,pady=5)
            datf.grid(row=6,column=0,padx=5,pady=5)
            txtdatff.grid(row=6,column=1,padx=5,pady=5)
            datP.grid(row=6,column=2,padx=5,pady=5)
            txtdatPP.grid(row=6,column=3,padx=5,pady=5)
            
            rem.grid(row=7,column=2,padx=5,pady=5)
            txtremm.grid(row=7,column=3,padx=5,pady=5)
            
            
            fen.resizable(width=False,height=False)
            fen.transient(fenp)
            fen.mainloop()
        
        def AjouterMedicament():
            id_prod=random.randint(000000000000000,100000000000000)
            description=txtdesc.get()
            categorie=txtyp.get()
            prix=txtpr.get()
            quantite=txtquant.get()
            unite=cmbunit.get()
            dateentrer=txtdatf.get()
            dateperemption=txtdatP.get()
            composition=cmbcomp.get()
            remarque=txtrem.get('1.0','end')
            if description=='':
                messagebox.showerror('Information','Le champ de description du medicament est vide.')
            elif categorie=='':
                    messagebox.showerror('Information','Le champ de categorie du medicament est vide.')
            
            #prix
            elif prix=='':
                messagebox.showerror('Information','Le champ de prix du medicament est vide.')
            elif prix ==0:
                messagebox.showerror('Information', 'Le champ de prix du medicament est vide.')
            elif str(prix)<str(0):
                messagebox.showerror('Information', '.')
            elif prix.isalpha():
                messagebox.showerror('Information', '.')

            elif quantite=='':
                messagebox.showerror('Information','Le champ de quantite du medicament est vide.')
            elif quantite=='0':
                messagebox.showwarning('Attention', "la quantite ne peut pas egal a zero.")
            elif str(quantite)<str(0):
                messagebox.showerror('Information', '.')
            elif quantite.isalpha():
                messagebox.showerror('Information', '.')

            #unite 
            elif unite=='':
                messagebox.showerror('Information','Le champ de unite du medicament est vide.')            
            #date entrer
            elif dateentrer=='':
                messagebox.showerror('Information','Le champ de date entrer du medicament est vide.')            
            #date perime
            elif dateperemption=='':
                messagebox.showerror('Information','Le champ de date de peremption du medicament est vide.')            
            #comp
            elif composition=='':
                messagebox.showerror('Information','Le champ de composition du medicament est vide.')            
            #remarque
            elif remarque=='':
                messagebox.showerror('Information','Le champ de remarque du medicament est vide.')            
            else:
                med=medic.AjouterMedicament(id_prod,description,categorie,prix,quantite,unite,dateentrer,dateperemption,composition,remarque)
                messagebox.showinfo("Information","Un nouveau medicament a ete ajoute avec succes.")
                
            
        def RechercherMedic():
            #txtdes,txtypc,txtp,txtquan,txtdatff,txtdatPP,cmbunitt,cmbcompp,txtremm
            # description=txtdes.get()
            # composition=cmbcompp.get()
            id_prod=txtcod.get()
            if id_prod=='':
                messagebox.showerror('Information','le champ code de medicament est vide.')
            else:
                med=medic.RechercherMedicament(id_prod)
                if med!=0:
                    txtdes.delete(0, 'end')
                    txtdes.insert(tkinter.END, med[0][1])
                    cmbunitt.delete(0, 'end')
                    cmbunitt.set(med[0][5])
                    cmbcompp.delete(0, 'end')
                    cmbcompp.set(med[0][8])
                    txtypc.delete(0,'end')
                    txtypc.insert(tkinter.END,med[0][2])
                    txtp.delete(0,'end')
                    txtp.insert(tkinter.END,med[0][3])
                    txtquan.delete(0,'end')
                    txtquan.insert(tkinter.END,med[0][4])
                    cmbunitt.delete(0,'end')
                    cmbunitt.insert(tkinter.END,med[0][5])
                    txtdatff.delete(0,'end')
                    txtdatff.insert(tkinter.END,med[0][6])
                    txtdatPP.delete(0,'end')
                    txtdatPP.insert(tkinter.END,med[0][7])
                    txtremm.delete('1.0','end')
                    txtremm.insert(tkinter.END,med[0][9])
                else:
                    messagebox.showerror("Message d'erreur","Ce medicament n'a pas ete enregistre sur notre systeme.")
            
        def FenEffectuerAchat():
            global txtco,txtdescriptionac, txtcodeac, txtcomac, txtdateac, txtquantac, txtquantstac, txtuniteac, txtpx, tr
            fen=tkinter.Toplevel(fenp)
            fen.title('Effectuer Achat')
            #fenprinc.iconbitmap('Images/pharmacie.ico')
            larg=1220
            haut=660
            largeecran=fen.winfo_screenwidth()
            hautecran=fen.winfo_screenheight()
            x=(largeecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fen.geometry('%dx%d+%d+%d' % (larg,haut,x,y))    
            legend=tkinter.LabelFrame(fen,text='Approvisonnement de produit')
            lbco = tkinter.Label(legend, text='Code de produit')
            lbdescription=tkinter.Label(legend,text='Description')
            lbunite=tkinter.Label(legend,text='Unite')
            lbcom=tkinter.Label(legend,text='Composition')
            butr=tkinter.Button(legend,text='Afficher',command=lambda:RechercherProdPourAchat())
            lbcodeach=tkinter.Label(legend,text="Numero de l'achat")
            lbQuantites=tkinter.Label(legend,text='Quantite en stock')
            lbquantitea=tkinter.Label(legend,text='Quantite acheter')
            lbdateach=tkinter.Label(legend,text="Date de l'achat")
            lbpx=tkinter.Label(legend,text='Prix')
            butv=tkinter.Button(legend,text='Valider',command=lambda:ValiderAchat())
            buta=tkinter.Button(legend,text='Annuler')
            
            tr=tkinter.ttk.Treeview(legend,columns=('Numero Produit','Description','Unite','Composition','Quantite-stock','Quantite-acheter','Date-achat'),show='headings',height=24)
            tr.heading('Numero Produit',text='Numero Produit')
            tr.heading('Description',text='Description')
            tr.heading('Unite',text='Unite')
            tr.heading('Composition',text='Composition')
            tr.heading('Quantite-stock',text='Quantite-stock')
            tr.heading('Quantite-acheter',text='Quantite-acheter')
            tr.heading('Date-achat',text='Date-achat')
            
            tr.column('Quantite-stock',width=90)
            #tr.column('Quantite-acheter',width=100)
            tr.column('Date-achat',width=90)

            txtco = tkinter.Entry(legend, width=30)
            txtdescriptionac=tkinter.Entry(legend,width=30)
            txtdescriptionac.configure(state='disabled')
            txtuniteac=tkinter.Entry(legend,width=30)
            txtuniteac.configure(state='disabled')
            txtcomac=tkinter.Entry(legend,width=30)
            txtcomac.configure(state='disabled')
            txtcodeac=tkinter.Entry(legend,width=30)
            txtcodeac.configure(state='disabled')
            txtquantstac=tkinter.Entry(legend,width=30)
            txtquantstac.configure(state='disabled')
            txtquantac=tkinter.Entry(legend,width=30)
            txtpx=tkinter.Entry(legend,width=30)
            txtpx.configure(state='disabled')

            dte=datetime.date.today()
            txtdateac=tkinter.Entry(legend,width=30)
            txtdateac.insert(tkinter.END,dte)
            txtdateac.configure(state='disabled')
            
            
            legend.grid(row=0,column=0)
            lbco.grid(row=0,column=0,padx=5,pady=5)
            txtco.grid(row=0,column=1,padx=5,pady=5)
            butr.grid(row=0,column=2)
            lbdescription.grid(row=1,column=0,padx=5,pady=5)
            txtdescriptionac.grid(row=1,column=1,padx=5,pady=5)
            lbunite.grid(row=1,column=2,padx=5,pady=5)
            txtuniteac.grid(row=1,column=3,padx=5,pady=5)
            lbcom.grid(row=1,column=4,padx=5,pady=5)
            txtcomac.grid(row=1,column=5,padx=5,pady=5)

            lbcodeach.grid(row=2,column=0,padx=5,pady=5)
            txtcodeac.grid(row=2,column=1,padx=5,pady=5)
            lbQuantites.grid(row=2,column=2,padx=5,pady=5)
            txtquantstac.grid(row=2,column=3,padx=5,pady=5)
            lbquantitea.grid(row=2,column=4,padx=5,pady=5)
            txtquantac.grid(row=2,column=5,padx=5,pady=5)
            lbpx.grid(row=3,column=0,padx=5,pady=5)
            txtpx.grid(row=3,column=1,padx=5,pady=5)
            lbdateach.grid(row=3,column=2,padx=5,pady=5)
            txtdateac.grid(row=3,column=3,padx=5,pady=5)
            #lbhr.grid(row=2,column=2)
            #txthr.grid(row=1,column=3)
            butv.grid(row=4,column=1)
            buta.grid(row=4,column=3)
            tr.grid(row=5,column=0,rowspan=15,columnspan=15,sticky=('N','S','W','E'))
            fen.transient(fenp)
            fen.resizable(width=False,height=False)
            fen.mainloop()
             
        def RechercherProdPourAchat():
            global txtco,txtdescriptionac,txtcodeac,txtcomac,txtdateac,txtquantac,txtquantstac,txtuniteac,txtpx,tr
            #Recuperer de donnees
            id_prod=txtco.get()
            description=txtdescriptionac.get()
            unite=txtuniteac.get()
            composition=txtcomac.get()
            if id_prod == '':
                messagebox.showerror("Information", "le champ de texte pour le code du medicament est vide.")
            # elif description=='':
            #     messagebox.showerror("Information","le champ de texte pour la description du medicament est vide.")
            # elif unite=='':
            #     messagebox.showerror("Information","le champ de texte pour le nom de l'unite du medicament est vide.")
            # elif composition=='':
            #     messagebox.showerror("Information","le champ de texte pour la composition du medicament est vide.")
            else:               
                #rechercher le produit a acheter
                rechmedic=medic.RechercherMedicament(id_prod)
                txtdescriptionac.configure(state='normal')
                txtdescriptionac.delete(0, 'end')
                txtdescriptionac.insert(tkinter.END,rechmedic[0][1])
                txtdescriptionac.config(state='disabled')
                txtuniteac.config(state='normal')
                txtuniteac.delete(0,'end')
                txtuniteac.insert(tkinter.END,rechmedic[0][5])
                txtuniteac.config(state='disabled')
                txtcomac.config(state='normal')
                txtcomac.delete(0,'end')
                txtcomac.insert(tkinter.END,rechmedic[0][8])
                txtcomac.config(state='disabled')
                #composition
                txtquantstac.configure(state='normal')
                txtquantstac.delete(0,'end')
                txtquantstac.insert(tkinter.END,rechmedic[0][4]) #retourner la valeur quantite
                txtquantstac.configure(state='disabled')
                id_ac=random.randint(000000000000000,100000000000000) #nombre aleatoire de code achat
                txtcodeac.configure(state='normal')
                txtcodeac.delete(0,'end')
                txtcodeac.insert(tkinter.INSERT,id_ac)# numero aleatoire de different produit
                txtcodeac.configure(state='disabled') # Griser le champ numero achat
                txtpx.configure(state='normal')  # griser le champ prix unitaire
                txtpx.delete(0,'end') # nettoyer le champ prix 
                txtpx.insert(tkinter.END,rechmedic[0][3]) # Inserer le Prix unitaire dans le champ de texte
                txtpx.config(state='disabled')
            
        def ValiderAchat():
            id_prod=txtco.get()
            description=txtdescriptionac.get()
            unite=txtuniteac.get()
            composition=txtcomac.get()
            quantite_stock=txtquantstac.get()
            quantite_ac=txtquantac.get()
            id_ach=txtcodeac.get()
            prix=txtpx.get()
            # date_ach=txtdateac.get()

            #Condition si les champs sont vides.
            if description=='':
                messagebox.showerror("Information","le champ de texte pour la description du medicament est vide.")
            elif unite=='':
                messagebox.showerror("Information","le champ de texte pour le nom de l'unite du medicament est vide.")
            elif composition=='':
                messagebox.showerror("Information","le champ de texte pour la composition du medicament est vide.")
            elif quantite_stock=='':
                messagebox.showerror("Information", "le champ de quantite en stock de medicament est vide.")
            elif quantite_stock == '0':
                messagebox.showwarning("Attention", "la quantite  ne peut pas etre egale a zero.")
            elif quantite_stock.isalpha():
                messagebox.showwarning("Attention", "le champ quantite achetee peut prendre seulement des valeurs numeriques.")
            elif str(quantite_stock) < str(0):
                messagebox.showwarning("Attention","le champ quantite en stock ne peut pas prendre les nombres negatifs (-) ainsi que les nombres commencant par la signe (+).")

            elif quantite_ac=='':
                messagebox.showerror("Information", "le champ de quantite achete est vide.")
            elif quantite_ac=='0':
                messagebox.showwarning("Attention","le champ quantite achetee ne peut pas egale a zero.")
            elif str(quantite_ac)<str(0):
                messagebox.showwarning("Attention", "le champ quantite ne peut pas prendre les nombres negatifs (-) ainsi que les nombres commencant par la signe (+).")

            elif quantite_ac.isalpha():
                messagebox.showwarning("Attention", "le champ quantite achetee peut prendre seulement des valeurs numeriques.")
            # elif re.search(r'^[+]',quantite_ac) :
            #     messagebox.showwarning("Attention",'le champ quantite ne peut pas prendre les nombres negatifs ainsi que les nombres commencant par la signe (+).')
            elif id_ach=="":
                messagebox.showerror("Information", "le champ id achat est vide.")
            elif prix=="":
                messagebox.showerror("Information", "le champ de prix de medicament est vide.")
            elif prix.isalpha():
                messagebox.showwarning("Attention","le champ de prix peut prendre seulement des valeurs numeriques.")
            elif id_ach.isalpha():
                messagebox.showwarning("Attention","le champ id  achat peut prendre seulement des valeurs numeriques.")
            else:
                #si on trouve, on recupere le code du produit ainsi que
                rechmedic=medic.RechercherMedicament(id_prod) #methode qui va rechercher l'id du produit et quantite, et prix
                id_prod=rechmedic[0][0] #le code du produit
                quantite_stock=rechmedic[0][4] # la quantite en stock qui est enregistre dans la base de donnees.
                quantite=rechmedic[0][4] 
                quantite_ach=txtquantac.get() #la quantite acheter
                date_ach=datetime.date.today() # la date du systeme considere pour la date achat journalier.
                #Insertion achat
                id_ach=txtcodeac.get() #Recuperer l'id de l'achat qui a ete ajoute dans le champ precedemment
                ach.EffectuerAchat(id_ach,id_prod,quantite_stock,quantite_ach,date_ach) #Methode effectuer achat
                #Update le stock
                medic.AugmenterStockMedic(id_prod,quantite_ach) #Methode augmentation de stock de medicament
                messagebox.showinfo("Information","Validation de l'achat reussie...")  #message
                txtco.delete(0,'end')
                txtdescriptionac.delete(0,'end')
                txtuniteac.delete(0,'end')
                txtcomac.delete(0,'end')
                txtcodeac.delete(0,'end')
                txtpx.delete(0,'end')
                txtquantstac.delete(0,'end')
                txtquantac.delete(0,'end')
                txtdateac.delete(0,'end')

                #Remplir la grille avec les donnees de l'achat en cours a chaque validation
                tr.insert('','end',values=(id_ach,description,unite,composition,quantite,quantite_ach,date_ach))


        def FenListeAchat():
            fen=tkinter.Toplevel(fenp)
            fen.title('Liste des achats')
            # fen.iconbitmap()
            larg=1050
            haut=660
            largecran=fen.winfo_screenwidth()
            hautecran=fen.winfo_screenheight()
            x=(largecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fen.geometry('%dx%d+%d+%d'%(larg,haut,x,y))
            legend=tkinter.LabelFrame(fen,text='liste des achats de la journee')
            legend.grid(row=0,column=0) #positionner la legende dans la fenetre
            tr=tkinter.ttk.Treeview(legend,columns=('code achat','code produit','quantite en stock','quantite achete','date-achat'),show='headings',height=30)
            tr.heading('code achat',text='code achat')
            tr.heading('code produit',text='code produit')
            tr.heading('quantite en stock',text='quantite en stock')
            tr.heading('quantite achete',text='quantite achete')
            tr.heading('date-achat',text='date-achat')
            #Remplir la grille de donnees
            #methode lister
            date_ach=datetime.date.today()
            ac=ach.ListeAchatJr(date_ach)
            codeac=[x[0] for x in ac] #recuperer toutes les premieres valeurs qui se trouvent dans le tuple qui contiennent des tuples
            codep=[x[1] for x in ac]
            qtst=[x[2] for x in ac]
            qtac=[x[3] for x in ac]
            dat=[x[4] for x in ac]
            #Fusionner les valeurs
            for ca,cp,qts,qta,da in zip(codeac,codep,qtst,qtac,dat):
                tr.insert('','end',values=(ca,cp,qts,qta,da))

            tr.grid(row=1,column=0,rowspan=12,columnspan=12,sticky=('N','W','S','E'))
            fen.resizable(width=False,height=False)
            fen.transient(fenp) # rendre la fenetre fille depend de la fenetre mere
            fen.mainloop() # affichage de la fenetre

        def FenRechercherAchat():

            fen = tkinter.Toplevel(fenp)
            fen.title('Rechercher un achat')
            # fen.iconbitmap()
            larg = 500
            haut = 300
            largecran = fen.winfo_screenwidth()
            hautecran = fen.winfo_screenheight()
            x = (largecran / 2) - (larg / 2)
            y = (hautecran / 2) - (haut / 2)
            fen.geometry('%dx%d+%d+%d' % (larg, haut, x, y))
            legend=tkinter.LabelFrame(fen,text='Rechercher')
            lbcode=tkinter.Label(legend)
            txtcode=tkinter.Entry(legend,width=30)
            butre=tkinter.Button(legend,text='Rechercher')
            butan=tkinter.Button(legend,text='Annuler')
            legend.grid(row=0,column=0)






        def FenEffectuerVente():
            global fenprinc,txtnompro,txtpri,txtquantdisp,prod,txtdem,lbcheck1,treeresult,txtmontp
            fenprinc=tkinter.Toplevel(fenp)
            fenprinc.title('Fenetre de vente de medicament')
            fenprinc.iconbitmap('Images/pharmacie.ico')
            larg=1360
            haut=660
            largeecran=fenprinc.winfo_screenwidth()
            hautecran=fenprinc.winfo_screenheight()
            x=(largeecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fenprinc.geometry('%dx%d+%d+%d' % (larg,haut,x,y))
            nompr=tkinter.StringVar()
            lbtit=tkinter.Label(fenprinc,text='Effectuer une vente',font=('arial',20,'bold'),fg='green',bg='white')
            log=Image.open('Images/784072.png')
            lo=ImageTk.PhotoImage(log.resize((80,50)),master=fenprinc)
            lb=tkinter.Label(fenprinc,image=lo)
            lb.lo=lo
            lb.grid(row=0,column=5)
            lbnompro=tkinter.Label(fenprinc,text='Nom du medicament',bg='black',fg='white')
            lbvendeur=tkinter.Label(fenprinc,text='Vendeur: '+txtnomut.get(),bg='white',font=('arial',10,'bold'))
            txtnompro=tkinter.Entry(fenprinc,textvariable=nompr,width=30,fg='green')
            lbcrite=tkinter.Label(fenprinc,text='Critère de recherche:')
            butaj=tkinter.Button(fenprinc,text='Valider',command=lambda:ValiderVente())

            # styl.configure("Treeview", background='#D3D3D3', foreground='black', rowheight=25, fieldbackground='#D3D3D3')
            # styl.map("Treeview", background=[('selected', 'red')])
            treeresult=ttk.Treeview(fenprinc,columns=('Description','Quantite','Prix','Montant','Categorie'),show='headings',height=15)
            treeresult.heading('Description',text='Description')
            treeresult.column('Description',width=50)
            treeresult.heading('Quantite',text='Quantite')
            treeresult.column('Quantite',width=50)
            treeresult.heading('Prix',text='Prix')
            treeresult.column('Prix',width=50)
            treeresult.heading('Montant',text='Montant')
            treeresult.column('Montant',width=50)
            treeresult.heading('Categorie',text='Categorie')
            treeresult.column('Categorie',width=50)
            sc=ttk.Scrollbar(fenprinc,command=treeresult.yview,orient='vertical')
            treeresult.configure(yscrollcommand=sc.set)

            # style.theme_use('clam') #Definir un theme pour la grille
            style = ttk.Style()
            style.theme_use('default')
            style.configure("Treeview", background="red", foreground='white', borderwidth=0, fieldbackground='red',relief='flat')

            sc.grid(row=7,column=5,sticky='nswe')
            
            # style.configure("Treeview",background='green',foreground='black')
            lbquantdisp=tkinter.Label(fenprinc,text='Quantité disponible:',bg='black',fg='white')
            txtquantdisp=tkinter.Entry(fenprinc,width=5)
            txtquantdisp.config(state='disabled')
            lbpr=tkinter.Label(fenprinc,text='Prix unitaire:',bg='black',fg='white')
            txtpri=tkinter.Entry(fenprinc,width=15)
            txtpri.config(state='disabled')
            lbinfcli=tkinter.Label(fenprinc,text='Informations du client:',bg='white',font=('arial',10,'bold'))
            lbdem=tkinter.Label(fenprinc,text='Quantité demandé par le client',bg='gray',fg='aqua')
            txtdem=tkinter.Entry(fenprinc,width=5)     
            
            prod=tkinter.StringVar()
            prod.set("Sirop") #Rendre select le premier bouton radio
            def affp():
                global prod
            lbcheck1=tkinter.ttk.Combobox(fenprinc,values=('tube','comprimé','sirop','ml','gramme','nombre'),width=27)
            lbcheck1.config(state='readonly') #Rendre le combobox non modifiable
            # lbcheck1=tkinter.Radiobutton(master=fenprinc,text='Sirop',variable=prod,value='Sirop',command=lambda:affp(),activeforeground='gray')
            # lbcheck2=tkinter.Radiobutton(fenprinc,text='Comprimé',variable=prod,value='Comprimé',command=lambda:affp(),activeforeground='gray')
            # lbcheck3=tkinter.Radiobutton(fenprinc,text='Piqure',variable=prod,value='Piqure',command=lambda:affp(),activeforeground='gray')
            # lbcheck4=tkinter.Radiobutton(fenprinc,text='Serum',variable=prod,value='Serum',command=lambda:affp(),activeforeground='gray')

            lbmontp=tkinter.Label(fenprinc,text='Montant à payer:',fg='Green',font=('arial',12,'bold'))
            txtmontp=tkinter.Entry(fenprinc,width=19,font=('arial',12,'bold'))
            txtmontp.insert(tkinter.END,'0.0')
            txtmontp.configure(state='disabled')
            butrec=tkinter.Button(fenprinc,text='Rechercher',command=lambda:RechercherMedicamentVente())
            butv=tkinter.Button(fenprinc,text='Imprimer',bg='green',fg='aqua',command=lambda:ImprimerVente())
            buta=tkinter.Button(fenprinc,text='Annuler',bg='green',fg='aqua') 
            butaa=tkinter.Button(fenprinc,text='Annuler',bg='green',fg='aqua') 
            #calcul=tkinter.StringVar()
            #Champ de la Calculatrice
            # lbcall=tkinter.Label(fenprinc,text='Votre calculatrice',font=('arial',12,'bold'))
            champcalcula=tkinter.Entry(fenprinc,width=60,bg='white',borderwidth=3)
            #les boutons de la calculatrice
            
            def bouton_click(nombre):
                chnombre=champcalcula.get()
                champcalcula.delete(0,'end')
                champcalcula.insert(tkinter.END,str(chnombre)+str(nombre))
                      
            def boutonaddition():
                premiernombre=champcalcula.get()
                global nombre_entre_plus, op
                op=1
                nombre_entre_plus=int(premiernombre)
                champcalcula.delete(0,'end')

            def boutonmoins():
                premiernombre=champcalcula.get()
                global nombre_entre_moins,op
                op=2
                nombre_entre_moins=int(premiernombre)
                champcalcula.delete(0,'end')

            def boutoneffacer():
                champcalcula.delete(0,'end')
                
            def boutonegal():
                secondnombre=champcalcula.get()
                if op==1:
                    champcalcula.delete(0,'end')
                    champcalcula.insert(tkinter.END, int(secondnombre)+int(nombre_entre_plus))
                if op==2:
                    champcalcula.delete(0,'end')
                    champcalcula.insert(tkinter.END, abs(int(secondnombre)-int(nombre_entre_moins)))
                   
            

                
            but9=tkinter.Button(fenprinc, text='9', padx=40,pady=20, command=lambda:bouton_click(9),width=8,bg='aqua')
            but8=tkinter.Button(fenprinc, text='8',padx=40,pady=20, command=lambda:bouton_click(8),width=8,bg='aqua')
            but7=tkinter.Button(fenprinc, text='7',padx=40,pady=20, command=lambda:bouton_click(7),width=8,bg='aqua')
            but6=tkinter.Button(fenprinc, text='6',padx=40,pady=20, command=lambda:bouton_click(6),width=8,bg='aqua')
            but5=tkinter.Button(fenprinc, text='5',padx=40,pady=20, command=lambda:bouton_click(5),width=8,bg='aqua')
            but4=tkinter.Button(fenprinc, text='4',padx=40,pady=20, command=lambda:bouton_click(4),width=8,bg='aqua')
            but3=tkinter.Button(fenprinc, text='3',padx=40,pady=20, command=lambda:bouton_click(3),width=8,bg='aqua')
            but2=tkinter.Button(fenprinc, text='2',padx=40,pady=20, command=lambda:bouton_click(2),width=8,bg='aqua')
            but1=tkinter.Button(fenprinc, text='1',padx=40,pady=20, command=lambda:bouton_click(1),width=8,bg='aqua')
            but0=tkinter.Button(fenprinc, text='0',padx=40,pady=20, command=lambda:bouton_click(0),width=8,bg='aqua')
            butmoins=tkinter.Button(fenprinc, text='-',padx=40,pady=20, command=lambda:boutonmoins(),width=8,bg='aqua')
            butpoint=tkinter.Button(fenprinc, text='.',padx=40,pady=20,width=8,command='',bg='aqua')
            butplus=tkinter.Button(fenprinc, text='+',padx=40,pady=20,width=8,bg='aqua',command=lambda:boutonaddition())
            butegal=tkinter.Button(fenprinc, text='=',padx=40,pady=20,width=8,bg='aqua',command= lambda:boutonegal())
            butdiv=tkinter.Button(fenprinc, text='/',padx=40,pady=20,width=8,bg='aqua')
            butmul=tkinter.Button(fenprinc, text='*',padx=40,pady=20,width=8,bg='aqua')
            butCE=tkinter.Button(fenprinc, text='CE',padx=40,pady=20,width=8,bg='aqua')
            butpourc=tkinter.Button(fenprinc, text='%',padx=40,pady=20,width=8,bg='aqua')
            butplusouMoins=tkinter.Button(fenprinc, text='+/-',padx=40,pady=20,width=8,bg='aqua')
            butC=tkinter.Button(fenprinc, text='C',padx=40,pady=20,width=8,bg='aqua',command= lambda:boutoneffacer())
            
           
            
            lbtit.grid(row=0,column=4)
            lbvendeur.grid(row=1,column=0)
            lbnompro.grid(row=2,column=0)
            txtnompro.grid(row=2,column=1,padx=3,pady=3)
            
            lbcrite.grid(row=3,column=0,padx=5,pady=5)
            lbcheck1.grid(row=3,column=1,padx=5,pady=5)
            # lbcheck2.grid(row=3,column=2,padx=8,pady=8)
            # lbcheck3.grid(row=3,column=3)
            # lbcheck4.grid(row=3,column=4)
            # lbcal.grid(row=2,column=10)
            champcalcula.grid(row=3,column=9,columnspan=3) #le champ entrer
            butrec.grid(row=4,column=0,padx=5,pady=5)
            buta.grid(row=4,column=1,padx=5,pady=5)
            lbquantdisp.grid(row=5,column=0) 
            txtquantdisp.grid(row=5,column=1) 
            lbpr.grid(row=5,column=2,padx=8,pady=8) 
            txtpri.grid(row=5,column=3,padx=8,pady=8) 
            lbinfcli.grid(row=6,column=0,padx=8,pady=8)   
            lbdem.grid(row=6,column=1,padx=8,pady=8)  
            txtdem.grid(row=6,column=2,padx=8,pady=8)  
            butaj.grid(row=6,column=3,padx=5,pady=5)
            treeresult.grid(row=7,column=0,rowspan=5,columnspan=5,sticky=('N','W','E','S'))
            lbmontp.grid(row=15,column=0,padx=8,pady=8)
            txtmontp.grid(row=15,column=1,padx=8,pady=8)
            butv.grid(row=16,column=1,padx=5,pady=5)
            butaa.grid(row=16,column=3,padx=5,pady=5)
            #positionnement de la bouton de la calculatrice...
            but7.grid(row=4, column=9)
            but8.grid(row=4,column=10)
            but9.grid(row=4, column=11)
            but4.grid(row=5,column=9)
            but5.grid(row=5,column=10)
            but6.grid(row=5,column=11)
            but1.grid(row=6,column=9)
            but2.grid(row=6,column=10)
            but3.grid(row=6,column=11)
            but0.grid(row=7,column=9)
            butpoint.grid(row=7, column=10)
            butegal.grid(row=7, column=11)
            butCE.grid(row=8,column=9)
            butpourc.grid(row=8,column=10)
            butplusouMoins.grid(row=8,column=11)
            butdiv.grid(row=9,column=9)
            butmul.grid(row=9,column=10)
            butmoins.grid(row=9,column=11)
            butplus.grid(row=10,column=9)
            butC.grid(row=10,column=10)
            #fenprinc.state('zoomed') #rendre extrement large la fenetre
            #fenprinc.config(bg='white') #couleur de l'arriere plan de la fenetre
            fenprinc.resizable(width=False,height=False)
            fenprinc.transient(fenp)
            fenprinc.mainloop() # boucle d'affichage de tkinter.

        def RechercherMedicamentVente():
            global fenprinc,txtnompro,txtquantdisp,prod,txtpri,id_prod
            description=txtnompro.get()
            unite=lbcheck1.get()  # prod.get()
            if description== '':
                messagebox.showerror("Resultat de recherche", "Vous avez laisser vide le champ nom de medicament.")
            elif unite == '':
                messagebox.showerror("Resultat de recherche", "Il faut selectionner un critere de recherche.")

            else:
                p=medic.RechercherMedicamentPourVente(description,unite)  #place au methode rechercher medicament afin de retrouver id du produit
                id_prod=p[0][0] #Recuperer le code du medicament rechercher
                txtquantdisp.config(state='normal')
                txtquantdisp.delete(0, 'end')
                txtquantdisp.insert(tkinter.INSERT,p[0][4])
                txtquantdisp.config(state='disabled')
                txtpri.config(state='normal')
                txtpri.delete(0,'end')
                txtpri.insert(tkinter.INSERT,p[0][3])
                txtpri.config(state='disabled')

        def ValiderVente():
            global id_prod
            id_v=random.randint(00000000000000000000,10000000000000000000)#nombre aleatoire
            description=txtnompro.get()#description du produit
            unite=lbcheck1.get()#l'unite de produit
            prix=txtpri.get()#le prix 
            quanntitest=txtquantdisp.get()#la quantite
            quantite_v=txtdem.get()#la quantite de vente
            categorie=lbcheck1.get()# le categorie
            datevente=datetime.date.today()# la date de la vente
            if description=="":
                messagebox.showerror("Information","Vous avez laisser vide le champ description de medicament.")
            elif unite=='':
                messagebox.showerror("Information","Il faut choisi un critere de recherche.")
            elif str(quantite_v) == "":
                messagebox.showerror("Information", "Vous avez laisser vide le champ de quantite de vente.")
            elif str(quantite_v) == '0':
                messagebox.showwarning("Attention", "Ce champ ne peut pas avoir des valeurs nulles.")
            elif str(quantite_v)<str('0'):
                messagebox.showwarning("Attention", "Ce champ ne peut pas avoir des nombres negatifs et positifs.")
            elif str(quantite_v).isalpha():
                messagebox.showwarning("Attention", "Ce champ ne peut pas recevoir des nombres alphabetiques.")
            else:
                p = medic.RechercherMedicamentPourVente(description,unite)  # place au methode rechercher medicament afin de retrouver id du produit
                id_prod = p[0][0] # on recupere l'identifiant du produit
                quantite_v = int(txtdem.get())
                prix=int(txtpri.get())
                montant=quantite_v * prix
                vent.EffectuerVente(id_v, id_prod, quantite_v, prix, montant, datevente)# methode insertion dans la table vente
                medic.DiminuerStockMedic(id_prod, quantite_v)# methode de dimunition dans la table de medicament
                treeresult.insert('','end',values=(description,quantite_v,prix,montant,categorie)) #Remplir le champ treeview
                tot = 0.0
                for tbl in treeresult.get_children():
                    #normal
                    txtmontp.configure(state='normal')
                    tot+=float(treeresult.item(tbl,'values')[3]) #Recuperer toutes les valeurs de la colonne 3
                    txtmontp.delete(0,'end') #Supprimer les dernieres valeurs du montant et ajouter la nouvelle valeur montant
                txtmontp.insert(tkinter.END,str(tot)+str(" Gourdes")) # Inserer la valeur dans le champ
                txtmontp.config(state='disabled') #Griser le champ
                #Nettoyer le champ apres avoir valider la vente
                txtnompro.delete(0,'end')
                txtquantdisp.config(state='normal')
                txtquantdisp.delete(0,'end')
                txtquantdisp.config(state='disabled')
                txtpri.config(state='normal')
                txtpri.delete(0,'end')
                txtpri.config(state='disabled')
                txtdem.delete(0,'end')
                lbcheck1.delete(0,'end')

                # messagebox.showinfo("Information","Une vente a ete effectue avec succes.") #message de reussite

        def ImprimerVente():
            #Definition de style
            styleN=getSampleStyleSheet()
            styleNN=getSampleStyleSheet()
            stylea=styleN['Normal']
            styleb=styleNN['Normal']
            stylea.alignment=TA_CENTER
            stylea.fontSize=12
            stylea.font='bold'
            styleb.fontSize=10
            styleb.alignment=TA_CENTER #ajuster au centre.
            elements=[] #liste vide
            #mettre un image
            imag=Image.open('Images/800x600_logo-pharmacie-2309.jpg')
            im=ImageTk.PhotoImage(imag.resize((20,30)),master=fenp)
            # elements.append(im)
            elements.append(Paragraph("PharmaTech",stylea))#ajouter des paragraphes#
            elements.append(Spacer(0,13))
            elements.append(Paragraph("Adresse: delmas 95 impasse jacob",styleb))
            elements.append(Paragraph("Telephone: +(509)4900-2300",styleb))
           #Pour chaque dans la table, on recupere
            colo = []
            colo.append(['Description', 'Quantite', 'Prix'])# creation de l'entete
            tb = Table(colo)  # ajouter les entetes dans une table
            tb.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                     ('Box', (0, 0), (-1, -1), 0.25, colors.black),
                                     ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                     ], colWidths=[130, 250, 135]))
            elements.append(tb) #ajouter le tableau dans la liste
            for tb in treeresult.get_children():

                descript= str(treeresult.item(tb,'values')[0])
                quant = str(treeresult.item(tb, 'values')[1])
                px=str(treeresult.item(tb, 'values')[2])
                #ajouter les donnnes
                col=[[descript,quant,px]]
                tbl=Table(col)#ajouter les entetes dans une table
                tbl.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                       ('Box', (0, 0), (-1, -1), 0.25, colors.black),
                                       ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                       ], colWidths=[130, 250, 135]))
                elements.append(tbl)
            # nom de la machine du client
            nomutilisateur=os.getenv('username')
            # Creation de repertoire s'il n'existe pas
            if not os.path.exists("C:/Users/"+nomutilisateur+"/Desktop/ImpressionVentePharmatech"):
                os.makedirs("C:/Users/"+nomutilisateur+"/Desktop/ImpressionVentePharmatech")
            #Creation de document
            doc=SimpleDocTemplate("C:/Users/"+nomutilisateur+"/Desktop/ImpressionVentePharmatech/vente1.pdf",pagesize=landscape(A5),title='Fiche de vente',author='Pharmatech')
            #Construire le document
            doc.build(elements)
            #lancer le fichier
            os.startfile("C:/Users/"+nomutilisateur+"/Desktop/ImpressionVentePharmatech/vente1.pdf")


        def FenEmbaucherEmp():
            global txtnom,txtpre,txtsex,txtdatn,txtlieu,txtad,txttype,txtetat,txtsal,txttelep,lbpho,chemin,lbphot,fen #rendre accessibles
            fen=tkinter.Toplevel(fenp)
            fen.title("Embaucher un employe")#titre de la fenetre
            #centrer la fenetre
            larg=635
            haut=420
            largecran=fen.winfo_screenwidth()# Retrouver la largeur de l'ecran
            hautecran=fen.winfo_screenheight()# Retrouver la hauteur de l'ecran
            x=(largecran/2)-(larg/2) #decouper en deux la largeur de l'ecran par rapport a la largeur de la fenetre
            y=(hautecran/2)-(haut/2) # decouper en deux la hauteur de l'ecran par rapport a la hauteur de la fenetre
            fen.geometry('%dx%d+%d+%d'%(larg,haut,x,y))
            legend=tkinter.LabelFrame(fen,text='Embaucher un employe') #creation de legende.
            lbnom=tkinter.Label(legend,text='Nom')#nom
            txtnom=tkinter.Entry(legend,width=30)
            lbpre=tkinter.Label(legend,text='Prenom')
            txtpre=tkinter.Entry(legend,width=30)
            lbsex=tkinter.Label(legend,text='Sexe')
            txtsex=tkinter.ttk.Combobox(legend,values=('Masculin','Feminin'),width=27)
            lbdatn = tkinter.Label(legend, text='Date de naissance')
            txtdatn=DateEntry(legend,background='white',foreground='green',borderwidth=2,locale='fr_FR',width=27)
            lblieu=tkinter.Label(legend,text='Lieu de naissance')
            txtlieu=tkinter.Entry(legend,width=30)
            lbad = tkinter.Label(legend, text='Adresse')
            txtad = tkinter.Entry(legend, width=30)
            lbtype= tkinter.Label(legend, text="Type d'emploi")
            txttype = tkinter.Entry(legend, width=30)
            lbetat = tkinter.Label(legend, text='Etat')
            txtetat = tkinter.Entry(legend, width=30)
            lbsal = tkinter.Label(legend, text='Salaire')
            txtsal = tkinter.Entry(legend, width=30)
            lbtelep = tkinter.Label(legend, text='Telephone')
            txttelep = tkinter.Entry(legend, width=30)
            def ParcouriRepertoire():
                global chemin
                chemin=filedialog.askopenfilename(initialdir='/',title="Ajouter une photo pour l'employe",filetype=(('jpeg files','*.jpg'),('All files','*.*')))
                #lire l'image #ouverture de l'image
                ima=Image.open(chemin)
                img=ImageTk.PhotoImage(ima.resize((200,150)),master=legend)# redimensionner l'image
                lbphot=tkinter.Label(legend,image=img)
                lbphot.img=img #ajouter l'image dans le label
                lbphot.grid(row=5, column=3)
                
            butpar=tkinter.Button(legend,text='Parcourir',command=lambda:ParcouriRepertoire())
            butemb=tkinter.Button(legend,text='Embaucher',command=lambda:EmbaucherEmploye())
            butann=tkinter.Button(legend,text='Annuler')
            lbph = tkinter.Label(legend, text='Photo')
            ph=Image.open("Images/8c8b3766126753c6d098cdb2e42cff49.png")#ajouter une image
            ph1=ImageTk.PhotoImage(ph.resize((200,150)),master=fen)#redimensionner l'image, #largeur par hauteur, #
            lbpho=tkinter.Label(legend,image=ph1) #ajouter l'image dans un label
            lbpho.ph1=ph1 #afficher l'image
            #positionnement des widgets
            legend.grid(row=0,column=0)#positionnement de la legende
            lbnom.grid(row=0,column=0, padx=5, pady=5)
            txtnom.grid(row=0,column=1,padx=5, pady=5)
            lbpre.grid(row=0,column=2,padx=5, pady=5)
            txtpre.grid(row=0,column=3,padx=5, pady=5)
            lbsex.grid(row=1,column=0,padx=5, pady=5)
            txtsex.grid(row=1,column=1,padx=5, pady=5)
            lbdatn.grid(row=1,column=2,padx=5, pady=5)
            txtdatn.grid(row=1,column=3, padx=5, pady=5)
            lblieu.grid(row=2, column=0, padx=5, pady=5)
            txtlieu.grid(row=2, column=1, padx=5, pady=5)
            lbad.grid(row=2, column=2, padx=5, pady=5)
            txtad.grid(row=2, column=3, padx=5, pady=5)
            lbtype.grid(row=3,column=0, padx=5, pady=5)
            txttype.grid(row=3,column=1, padx=5, pady=5)
            lbetat.grid(row=3, column=2, padx=5, pady=5)
            txtetat.grid(row=3, column=3, padx=5, pady=5)
            lbsal.grid(row=4, column=0, padx=5, pady=5)
            txtsal.grid(row=4, column=1, padx=5, pady=5)
            lbtelep.grid(row=4, column=2, padx=5, pady=5)
            txttelep.grid(row=4, column=3, padx=5, pady=5)
            lbph.grid(row=5, column=2, padx=5, pady=5)
            lbpho.grid(row=5, column=3, padx=5, pady=5)
            butpar.grid(row=6,column=3, padx=5, pady=5)
            butemb.grid(row=7,column=1)
            butann.grid(row=7,column=2)
            fen.transient(fenp) #rendre la fenetre depend de la fenetre mere
            fen.resizable(width=False,height=False) #rendre non redimensionnable
            fen.mainloop()# afficher la fenetre

        def FenModifierEmp():
            global txtcode, txtnom, txtprenom, txtsex, txtdatn, txtlieu, txtad, txttype, txtetat, txtsal, txttelep, lbpho, chemin, lbphot, fen # les variables globales.
            fen = tkinter.Toplevel(fenp)
            fen.title("Modifier un employé") #titre de la fenetre
            # centrer la fenetre
            larg = 635 # definir ma propre largeur
            haut = 450 # definir ma propre hauteur
            largecran = fen.winfo_screenwidth()
            hautecran = fen.winfo_screenheight()
            x = (largecran / 2) - (larg / 2) #decouper en deux la largeur de l'ecran
            y = (hautecran / 2) - (haut / 2)#decouper en deux la hauteur de l'ecran
            fen.geometry('%dx%d+%d+%d' % (larg, haut, x, y))# centrer la fenetre
            legend = tkinter.LabelFrame(fen, text="Modifier l'information sur un employé")  # la legende
            lbcode=tkinter.Label(legend,text="Code de l'employé")
            txtcode=tkinter.Entry(legend,width=30)
            lbnom=tkinter.Label(legend,text='Nom')
            txtnom=tkinter.Entry(legend,width=30)
            lbprenom = tkinter.Label(legend, text='Prenom')
            txtprenom = tkinter.Entry(legend, width=30)
            lbsex = tkinter.Label(legend, text='Sexe')
            txtsex = tkinter.ttk.Combobox(legend, values=('Masculin', 'Feminin'), width=27)
            lbdatn = tkinter.Label(legend, text='Date de naissance')
            txtdatn = DateEntry(legend, background='white', foreground='green', borderwidth=2, locale='fr_FR', width=27)
            lblieu = tkinter.Label(legend, text='Lieu de naissance')
            txtlieu = tkinter.Entry(legend, width=30)
            lbad = tkinter.Label(legend, text='Adresse')
            txtad = tkinter.Entry(legend, width=30)
            lbtype = tkinter.Label(legend, text="Type d'emploi")
            txttype = tkinter.Entry(legend, width=30)
            lbetat = tkinter.Label(legend, text='Etat')
            txtetat = tkinter.Entry(legend, width=30)
            lbsal = tkinter.Label(legend, text='Salaire')
            txtsal = tkinter.Entry(legend, width=30)
            lbtelep = tkinter.Label(legend, text='Telephone')
            txttelep = tkinter.Entry(legend, width=30)
            def parcouririmage():
                global chemin
                chemin=filedialog.askopenfilename(initialdir='/',title='selectionner une autre image pour cet employe',filetype=(('jpeg files','*.jpg'),('All files','*.*')))
                imag=Image.open(chemin)
                img=ImageTk.PhotoImage(imag.resize((200,150)),master=fen)
                lbpho=tkinter.Label(legend,image=img)
                lbpho.img=img
                lbpho.grid(row=6,column=3)

            butparc = tkinter.Button(legend, text='Parcourir',command=lambda:parcouririmage())
            butemb = tkinter.Button(legend, text='Modifier',command=lambda:ModifierEmploye())
            butann = tkinter.Button(legend, text='Annuler',command=fen.quit())
            butre=tkinter.Button(legend,text='Rechercher',command=lambda:RechercherEmploye())
            lbph = tkinter.Label(legend, text='Photo')
            ph1 = Image.open("Images/8c8b3766126753c6d098cdb2e42cff49.png")  # ajouter une image
            ph2 = ImageTk.PhotoImage(ph1.resize((200, 150)),master=fen)  # redimensionner l'image, #largeur par hauteur, #
            lbpho = tkinter.Label(legend, image=ph2)  # ajouter l'image dans un label
            lbpho.ph2 = ph2  # afficher l'image

            #positionnement des widgets
            legend.grid(row=0,column=0)
            lbcode.grid(row=0,column=0,padx=5,pady=5)
            txtcode.grid(row=0,column=1,padx=5,pady=5)
            lbnom.grid(row=1,column=0,padx=5,pady=5)
            txtnom.grid(row=1,column=1,padx=5,pady=5)
            lbprenom.grid(row=1,column=2,padx=5,pady=5)
            txtprenom.grid(row=1,column=3,padx=5,pady=5)
            lbsex.grid(row=2,column=0,padx=5, pady=5)
            txtsex.grid(row=2,column=1,padx=5, pady=5)
            lbdatn.grid(row=2,column=2,padx=5, pady=5)
            txtdatn.grid(row=2,column=3, padx=5, pady=5)
            lblieu.grid(row=3, column=0, padx=5, pady=5)
            txtlieu.grid(row=3, column=1, padx=5, pady=5)
            lbad.grid(row=3, column=2, padx=5, pady=5)
            txtad.grid(row=3, column=3, padx=5, pady=5)
            lbtype.grid(row=4,column=0, padx=5, pady=5)
            txttype.grid(row=4,column=1, padx=5, pady=5)
            lbetat.grid(row=4, column=2, padx=5, pady=5)
            txtetat.grid(row=4, column=3, padx=5, pady=5)
            lbsal.grid(row=5, column=0, padx=5, pady=5)
            txtsal.grid(row=5, column=1, padx=5, pady=5)
            lbtelep.grid(row=5, column=2, padx=5, pady=5)
            txttelep.grid(row=5, column=3, padx=5, pady=5)
            lbph.grid(row=6, column=2, padx=5, pady=5)
            lbpho.grid(row=6, column=3, padx=5, pady=5)
            butparc.grid(row=7,column=3, padx=5, pady=5)
            butre.grid(row=0,column=2)
            butemb.grid(row=8,column=1)
            butann.grid(row=8,column=2)
            fen.transient(fenp)
            fen.resizable(width=False,height=False)
            fen.mainloop()


        def FenRechercherEmp():
            global txtcode,txtnom, txtprenom, txtsex, txtdatn, txtlieu, txtad, txttype, txtetat, txtsal, txttelep, lbpho, chemin, lbphot, fen # les variables globales.
            fen = tkinter.Toplevel(fenp)
            fen.title("Rechercher un employe")  # titre de la fenetre
            # centrer la fenetre
            larg = 635  # definir ma propre largeur
            haut = 400 # definir ma propre hauteur
            largecran = fen.winfo_screenwidth() #largeur ecran
            hautecran = fen.winfo_screenheight() #hauteur ecran
            x = (largecran / 2) - (larg / 2)  # decouper en deux la largeur de l'ecran
            y = (hautecran / 2) - (haut / 2)  # decouper en deux la hauteur de l'ecran
            fen.geometry('%dx%d+%d+%d' % (larg, haut, x, y))  # centrer la fenetre
            legend = tkinter.LabelFrame(fen, text="Rechercher l'information sur un employe")#la legende
            lbcode = tkinter.Label(legend, text="Code de l'employe")
            txtcode = tkinter.Entry(legend, width=30)
            lbnom = tkinter.Label(legend, text='Nom')
            txtnom = tkinter.Entry(legend, width=30)
            lbprenom = tkinter.Label(legend, text='Prenom')
            txtprenom = tkinter.Entry(legend, width=30)
            lbsex = tkinter.Label(legend, text='Sexe')
            txtsex = tkinter.ttk.Combobox(legend, values=('Masculin', 'Feminin'), width=27)
            lbdatn = tkinter.Label(legend, text='Date de naissance')
            txtdatn = DateEntry(legend, background='white', foreground='green', borderwidth=2, locale='fr_FR', width=27)
            lblieu = tkinter.Label(legend, text='Lieu de naissance')
            txtlieu = tkinter.Entry(legend, width=30)
            lbad = tkinter.Label(legend, text='Adresse')
            txtad = tkinter.Entry(legend, width=30)
            lbtype = tkinter.Label(legend, text="Type d'emploi")
            txttype = tkinter.Entry(legend, width=30)
            lbetat = tkinter.Label(legend, text='Etat')
            txtetat = tkinter.Entry(legend, width=30)
            lbsal = tkinter.Label(legend, text='Salaire')
            txtsal = tkinter.Entry(legend, width=30)
            lbtelep = tkinter.Label(legend, text='Telephone')
            txttelep = tkinter.Entry(legend, width=30)
            # butpar = tkinter.Button(legend, text='Parcourir')
            # butemb = tkinter.Button(legend, text='Modifier')
            butann = tkinter.Button(legend, text='Annuler',command=fen.quit())
            butre = tkinter.Button(legend, text='Rechercher',command=lambda:RechercherEmploye())
            lbph = tkinter.Label(legend, text='Photo')
            ph1 = Image.open("Images/8c8b3766126753c6d098cdb2e42cff49.png")  # ajouter une image
            ph2 = ImageTk.PhotoImage(ph1.resize((200, 150)),master=fen)  # redimensionner l'image, #largeur par hauteur, #
            lbpho = tkinter.Label(legend, image=ph2)  # ajouter l'image dans un label
            lbpho.ph2 = ph2  # afficher l'image

            # positionnement des widgets
            legend.grid(row=0, column=0)
            lbcode.grid(row=0, column=0, padx=5, pady=5)
            txtcode.grid(row=0, column=1, padx=5, pady=5)
            lbnom.grid(row=1, column=0, padx=5, pady=5)
            txtnom.grid(row=1, column=1, padx=5, pady=5)
            lbprenom.grid(row=1, column=2, padx=5, pady=5)
            txtprenom.grid(row=1, column=3, padx=5, pady=5)
            lbsex.grid(row=2, column=0, padx=5, pady=5)
            txtsex.grid(row=2, column=1, padx=5, pady=5)
            lbdatn.grid(row=2, column=2, padx=5, pady=5)
            txtdatn.grid(row=2, column=3, padx=5, pady=5)
            lblieu.grid(row=3, column=0, padx=5, pady=5)
            txtlieu.grid(row=3, column=1, padx=5, pady=5)
            lbad.grid(row=3, column=2, padx=5, pady=5)
            txtad.grid(row=3, column=3, padx=5, pady=5)
            lbtype.grid(row=4, column=0, padx=5, pady=5)
            txttype.grid(row=4, column=1, padx=5, pady=5)
            lbetat.grid(row=4, column=2, padx=5, pady=5)
            txtetat.grid(row=4, column=3, padx=5, pady=5)
            lbsal.grid(row=5, column=0, padx=5, pady=5)
            txtsal.grid(row=5, column=1, padx=5, pady=5)
            lbtelep.grid(row=5, column=2, padx=5, pady=5)
            txttelep.grid(row=5, column=3, padx=5, pady=5)
            lbph.grid(row=6, column=2, padx=5, pady=5)
            lbpho.grid(row=6, column=3, padx=5, pady=5)
            # butpar.grid(row=6, column=3, padx=5, pady=5)
            butre.grid(row=0, column=2)
            # butemb.grid(row=7, column=1)
            # butann.grid(row=7, column=2)
            fen.transient(fenp)
            fen.resizable(width=False, height=False)
            fen.mainloop()


        def EmbaucherEmploye():
            codeemp=random.randint(000000000000000,100000000000000)
            nom=txtnom.get()
            prenom=txtpre.get()
            sexe=txtsex.get()
            datenaissance=txtdatn.get()
            lieunaissance=txtlieu.get()
            adresse=txtad.get()
            etat=txtetat.get()
            typeemploi=txttype.get()
            telephone=txttelep.get()
            salaire=txtsal.get()
            try:
                if nom=="":
                    messagebox.showerror("Information","le champ nom est vide.")
                elif prenom=="":
                    messagebox.showerror("Information","le champ prenom est vide.")
                elif sexe=="":
                     messagebox.showerror("Information", "le champ sexe est vide.")
                elif datenaissance == "":
                    messagebox.showerror("Information", "le champ date de naissance est vide.")
                elif lieunaissance=="":
                    messagebox.showerror("Information",'Le champ lieu de naissance est vide.')
                elif adresse=="":
                    messagebox.showerror("Information","Le champ adresse est vide.")
                elif etat=="":
                    messagebox.showeror("Information","Le champ etat matrimonial est vide.")
                elif type == "":
                    messagebox.showeror("Information", "Le champ etat matrimonial est vide.")
                elif telephone == "":
                    messagebox.showeror("Information", "Le champ etat matrimonial est vide.")
                elif salaire == "":
                    messagebox.showeror("Information", "Le champ etat matrimonial est vide.")

                else:
                    #Lire l'image par rapport a son chemin#
                    with open(chemin,'rb') as f:
                        ph=base64.b64encode(f.read()) #mettre en binaire
                        photo=ph.decode('utf-8') #mettre sous forme de chaine de caractere
                        emp.EmbaucherEmploye(codeemp,nom,prenom,sexe,datenaissance,lieunaissance,adresse,typeemploi,etat,salaire,telephone,photo)# la methode insertion
                        messagebox.showinfo("Information","Un employé a été embauché avec succès.\n code de l'employé: "+str(codeemp))
                        #nettoyage des champs
                        txtnom.delete(0,'end')
                        txtpre.delete(0,'end')
                        txtsex.delete(0,'end')
                        txtetat.delete(0,'end')
                        txtdatn.delete(0,'end')
                        txtlieu.delete(0,'end')
                        txtad.delete(0,'end')
                        txtetat.delete(0,'end')
                        txttype.delete(0,'end')
                        txttelep.delete(0,'end')
                        txtsal.delete(0,'end')
                        #Image par defaut apres insertion
                        ph = Image.open("Images/8c8b3766126753c6d098cdb2e42cff49.png")  # ajouter une image
                        ph1 = ImageTk.PhotoImage(ph.resize((200, 150)),master=fen)  # redimensionner l'image, #largeur par hauteur, #
                        lbpho.config(image=ph1)  # ajouter l'image dans un label
                        lbpho.ph1 = ph1
                        lbpho.grid(row=5,columnspan=3,padx=5,pady=5)#afficher l'image

            except Pyro4.core.errors.ConnectionClosedError:
                messagebox.showerror("Information","Le serveur est eteint.")

        def RechercherEmploye():
            codeemp=txtcode.get()
            try:
                if codeemp=="":
                    messagebox.showwarning("Information","Le champ de code de l'employé est vide.")
                else:
                    Emp=emp.RechercherEmploye(codeemp) #methode rechercher employe
                    txtnom.delete(0,'end')
                    txtnom.insert(tkinter.END,Emp[0][1])
                    txtprenom.delete(0,'end')
                    txtprenom.insert(tkinter.END,Emp[0][2])
                    txtsex.delete(0,'end')
                    txtsex.insert(tkinter.END,Emp[0][3])
                    txtdatn.delete(0,'end')
                    txtdatn.insert(tkinter.END,Emp[0][4])
                    txtlieu.delete(0,'end')
                    txtlieu.insert(tkinter.END,Emp[0][5])
                    txtad.delete(0,'end')
                    txtad.insert(tkinter.END,Emp[0][6])
                    txttype.delete(0,'end')
                    txttype.insert(tkinter.END,Emp[0][7])
                    txtetat.delete(0,'end')
                    txtetat.insert(tkinter.END,Emp[0][8])
                    txtsal.delete(0,'end')
                    txtsal.insert(tkinter.END,Emp[0][9])
                    txttelep.delete(0,'end')
                    txttelep.insert(tkinter.END,Emp[0][10])
                    #Recuperer l'image qui a ete stocke en sous forme de chaine de caractere
                    # Nous allons ecrire l'image
                    ph=str(Emp[0][11]).encode('utf-8')# mettre en binaire # la position de la photo dans la base de donnees
                    with open("{}.png".format(Emp[0][1]),'wb') as f:
                        # os.chdir('./')
                        pho=base64.decodebytes(ph) #mettre en octet
                        f.write(pho) #ecriture
                        f.flush() #mode ecriture et lecture
                        ImageFile.LOAD_TRUNCATED_IMAGES=True
                        nom_fichierim=Emp[0][1]+".png"
                        im=Image.open(nom_fichierim)
                        img=ImageTk.PhotoImage(im.resize((200,150)),master=fen)
                        lbpho.config(image=img)# ajouter l'image dans le label
                        lbpho.img=img
                        lbpho.grid(row=6,column=3)
                        #Suppression de photo
                        # os.remove(nom_fichierim)

            except Pyro4.core.errors.ConnectionClosedError:
                messagebox.showerror("Information", "Le serveur est eteint.")

        def ModifierEmploye():
            try:
                codeemp=txtcode.get()
                nom = txtnom.get()
                prenom = txtprenom.get()
                sexe = txtsex.get()
                datenaissance = txtdatn.get()
                lieunaissance = txtlieu.get()
                adresse = txtad.get()
                etat = txtetat.get()
                typeemploi = txttype.get()
                telephone = txttelep.get()
                salaire = txtsal.get()
                if codeemp=='':
                    messagebox.showwarning("Information","le champ de code de l'employé est vide.")
                elif nom=='':
                    messagebox.showwarning("Information","le champ nom de l'employé est vide.")
                else:
                    #Recuperons la photo
                    f=open(chemin,'rb') #ouverture du fichier
                    ph=base64.b64encode(f.read()) #lire le fichier
                    photo=ph.decode('utf-8') #afficher sous forme de caractere
                    if  chemin!=0:
                        emp.ModifierEmploye(codeemp,nom,prenom,sexe,datenaissance,lieunaissance,adresse,typeemploi,etat,salaire,telephone,photo)
                        messagebox.showinfo("Information",'Un employé  a été  modifié  avec succès.')
                        txtcode.delete(0,'end')
                        txtnom.delete(0,'end')
                        txtprenom.delete(0,'end')
                        txtsex.delete(0,'end')
                        txtdatn.delete(0,'end')
                        txtlieu.delete(0,'end')
                        txtad.delete(0,'end')
                        txttype.delete(0,'end')
                        txtetat.delete(0,'end')
                        txtsal.delete(0,'end')
                        txttelep.delete(0,'end')
                    else:
                        messagebox.showwarning("Infomation","Il faut ajouter une photo pour l'employé.")
            except Pyro4.core.errors.ConnectionClosedError:
                messagebox.showerror("les serveur est eteint.")
        def FenrevocationEmploye():
            global txtcode
            fen=tkinter.Toplevel(fenp)
            fen.title("Revoquer un employé")
            larg=210
            haut=100
            largecran=fen.winfo_screenwidth()
            hautecran=fen.winfo_screenheight()
            x=(largecran/2)-(larg/2)
            y=(hautecran/2)-(haut/2)
            fen.geometry("%dx%d+%d+%d"%(larg,haut,x,y))
            legend=tkinter.LabelFrame(fen)
            lbcode=tkinter.Label(legend,text="Code de l'employé")
            txtcode=tkinter.Entry(legend,width=30)
            but=tkinter.Button(legend,text='Revoquer',command=lambda:RevoquerEmploye())
            legend.grid(row=0,column=0)
            lbcode.grid(row=0,column=0)
            txtcode.grid(row=1,column=0)
            but.grid(row=2,column=0)
            fen.transient(fenp)
            fen.resizable(width=False,height=False)
            fen.mainloop()

        def RevoquerEmploye():
            codeemp=txtcode.get()
            if codeemp=='':
                messagebox.showerror("Information","Vous avez laisser vide le champ de code.")
            else:
                emp.RevoquerEmploye(codeemp)
                if messagebox.askyesno("Revoquer","Etes vous sur de revoquer cet employe?"):
                    messagebox.showinfo("Information","Un employé a été revoqué avec succès.")

        def FenMentionAbs():
            global txtanne, txtnom, txtpre, txtdatd, txtdatf, txtmen, txtper
            fen = tkinter.Toplevel(fenp)
            fen.title("Mentionner une absence")
            # fen.colormapwindows('blue')
            fen.iconbitmap('Images/pl.ico')
            large = 600
            haut = 400
            largeecran = fen.winfo_screenwidth()
            hautecran = fen.winfo_screenheight()
            x = (largeecran / 2) - (large / 2)
            y = (hautecran / 2) - (haut / 2)
            fen.geometry('%dx%d+%d+%d'%(large,haut,x,y))
            annee = tkinter.StringVar()
            nom = tkinter.StringVar()
            prenom = tkinter.StringVar()

            dateencours = datetime.date.today() # la date du jour
            anncours = dateencours.strftime('%Y') #Annee du systeme
            ann=str(anncours)+'-'+str(int(anncours)+1) #yyyy-yyyy 2020-2021

            lbanne = tkinter.Label(fen, text='Annee en cours')
            txtanne = tkinter.Entry(fen, textvariable=annee, width=30)
            txtanne.insert(tkinter.INSERT,ann)
            txtanne.config(state='disabled')
            lbdeb = tkinter.Label(fen, text='Date debut')
            txtdatd = DateEntry(fen, locale='fr_FR')
            txtdatd.config(state='disabled')
            lbfin = tkinter.Label(fen, text='Date fin')
            txtdatf = DateEntry(fen, locale='fr_FR', background='gray', foreground='green') #champ date entry
            hr = tkinter.Label(fen, text='Heure mention')
            lbmen = tkinter.Label(fen, text='Motif') #champ de texte motif
            txtmen = tkinter.Text(fen, width=60, height=10, font=('arial', 8))
            sc = tkinter.Scrollbar(fen, orient='horizontal', command=txtmen.yview)
            txtmen.configure(yscrollcommand=sc.set)# configurer la barre de defilement
            lbnom = tkinter.Label(fen, text='Nom')
            txtnom = tkinter.Entry(fen, textvariable=nom, width=30)
            lbpre = tkinter.Label(fen, text='Prenom')
            txtpre = tkinter.Entry(fen, textvariable=prenom, width=30)
            lbper = tkinter.Label(fen, text='Personne affecte')
            txtper = ttk.Combobox(fen, values=('Docteur', 'Doctoresse', 'Secretaire', 'Infirmiere','Administrateur'), width=27)
            # txtper=tkinter.Entry(fen,width=30)
            # txtper.config(state='readonly')
            dt = datetime.datetime.today()
            hr = str(dt.hour) #Retrouver l'heure
            sec = str(dt.minute)# Retrouver la minute
            mesj = str('Heure:')#Heure: Minute
            hre = mesj + '' + hr + ':' + sec
            lbH = tkinter.Label(fen, text=hre, font=('arial', 8, 'bold'))
            butsave = tkinter.Button(fen, text='Enregistrer', command=lambda:MentionnerUneAbsence())
            # butannul = tkinter.Button(fen, text='Annuler')

            lbanne.grid(row=0, column=0, padx=3, pady=3)
            txtanne.grid(row=0, column=1, padx=3, pady=3)
            lbnom.grid(row=1, column=0, padx=3, pady=3)
            txtnom.grid(row=1, column=1, padx=3, pady=3)
            lbpre.grid(row=2, column=0, padx=3, pady=3)
            txtpre.grid(row=2, column=1, padx=3, pady=3)
            lbper.grid(row=3, column=0, padx=3, pady=3)
            txtper.grid(row=3, column=1, padx=3, pady=3)
            lbdeb.grid(row=4, column=0)
            txtdatd.grid(row=4, column=1)
            lbfin.grid(row=4, column=2)
            txtdatf.grid(row=4, column=3)
            lbmen.grid(row=5, column=0, padx=3, pady=3)
            txtmen.grid(row=5, column=1, padx=3, pady=3, rowspan=12, columnspan=12, sticky=('N', 'W', 'S', 'E'))
            lbH.grid(row=20, column=4)
            butsave.grid(row=22, column=1)
            # butannul.grid(row=22, column=3)
            fen.transient(fenp)  # rendre la fenetre fille depend de la fenetre parent
            fen.resizable(0,0) # Retirer le bouton maximize
            fen.mainloop()

        def MentionnerUneAbsence():

            codeabs = random.randint(100000, 200000) #code aleatoire
            anneeencours = txtanne.get() # l'annee en cours
            nom = txtnom.get() #le nom
            prenom = txtpre.get()#le prenom
            motif = txtmen.get('1.0', 'end')#le motif concernant son absence.
            datedebut = txtdatd.get() #la date debut
            datefin = txtdatf.get() #la date de fin
            personneaffecte = txtper.get() #la personne affecte
            datemention = datetime.date.today() #la date du mention de l'absence.
            try:
                if nom == '':
                    messagebox.showerror('Echec', "le champ nom est vide.")
                elif prenom == '':
                    messagebox.showerror('Echec', "le champ prenom est vide.")
                elif motif == '':
                    messagebox.showerror('Echec', "le champ motif est vide.")
                elif datedebut == '':
                    messagebox.showerror('Echec', "le champ date de debut est vide.")
                elif datefin == '':
                    messagebox.showerror('Echec', "le champ date de fin est vide.")
                elif personneaffecte == '':
                    messagebox.showerror('Echec', "le champ personne-affecte est vide.")
                else:
                    abs.MentionnerAbsence(codeabs,nom,prenom,motif,anneeencours,personneaffecte,datedebut,datefin,datemention)#methode insertion
                    messagebox.showinfo("Information", "Une absence a été mentionnée avec succès.")#message de reussite
                    #nettoyer les champs
                    txtnom.delete(0, 'end')
                    txtpre.delete(0, 'end')
                    txtmen.delete('1.0', 'end')
                    txtdatd.delete(0, 'end')
                    txtdatf.delete(0, 'end')
                    txtper.delete(0,'end')
                    txtanne.delete(0,'end')
            except Pyro4.core.errors.ConnectionClosedError:
                messagebox.showerror("les serveur est eteint.")

        def AideLog():
            fena=tkinter.Toplevel(fenp)
            fena.title('Concernant le logiciel Hopital La Reforme')
            large=860
            haut=276
            largecran=fena.winfo_screenwidth()
            hautecran=fena.winfo_screenheight()
            x=(largecran/2)-(large/2)
            y=(hautecran/2)-(haut/2)
            fena.geometry('%dx%d+%d+%d' % (large,haut,x,y))
            lbt=tkinter.Label(fena,text='Hopital la reforme',font=('arial',10,'bold'))
            version=tkinter.Label(fena,text='v1.0   32 bit, 64 bit',font=('arial',10,'bold'))
            auteur=tkinter.Label(fena,text='Programmeur: Beneche Nelson')
            contactfacebook=tkinter.Label(fena,text='www.facebook.com/NelsonBeneche',font=('arial','9','underline'),cursor='hand2') #lancer automatiquement le navigateur du client
            email=tkinter.Label(fena,text='Email: benechenelson@gmail.com')
            lbdoc=tkinter.Label(fena,text='Lire la Documentation',font=('arial','9','underline'),cursor='hand2')
            def lancer(event):
                webbrowser.open('www.facebook.com/NelsonBeneche')
            contactfacebook.bind('<Button-1>', lancer)          #lambda e: lancer() #permet aussi de lancer le navigateur du client
            
            def LireDocument(event):
                os.startfile('GuideUtilisateur.pdf')
            lbdoc.bind('<Button-1>', LireDocument)    
                
            telephoneauteur=tkinter.Label(fena,text='Telephone: (+509)4926-0866')
            droit=tkinter.Label(fena,text='Tous droits reservés- 2020')
            descript=tkinter.Label(fena,text="Ce programme a été concu dans l'objectif pour permettre à les différentes hopitaux de mieux gérer les données \n de ses patients, des ses employés, de mentionner une absence, de gerer les informations sur les employés, de \n faire des achats des medicaments, et de faire la vente des medicaments.",width=90,justify='left',anchor='w',font=('arial',9,'bold'))
            im=Image.open('Images/784072.png')
            ima=ImageTk.PhotoImage(im.resize((50,50)),master=fena)
            img=tkinter.Label(fena,image=ima)
            img.grid(row=0,column=0)
            lbt.grid(row=1,column=0,padx=5,pady=5)
            descript.grid(row=3,column=2)
            version.grid(row=2,column=0)
            droit.grid(row=3,column=0)
            auteur.grid(row=4,column=0)
            contactfacebook.grid(row=5,column=0)
            telephoneauteur.grid(row=6,column=0)
            email.grid(row=7,column=0)
            lbdoc.grid(row=8,column=0)
            #fena.config(bg='white') #couleur de l'arriere plan de la fenetre
            fena.resizable(width=False,height=False)
            fena.transient(fenp)            
            fena.mainloop()
        #Ajout de sous menu
        #sub=tkinter.Menu(menu1)
        #sub.add_command(label='Se connecter')
        #sub.add_command(label='Se connecter')
        #menu1.add_cascade(label='Se connecter',menu=sub)
        img=Image.open('Images/Admin-icon.png')
        im1=ImageTk.PhotoImage(img.resize((17,17)),master=app)
        imgg=Image.open('Images/fermerapp.png')
        im2=ImageTk.PhotoImage(imgg.resize((17,17)),master=app)        
        menu1.add_command(label='Se connecter',image=im1,compound='left',command=lambda:fenconnection())
        menu1.add_command(label='Quitter',image=im2,compound='left',command=app.destroy)
        main.add_cascade(label='Connexion',menu=menu1)
        ima=Image.open('Images/apt.png')
        im=ImageTk.PhotoImage(ima.resize((1050,700)),master=app)
        lb=tkinter.Label(app,image=im)
        lb.pack()
        
        
        app.config(menu=main)
        app.state('zoomed')
        app.mainloop()#affichage de la fenetre
        
if __name__=='__main__':
    FenPrincipalePharmatech()
