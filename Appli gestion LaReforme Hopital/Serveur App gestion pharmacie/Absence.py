import pymysql
import Pyro4
# from modele.Achat import Achat
class Absence(object):
    global connection
    connection=pymysql.connect(host='localhost',user='root',db='pharmatech',password='')

    #Exposition de la methode
    @Pyro4.expose
    def MentionnerAbsence(self,codeabs,nom,prenom,motif,anneeencours,personneaffecte,datedebut,datefin,datemention):
        cur=connection.cursor()
        req=cur.execute("insert into absence values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(codeabs,nom,prenom,motif,anneeencours,personneaffecte,datedebut,datefin,datemention))#la requete
        connection.commit()#execution de la requete
        if req!=0:
            print("une employe a mentionne son absence avec succes.")
        else:
            print("echec.")
            #afficher les absences de la journee
    @Pyro4.expose
    def AfficherAbs(self,datemention):
        cur=connection.cursor()
        req=cur.execute("select * from absence where datemention=%s",(datemention))# on fait la requete
        connection.commit()#execution de la requete
        result=cur.fetchall()#parcourir tous les donnees de la requete
        return result# Retourner tous

