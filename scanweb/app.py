import subprocess
import ipaddress
import nmap 
import psycopg2
import json


from flask import Flask , jsonify,render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    resultat = subprocess.run(["sudo", "airmon-ng", "start", interface], capture_output=True, text=True)
    return (resultat.stdout)

def desactiver_mode_monitor():
    interface_pis = f"{interface}mon"
    resultat = subprocess.run(["sudo", "airmon-ng", "stop", interface_pis], capture_output=True, text=True)
    resultat = subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], capture_output=True, text=True)
    return (resultat.stdout)

number = 1

def parcourir_air():
    global number
    interface_pis = f"{interface}mon"
    fichier="/home/tchenga/projet/scanweb/scan_wifi"
    subprocess.run(["sudo", "timeout","-k" ,"5","15","airodump-ng",  interface_pis,"--output-format","csv","--write",fichier],
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

@app.route("/api/wifi")
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


if __name__ == "__main__":
    app.run(debug=True, port=5000)