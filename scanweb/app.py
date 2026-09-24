import subprocess
import ipaddress
import nmap 
import psycopg2
import json
import threading
import time

from flask import Flask , jsonify,render_template,request
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
    subprocess.run(["airmon-ng","check","kill"],capture_output=True,text=True)
    subprocess.run(["airmon-ng","check","kill"],capture_output=True,text=True)
    return (resultat.stdout)

def desactiver_mode_monitor():
    interface_pis = f"{interface}mon"
    resultat = subprocess.run(["airmon-ng", "stop", interface_pis], capture_output=True, text=True)
    subprocess.run(["systemctl","restart","NetworkManager"])
    return (resultat.stdout)

number = 1

def parcourir_air():
    global number
    interface_pis = f"{interface}mon"
    fichier="/tmp/scan_wifi"
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
                parcour.append({"BSSID": t[0],"Channel" : t[3].strip(),"Chiffrement" :t[5],"Essid":t[13]})
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

times = 1
def capturer_handshake(bssid, canal, interface_monitor):
    global times
    fichier = "tmp/handshake"
    processus_capture = subprocess.Popen(["airodump-ng", "--bssid", bssid, "--channel", str(canal), "--write", fichier, interface_monitor],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2) 
    death =  subprocess.run(["aireplay-ng","--deauth","8","-a",bssid,interface_monitor])
    if death.returncode == 0:
        time.sleep(20)
        processus_capture.terminate()
        processus_capture.wait()
        fiche = fichier + f"-0{times}.cap"
        times +=1
        return fiche
    else:
        return 

etat_test_wifi = {"en_cours": False, "resultat": None}
def test_password(bssid,canal):
    global interface
    interface = detecter_interface()
    activer_mode_monitor()
    interface_pis = f"{interface}mon"
    handshake = capturer_handshake(bssid,canal,interface_pis)
    if handshake is None:
        etat_test_wifi["resultat"] = {"erreur": "Échec de la capture"}
        etat_test_wifi["en_cours"] = False
        return ()
    else:
        word = test_force(handshake)
    desactiver_mode_monitor()
    time.sleep(5)
    etat_test_wifi["en_cours"] = False
    etat_test_wifi["resultat"] = word

@app.route("/api/wifi/test-force")
def lancer_status_password():
    bssid =request.args.get('bssid')
    canal = request.args.get('canal')
    if etat_test_wifi["en_cours"]:
        return jsonify({"erreur": "Un scan est déjà en cours"}), 409
    etat_test_wifi["en_cours"] = True
    etat_test_wifi["resultat"] = None
    thread = threading.Thread(target=test_password,args=(bssid,canal))
    thread.start()
    return jsonify({"status": "lancé"})

@app.route("/api/wifi/statut_test")
def status_password():
    return jsonify(etat_test_wifi)

def test_force(handshake):
    global interface
    interface = detecter_interface()
    test_force_brut = subprocess.run(["aircrack-ng",handshake,"-w","/home/tchenga/projet/scanweb/ignis-1M.txt"],capture_output=True,text=True)
    password=test_force_brut.stdout
    if  "No valid WPA handshakes found" in  password:
           return {"Erreur":"Erreur!!! le handshake n'as pas eu lieu : Verifier si un appareil est connecter a votre point d'acces ou augmenter le nombre de paquets deauth a envoyer"},500
    else:
                password_ligne=password.splitlines()
                password_find=[]
                for j in password_ligne:
                    if "KEY FOUND!" in j :
                        password_find.append(j)
                if password_find != []:
                    password_1=password_find[0].split("[")
                    for i in password_1:
                        if "]" in i :
                            global pasword
                            pasword=i.split("]")
                    resultat=pasword[0].strip()
                    print(f"le resutat est iciiiiiiiiiiiiiiiiiiiiiiii 1:{password_1}")
                    print(f"le resutat est iciiiiiiiiiiiiiiiiiiiiiiii 2:{pasword}")
                    print(f"le resutat est iciiiiiiiiiiiiiiiiiiiiiiii :{resultat}")
                    return {"Mot de passe":resultat}
                else:
                    return {"message" :"Test reussi , mot de passe introuvable"}
                

if __name__ == "__main__":
    app.run(debug=True, port=5000,threaded=True,use_reloader=False)
