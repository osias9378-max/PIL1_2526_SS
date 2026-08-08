const sujets=document.getElementById("sujets");
const generer_btn=document.getElementById("generer_btn");
const Quiz_container=document.getElementById("Quiz_container");
const trol=document.getElementById("trol");

generer_btn.addEventListener("click",async () => {
    const sujet=sujets.value;
    if (!sujet|| sujet.trim===""){
        alert("Erreur!!!!!Veuillez taper un sujet");
        return;
    }
    const response =await fetch("/generer-sujet",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({sujet:sujet})
    });
    const data = await response.json();
    if(data.error){
        alert(data.error);
        return;
    }
    let qcm = "";
    data.questions.forEach((q, index) => {
        qcm += `<div>${index+1}-${q.question}</div>
            <p><button>${q.choix[0]}</button></p>
            <p><button>${q.choix[1]}</button></p>
            <p><button>${q.choix[2]}</button></p>
            <p><button>${q.choix[3]}</button></p>`;
      });
    Quiz_container.innerHTML = qcm;

    const boutons = Array.from(document.querySelectorAll("#Quiz_container button"));
    let tab = [];

    boutons.forEach((bouton) => {
        bouton.addEventListener("click", () => {
            let j = Number(bouton.textContent[0]) - 1;
            if (bouton.textContent[1] === data.questions[j].reponse_correcte) {
                tab.push({question: j, reponse: "correct✅"});
            } else {
                tab.push({question: j, reponse: "incorrect☢️"});
            }

           let boutonquestion = boutons.filter((b) => Number(b.textContent[0]) - 1 === j);
           boutonquestion.forEach((b) => b.disabled = true);

           if (tab.length === data.questions.length) {
                let bon_reponse = tab.filter((rep) => rep.reponse === "correct✅");
                let score = bon_reponse.length;
                let pourcentage = Math.round((score / data.questions.length) * 100);
                trol.innerHTML = JSON.stringify(tab) + " Score: " + pourcentage + "%";
            }
         });
    });
    })