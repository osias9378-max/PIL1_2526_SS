const bout = document.getElementById("btn-scan");
const loader = document.getElementById("loader");
const history = document.getElementById("btn-history");
const air = document.getElementById("btn-air")


bout.addEventListener("click", async () =>{
    loader.classList.remove("cache");   
    const reponse= await fetch("http://127.0.0.1:5000/api/scanner_reseau");
    if (!reponse.ok){
        const erreur = await reponse.json();
        window.alert(Object.entries(erreur)[0]);
        loader.classList.remove("cache");   
        return;
    }
    const donne = await  reponse.json();
    loader.classList.add("cache");      
    console.log(donne);
    let table="" ;
    let k=1;
    table += "<table >" +
                  "<tr>" +
                     "<th>" + "Device number" + "</th>"+
                     "<th>" + "Hostname" + "</th>"+
                     "<th>" + "Ipv4" + "</th>"+
                     "<th>" + "Mac address" + "</th>"+
                     "<th>" + "State" + "</th>"+
                  "<tr>"
    for (let i of donne){
        table += "<tr>" +
                    "<td>" + k + "</td>"
        for( const [key,value] of Object.entries(i)){
            table += "<td>" + value + "</td>" 
        }
        table +=   "<tr>"
        k++;

    }
    table += "</table>"
    document.getElementById("tableau").innerHTML=table

});

history.addEventListener("click",async () => {
    const hist_brute = await fetch("http://127.0.0.1:5000/api/history");
    const hist = await hist_brute.json();
    if (hist_brute.ok){
        let table_hist ="";
        table_hist += "<table>" +
                           "<tr>" +
                                "<th>" + "Capture number" + "</th>"+
                                "<th>" + "Date" + "</th>"+
                                "<th>" + "Device number" + "</th>"+
                                "<th>" + "Hostname" + "</th>"+
                                "<th>" + "Ipv4" + "</th>"+
                                "<th>" + "Mac address" + "</th>"+
                                "<th>" + "State" + "</th>"+
                           "</tr>"
        for (let item of hist){
                console.log(item[2]);
                let j=1;
                for (items of item[2]){
                    table_hist += "<tr>" +
                                           "<td>" + item[0] + "</td>"+ 
                                           "<td>" + item[1] + "</td>"+
                                           "<td>" + j + "</td>"
                    j++;
                    for (const [key,value] of Object.entries(items)){
                        table_hist += "<td>" + value + "</td>" 
                    }

                    table_hist += "</tr>"

                }
        }
        table_hist += "</table>"
        console.log(hist);
        document.getElementById("table_hist").innerHTML = table_hist;
    }
    else{
        alert("Erreur!!!!");
    }
});


air.addEventListener("click", async () => {
    loader.classList.remove("cache")
    const lancement = await fetch("http://127.0.0.1:5000/api/wifi/lancer");
    if (!lancement.ok) {
        const erreur = await lancement.json();
        alert(erreur.erreur);
        return;
    }
    const intervalId = setInterval(async () => {
        const statut_reponse = await fetch("http://127.0.0.1:5000/api/wifi/statut");
        const statut = await statut_reponse.json();

        if (!statut.en_cours) {
            clearInterval(intervalId); 
            loader.classList.add("cache")
            afficherResultatsWifi(statut.resultat); 
        }
    }, 2000);
});

function afficherResultatsWifi(air){
        let wifi = "<table>" +
                   "<tr>" +
                   "<th>"+"Device number"+"</th>" +
                   "<th>"+"BSSID"+ "</th>" +
                   "<th>"+"Channel"+"</th>" +
                   "<th>"+"Chiffrement"+"</th>" +
                   "<th>"+"Name"+"</th>" +
                   "</tr>";
        let comp=1;
        for (let wi of air) {
            wifi += "<tr>";
            wifi += "<td>" +"<button class='btn-test' data-bssid='" + wi.BSSID + "' data-channel='"+ wi.Channel +"'>" + comp + "</button>"+"</td>";
            for (const [key, value] of Object.entries(wi)) {
                wifi += "<td>" + value + "</td>";
            }
                comp+=1;

            wifi += "</tr>";
        }
    wifi += "</table>"
    document.getElementById("table_wifi").innerHTML = wifi
    console.log()
};
document.getElementById("table_wifi").addEventListener("click", (event) => {
    if (event.target.classList.contains("btn-test")) {
        const bssid = event.target.dataset.bssid;
        const canal = event.target.dataset.channel;
        window.alert("Cher utilisateur veuillez confirmer que ce reseau wifi vous appartient bien.Toute operatoins sur un reseau qui ne vous appartient pourrais vous exposer a certaines consequences judiciaires")
    }
});