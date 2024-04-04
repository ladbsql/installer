import os
import platform
import zipfile
import requests
import shutil
import customtkinter as ctk
from tkinter import messagebox, ttk

def install():
    base_path = get_base_path()
    www_path = os.path.join(base_path, "www")
    engine_path = os.path.join(base_path, "engine")
    launcher_path = os.path.join(base_path, "launcher")
    download_and_extract_repository("https://github.com/ladbsql/www/archive/refs/heads/master.zip", www_path)
    download_and_extract_repository("https://github.com/ladbsql/engine/archive/refs/heads/master.zip", engine_path)
    download_and_extract_repository("https://github.com/ladbsql/launcher/archive/refs/heads/master.zip", launcher_path)

def get_base_path():
    os_type = platform.system()
    if os_type == "Windows":
        return os.path.join(os.environ['PROGRAMFILES'], 'laDB')
    elif os_type == "Darwin":  # macOS
        return os.path.join("/Applications", 'laDB')
    elif os_type == "Linux":
        return os.path.join('/usr/local', 'laDB')
    else:
        raise Exception("Sistema Operativo no Soportado")

def download_and_extract_repository(url, extract_to):
    try:
        os.makedirs(extract_to, exist_ok=True)
        response = requests.get(url, stream=True)
        total_size_in_bytes= int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar['maximum'] = total_size_in_bytes
        progress_label.configure(text="Descargando...")
        zip_path = os.path.join(extract_to, 'repository.zip')
        with open(zip_path, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar['value'] += len(data)
                app.update_idletasks()  # Actualizar la barra de progreso
                file.write(data)
        progress_label.configure(text="Extrayendo...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for member in zip_ref.infolist():
                # Construir el path de destino omitiendo el primer componente del nombre del archivo
                target_path = os.path.join(extract_to, os.path.join(*member.filename.split('/')[1:]))
                if member.filename[-1] == '/':  # Si es un directorio
                    os.makedirs(target_path, exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    with open(target_path, 'wb') as f:
                        f.write(zip_ref.read(member))
        os.remove(zip_path)  # Eliminar el archivo ZIP después de la extracción
        progress_label.configure(text="Instalación completa")
    except Exception as e:
        messagebox.showerror("Error", f"Error descargando el repositorio: {e}")

def setup_ui():
    global app, progress_bar, progress_label

    app = ctk.CTk()
    app.title("Instalador de laDB")
    app.geometry("400x240")

    progress_bar = ttk.Progressbar(app, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=20)

    progress_label = ctk.CTkLabel(app, text="Haga clic en 'Iniciar Instalación' para comenzar.")
    progress_label.pack(pady=10)

    tos_label = ctk.CTkLabel(app, text="Al hacer clic en 'Iniciar Instalación',\n usted acepta los términos y condiciones.")
    tos_label.pack(pady=12)

    install_button = ctk.CTkButton(app, text="Iniciar Instalación", command=lambda: install())
    install_button.pack(pady=20)

    app.mainloop()

if __name__ == "__main__":
    setup_ui()
