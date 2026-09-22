const $ = (selector) => document.querySelector(selector);

function texto(selector, value) {
  const elemento = $(selector);
  if (elemento && value) elemento.textContent = value;
}

function abrirModal(obra) {
  const modal = $('#modal');
  $('#imagen-modal').src = obra.imagen;
  $('#imagen-modal').alt = obra.titulo;
  texto('#titulo-modal', obra.titulo);
  texto('#detalle-modal', obra.detalle);
  modal.classList.add('abierto');
  modal.setAttribute('aria-hidden', 'false');
}

function cerrarModal() {
  $('#modal').classList.remove('abierto');
  $('#modal').setAttribute('aria-hidden', 'true');
}

function crearGaleria(obras) {
  const galeria = $('#galeria');
  if (!galeria) return;
  $('#sin-obras').hidden = obras.length !== 0;
  obras.forEach((obra) => {
    const tarjeta = document.createElement('article');
    tarjeta.className = 'obra';
    const imagen = document.createElement('img');
    imagen.src = obra.imagen;
    imagen.alt = obra.titulo;
    imagen.loading = 'lazy';
    const info = document.createElement('div');
    info.className = 'obra-info';
    const titulo = document.createElement('h3');
    titulo.textContent = obra.titulo;
    const detalle = document.createElement('p');
    detalle.textContent = obra.detalle || '';
    info.append(titulo, detalle);
    tarjeta.append(imagen, info);
    tarjeta.addEventListener('click', () => abrirModal(obra));
    galeria.append(tarjeta);
  });
}

async function iniciar() {
  try {
    const respuesta = await fetch('contenido.json');
    if (!respuesta.ok) throw new Error('No se pudo leer contenido.json');
    const datos = await respuesta.json();
    const artista = datos.artista || {};
    texto('#texto-bienvenida', datos.inicio?.bienvenida);
    texto('#titulo-coleccion', datos.coleccion?.titulo);
    texto('#nombre-artista', artista.nombre);
    texto('#bio-artista', artista.biografia);
    texto('#ubicacion-artista', artista.ubicacion);
    texto('#pie-nombre', artista.nombre || 'Obra');
    const retrato = $('#retrato-artista');
    if (artista.retrato && retrato) { retrato.src = artista.retrato; retrato.hidden = false; }
    crearGaleria(datos.coleccion?.obras || []);
  } catch (error) {
    $('#sin-obras').hidden = false;
    $('#sin-obras').textContent = 'No se ha podido cargar el contenido. Publica la carpeta completa o inicia un servidor local.';
    console.error(error);
  }
}

if ($('.cerrar')) $('.cerrar').addEventListener('click', cerrarModal);
if ($('#modal')) $('#modal').addEventListener('click', (event) => { if (event.target.id === 'modal') cerrarModal(); });
document.addEventListener('keydown', (event) => { if (event.key === 'Escape' && $('#modal')) cerrarModal(); });
if ($('#anio')) $('#anio').textContent = new Date().getFullYear();
iniciar();
