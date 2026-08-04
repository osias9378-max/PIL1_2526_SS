const fileinput=document.getElementById("fileinput");
const upload_btn=document.getElementById("upload_btn");
const Quiz_container=document.getElementById("Quiz_container")

upload_btn.addEventListener("click",async () => {
    const file = fileinput.files[0];
    if (!file){
        window.alert("Veuillez choisir un fichier");
        return;
    }
    const formData = new FormData();
    formData.append("file",file);
    const response= await fetch("/upload",{
        method:"POST",
        body: formData

    });
    const data = await response.json() ;
    console.log(data);
    let qcm = "";
    data.questions.forEach((q,index) => {
        qcm+= `<p> ${index+1}-${q.question}</p>
        <p> ${"-"+q.choix[0]}</p>
        <p> ${"-"+q.choix[1]}</p>
        <p> ${"-"+q.choix[2]}</p>
        <p> ${"-"+q.choix[3]}</p>`;
    })
    Quiz_container.innerHTML = qcm; 

    })