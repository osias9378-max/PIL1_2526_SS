import subprocess
import ipaddress
import nmap 
import psycopg2
import json
import threading

from flask import Flask , jsonify,render_template
from flask_cors import CORS

app = Flask(__name__,template_folder="frontend",static_folder="frontend")
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

def detecter_sous_reseau():
    sortie = subprocess.check_output(["ip", "-o", "-4", "addr", "show"]).decode()
    lignes = sortie.strip().splitlines()
    ligne_ip = []
    for ite in lignes:
        ite=ite.split(" ")
        if ite[1] != "lo" and  ite[1]!= "docker0":
            ligne_ip.append(ite)
    add=None
    if ligne_ip !=[]:
        for ite in ligne_ip [0]:
             if "/24" in ite :
                add=ite
        if add != None:
            add=ipaddress.ip_interface(f"{add}").network
            return add
        else:
            return None
    else:
        return None

@app.route("/api/scanner_reseau")
def scanner_reseau():
    sous_reseau=detecter_sous_reseau()
    if sous_reseau==None:
        return jsonify({"Erreur":"!!!! Impossible de detecter le sous-reseau Veuillez vous connecter"}),500
    scanner = nmap.PortScanner()
    scanner.scan(hosts=str(sous_reseau), arguments="-sn")
    scanner.all_hosts()
    scanners=scanner.all_hosts()
    scan=[]
    for ip in scanners:
        scan.append({"Ip":f"{ip}","Hostname": f"{scanner[ip].hostname()}","Sate" : f"{scanner[ip].state()}","Mac address": f"{scanner[ip]['addresses'].get('mac')}"})
    for device in scan :
        for j in device :
            if j=="Hostname" and device[j]=="None":
                device[j]="Hostname not available"
            if j=="Mac address" and device[j]=="None":
                device[j] = "Mac address not available"

    sauvegarder_scan(scan)
    return scan

@app.route("/api/ping")
def ping():
    return jsonify({"status": "ok", "message": "Backend opérationnel"})

def connexion_bdd():
    return psycopg2.connect(
        dbname="scanweb",
        user="tchenga",
        password="1019721tatiannna;",
        host="localhost"
    )

def sauvegarder_scan(resultat):
    conn = connexion_bdd()
    cur = conn.cursor()
    cur.execute("INSERT INTO scan (result_scan) VALUES (%s)", (json.dumps(resultat),))
    conn.commit()
    cur.close()
    conn.close()

@app.route("/api/history")
def history():
    conn= connexion_bdd()
    cur = conn.cursor()
    cur.execute("SELECT *FROM scan;",)
    resultat = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return resultat

def detecter_interface():
    sortie = subprocess.check_output(["ip", "-o", "-4", "addr", "show"]).decode()
    lignes = sortie.strip().splitlines()
    ligne_ip = []
    for ite in lignes:
        ite=ite.split(" ")
        if ite[1] != "lo" and  ite[1]!= "docker0":
            ligne_ip.append(ite)
    add=None
    if ligne_ip !=[]:
        add=ligne_ip[0][1]
        if add != None:
            return add
        else:
            return None
    else:
        return None
    
def activer_mode_monitor():
    resultat = subprocess.run([ "airmon-ng", "start", interface], capture_output=True, text=True)
    return (resultat.stdout)

def desactiver_mode_monitor():
    interface_pis = f"{interface}mon"
    resultat = subprocess.run(["airmon-ng", "stop", interface_pis], capture_output=True, text=True)
    return (resultat.stdout)

number = 1

def parcourir_air():
    global number
    interface_pis = f"{interface}mon"
    fichier="/home/tchenga/projet/scanweb/scan_wifi"
    subprocess.run(["timeout","-k" ,"5","15","airodump-ng",  interface_pis,"--output-format","csv","--write",fichier],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
    )
    parcour=[]
    print("check1")
    with open(fichier + f"-0{number}" + ".csv", "r", encoding="utf-8", errors="ignore") as f:
        lignes = f.readlines()
        for l,t in enumerate(lignes):
            if t != "\n" and l>1:
                t=t.split(",")
                parcour.append({"BSSID": t[0],"Channel" : t[3],"Chiffrement" :t[5],"Essid":t[13]})
            elif t == "\n" and l >1 :
                break
    number += 1
    print(parcour)
    return parcour

def aircrack():
    global interface
    interface = detecter_interface()
    activer_mode_monitor()
    print("check2")
    resultat = parcourir_air()
    print("check3")
    print(resultat)
    desactiver_mode_monitor()
    return resultat


etat_scan_wifi = {"en_cours": False, "resultat": None}
def executer_scan_wifi():
    global interface
    interface = detecter_interface()
    activer_mode_monitor()
    resultat = parcourir_air()
    desactiver_mode_monitor()
    etat_scan_wifi["resultat"] = resultat
    etat_scan_wifi["en_cours"] = False

@app.route("/api/wifi/lancer")
def lancer_scan_wifi():
    if etat_scan_wifi["en_cours"]:
        return jsonify({"erreur": "Un scan est déjà en cours"}), 409
    etat_scan_wifi["en_cours"] = True
    etat_scan_wifi["resultat"] = None
    thread = threading.Thread(target=executer_scan_wifi)
    thread.start()
    return jsonify({"status": "lancé"})

@app.route("/api/wifi/statut")
def statut_scan_wifi():
    return jsonify(etat_scan_wifi)

if __name__ == "__main__":
    app.run(debug=True, port=5000,threaded=True,use_reloader=False)
