'use strict';

// Research scope and exact source snapshots are documented in docs/SOURCES.md.
// Editorial observations are deliberately separate from chart facts.
const chartBase =
  'https://github.com/mhollingshead/billboard-hot-100/blob/abefdd18eaf587c102bda9b0f2bc11aa9ae250d5/date/';
const artistContent = {
  carti: {
    history: {
      kind: 'fact',
      label: 'DATO DOCUMENTADO',
      title: 'Un recorrido a través de las listas.',
      paragraphs: [
        '«Magnolia» y «Wokeuplikethis*», con Lil Uzi Vert, aparecen en el Billboard Hot 100 del 20 de mayo de 2017. «Magnolia» alcanza el puesto 29 en la lista del 8 de julio de ese año.',
        'Es un hito documentado de su trayectoria, no una biografía completa ni la fecha de inicio de su carrera.',
      ],
      source: '2017-07-08',
    },
    evolution: {
      kind: 'fact',
      label: 'HITOS DOCUMENTADOS',
      title: '2017 → 2025: distintas etapas.',
      paragraphs: [
        '«Magnolia» (2017), «Shoota» con Lil Uzi Vert (2018) y «FE!N» de Travis Scott con Carti (2023) ofrecen tres puntos de entrada. En 2025, «Evil J0rdan» figura en el puesto 2 del Hot 100 del 29 de marzo.',
        'Las fechas describen presencia en listas. Los cambios de timbre, producción y energía son preguntas de escucha; no se deducen de una posición comercial.',
      ],
      source: '2025-03-29',
    },
    style: {
      kind: 'editorial',
      label: 'LECTURA EDITORIAL',
      title: 'La voz como parte del ritmo.',
      paragraphs: [
        'Nuestra propuesta: escuchar «Magnolia» y «FE!N» prestando atención a la repetición, las intervenciones vocales y la energía que producen. «Intenso» describe aquí una impresión musical, no un rasgo psicológico.',
        'No atribuimos influencias personales sin una declaración comprobada del artista. Compartir una colaboración tampoco demuestra una influencia.',
      ],
    },
  },
  cochise: {
    history: {
      kind: 'fact',
      label: 'DATO DOCUMENTADO',
      title: 'Una entrada con nombre propio.',
      paragraphs: [
        '«Tell Em», acreditada a Cochise y $NOT, figura en el puesto 64 del Billboard Hot 100 del 12 de junio de 2021. Es un punto documentado de su visibilidad comercial.',
        'Este dato no establece cuándo comenzó a hacer música. Tampoco convierte una colaboración en una canción exclusivamente suya.',
      ],
      source: '2021-06-12',
    },
    evolution: {
      kind: 'fact',
      label: 'ALCANCE DOCUMENTAL',
      title: 'Una canción no cuenta toda la historia.',
      paragraphs: [
        '«Tell Em» aparece en cuatro listas semanales de junio y julio de 2021 en el archivo consultado. Ese registro documenta un hito, no toda su discografía.',
        'La ausencia de otros títulos en esta selección no significa menor valor artístico. Ampliar su biografía y evolución requiere verificar discografía y entrevistas adicionales.',
      ],
      source: '2021-07-03',
    },
    style: {
      kind: 'editorial',
      label: 'LECTURA EDITORIAL',
      title: 'El contraste también tiene personalidad.',
      paragraphs: [
        'En «Tell Em», proponemos comparar los fraseos de Cochise y $NOT y escuchar cómo cambia la sensación de movimiento entre ambos. «Juguetón» es una posibilidad de lectura del sonido, no una afirmación sobre su vida privada.',
        'No presentamos a Carti como influencia confirmada de Cochise. Un parecido que perciba el oyente no prueba una relación artística ni una declaración del músico.',
      ],
    },
  },
};

const songs = [
  {
    title: 'Magnolia',
    artist: 'carti',
    credit: 'Playboi Carti',
    year: '2017',
    chart: '2017-07-08',
    position: 29,
  },
  {
    title: 'Tell Em',
    artist: 'cochise',
    credit: 'Cochise & $NOT',
    year: '2021',
    chart: '2021-06-12',
    position: 64,
  },
  {
    title: 'Shoota',
    artist: 'carti',
    credit: 'Playboi Carti feat. Lil Uzi Vert',
    year: '2018',
    chart: '2018-05-26',
    position: 46,
  },
  {
    title: 'FE!N',
    artist: 'carti',
    credit: 'Travis Scott feat. Playboi Carti',
    year: '2023',
    chart: '2023-08-12',
    position: 5,
  },
];

const comparisons = [
  [
    'Punto de partida',
    '«Magnolia» y «FE!N»: compara la función de la voz en dos momentos distintos.',
    '«Tell Em»: compara el fraseo de Cochise con el de $NOT dentro de la misma canción.',
  ],
  [
    'Energía · interpretación',
    'Una invitación a escuchar repetición, tensión y fuerza rítmica.',
    'Una invitación a escuchar contraste, movilidad y ligereza en el fraseo.',
  ],
  [
    'Actitud · interpretación',
    'La intensidad puede ser una lectura del sonido. No equivale a describir su carácter privado.',
    'Lo juguetón puede ser una lectura del sonido. No equivale a describir su carácter privado.',
  ],
  [
    'Influencias personales',
    'Sin atribuciones: falta una entrevista directa verificada para documentarlas.',
    'Sin atribuciones: el parecido vocal no demuestra que Carti sea una influencia declarada.',
  ],
];

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function externalLink(url, text, className) {
  const link = element('a', className, text);
  link.href = url;
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
  return link;
}

function renderArtist(card, view) {
  const artist = card.dataset.artist;
  const content = artistContent[artist][view];
  const panel = card.querySelector('[role="tabpanel"]');
  panel.replaceChildren();
  panel.setAttribute(
    'aria-labelledby',
    `${artist}-${view === 'history' ? 'history' : view === 'evolution' ? 'evolution' : 'style'}-tab`,
  );
  panel.append(element('span', `content-kind ${content.kind}`, content.label));
  panel.append(element('h4', '', content.title));
  content.paragraphs.forEach((text) => panel.append(element('p', '', text)));
  if (content.source) {
    panel.append(
      externalLink(
        `${chartBase}${content.source}.json`,
        'Consultar el registro ↗ (nueva pestaña)',
        'inline-source',
      ),
    );
  }
  card.querySelectorAll('[role="tab"]').forEach((tab) => {
    const selected = tab.dataset.view === view;
    tab.setAttribute('aria-selected', String(selected));
    tab.tabIndex = selected ? 0 : -1;
  });
}

document.querySelectorAll('.artist-card').forEach((card) => {
  const tabs = [...card.querySelectorAll('[role="tab"]')];
  renderArtist(card, 'history');
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => renderArtist(card, tab.dataset.view));
    tab.addEventListener('keydown', (event) => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft')
        next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next === undefined) return;
      event.preventDefault();
      tabs[next].focus();
      renderArtist(card, tabs[next].dataset.view);
    });
  });
});

function renderSongs(filter) {
  const list = document.querySelector('#songs');
  const selection = songs.filter(
    (song) => filter === 'all' || song.artist === filter,
  );
  list.replaceChildren();
  selection.forEach((song, index) => {
    const row = element('article', 'song-row');
    row.append(
      element('span', 'song-index', String(index + 1).padStart(2, '0')),
    );
    const artwork = element('div', `song-art ${song.artist}`);
    artwork.setAttribute('aria-hidden', 'true');
    row.append(artwork);
    const title = element('div', 'song-info');
    title.append(element('h3', 'song-title', song.title));
    title.append(element('p', 'song-credit', song.credit));
    row.append(title);
    const chart = externalLink(
      `${chartBase}${song.chart}.json`,
      `HOT 100 · #${song.position}`,
      'song-project',
    );
    chart.setAttribute(
      'aria-label',
      `${song.title}: puesto ${song.position} en la lista del ${song.chart}, consultar fuente en nueva pestaña`,
    );
    row.append(chart, element('span', 'song-year', song.year));
    const query = encodeURIComponent(`${song.title} ${song.credit}`);
    const listen = externalLink(
      `https://open.spotify.com/search/${query}`,
      '',
      'listen-link',
    );
    listen.setAttribute(
      'aria-label',
      `Buscar ${song.title}, ${song.credit}, en Spotify (nueva pestaña)`,
    );
    listen.append(element('span', '', 'Buscar en Spotify'));
    const play = element('span', 'play-icon', '↗');
    play.setAttribute('aria-hidden', 'true');
    listen.append(play);
    row.append(listen);
    list.append(row);
  });
  document.querySelector('#song-count').textContent =
    `${selection.length} ${selection.length === 1 ? 'CANCIÓN DOCUMENTADA' : 'CANCIONES DOCUMENTADAS'}`;
  document.querySelectorAll('.filter-button').forEach((button) => {
    const selected = button.dataset.filter === filter;
    button.classList.toggle('selected', selected);
    button.setAttribute('aria-pressed', String(selected));
  });
}

document.querySelectorAll('.filter-button').forEach((button) => {
  button.addEventListener('click', () => renderSongs(button.dataset.filter));
});
renderSongs('all');

const comparisonBody = document.querySelector('#comparison-body');
comparisons.forEach(([topic, carti, cochise]) => {
  const row = element('tr');
  const heading = element('th', '', topic);
  heading.scope = 'row';
  row.append(heading, element('td', '', carti), element('td', '', cochise));
  comparisonBody.append(row);
});

const sourceList = document.querySelector('#source-list');
sourceList.append(
  element(
    'p',
    '',
    'Selección histórica de entradas en el Billboard Hot 100 estadounidense, entre 2017 y 2025. No es un ranking de reproducciones actuales ni una discografía completa.',
  ),
);
const archive = element('div', 'source-item');
archive.append(
  externalLink(
    'https://github.com/mhollingshead/billboard-hot-100',
    '01 / Archivo independiente del Billboard Hot 100 ↗',
  ),
);
archive.append(
  element(
    'small',
    '',
    'Datos consultados el 12 de octubre de 2026. Es un archivo de terceros; las listas originales pertenecen a Billboard. Las fichas enlazan cada registro utilizado.',
  ),
);
sourceList.append(archive);
const scope = element('p', 'source-item');
scope.textContent =
  'La posición indicada pertenece a una lista semanal concreta. La selección no es proporcional entre artistas: una lista estadounidense no mide toda su relevancia artística ni documenta todas sus canciones.';
sourceList.append(scope);
const status = element('p', 'source-item research-status');
status.textContent =
  'Esta edición se concentra en hitos de las listas. No incluye biografías completas ni influencias personales: esos apartados quedan pendientes de contrastar con discografías y entrevistas directas.';
sourceList.append(status);

const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
function closeMenu(returnFocus = false) {
  navigation.classList.remove('open');
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'Abrir menú');
  if (returnFocus) menuButton.focus();
}
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  navigation.classList.toggle('open', open);
});
navigation
  .querySelectorAll('a')
  .forEach((link) => link.addEventListener('click', () => closeMenu()));
document.addEventListener('keydown', (event) => {
  if (
    event.key === 'Escape' &&
    menuButton.getAttribute('aria-expanded') === 'true'
  )
    closeMenu(true);
});
document.addEventListener('click', (event) => {
  if (!navigation.contains(event.target) && !menuButton.contains(event.target))
    closeMenu();
});
const mobileBreakpoint = window.matchMedia('(max-width: 650px)');
mobileBreakpoint.addEventListener('change', () => closeMenu());

const navLinks = [...navigation.querySelectorAll('.nav-link')];
const navSections = navLinks.map((link) => document.querySelector(link.hash));
let scheduled = false;
function updateNavigation() {
  const position = window.scrollY + 160;
  let active = navSections[0];
  navSections.forEach((section) => {
    if (section.offsetTop <= position) active = section;
  });
  navLinks.forEach((link) => {
    const current = link.hash === `#${active.id}`;
    link.classList.toggle('active', current);
    if (current) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
  scheduled = false;
}
window.addEventListener(
  'scroll',
  () => {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(updateNavigation);
  },
  { passive: true },
);
window.addEventListener('resize', updateNavigation);
updateNavigation();
