# *-* coding:utf-8 *-*
import sqlite3
import pymysql
import Pyro4
#Creation de la classe

#@Pyro4.expose
class Consultation(object):
    global connection
    connection=pymysql.connect(host='localhost',db='pharmatech',user='root', password='')
   #Les methodes distantes    
    @Pyro4.expose    
    def EffectuerConsultation(self,numerocarte,age,poids,motif,temperature,tensionarteriel,prescription,resultatexamen,Heure,dateconsultation,datemodification):
       
        cur=connection.cursor()
        req=cur.execute('insert into Consultation values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(numerocarte,age,poids,motif,temperature,tensionarteriel,prescription,resultatexamen,Heure,dateconsultation,datemodification))
        connection.commit()
        if req!=0:
            
            print('Un patient a ete consulte avec succes..')
        else:  
            
            print('echec...')
            
        connection.close()
   
   
    @Pyro4.expose
    def RechercherDossierPatientConsulter(self,numerocarte):
        cur=connection.cursor()
        req=cur.execute('select patient.nom,patient.prenom,consultation.age,consultation.poids,consultation.motif,consultation.temperature,consultation.tensionarteriel,consultation.prescription,consultation.resultatexamen, consultation.dateconsultation from Consultation,Patient where patient.numerocarte=consultation.numerocarte and consultation.numerocarte=%s order by consultation.dateconsultation desc limit 1',(numerocarte))
        connection.commit()       
        res=cur.fetchall() #Retourner toutes les donnees de la table 
        return res
    
    @Pyro4.expose
    def ModifierConsultation(self,age,poids,motif,temperature,tensionarteriel,prescription,resultatexamen,datemodification,numerocarte,dateconsultation):
        cur=connection.cursor()
        req=cur.execute("update consultation set age=%s,poids=%s,motif=%s,temperature=%s,tensionarteriel=%s,prescription=%s,resultatexamen=%s,datemodification=%s where numerocarte=%s and dateconsultation=%s",(age,poids,motif,temperature,tensionarteriel,prescription,resultatexamen,datemodification,numerocarte,dateconsultation))
        connection.commit()
        if req!=0:
            print("Les informations de consultation sur ce patient a ete modifie avec succes.")
        else:
            print('Echec de modification..')
        connection.close()
        
    @Pyro4.expose
    def RechMoConsul(self,numerocarte,dateconsultation):
        cur=connection.cursor()
        req=cur.execute("select * from consultation where numerocarte=%s and dateconsultation=%s",(numerocarte,dateconsultation))
        connection.commit() 
        rechmo=cur.fetchall()
        return rechmo
    
    
    @Pyro4.expose
    def ListerToutJournee(self,dateconsultation):
        cur=connection.cursor()
        req=cur.execute("select * from consultation where dateconsultation=%s",(dateconsultation))
        connection.commit()       
        listertoutjournee=cur.fetchall() #Retourner toutes les donnees de la table consultation
        return listertoutjournee
      
    