# Sitio de obra estático

El sitio está listo para GitHub Pages: publica esta carpeta completa y selecciona la rama/carpeta raíz en **Settings → Pages**.

## Cambiar el contenido

Con Python 3 instalado, ejecuta:

```powershell
python .\actualizar_galeria.py
```

Se abrirá una ventana con tres pestañas: **Inicio**, **Obras** y **Artista**. Desde ella puedes añadir, editar o quitar obras, elegir las imágenes y actualizar los textos. Todo queda guardado en `contenido.json`; sube ese archivo y las imágenes nuevas al repositorio.

## Publicar directamente desde el editor

Después de crear el repositorio en GitHub y activar GitHub Pages una sola vez, usa **Publicar en GitHub** dentro del editor. El botón guarda el contenido, crea un commit y ejecuta `git push`; GitHub Pages publica automáticamente la nueva versión.

La carpeta debe ser un repositorio Git con un remoto llamado `origin`. El editor utiliza tu inicio de sesión normal de Git/GitHub y no almacena contraseñas ni tokens.

Para previsualizarlo en local sin el límite de `fetch` del navegador:

```powershell
python -m http.server 8000
```

Después abre `http://localhost:8000`.
