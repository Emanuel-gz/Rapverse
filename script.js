'use strict';

// Research scope and exact sources are documented in docs/SOURCES.md.
// A critic's description or a collaboration is not an artist-declared influence.
const chartBase =
  'https://github.com/mhollingshead/billboard-hot-100/blob/abefdd18eaf587c102bda9b0f2bc11aa9ae250d5/date/';
const appleCarti = 'https://music.apple.com/us/artist/playboi-carti/982372505';
const appleCochise = 'https://music.apple.com/us/artist/cochise/163302681';
const pitchforkCarti = 'https://pitchfork.com/artists/34362-playboi-carti/';
const pitchforkDebut = 'https://pitchfork.com/reviews/albums/23196-playboi-carti/';
const pitchforkDieLit = 'https://pitchfork.com/reviews/albums/playboi-carti-die-lit/';
const pitchforkRed = 'https://pitchfork.com/reviews/albums/playboi-carti-whole-lotta-red/';
const pitchforkMusic = 'https://pitchfork.com/reviews/albums/playboi-carti-music/';
const pitchforkFreshmen = 'https://pitchfork.com/news/xxl-2022-freshman-class-babyface-ray-doechii-nardo-wick-babytron-sofaygo-and-more/';
const billboardTurnItUp = 'https://www.billboard.com/music/rb-hip-hop/best-new-hip-hop-cochise-josh-levi-1235086388/';
const billboardHydroplane = 'https://www.billboard.com/music/rb-hip-hop/best-new-hip-hop-songs-j-hus-kenny-mason-khamari-1235342926/';
const source = (label, url) => ({ label, url });
const artistContent = {
  carti: {
    history: {
      kind: 'fact',
      label: 'BIOGRAFÍA DOCUMENTADA',
      title: 'De Atlanta a una voz propia.',
      paragraphs: [
        'Jordan Carter nació en 1996. Según la biografía editorial de Apple Music, comenzó en el circuito underground de Atlanta y conoció a A$AP Rocky en un festival en 2015; aquella relación impulsó su proyección pública.',
        'Pitchfork sitúa «Broke Boi» entre sus primeros temas destacados de 2015. Su mixtape homónima llegó en 2017 con «Magnolia» y «wokeuplikethis*», junto a Lil Uzi Vert. Después publicó Die Lit (2018), Whole Lotta Red (2020) y MUSIC (2025).',
      ],
      sources: [source('Apple Music · biografía', appleCarti), source('Pitchfork · debut', pitchforkDebut), source('Pitchfork · discografía', pitchforkCarti)],
    },
    evolution: {
      kind: 'fact',
      label: 'EVOLUCIÓN · CRÍTICA IDENTIFICADA',
      title: 'Minimalismo, tensión y nuevas voces.',
      paragraphs: [
        'Pitchfork describe la mixtape de 2017 mediante la repetición, las intervenciones vocales y las producciones de Pi’erre Bourne. En Die Lit (2018) observa un tratamiento más extremo de esas ideas; «Shoota» muestra además su colaboración con Lil Uzi Vert.',
        'La misma publicación sitúa Whole Lotta Red (2020) en un sonido más áspero y acelerado, con registros vocales variados. Su reseña de MUSIC (2025) presenta un proyecto extenso que reúne varias de esas etapas. Son lecturas críticas del sonido, no datos sobre su carácter.',
      ],
      sources: [source('Pitchfork · debut', pitchforkDebut), source('Die Lit', pitchforkDieLit), source('Whole Lotta Red', pitchforkRed), source('MUSIC', pitchforkMusic)],
    },
    style: {
      kind: 'editorial',
      label: 'LECTURA EDITORIAL',
      title: 'La voz como parte del ritmo.',
      paragraphs: [
        'Escucha «Magnolia», «Shoota» y «FE!N» atendiendo a cómo las repeticiones y los cambios de voz dialogan con cada producción. Nuestra impresión de intensidad describe el resultado musical; no pretende explicar su personalidad privada.',
        'Apple Music habla de minimalismo trap y energía punk para caracterizar su obra. Son términos editoriales sobre la música y la imagen pública, no declaraciones del artista sobre sus fuentes de inspiración.',
      ],
      sources: [source('Apple Music · lectura editorial', appleCarti)],
    },
    influences: {
      kind: 'fact',
      label: 'INFLUENCIAS · ALCANCE VERIFICADO',
      title: 'Mentoría y antecedentes sonoros.',
      paragraphs: [
        'A$AP Rocky figura como mentor en la reseña de Pitchfork de 2017; Apple Music documenta su encuentro en 2015. Es una influencia en la trayectoria y la imagen pública, sin atribuirle una enseñanza musical concreta que las fuentes no detallan.',
        'Pi’erre Bourne es un colaborador decisivo en las producciones de sus primeros proyectos, según Pitchfork. La reseña de Die Lit sitúa a Travis Porter y Rich Kidz como antecedentes de un estilo cercano. Esa genealogía la propone la crítica: no es una lista de ídolos declarada por Carti.',
      ],
      sources: [source('Pitchfork · debut', pitchforkDebut), source('Pitchfork · Die Lit', pitchforkDieLit), source('Apple Music', appleCarti)],
    },
  },
  cochise: {
    history: {
      kind: 'fact',
      label: 'BIOGRAFÍA DOCUMENTADA',
      title: 'De Palm Bay al alcance global.',
      paragraphs: [
        'Cochise creció en Palm Bay, Florida, con padres caribeños. Apple Music cuenta que, tras el instituto, recibió ofertas para jugar al fútbol universitario, pero siguió cerca de casa y publicaba música en línea mientras estudiaba en un community college.',
        '«Moshi Moshi» obtuvo atención en 2017; «Hatchback» amplió su visibilidad en 2019. En 2020 firmó con Columbia Records, según la biografía de Apple Music. «Tell Em», junto a $NOT, entró en el Hot 100 en 2021; Pitchfork informó de su inclusión en la promoción XXL Freshman de 2022.',
      ],
      sources: [source('Apple Music · biografía', appleCochise), source('Hot 100 · 12 jun 2021', `${chartBase}2021-06-12.json`), source('Pitchfork · XXL 2022', pitchforkFreshmen)],
    },
    evolution: {
      kind: 'fact',
      label: 'DISCOGRAFÍA DOCUMENTADA',
      title: 'Más allá de un solo viral.',
      paragraphs: [
        'Apple Music lista Pulp (2018), «Hatchback» (2019), Benbow Crescent y «POCKET ROCKET» (2021), y «TURN IT UP» en THE INSPECTION (2022). El catálogo continúa con NO ONE’S NICE TO ME (2023), WHY ALWAYS ME? (2024) y TRENCH TOWN (2026).',
        'Billboard describe «TURN IT UP» como una producción compartida por Cochise, Nonbruh y Ransom. Su reseña de «Hydroplane» (2023) observa una dicción distinta a la habitual. Son ejemplos concretos de su trabajo y de la lectura crítica de su evolución, no una jerarquía definitiva de sus discos.',
      ],
      sources: [source('Apple Music · catálogo', appleCochise), source('Billboard · TURN IT UP', billboardTurnItUp), source('Billboard · Hydroplane', billboardHydroplane)],
    },
    style: {
      kind: 'editorial',
      label: 'LECTURA EDITORIAL',
      title: 'Una energía que cambia de forma.',
      paragraphs: [
        'En «Tell Em», «Hatchback» y «TURN IT UP» proponemos escuchar el fraseo, la voz aguda y el ritmo de las intervenciones. Apple Music destaca su variedad de registros y Billboard describe la energía de «TURN IT UP».',
        '«Juguetón» puede describir una impresión de escucha, no su personalidad fuera de la música. Tampoco presentamos un parecido vocal con Carti como prueba de una influencia directa.',
      ],
      sources: [source('Apple Music · biografía', appleCochise), source('Billboard · TURN IT UP', billboardTurnItUp)],
    },
    influences: {
      kind: 'fact',
      label: 'INFLUENCIAS · ALCANCE VERIFICADO',
      title: 'Cine, videojuegos y referencias pop.',
      paragraphs: [
        'La biografía de Apple Music explica que su nombre artístico rinde homenaje a The Warriors, película de 1979, y al videojuego basado en ella. Esa es una referencia cultural documentada, no una hipótesis construida a partir de su sonido.',
        'Apple Music describe referencias a la cultura popular en «Hatchback» y documenta su crianza en una familia caribeña. Esos datos dan contexto a su obra; la fuente no afirma qué músicos lo inspiraron ni que Carti sea una influencia declarada.',
      ],
      sources: [source('Apple Music · biografía', appleCochise)],
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
    title: 'Hatchback',
    artist: 'cochise',
    credit: 'Cochise',
    year: '2019',
    catalog: appleCochise,
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
    title: 'Tell Em',
    artist: 'cochise',
    credit: 'Cochise & $NOT',
    year: '2021',
    chart: '2021-06-12',
    position: 64,
  },
  {
    title: 'Sky',
    artist: 'carti',
    credit: 'Playboi Carti',
    year: '2020',
    catalog: appleCarti,
  },
  {
    title: 'POCKET ROCKET',
    artist: 'cochise',
    credit: 'Cochise',
    year: '2021',
    catalog: appleCochise,
  },
  {
    title: 'FE!N',
    artist: 'carti',
    credit: 'Travis Scott feat. Playboi Carti',
    year: '2023',
    chart: '2023-08-12',
    position: 5,
  },
  {
    title: 'TURN IT UP',
    artist: 'cochise',
    credit: 'Cochise',
    year: '2022',
    catalog: appleCochise,
  },
];

const comparisons = [
  [
    'Trayectoria · dato',
    'Atlanta: mixtape Playboi Carti (2017), Die Lit (2018), Whole Lotta Red (2020) y MUSIC (2025).',
    'Palm Bay: «Moshi Moshi» (2017), «Hatchback» (2019), «Tell Em» (2021) y TRENCH TOWN (2026).',
  ],
  [
    'Sonido · lectura crítica',
    'Pitchfork destaca el minimalismo y las intervenciones vocales; luego describe la intensidad de Whole Lotta Red.',
    'Apple Music describe una voz aguda y múltiples registros; Billboard destaca la energía de «TURN IT UP».',
  ],
  [
    'Influencias · alcance',
    'Pitchfork llama mentor a A$AP Rocky y sitúa a Travis Porter y Rich Kidz como antecedentes sonoros.',
    'Apple Music documenta el homenaje de su nombre a The Warriors y su videojuego; no confirma una influencia musical de Carti.',
  ],
  [
    'Actitud · interpretación',
    'La intensidad puede ser una lectura del sonido; no describe su carácter privado.',
    'Lo juguetón puede ser una lectura del sonido; no describe su carácter privado.',
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
  panel.setAttribute('aria-labelledby', `${artist}-${view}-tab`);
  panel.append(element('span', `content-kind ${content.kind}`, content.label));
  panel.append(element('h4', '', content.title));
  content.paragraphs.forEach((text) => panel.append(element('p', '', text)));
  if (content.sources) {
    const links = element('div', 'artist-sources');
    content.sources.forEach(({ label, url }) => {
      const link = externalLink(url, `${label} ↗`, 'inline-source');
      link.setAttribute('aria-label', `${label}, abrir fuente en nueva pestaña`);
      links.append(link);
    });
    panel.append(links);
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
      song.chart ? `${chartBase}${song.chart}.json` : song.catalog,
      song.chart ? `HOT 100 · #${song.position}` : 'APPLE MUSIC · DESTACADA',
      'song-project',
    );
    chart.setAttribute(
      'aria-label',
      song.chart
        ? `${song.title}: puesto ${song.position} en la lista del ${song.chart}, consultar fuente en nueva pestaña`
        : `${song.title}: aparece en Top Songs de Apple Music, consultar fuente en nueva pestaña`,
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
    'Biografías y catálogos de Apple Music, reseñas de Pitchfork, notas de Billboard y una selección histórica del Hot 100. Las fichas enlazan los textos consultados.',
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
    'Archivo de terceros consultado el 12 de octubre de 2026; las listas originales pertenecen a Billboard. Cada posición mostrada enlaza su registro semanal.',
  ),
);
sourceList.append(archive);
[
  ['02 / Apple Music · Playboi Carti ↗', appleCarti],
  ['03 / Apple Music · Cochise ↗', appleCochise],
  ['04 / Pitchfork · Playboi Carti ↗', pitchforkCarti],
  ['05 / Pitchfork · XXL Freshmen 2022 ↗', pitchforkFreshmen],
].forEach(([label, url]) => {
  const item = element('div', 'source-item');
  item.append(externalLink(url, label));
  sourceList.append(item);
});
const scope = element('p', 'source-item');
scope.textContent =
  '«Top Songs» de Apple Music es una selección editorial de la plataforma; el puesto del Hot 100 pertenece a una semana concreta. Ninguno es un ranking actual de toda la música de ambos artistas.';
sourceList.append(scope);
const status = element('p', 'source-item research-status');
status.textContent =
  'Las biografías cubren los hitos documentados hasta 2026. «Influencia» se usa con precisión: mentoría, antecedentes descritos por críticos o referencias culturales verificadas; no se presenta una lista de inspiraciones musicales declaradas sin entrevista directa.';
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
