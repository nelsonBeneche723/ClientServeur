import Pyro4
import pymysql

class Employe(object):
    global connection
    connection=pymysql.connect(host='localhost', user='root', password='', db='pharmatech')
    #Exposition des methodes
    @Pyro4.expose
    def EmbaucherEmploye(self,codeemp,nom,prenom,sexe,datenaissance,lieunaissance,adresse,typeemploi,etat,salaire,telephone,photo):
        cur=connection.cursor()
        req=cur.execute("insert into employe values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(codeemp,nom,prenom,sexe,datenaissance,lieunaissance,adresse,typeemploi,etat,salaire,telephone,photo))
        connection.commit()
        if req!=0:
            print("Un employé a été embauché avec succès...")
        else:
            print("Echec de l'embauchement.")

    #Rechercher Employe
    @Pyro4.expose
    def RechercherEmploye(self,codeemp):
         cur=connection.cursor()
         req=cur.execute('select * from employe where codeemp=%s',(codeemp))
         connection.commit()
         result=cur.fetchall()
         return result

    #Lister Employe
    @Pyro4.expose
    def ListerEmploye(self):
        cur = connection.cursor()
        req = cur.execute("select * from employe")
        connection.commit()
        result = cur.fetchall()
        return result
    #Modifier employe
    @Pyro4.expose
    def ModifierEmploye(self,codeemp,nom,prenom,sexe,datenaissance,lieunaissance,adresse,typeemploi,etat,salaire,telephone,photo):
        cur=connection.cursor()
        req=cur.execute("update employe set nom=%s,prenom=%s,sexe=%s,datenaissance=%s,lieunaissance=%s,adresse=%s,typeemploi=%s,etat=%s,salaire=%s,telephone=%s,photo=%s where codeemp=%s",(nom,prenom,sexe,datenaissance,lieunaissance,adresse,typeemploi,etat,salaire,telephone,photo,codeemp))
        connection.commit()
        if req!=0:
            print("Un employé a été modifié avec succès...")
        else:
            print("Echec de modification. ")

    #Supprimer employe
    @Pyro4.expose
    def RevoquerEmploye(self,codeemp):
        cur=connection.cursor()
        req=cur.execute("delete from employe where codeemp=%s",(codeemp))
        connection.commit()
        if req!=0:
            print("un employe a ete revoque avec succes.")
        else:
            print("Echec de revocation..")