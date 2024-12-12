# *-* coding:utf-8 *-*
import pymysql
import Pyro4
import pickle

# Creation de la classe
# Connecteur de python a mysql
class Patient(object):
    global connection
    connection=pymysql.connect(host='localhost',user='root',db='pharmatech',password='')
    
   #Les methodes distantes    
    @Pyro4.expose
    def CreerPatient(self,numerocarte,nom,prenom,sexe,datenaissance,adresse,telephone,etat_matrimoniale,groupesanguin,personneresponsable,numeropersonneresponsable,typeassurance,entreprise_assuree,profession,photo,dateenregistrer,datemodification):
        cur=connection.cursor()
        req=cur.execute("insert into Patient values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(numerocarte,nom,prenom,sexe,datenaissance,adresse,telephone,etat_matrimoniale,groupesanguin,personneresponsable,numeropersonneresponsable,typeassurance,entreprise_assuree,profession,photo,dateenregistrer,datemodification))
        connection.commit()
        if req!=0:
            print('insertion réussie')
        else:
            print("Echec d'insertion de données")
        connection.close()  
        return True
    
    @Pyro4.expose    
    def RechercherPatient(self,numerocarte):
        cur=connection.cursor()
        req=cur.execute("select * from patient where numerocarte=%s",(numerocarte))
        connection.commit()
        print('Vous effetuez une recherche sur un patient')
        res=cur.fetchall()
        return res 
    
    @Pyro4.expose
    def RechercherIdPatient(self,numerocarte):
        cur=connection.cursor()
        req=cur.execute("select numerocarte from patient where numerocarte=%s",(numerocarte))
        connection.commit()
        res=cur.fetchall()
        return res
        

    @Pyro4.expose
    def ModifierPatient(self,numerocarte,nom,prenom,sexe,datenaissance,adresse,telephone,etat_matrimoniale,groupesanguin,personneresponsable,numeropersonneresponsable,typeassurance,entreprise_assuree,profession,photo,datemodification):
        cur=connection.cursor()
        req=cur.execute("update patient set nom=%s,prenom=%s,datenaissance=%s,sexe=%s,adresse=%s,telephone=%s,etat_matrimoniale=%s,groupesanguin=%s,personneresponsable=%s,numeropersonneresponsable=%s,typeassurance=%s,entreprise_assuree=%s,profession=%s,photo=%s,datemodification=%s where numerocarte=%s",(nom,prenom,datenaissance,sexe,adresse,telephone,etat_matrimoniale,groupesanguin,personneresponsable,numeropersonneresponsable,typeassurance,entreprise_assuree,profession,photo,datemodification,numerocarte))
        connection.commit()
        print('vous avez modifier le patient',numerocarte)
        modif=cur.fetchall()
        return modif
    
    
    @Pyro4.expose
    def ListerPatientAge(self,age,datesys):
        cur=connection.cursor()
        req=cur.execute("select numerocarte,nom,prenom,sexe,datenaissance,adresse,telephone from patient where year(datenaissance)+"+age+"="+datesys+"")
        connection.commit()
        print('vous avez afficher la liste des patients,classe selon son age')
        lis=cur.fetchall()
        return lis
    
    @Pyro4.expose
    def ListerPatientNom(self,nom):
        cur=connection.cursor()
        req=cur.execute("select numerocarte,nom,prenom,sexe,datenaissance,adresse,telephone from patient where nom=%s",(nom))
        connection.commit()
        listnom=cur.fetchall()
        return listnom
       
    
    @Pyro4.expose
    def ListerPatientSexe(self,sexe):
        cur=connection.cursor()
        req=cur.execute("select numerocarte,nom,prenom,sexe,datenaissance,adresse,telephone from patient where sexe=%s",(sexe))
        connection.commit()
        listsexe=cur.fetchall()
        return listsexe
       
    
    