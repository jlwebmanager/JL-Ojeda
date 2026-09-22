# Publicar la web en GitHub Pages

## Primera publicación (sin comandos)

1. Entra en [github.com](https://github.com) e inicia sesión.
2. Pulsa **New** y crea un repositorio, por ejemplo `mi-galeria`. Déjalo público y no marques las opciones de README, `.gitignore` ni licencia.
3. En la pantalla del repositorio nuevo, pulsa **uploading an existing file**.
4. Abre esta carpeta y arrastra **todo lo que hay dentro** a GitHub: `index.html`, `obras.html`, `artista.html`, las carpetas `Vadim _ klevenskiy_files`, etc. No arrastres la carpeta exterior completa.
5. Pulsa **Commit changes**.
6. En el repositorio, entra en **Settings → Pages**. En **Build and deployment**, selecciona **Deploy from a branch**, rama `main` y carpeta `/(root)`. Guarda.
7. Espera uno o dos minutos. GitHub mostrará el enlace público de tu página en esa misma pantalla.

## Publicar actualizaciones desde el editor

Para usar el botón **Publicar en GitHub** de `actualizar_galeria.py`, instala [GitHub Desktop](https://desktop.github.com/), usa **File → Add local repository** con esta carpeta y luego **Publish repository**. A partir de ese momento, el botón del editor hará el envío de cambios a GitHub.

> No subas ni compartas contraseñas, tokens o claves de GitHub dentro de esta carpeta.
