const sujets=document.getElementById("sujets");
const generer_btn=document.getElementById("generer_btn");
const Quiz_container=document.getElementById("Quiz_container");
const trol=document.getElementById("trol");
const accroche_up=document.getElementById("accroche_up");

generer_btn.addEventListener("click",async () => {
    const sujet=sujets.value;
    if (!sujet|| sujet.trim===""){
        alert("Erreur!!!!!Veuillez taper un sujet");
        return;
    }
    gsap.to(generer_btn,{
        scale:1.08,
        duration:0.6,
        repeat:-1,
        yoyo:true
     });
    generer_btn.textContent="⚡ Génération du quiz...";
    generer_btn.disabled=true;
    const response =await fetch("/generer-sujet",{
    method:"POST",
    headers:{
    "Content-Type":"application/json"
            },
    body:JSON.stringify({sujet:sujet})
        });
    gsap.killTweensOf(generer_btn);

    gsap.to(generer_btn,{
        scale:1,
        duration:0.2
    });
    generer_btn.textContent="Générer votre quiz";
    generer_btn.disabled=false;
    const data = await response.json();
    if(data.error){
        alert(data.error);
        return;
        }
    let qcm = "";
    data.questions.forEach((q, index) => {
    qcm+= `
        <div class="questions">
             <h3> ${index+1}-${q.question}</h3>
             <button>${q.choix[0]}</button>
             <button>${q.choix[1]}</button>
             <button>${q.choix[2]}</button>
             <button>${q.choix[3]}</button>
        </div>`;
       });
    Quiz_container.innerHTML = qcm;

    const boutons = Array.from(document.querySelectorAll("#Quiz_container button"));
    let tab = [];

    boutons.forEach((bouton) => {
         bouton.addEventListener("click", () => {
         let j = Number(bouton.textContent[0]) - 1;
         if (bouton.textContent[1] === data.questions[j].reponse_correcte) {
             tab.push({question: j, reponse: "correct✅"});
             bouton.classList.add("bonne-reponse");
            }
             else {
             tab.push({question: j, reponse: "incorrect☢️"});
             bouton.classList.add("mauvaise-reponse");
            }

         let boutonquestion = boutons.filter((b) => Number(b.textContent[0]) - 1 === j);
         boutonquestion.forEach((b) => b.disabled = true);

        if (tab.length === data.questions.length) {
            let bon_reponse = tab.filter((rep) => rep.reponse === "correct✅");
            let score = bon_reponse.length;
            let pourcentage = Math.round((score / data.questions.length) * 100);
            let mess="";
            if (pourcentage<50){
                mess="Continue de t'entrainer tu as encore du chemin";
            }else{
                if(pourcentage<80){
                    mess="Bravo continue comme ca "
                }else{
                    mess="Felicitation tu as bien appris ton cours!!!!!!"
                }
            }
            trol.innerHTML =`<p><strong>Score : ${score}/${data.questions.length}  Pourcentage :(${pourcentage}%)      ${mess}</strong></p>`;
                }
            });
        });
    })
gsap.fromTo(accroche_up,
    { opacity: 0, y: 8 },
    { opacity: 1, y: 0, duration: 0.6, delay: 0.5, ease: "power2.out" });
gsap.fromTo(sujets,
    { opacity: 0, y: 8 },
    { opacity: 1, y: 0, duration: 0.6, delay: 0.7, ease: "power2.out" });
gsap.fromTo(generer_btn,
    { opacity: 0, y: 8 },
    { opacity: 1, y: 0, duration: 0.6, delay: 0.9, ease: "power2.out" });