# PIA_modulo.py
import os
import requests
import pandas as pd
import ast
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

# Rutas
CARPETA_PRINCIPAL = "Elementos"
CARPETA_SPRITES = os.path.join(CARPETA_PRINCIPAL, "Sprites", "Pokemon")
ARCHIVO_EXCEL = os.path.join(CARPETA_PRINCIPAL, "pokedex.xlsx")
os.makedirs(CARPETA_SPRITES, exist_ok=True)

def descargar_datos_y_guardar():
    datos = []
    for numero in range(1, 1011):
        url = f"https://pokeapi.co/api/v2/pokemon/{numero}"
        respuesta = requests.get(url)
        if respuesta.status_code != 200:
            continue

        datos_json = respuesta.json()
        nombre = datos_json["name"].capitalize()
        altura = datos_json["height"]
        peso = datos_json["weight"]
        tipos = ", ".join([t["type"]["name"].capitalize() for t in datos_json["types"]])
        habilidades = ", ".join([h["ability"]["name"].capitalize() for h in datos_json["abilities"]])
        stats = {s["stat"]["name"]: s["base_stat"] for s in datos_json["stats"]}
        primeros_movs = ", ".join([m["move"]["name"].capitalize() for m in datos_json["moves"][:5]])

        sprites = datos_json["sprites"]
        sprite_paths = {}

        for key in ["front_default", "back_default", "front_shiny", "back_shiny",
                    "front_female", "back_female", "front_shiny_female", "back_shiny_female"]:
            if sprites[key]:
                sprite_name = f"{numero}_{key}.png"
                ruta_local = os.path.join(CARPETA_SPRITES, sprite_name)
                if not os.path.exists(ruta_local):
                    img_data = requests.get(sprites[key]).content
                    with open(ruta_local, "wb") as f:
                        f.write(img_data)
                sprite_paths[key] = ruta_local

        species_resp = requests.get(datos_json["species"]["url"])
        if species_resp.status_code != 200:
            continue
        species_data = species_resp.json()
        is_legendary = species_data["is_legendary"]
        is_mythical = species_data["is_mythical"]
        is_baby = species_data["is_baby"]
        capture_rate = species_data["capture_rate"]
        rareza = "Muy Raro" if capture_rate < 30 else "Raro" if capture_rate < 90 else "Común"

        evo_chain_resp = requests.get(species_data["evolution_chain"]["url"])
        cadena = []
        if evo_chain_resp.status_code == 200:
            evo_data = evo_chain_resp.json()["chain"]
            while evo_data:
                cadena.append(evo_data["species"]["name"].capitalize())
                evo_data = evo_data["evolves_to"][0] if evo_data["evolves_to"] else None
        cadena_evo = " → ".join(cadena)

        pokemon = {
            "Numero": numero,
            "Nombre": nombre,
            "Altura": altura,
            "Peso": peso,
            "Tipos": tipos,
            "Habilidades": habilidades,
            "Legendario": is_legendary,
            "Mítico": is_mythical,
            "Bebé": is_baby,
            "Rareza": rareza,
            "CaptureRate": capture_rate,
            "Evoluciones": cadena_evo,
            "Ataques": primeros_movs,
            "HP": stats.get("hp", 0),
            "Attack": stats.get("attack", 0),
            "Defense": stats.get("defense", 0),
            "Sp. Atk": stats.get("special-attack", 0),
            "Sp. Def": stats.get("special-defense", 0),
            "Speed": stats.get("speed", 0),
            "Sprites": sprite_paths
        }
        datos.append(pokemon)
    df = pd.DataFrame(datos)
    df.to_excel(ARCHIVO_EXCEL, index=False)

def cargar_datos():
    if not os.path.exists(ARCHIVO_EXCEL):
        descargar_datos_y_guardar()
    return pd.read_excel(ARCHIVO_EXCEL)

def obtener_info_local(df_pokedex, numero):
    numero = int(numero)
    if numero not in df_pokedex["Numero"].values:
        return "Pokémon no encontrado", []
    p = df_pokedex[df_pokedex["Numero"] == numero].iloc[0]

    sprites_dict = ast.literal_eval(p["Sprites"]) if isinstance(p["Sprites"], str) else p["Sprites"]

    stats = (
        f"HP: {p['HP']}\nAttack: {p['Attack']}\nDefense: {p['Defense']}\n"
        f"Sp. Atk: {p['Sp. Atk']}\nSp. Def: {p['Sp. Def']}\nSpeed: {p['Speed']}"
    )
    info = (
        f"Nombre: {p['Nombre']}\nAltura: {p['Altura']}\nPeso: {p['Peso']}\n"
        f"Tipos: {p['Tipos']}\nHabilidades: {p['Habilidades']}\n"
        f"Legendario: {'Sí' if p['Legendario'] else 'No'}\n"
        f"Mítico: {'Sí' if p['Mítico'] else 'No'}\nBebé: {'Sí' if p['Bebé'] else 'No'}\n"
        f"Rareza: {p['Rareza']} (Capture rate: {p['CaptureRate']})\n"
        f"Evoluciones: {p['Evoluciones']}\n\nEstadísticas:\n{stats}\n\nAtaques: {p['Ataques']}"
    )
    imagenes = []
    for ruta in sprites_dict.values():
        if os.path.exists(ruta):
            img = Image.open(ruta).resize((96, 96))
            imagenes.append(ImageTk.PhotoImage(img))
    return info, imagenes

def mostrar_grafica_tipos(df_pokedex):
    tipos_series = df_pokedex["Tipos"].dropna().str.split(", ")
    conteo_tipos = {}

    for tipos in tipos_series:
        for tipo in tipos:
            conteo_tipos[tipo] = conteo_tipos.get(tipo, 0) + 1

    etiquetas = list(conteo_tipos.keys())
    cantidades = list(conteo_tipos.values())

    plt.figure(figsize=(8, 8))
    plt.pie(cantidades, labels=etiquetas, autopct='%1.1f%%', startangle=140)
    plt.title("Distribución de Tipos de Pokémon")
    plt.axis('equal')
    plt.show()
