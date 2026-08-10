const fileinput=document.getElementById("fileinput");
const upload_btn=document.getElementById("upload_btn");
const Quiz_container=document.getElementById("Quiz_container");
const trol=document.getElementById("trol");
const accroche_up=document.getElementById("accroche_up");
const zone=document.getElementById("zone")


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
    const formData = new FormData();
    formData.append("file",file);
    const response= await fetch("/upload",{
        method:"POST",
        body: formData
    });
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
            }
        else {
            tab.push({question:j,reponse:"incorrect☢️"});
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
            trol.innerHTML = resume + `<p><strong>Score : ${score}/${data.questions.length} (${pourcentage}%)</strong></p>`;
  
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

