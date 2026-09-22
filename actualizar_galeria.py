#!/usr/bin/env python3
"""Editor gráfico del sitio. Ejecuta: python actualizar_galeria.py"""
from __future__ import annotations
import json
import shutil
import subprocess
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

RAIZ = Path(__file__).resolve().parent
ARCHIVO = RAIZ / "contenido.json"
CARPETA_IMAGENES = RAIZ / "assets" / "obras"
EXTENSIONES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def cargar():
    return json.loads(ARCHIVO.read_text(encoding="utf-8"))


def guardar(datos):
    ARCHIVO.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class Editor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.datos = cargar()
        self.title("Editor de la galería")
        self.geometry("780x610")
        self.minsize(680, 520)
        self.configure(bg="#292d38")
        self.configurar_estilos()
        marco = ttk.Frame(self, padding=22)
        marco.pack(fill="both", expand=True)
        cabecera = ttk.Frame(marco)
        cabecera.pack(fill="x")
        ttk.Label(cabecera, text="EDITOR DEL SITIO", style="Title.TLabel").pack(side="left")
        ttk.Button(cabecera, text="Publicar en GitHub", command=self.publicar_en_github).pack(side="right")
        ttk.Label(marco, text="Actualiza tus textos, obras y artista. Guarda los cambios con un botón.", style="Sub.TLabel").pack(anchor="w", pady=(2, 16))
        pestanas = ttk.Notebook(marco)
        pestanas.pack(fill="both", expand=True)
        self.inicio_frame = ttk.Frame(pestanas, padding=20)
        self.obras_frame = ttk.Frame(pestanas, padding=20)
        self.artista_frame = ttk.Frame(pestanas, padding=20)
        pestanas.add(self.inicio_frame, text="  Inicio  ")
        pestanas.add(self.obras_frame, text="  Obras  ")
        pestanas.add(self.artista_frame, text="  Artista  ")
        self.crear_inicio()
        self.crear_obras()
        self.crear_artista()

    def configurar_estilos(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TFrame", background="#292d38")
        s.configure("TLabel", background="#292d38", foreground="#eef6ff", font=("Segoe UI", 10))
        s.configure("Title.TLabel", foreground="#72d2ff", font=("Segoe UI", 18, "bold"))
        s.configure("Sub.TLabel", foreground="#b8c0cf", font=("Segoe UI", 9))
        s.configure("TButton", background="#416cff", foreground="white", borderwidth=0, padding=(13, 8), font=("Segoe UI", 9, "bold"))
        s.map("TButton", background=[("active", "#63c8ff")])
        s.configure("TEntry", fieldbackground="#1e222b", foreground="#f2f6ff", insertcolor="white", padding=7)
        s.configure("TNotebook", background="#292d38", borderwidth=0)
        s.configure("TNotebook.Tab", background="#353b49", foreground="#cfd6e5", padding=(15, 9))
        s.map("TNotebook.Tab", background=[("selected", "#416cff")], foreground=[("selected", "white")])

    @staticmethod
    def campo(parent, texto, variable, fila):
        ttk.Label(parent, text=texto).grid(row=fila, column=0, sticky="w", pady=(0, 6))
        ttk.Entry(parent, textvariable=variable).grid(row=fila + 1, column=0, sticky="ew", pady=(0, 15))

    def crear_inicio(self):
        self.inicio_frame.columnconfigure(0, weight=1)
        inicio = self.datos.setdefault("inicio", {})
        coleccion = self.datos.setdefault("coleccion", {})
        self.bienvenida = tk.StringVar(value=inicio.get("bienvenida", ""))
        self.titulo_coleccion = tk.StringVar(value=coleccion.get("titulo", ""))
        self.campo(self.inicio_frame, "Texto de bienvenida", self.bienvenida, 0)
        self.campo(self.inicio_frame, "Título de la colección", self.titulo_coleccion, 2)
        ttk.Button(self.inicio_frame, text="Guardar textos", command=self.guardar_inicio).grid(row=4, column=0, sticky="w", pady=(8, 0))

    def guardar_inicio(self):
        self.datos["inicio"]["bienvenida"] = self.bienvenida.get().strip()
        self.datos["coleccion"]["titulo"] = self.titulo_coleccion.get().strip()
        self.persistir("Textos guardados correctamente.")

    def crear_obras(self):
        self.obras_frame.columnconfigure(0, weight=1)
        self.obras_frame.rowconfigure(1, weight=1)
        ttk.Label(self.obras_frame, text="Todas las obras quedan en la misma colección.").grid(row=0, column=0, sticky="w", pady=(0, 10))
        lista_frame = ttk.Frame(self.obras_frame)
        lista_frame.grid(row=1, column=0, sticky="nsew")
        lista_frame.columnconfigure(0, weight=1)
        lista_frame.rowconfigure(0, weight=1)
        self.lista = tk.Listbox(lista_frame, bg="#1e222b", fg="#eef6ff", selectbackground="#416cff", selectforeground="white", relief="flat", highlightthickness=0, font=("Segoe UI", 10), activestyle="none")
        barra = ttk.Scrollbar(lista_frame, command=self.lista.yview)
        self.lista.config(yscrollcommand=barra.set)
        self.lista.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")
        acciones = ttk.Frame(self.obras_frame)
        acciones.grid(row=2, column=0, sticky="w", pady=(14, 0))
        ttk.Button(acciones, text="+ Añadir obra", command=lambda: self.ventana_obra()).pack(side="left", padx=(0, 8))
        ttk.Button(acciones, text="Editar seleccionada", command=self.editar_obra).pack(side="left", padx=(0, 8))
        ttk.Button(acciones, text="Eliminar", command=self.eliminar_obra).pack(side="left")
        self.actualizar_lista()

    def actualizar_lista(self):
        self.lista.delete(0, "end")
        for numero, obra in enumerate(self.datos["coleccion"].get("obras", []), 1):
            self.lista.insert("end", f"{numero:02d}  ·  {obra.get('titulo') or 'Sin título'}")

    def seleccionado(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showinfo("Selecciona una obra", "Elige primero una obra de la lista.", parent=self)
            return None
        return seleccion[0]

    def copiar_imagen(self, ruta, anterior=""):
        if not ruta:
            return anterior
        origen = Path(ruta)
        if not origen.is_file() or origen.suffix.lower() not in EXTENSIONES:
            raise ValueError("Selecciona una imagen JPG, PNG, WEBP o GIF válida.")
        CARPETA_IMAGENES.mkdir(parents=True, exist_ok=True)
        destino = CARPETA_IMAGENES / origen.name
        contador = 2
        while destino.exists() and destino.resolve() != origen.resolve():
            destino = CARPETA_IMAGENES / f"{origen.stem}-{contador}{origen.suffix.lower()}"
            contador += 1
        if destino.resolve() != origen.resolve():
            shutil.copy2(origen, destino)
        return destino.relative_to(RAIZ).as_posix()

    def ventana_obra(self, indice=None):
        existente = self.datos["coleccion"]["obras"][indice] if indice is not None else {}
        ventana = tk.Toplevel(self)
        ventana.title("Editar obra" if existente else "Añadir obra")
        ventana.configure(bg="#292d38")
        ventana.resizable(False, False)
        marco = ttk.Frame(ventana, padding=22)
        marco.pack(fill="both", expand=True)
        marco.columnconfigure(0, weight=1)
        titulo, detalle, imagen = tk.StringVar(value=existente.get("titulo", "")), tk.StringVar(value=existente.get("detalle", "")), tk.StringVar()
        self.campo(marco, "Título", titulo, 0)
        self.campo(marco, "Técnica, medidas o disponibilidad", detalle, 2)
        texto_imagen = "Imagen (elige otra solo para sustituirla)" if existente else "Imagen"
        ttk.Label(marco, text=texto_imagen).grid(row=4, column=0, sticky="w", pady=(0, 6))
        fila = ttk.Frame(marco)
        fila.grid(row=5, column=0, sticky="ew", pady=(0, 18))
        fila.columnconfigure(0, weight=1)
        ttk.Entry(fila, textvariable=imagen, width=45).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(fila, text="Elegir imagen", command=lambda: imagen.set(filedialog.askopenfilename(parent=ventana, title="Selecciona la imagen", filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.webp *.gif")]))).grid(row=0, column=1)

        def confirmar():
            if not titulo.get().strip() or (not existente and not imagen.get()):
                messagebox.showwarning("Datos incompletos", "Añade como mínimo el título y la imagen.", parent=ventana)
                return
            try:
                obra = {"titulo": titulo.get().strip(), "detalle": detalle.get().strip(), "imagen": self.copiar_imagen(imagen.get(), existente.get("imagen", ""))}
            except ValueError as error:
                messagebox.showerror("Imagen no válida", str(error), parent=ventana)
                return
            obras = self.datos["coleccion"].setdefault("obras", [])
            if indice is None: obras.append(obra)
            else: obras[indice] = obra
            guardar(self.datos)
            self.actualizar_lista()
            ventana.destroy()
            messagebox.showinfo("Listo", "Obra guardada correctamente.", parent=self)
        ttk.Button(marco, text="Guardar obra", command=confirmar).grid(row=6, column=0, sticky="w")
        ventana.transient(self)
        ventana.grab_set()

    def editar_obra(self):
        indice = self.seleccionado()
        if indice is not None: self.ventana_obra(indice)

    def eliminar_obra(self):
        indice = self.seleccionado()
        if indice is None: return
        obra = self.datos["coleccion"]["obras"][indice]
        if messagebox.askyesno("Eliminar obra", f"¿Eliminar «{obra.get('titulo', 'esta obra')}»?\nLa imagen no se borrará del ordenador.", parent=self):
            del self.datos["coleccion"]["obras"][indice]
            guardar(self.datos)
            self.actualizar_lista()
            messagebox.showinfo("Guardado", "Obra eliminada correctamente.", parent=self)

    def crear_artista(self):
        self.artista_frame.columnconfigure(0, weight=1)
        artista = self.datos.setdefault("artista", {})
        self.nombre = tk.StringVar(value=artista.get("nombre", ""))
        self.ubicacion = tk.StringVar(value=artista.get("ubicacion", ""))
        self.retrato = tk.StringVar(value=artista.get("retrato", ""))
        self.campo(self.artista_frame, "Nombre", self.nombre, 0)
        ttk.Label(self.artista_frame, text="Biografía").grid(row=2, column=0, sticky="w", pady=(0, 6))
        self.biografia = tk.Text(self.artista_frame, height=6, bg="#1e222b", fg="#f2f6ff", insertbackground="white", relief="flat", wrap="word", font=("Segoe UI", 10), padx=8, pady=8)
        self.biografia.insert("1.0", artista.get("biografia", ""))
        self.biografia.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        self.campo(self.artista_frame, "Ubicación", self.ubicacion, 4)
        ttk.Label(self.artista_frame, text="Retrato (opcional)").grid(row=6, column=0, sticky="w", pady=(0, 6))
        fila = ttk.Frame(self.artista_frame)
        fila.grid(row=7, column=0, sticky="ew", pady=(0, 16))
        fila.columnconfigure(0, weight=1)
        ttk.Entry(fila, textvariable=self.retrato).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(fila, text="Elegir retrato", command=lambda: self.retrato.set(filedialog.askopenfilename(parent=self, title="Selecciona el retrato", filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.webp *.gif")]))).grid(row=0, column=1)
        ttk.Button(self.artista_frame, text="Guardar artista", command=self.guardar_artista).grid(row=8, column=0, sticky="w")

    def guardar_artista(self):
        artista = self.datos["artista"]
        artista["nombre"] = self.nombre.get().strip()
        artista["biografia"] = self.biografia.get("1.0", "end-1c").strip()
        artista["ubicacion"] = self.ubicacion.get().strip()
        ruta = self.retrato.get().strip()
        if ruta and Path(ruta).is_file():
            origen = Path(ruta)
            destino = RAIZ / "assets" / f"retrato{origen.suffix.lower()}"
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(origen, destino)
            ruta = destino.relative_to(RAIZ).as_posix()
            self.retrato.set(ruta)
        artista["retrato"] = ruta
        self.persistir("Información del artista guardada.")

    def persistir(self, mensaje):
        guardar(self.datos)
        messagebox.showinfo("Guardado", mensaje, parent=self)

    def publicar_en_github(self):
        """Guarda los cambios y envía el sitio al remoto configurado con Git."""
        guardar(self.datos)
        try:
            comprobacion = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"], cwd=RAIZ,
                capture_output=True, text=True, check=True
            )
            if comprobacion.stdout.strip() != "true":
                raise RuntimeError("Esta carpeta no es un repositorio Git.")
            remoto = subprocess.run(
                ["git", "remote", "get-url", "origin"], cwd=RAIZ,
                capture_output=True, text=True, check=True
            ).stdout.strip()
        except (FileNotFoundError, subprocess.CalledProcessError, RuntimeError):
            messagebox.showerror(
                "GitHub no está configurado",
                "Para publicar desde aquí, primero convierte esta carpeta en un repositorio "
                "Git y conecta un remoto llamado «origin» a tu repositorio de GitHub.\n\n"
                "Después pulsa de nuevo «Publicar en GitHub».",
                parent=self,
            )
            return

        mensaje = f"Actualizar galería · {datetime.now():%d/%m/%Y %H:%M}"
        if not messagebox.askyesno(
            "Publicar en GitHub",
            f"Se guardarán los cambios, se creará un commit y se enviará a:\n{remoto}\n\n"
            "GitHub Pages actualizará la web tras terminar el despliegue. ¿Publicar ahora?",
            parent=self,
        ):
            return
        try:
            subprocess.run(["git", "add", "--all"], cwd=RAIZ, capture_output=True, text=True, check=True)
            estado = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=RAIZ, capture_output=True, text=True)
            if estado.returncode == 0:
                messagebox.showinfo("Sin cambios", "No hay cambios nuevos que publicar.", parent=self)
                return
            subprocess.run(["git", "commit", "-m", mensaje], cwd=RAIZ, capture_output=True, text=True, check=True)
            envio = subprocess.run(["git", "push"], cwd=RAIZ, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as error:
            detalle = (error.stderr or error.stdout or "Git no pudo completar la publicación.").strip()
            messagebox.showerror("No se pudo publicar", detalle, parent=self)
            return
        messagebox.showinfo(
            "Publicado",
            "Los cambios se han enviado a GitHub. GitHub Pages actualizará la web en unos instantes.\n\n"
            + (envio.stdout.strip() or "Push completado."),
            parent=self,
        )


if __name__ == "__main__":
    Editor().mainloop()
