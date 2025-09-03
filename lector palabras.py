import PyPDF2
import matplotlib.pyplot as plt

from wordcloud import WordCloud

def extraer_texto_pdf(nombre_archivo):
    texto = ""
    with open(nombre_archivo, "rb") as archivo:
        lector = PyPDF2.PdfReader(archivo)
        for pagina in lector.pages:
            texto += pagina.extract_text()
    return texto

def contar_palabras(texto):
    texto = texto.lower()
    caracteres_no_deseados = ",.;:¡!¿?()[]{}\"\'\n"
    for c in caracteres_no_deseados:
        texto = texto.replace(c, "")
    palabras = texto.split()

   
    articulos = ["el", "la", "los", "las", "un", "una", "unos", "unas"]
    adverbios = ["muy", "ya", "hoy", "mañana", "nunca", "siempre", "casi", "también", "aquí", "allí", "bien", "mal", "menos"]
    adjetivos = ["bueno", "malo", "grande", "pequeño", "bonito", "feo", "nuevo", "viejo", "mejor", "peor", "alto", "bajo", "rápido", "lento"]
    conectores = [
        "y", "e", "ni", "pero", "aunque", "sin", "embargo", "porque", "ya", "que", "puesto", "por", "lo", "tanto",
        "así", "si", "cuando", "mientras", "antes", "después", "entonces", "además", "incluso", "aunque", "porqué","de", "en", "a", "su", "como", "al","le","es","se"
,"eso","esto","esta","les","para","o","con","sea","ese"
    ]

    palabras_filtradas = []
    for palabra in palabras:
        if palabra not in articulos and palabra not in adverbios and palabra not in adjetivos and palabra not in conectores:
            palabras_filtradas.append(palabra)

    
    conteo = {}
    for palabra in palabras_filtradas:
        if palabra in conteo:
            conteo[palabra] += 1
        else:
            conteo[palabra] = 1
    return conteo

def graficar_top_palabras(conteo, top=50):
    
    top_palabras = sorted(conteo.items(), key=lambda x: x[1], reverse=True)[:top]

    palabras = [item[0] for item in top_palabras]
    frecuencias = [item[1] for item in top_palabras]

    plt.figure(figsize=(14, 7))
    plt.bar(palabras, frecuencias, color='skyblue')
    plt.xticks(rotation=75, ha='right')
    plt.title(f"Top {top} palabras más frecuentes (excluyendo artículos, adjetivos, adverbios, conectores)")
    plt.xlabel("Palabras")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


def generar_wordcloud(conteo, top=50):
    
    top_palabras = dict(sorted(conteo.items(), key=lambda x: x[1], reverse=True)[:top])

    
    nube = WordCloud(width=800, height=400, background_color='white', colormap='viridis')
    nube.generate_from_frequencies(top_palabras)

    
    plt.figure(figsize=(10, 5))
    plt.imshow(nube, interpolation='bilinear')
    plt.axis("off")
    plt.title(f"Word Cloud - Top {top} palabras más frecuentes")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    nombre_pdf = input("nombre ")

    texto_extraido = extraer_texto_pdf(nombre_pdf)
    resultado = contar_palabras(texto_extraido)

    print("\nFrecuencia de palabras (sin artículos, adjetivos, adverbios ni conectores):\n")
    for palabra, cantidad in resultado.items():
        print(f"{palabra}: {cantidad}")

    graficar_top_palabras(resultado, top=50)
generar_wordcloud(resultado, top=50)