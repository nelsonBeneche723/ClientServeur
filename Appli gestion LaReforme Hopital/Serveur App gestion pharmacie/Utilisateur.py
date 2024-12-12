# *-* coding:utf-8 *-*
import sqlite3
import pymysql
import Pyro4
#Creation de la classe

#@Pyro4.expose
class Utilisateur(object):
    
   #Les methodes distantes    
    @Pyro4.expose    
    def AjouterUtilisateur(self,codeut,nom,prenom,sexe,nomutilisateur,motpasse,fonction,photo,datecreation):
        connection=pymysql.connect(host='localhost',db='pharmatech',user='root', password='')
        cur=connection.cursor()
        req=cur.execute('insert into Utilisateur values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(codeut,nom,prenom,sexe,nomutilisateur,motpasse,fonction,photo,datecreation))
        connection.commit()
        if req!=0:
            print('Un utilisateur a ete cree avec succes..')
        else:  
            print('echec...')
        connection.close()
   
     
    @Pyro4.expose    
    def ConnexionUtilisateur(self,nomutilisateur,motpasse):
        
        connection=pymysql.connect(host='localhost',db='pharmatech',user='root', password='')
        cur=connection.cursor()
        req=cur.execute('select * from utilisateur where nomutilisateur=%s and motpasse=%s',(nomutilisateur,motpasse))
        connection.commit()
        res= cur.fetchall()
        print("Connexion réussie pour l'utilisateur:",nomutilisateur)
        return res
        
  
    @Pyro4.expose    
    def ListerUtilisateur(self):
        
        connection=pymysql.connect(host='localhost',user='root',db='pharmatech',password='')
        cur=connection.cursor()
        cur.callproc('AffUtilisateur')
        result=cur.fetchall()
        return result
       
    @Pyro4.expose 
    def RechercherUt(self,codeut):
        
        
        connection=pymysql.connect(host='localhost',db='pharmatech',user='root',password='')   
        cur=connection.cursor()
        req=cur.execute("select * from utilisateur where codeut=%s",codeut)
        connection.commit()
        print('Vous avez effectuee une recherche sur un utilisateur')
        res=cur.fetchall()
        return res 
    
    
    @Pyro4.expose
    def getFonction(fonction):
        return fonction
    
    @Pyro4.expose  
    def NombreUtilisateur(self):
        connection=pymysql.connect(host='localhost',db='pharmatech',user='root',password='')   
        cur=connection.cursor()
        req=cur.execute("select * from utilisateur")
        connection.commit()
        res=cur.rowcount #calcul  de nombre d'enregistrement qui est stocke dans la base de donnees
        return res