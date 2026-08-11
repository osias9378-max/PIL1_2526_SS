const titre=document.getElementById("titre");
const accroche=document.getElementById("accroche");
const bouton1=document.getElementById("bouton-1");
const bouton2=document.getElementById("bouton-2");


gsap.fromTo(titre,
    { opacity: 0, y: 8 },
    { opacity: 1, y: 0, duration: 0.6, delay: 0.5, ease: "power2.out" }
);
gsap.fromTo(accroche,
    { opacity: 0, y: 8 },
    { opacity: 1, y: 0, duration: 0.6, delay: 0.7, ease: "power2.out" }
);
gsap.fromTo(bouton1,
    { opacity: 0, y: 8 },
    { opacity: 1, y: 0, duration: 0.6, delay: 0.9, ease: "power2.out" }
);
gsap.fromTo(bouton2,
    { opacity: 0, y: 8 },
    { opacity: 1, y: 0, duration: 0.6, delay: 0.95, ease: "power2.out" }
);