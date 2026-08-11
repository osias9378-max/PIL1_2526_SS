const fileinput=document.getElementById("fileinput");
const upload_btn=document.getElementById("upload_btn");
const Quiz_container=document.getElementById("Quiz_container");
const trol=document.getElementById("trol");
const accroche_up=document.getElementById("accroche_up");
const zone=document.getElementById("zone");
const sous=document.getElementById("sous");


zone.addEventListener("click", () => {
    fileinput.click();
});
fileinput.addEventListener("change", () => {
    if (fileinput.files.length > 0) {
        zone.textContent = "📄 " + fileinput.files[0].name;
    }
});

upload_btn.addEventListener("click",async () => {
    const file = fileinput.files[0];
    if (!file){
        window.alert("Veuillez choisir un fichier");
        return;
    }
    if (file.size > 1024 * 1024) {
    alert("Le fichier est trop volumineux (max 1 Mo)");
    return;
    }
    gsap.to(upload_btn,{
    scale:1.08,
    duration:0.6,
    repeat:-1,
    yoyo:true
});

    upload_btn.textContent="⚡ Génération du quiz...";
    upload_btn.disabled=true;
    const formData = new FormData();
    formData.append("file",file);
    const response= await fetch("/upload",{
        method:"POST",
        body: formData
    });
    gsap.killTweensOf(upload_btn);

    gsap.to(upload_btn,{
        scale:1,
        duration:0.2
    });

    upload_btn.textContent="Générer le Quiz ⚡";
    upload_btn.disabled=false;
    const data = await response.json() ;
    let qcm = "";
    data.questions.forEach((q,index) => {
        qcm+= `
        <div class="questions">
             <h3> ${index+1}-${q.question}</h3>
             <button>${q.choix[0]}</button>
             <button>${q.choix[1]}</button>
             <button>${q.choix[2]}</button>
             <button>${q.choix[3]}</button>
        </div>`;
    })
    Quiz_container.innerHTML = qcm;
    const boutons = Array.from(document.querySelectorAll("#Quiz_container button"));
    const quest = document.querySelectorAll("#Quiz_container ")
    let tab=[];
    let i=0;
    boutons.forEach((bouton) => {
        bouton.addEventListener("click", () => {
        let j=Number(bouton.textContent[0])-1;
        if (bouton.textContent[1]===data.questions[j].reponse_correcte){
            tab.push({question:j,reponse:"correct✅"});
            bouton.classList.add("bonne-reponse");
            }
        else {
            tab.push({question:j,reponse:"incorrect☢️"});
            bouton.classList.add("mauvaise-reponse");
        }
        let boutonquestion= boutons.filter((b) => {
            return Number(b.textContent[0]) -1 ===j;
        });
        boutonquestion.forEach((b) => {
            b.disabled= true ;
        });
        if (tab.length===data.questions.length){
            let bon_reponse=tab.filter((rep) =>rep.reponse ==="correct✅");
            let score =bon_reponse.length;
            let pourcentage = Math.round((score / data.questions.length) * 100);
            let resume = tab.map((t) => `<p>Question ${t.question + 1} : ${t.reponse}</p>`).join("");
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
            fileinput.value="";
    }
    });
    })
    })
    gsap.fromTo(accroche_up,
    { opacity: 0, y: 8 },
    { opacity: 1, y: 0, duration: 0.6, delay: 0.5, ease: "power2.out" });
    gsap.fromTo(upload_btn,
    { opacity: 0, y: 8 },
    { opacity: 1, y: 0, duration: 0.6, delay: 0.7, ease: "power2.out" });
    gsap.fromTo(zone,
    { opacity: 0, y: 8 },
    { opacity: 1, y: 0, duration: 0.6, delay: 0.7, ease: "power2.out" });
    gsap.fromTo(sous,
    { opacity: 0, y: 8 },
    { opacity: 1, y: 0, duration: 0.6, delay: 0.9, ease: "power2.out" });

