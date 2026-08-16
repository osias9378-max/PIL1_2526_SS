import cairosvg
import os

dossier = os.path.dirname(os.path.abspath(__file__))

for fichier in os.listdir(dossier):
    if fichier.endswith(".svg"):
        nom_sans_extension = fichier.replace(".svg", "")
        chemin_svg = os.path.join(dossier, fichier)
        chemin_png = os.path.join(dossier, nom_sans_extension + ".png")
        cairosvg.svg2png(url=chemin_svg, write_to=chemin_png, output_width=120, output_height=120)
        print(f"{fichier} → {nom_sans_extension}.png")

print("Conversion terminée !")