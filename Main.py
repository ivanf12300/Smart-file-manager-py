import speech_recognition as sr
import os 
import shutil
import pyautogui
import pyttsx3
import subprocess

TARGET_DIR = r"Proyecto\TestFolder" # Reemplaza con la ruta, no hay comando para abrir carpetas aún

engine = pyttsx3.init()

def responder(texto):
    print(f"{texto}")
    engine.say(texto)
    engine.runAndWait()

def escuchar_comando():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        texto = recognizer.recognize_google(audio, language="es-ES")  # type: ignore
        print(f"{texto}")
        return texto.lower()
    except sr.UnknownValueError:
        responder("No entendi")
        return ""
    except sr.RequestError:
        responder("Error al conectar con el servicio de voz.")
        return ""

def crear_archivo(nombre_archivo, contenido=""):
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
    ruta_completa = os.path.join(TARGET_DIR, nombre_archivo)
    
    try:
        with open(ruta_completa, "w", encoding="utf-8") as f:
            f.write(contenido)
        responder(f"Archivo {nombre_archivo} creado con éxito.")
    except Exception as e:
        responder(f"No se pudo crear el archivo. Error: {str(e)}")

def abrir_o_ejecutar(nombre_o_comando):
    ruta_archivo = os.path.join(TARGET_DIR, nombre_o_comando)

    if os.path.exists(ruta_archivo):
        try:
            os.startfile(ruta_archivo) 
            responder(f"Abriendo {nombre_o_comando}.")
        except Exception as e:
            responder(f"Error al abrir: {str(e)}")
    else:
        try:
            subprocess.Popen(nombre_o_comando, shell=True)
            responder(f"Ejecutando {nombre_o_comando}.")
        except Exception as e:
            responder(f"No se pudo ejecutar {nombre_o_comando}.")

def ejecutar_comando(comando):
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
    if "crear carpeta" in comando:
        nombre = comando.replace("crear carpeta", "").strip() or "Nueva Carpeta"
        ruta = os.path.join(TARGET_DIR, nombre)
        os.makedirs(ruta, exist_ok=True)
        responder(f"Carpeta {nombre} creada con éxito.")
    elif "crear archivo" in comando:
        nombre_archivo = comando.replace("crear archivo", "").strip()
        if nombre_archivo:
            crear_archivo(nombre_archivo.replace(" punto ","."))
        else:
            responder("Especifica el nombre y la extensión del archivo")
    elif "abrir" in comando or "ejecutar" in comando:
        objetivo = comando.replace("abrir", "").replace("ejecutar", "").strip()
        if objetivo:
            abrir_o_ejecutar(objetivo.replace(" punto ","."))
        else:
            responder("Especifica el archivo que deseas abrir o programa ejecutar.")
    elif "listar archivos" in comando:
        archivos = os.listdir(TARGET_DIR)
        if archivos:
            responder(f"Los archivos encontrados son: {', '.join(archivos)}")
        else:
            responder("La carpeta está vacía.")
    elif "limpiar carpeta" in comando:
        for file in os.listdir(TARGET_DIR):
            file_path = os.path.join(TARGET_DIR, file)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        responder("Se limpió la carpeta")

    elif "bloquear equipo" in comando:
        responder("Bloqueando equipo.")
        pyautogui.hotkey('win', 'l')
    elif "cerrar" in comando.lower():
            responder("Cerrando.")
            pyautogui.hotkey('alt', 'f4')
    elif "buscar" in comando.lower():
            responder("Que buscamos")
            pyautogui.hotkey('win')
            for i in comando.replace("buscar ",""):
                pyautogui.write(i,interval=.02)
    elif "escribir" in comando.lower():
            responder("Escribiendo..")
            if not "enter" in comando: # falta implementar
                comando = comando.replace("escribir ","")
                for i in comando:
                    pyautogui.write(i,interval=.02)
            
if __name__ == "__main__":
    responder("Iniciando.")
    while True:
        comando = escuchar_comando()
        if "salir" in comando or "terminar" in comando:
            responder("Hasta luego.")
            break
        if comando:
            ejecutar_comando(comando)

# Comandos: Crear carpeta, Crear archivo, Abrir, Listar archivos, Limpiar carpeta,
# Bloquear equipo, Cerrar, Buscar, Escribir
