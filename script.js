'use strict';

document.documentElement.classList.add('js');

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
      label: 'LADO A / LOS ORÍGENES',
      title: 'Atlanta fue el punto de partida.',
      paragraphs: [
        'Antes de Playboi Carti estuvo Jordan Carter, abriéndose camino en el underground de Atlanta. En 2015, «Broke Boi» llamó la atención sobre su música. Ese mismo año conoció a A$AP Rocky en un festival: una conexión que ayudaría a ampliar su alcance.',
        'La mixtape Playboi Carti llegó en 2017 con «Magnolia» y «wokeuplikethis*», esta última junto a Lil Uzi Vert. Escuchar ese comienzo es volver al momento en que las frases cortas, las repeticiones y la voz ya empezaban a dejar una firma propia.',
      ],
      sources: [source('Los primeros años', appleCarti), source('La mixtape de 2017', pitchforkDebut), source('Más sobre su recorrido', pitchforkCarti)],
    },
    evolution: {
      kind: 'fact',
      label: 'LADO B / CAMBIO DE FRECUENCIA',
      title: 'Cada etapa cambia la temperatura.',
      paragraphs: [
        'En Playboi Carti (2017), las producciones de Pi’erre Bourne dejan espacio para que una repetición o una entrada vocal se queden contigo. Die Lit (2018) lleva esa fórmula más lejos: basta pasar por «Shoota», con Lil Uzi Vert, para reconocer el pulso de esa etapa.',
        'Whole Lotta Red (2020) cambia la temperatura con un sonido más áspero, acelerado y lleno de registros vocales. MUSIC (2025) reúne varias de esas caras en un proyecto extenso. La gracia está en recorrerlos en orden y escuchar cuánto cambia la voz sobre el beat.',
      ],
      sources: [source('El primer proyecto', pitchforkDebut), source('Die Lit', pitchforkDieLit), source('Whole Lotta Red', pitchforkRed), source('MUSIC', pitchforkMusic)],
    },
    style: {
      kind: 'editorial',
      label: 'EN EL BEAT / ESTILO',
      title: 'La voz también es percusión.',
      paragraphs: [
        'Pon «Magnolia», sigue con «Shoota» y salta a «FE!N». Fíjate en las repeticiones, los cambios de registro y esas entradas que parecen empujar el beat. En Carti, la voz puede funcionar como otro instrumento: importa lo que dice, pero también cómo lo hace sonar.',
        'El espacio del trap más minimalista y la descarga de energía punk conviven en su música. A veces una frase se queda dando vueltas; otras, una textura vocal ocupa toda la atención. Prueba a seguir solo la voz durante un fragmento y después vuelve al conjunto.',
      ],
      sources: [source('Claves de su sonido', appleCarti)],
    },
    influences: {
      kind: 'fact',
      label: 'CRÉDITOS / RAÍCES',
      title: 'Las conexiones detrás del sonido.',
      paragraphs: [
        'A$AP Rocky ocupa un lugar de mentor en su recorrido desde aquel encuentro de 2015. Pi’erre Bourne aparece en otra parte esencial de la historia: la producción de sus primeros proyectos. Volver a esos beats ayuda a escuchar cómo se construyó el espacio para la voz de Carti.',
        'Para ampliar el mapa, vale la pena acercarse a Travis Porter y Rich Kidz, antecedentes de la escena de Atlanta con los que se pueden trazar parentescos sonoros. Entre esas raíces, sus colaboradores y sus propios cambios, el recorrido tiene varias puertas de entrada.',
      ],
      sources: [source('Mentores y colaboradores', pitchforkDebut), source('Las raíces de Die Lit', pitchforkDieLit), source('El encuentro con Rocky', appleCarti)],
    },
  },
  cochise: {
    history: {
      kind: 'fact',
      label: 'LADO A / LOS ORÍGENES',
      title: 'Palm Bay, fútbol y música en internet.',
      paragraphs: [
        'Cochise creció en Palm Bay, Florida, con padres caribeños. Tras el instituto tuvo ofertas para jugar al fútbol universitario, pero se quedó cerca de casa. Mientras estudiaba en un community college, iba subiendo música a internet: ahí empezó a tomar forma su recorrido.',
        '«Moshi Moshi» atrajo atención en 2017 y «Hatchback» amplió su visibilidad en 2019. En 2020 firmó con Columbia Records; al año siguiente, «Tell Em», junto a $NOT, entró en el Hot 100. Su selección para XXL Freshman en 2022 sumó otro hito a una carrera que ya iba ganando alcance.',
      ],
      sources: [source('Los primeros años', appleCochise), source('El salto de Tell Em · 2021', `${chartBase}2021-06-12.json`), source('La clase XXL de 2022', pitchforkFreshmen)],
    },
    evolution: {
      kind: 'fact',
      label: 'LADO B / CAMBIO DE FRECUENCIA',
      title: 'Una canción abre la puerta a otra.',
      paragraphs: [
        'El camino pasa por Pulp (2018), «Hatchback» (2019) y Benbow Crescent (2021), año de «POCKET ROCKET». En THE INSPECTION (2022) aparece «TURN IT UP», producida por Cochise, Nonbruh y Ransom: además de la voz, él también participa en la construcción del beat.',
        'El catálogo sigue con NO ONE’S NICE TO ME (2023), WHY ALWAYS ME? (2024) y TRENCH TOWN (2026). Entre esos lanzamientos, «Hydroplane» (2023) ofrece otra pista para seguirlo: una dicción diferente que invita a prestar atención a cómo cambia su manera de entrar en cada canción.',
      ],
      sources: [source('Su discografía', appleCochise), source('Dentro de TURN IT UP', billboardTurnItUp), source('Otra cara en Hydroplane', billboardHydroplane)],
    },
    style: {
      kind: 'editorial',
      label: 'EN EL BEAT / ESTILO',
      title: 'Una voz que rebota sobre el beat.',
      paragraphs: [
        'En «Tell Em», «Hatchback» y «TURN IT UP», la voz aguda y el fraseo hacen que cada entrada tenga su propio movimiento. Hay algo juguetón en cómo se acomoda al ritmo: escucha dónde acelera, dónde repite y cómo una variación pequeña cambia la sensación del fragmento.',
        'Su variedad de registros deja espacio para comparar canciones sin quedarte con una sola impresión. Prueba a pasar de un tema a otro siguiendo la voz; después vuelve a escuchar el beat. Ese intercambio entre ambos es una buena forma de entrar en su música.',
      ],
      sources: [source('Claves de su voz', appleCochise), source('La energía de TURN IT UP', billboardTurnItUp)],
    },
    influences: {
      kind: 'fact',
      label: 'CRÉDITOS / RAÍCES',
      title: 'Un nombre con historia de película.',
      paragraphs: [
        'El nombre Cochise conecta con The Warriors, la película de 1979, y con el videojuego basado en ella. Es un detalle que abre otra puerta a su universo: antes de entrar en una lista de canciones, ya hay una referencia al cine y al gaming.',
        'Esa conversación con la cultura pop también aparece en «Hatchback». Su crianza en una familia caribeña forma parte de la historia personal que acompaña a la música. Cine, videojuegos y referencias compartidas ofrecen contexto para descubrirlo, mientras los temas dejan escuchar cómo da forma a su propia voz.',
      ],
      sources: [source('El nombre y sus referencias', appleCochise)],
    },
  },
};

const songs = [
  {
    title: 'Magnolia',
    cover: 'assets/music/magnolia.jpg',
    audio: 'assets/music/magnolia.mp3',
    mimeType: 'audio/mpeg',
    duration: 14.994286,
    artist: 'carti',
    credit: 'Playboi Carti',
    year: '2017',
    chart: '2017-07-08',
    position: 29,
  },
  {
    title: 'Hatchback',
    cover: 'assets/music/hatchback.jpg',
    audio: 'assets/music/hatchback.mp3',
    mimeType: 'audio/mpeg',
    duration: 20.32325,
    artist: 'cochise',
    credit: 'Cochise',
    year: '2019',
    catalog: appleCochise,
  },
  {
    title: 'Shoota',
    cover: 'assets/music/shoota.jpg',
    audio: 'assets/music/shoota.mp3',
    mimeType: 'audio/mpeg',
    duration: 13.113438,
    artist: 'carti',
    credit: 'Playboi Carti feat. Lil Uzi Vert',
    year: '2018',
    chart: '2018-05-26',
    position: 46,
  },
  {
    title: 'Tell Em',
    cover: 'assets/music/tell-em.jpg',
    audio: 'assets/music/tell-em.mp3',
    mimeType: 'audio/mpeg',
    duration: 15.072625,
    artist: 'cochise',
    credit: 'Cochise & $NOT',
    year: '2021',
    chart: '2021-06-12',
    position: 64,
  },
  {
    title: 'Sky',
    cover: 'assets/music/sky.jpg',
    audio: 'assets/music/sky.mp3',
    mimeType: 'audio/mpeg',
    duration: 14.053875,
    artist: 'carti',
    credit: 'Playboi Carti',
    year: '2020',
    catalog: appleCarti,
  },
  {
    title: 'POCKET ROCKET',
    cover: 'assets/music/pocket-rocket.jpg',
    audio: 'assets/music/pocket-rocket.mp3',
    mimeType: 'audio/mpeg',
    duration: 7.1575,
    artist: 'cochise',
    credit: 'Cochise',
    year: '2021',
    catalog: appleCochise,
  },
  {
    title: 'FE!N',
    cover: 'assets/music/fein.jpg',
    audio: 'assets/music/fein.mp3',
    mimeType: 'audio/mpeg',
    duration: 60.081625,
    artist: 'carti',
    credit: 'Travis Scott feat. Playboi Carti',
    year: '2023',
    chart: '2023-08-12',
    position: 5,
  },
  {
    title: 'TURN IT UP',
    cover: 'assets/music/turn-it-up.jpg',
    audio: 'assets/music/turn-it-up.m4a',
    mimeType: 'audio/mp4',
    duration: 60.0,
    artist: 'cochise',
    credit: 'Cochise',
    year: '2022',
    catalog: appleCochise,
  },
  {
    title: 'Location',
    artist: 'carti',
    credit: 'Playboi Carti',
    year: '2017',
    catalog: appleCarti,
    catalogLabel: 'PLAYBOI CARTI · 2017',
    cover: 'assets/music/location.jpg',
    audio: 'assets/music/location.mp3',
    mimeType: 'audio/mpeg',
    duration: 25.887313,
  },
];

const comparisons = [
  [
    'El recorrido',
    'Del underground de Atlanta a Playboi Carti (2017), Die Lit (2018), Whole Lotta Red (2020) y MUSIC (2025).',
    'De subir música en Palm Bay a «Hatchback» (2019), «Tell Em» (2021) y TRENCH TOWN (2026).',
  ],
  [
    'La voz',
    'Escucha cómo las repeticiones y los cambios de registro pasan del espacio del minimalismo a la aspereza de Whole Lotta Red.',
    'Sigue la voz aguda, el fraseo y los cambios de registro: cada entrada puede darle otro movimiento al beat.',
  ],
  [
    'Las raíces',
    'A$AP Rocky como mentor, Pi’erre Bourne en la producción y la escena de Atlanta como contexto para escuchar sus comienzos.',
    'The Warriors y su videojuego están detrás del nombre; las referencias a la cultura pop también asoman en «Hatchback».',
  ],
  [
    'La energía',
    'Prueba a seguir una frase repetida: la tensión crece por cómo la voz se cruza con el ritmo.',
    'Prueba a seguir las entradas de voz: ese rebote juguetón es parte del movimiento que se siente al escucharlo.',
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
    const credits = element('details', 'artist-sources source-disclosures');
    credits.append(element('summary', '', 'Créditos de este lado'));
    const links = element('div', 'source-links');
    content.sources.forEach(({ label, url }) => {
      const link = externalLink(url, `${label} ↗`, 'inline-source');
      link.setAttribute('aria-label', `${label}, abrir fuente en nueva pestaña`);
      links.append(link);
    });
    credits.append(links);
    panel.append(credits);
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

function normalizeSearch(value) {
  return value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
}

function songId(song) {
  return `${song.artist}:${normalizeSearch(song.title)}`;
}

const savedSongsKey = 'rapverse:saved-songs';
const knownSongIds = new Set(songs.map(songId));
function parseSavedSongs(value) {
  try {
    const parsed = JSON.parse(value);
    if (!Array.isArray(parsed)) return new Set();
    return new Set(parsed.filter((id) => typeof id === 'string' && knownSongIds.has(id)));
  } catch {
    return new Set();
  }
}

function readSavedSongs() {
  try {
    return parseSavedSongs(window.localStorage.getItem(savedSongsKey));
  } catch {
    return new Set();
  }
}

let savedSongIds = readSavedSongs();
let activeSongFilter = 'all';
let songQuery = '';
const songList = document.querySelector('#songs');
const songSearch = document.querySelector('#song-search');
const clearSearch = document.querySelector('#clear-search');
const songEmpty = document.querySelector('#song-empty');
const savedCount = document.querySelector('#saved-count');

// One persistent media element keeps playback independent of filtered list renders.
const previewAudio = document.querySelector('#preview-audio');
const previewDeck = document.querySelector('#preview-deck');
const previewToggle = document.querySelector('#preview-toggle');
const previewSeek = document.querySelector('#preview-seek');
const previewVolume = document.querySelector('#preview-volume');
const previewMute = document.querySelector('#preview-mute');
const previewStatus = document.querySelector('#preview-status');
let previewSong = null;
let previewPlaying = false;
let previewLoading = false;
let previewFailed = false;
let previewStopped = false;
let previewRequest = 0;

function formatPreviewTime(seconds) {
  const time = Number.isFinite(seconds) ? Math.max(0, Math.floor(seconds)) : 0;
  return `${Math.floor(time / 60)}:${String(time % 60).padStart(2, '0')}`;
}

function updatePreviewUI() {
  const id = previewSong ? songId(previewSong) : null;
  const duration = Number.isFinite(previewAudio.duration) ? previewAudio.duration : (previewSong?.duration || 0);
  const current = previewAudio.currentTime || 0;
  previewDeck.classList.toggle('is-playing', previewPlaying);
  previewDeck.classList.toggle('is-loading', previewLoading);
  previewToggle.disabled = !previewSong;
  document.querySelector('#preview-stop').disabled = !previewSong;
  previewToggle.textContent = '';
  previewToggle.setAttribute('aria-pressed', String(previewPlaying));
  previewToggle.setAttribute('aria-label', `${previewPlaying ? 'Pausar' : previewFailed ? 'Reintentar' : 'Reproducir'} fragmento${previewSong ? ` de ${previewSong.title}` : ''}`);
  previewSeek.disabled = !previewSong || previewAudio.readyState < 1 || previewFailed;
  previewSeek.max = String(duration || 1);
  previewSeek.value = String(Math.min(current, duration));
  previewSeek.style.setProperty('--progress', `${duration ? current / duration * 100 : 0}%`);
  previewSeek.setAttribute('aria-valuetext', `${formatPreviewTime(current)} de ${formatPreviewTime(duration)}`);
  document.querySelector('#preview-current').textContent = formatPreviewTime(current);
  document.querySelector('#preview-duration').textContent = formatPreviewTime(duration);
  previewMute.setAttribute('aria-pressed', String(previewAudio.muted));
  previewMute.setAttribute('aria-label', previewAudio.muted ? 'Activar sonido' : 'Silenciar');
  previewMute.textContent = previewAudio.muted ? '×' : '♪';
  previewVolume.value = String(previewAudio.volume);
  songList.querySelectorAll('.song-row').forEach((row) => {
    const selected = row.dataset.songId === id;
    const playing = selected && previewPlaying;
    const loading = selected && previewLoading;
    row.classList.toggle('is-playing', playing);
    row.classList.toggle('is-current', selected);
    const button = row.querySelector('.preview-toggle');
    if (!button) return;
    button.setAttribute('aria-pressed', String(playing));
    button.setAttribute('aria-busy', String(loading));
    const song = songs.find((candidate) => songId(candidate) === row.dataset.songId);
    const action = playing ? 'Pausar' : selected && previewFailed ? 'Reintentar' : 'Escuchar';
    button.setAttribute('aria-label', `${action} fragmento de ${song.title}, ${song.credit}`);
    button.querySelector('.preview-label').textContent = loading ? 'Cargando…' : action;
    button.querySelector('.preview-icon').textContent = '';
  });
}

function previewError() {
  previewPlaying = false;
  previewLoading = false;
  previewFailed = true;
  previewStatus.textContent = `No se pudo reproducir ${previewSong?.title || 'el fragmento'}. Vuelve a intentarlo.`;
  updatePreviewUI();
}

async function playPreview(song) {
  const request = ++previewRequest;
  previewStopped = false;
  const sameSong = previewSong && songId(previewSong) === songId(song);
  if (sameSong && (!previewAudio.paused || previewLoading)) {
    previewAudio.pause();
    previewPlaying = false;
    previewLoading = false;
    previewStatus.textContent = `Reproducción pausada: ${song.title}.`;
    updatePreviewUI();
    return;
  }
  if (!sameSong) {
    previewAudio.pause();
    previewSong = song;
    previewAudio.src = song.audio;
    document.querySelector('#now-title').textContent = song.title;
    document.querySelector('#now-index').textContent = String(songs.indexOf(song) + 1).padStart(2, '0');
    document.querySelector('#now-credit').textContent = song.credit;
    const cover = document.querySelector('#now-cover');
    cover.src = song.cover;
    cover.hidden = false;
  } else if (previewFailed) {
    previewAudio.load();
  }
  previewFailed = false;
  previewPlaying = false;
  previewLoading = true;
  previewStatus.textContent = `Cargando fragmento de ${song.title}…`;
  updatePreviewUI();
  try {
    await previewAudio.play();
  } catch (error) {
    // A newer selection, pause or stop can cancel a pending play promise.
    if (request === previewRequest && error.name !== 'AbortError') previewError();
  }
}

songList.addEventListener('click', (event) => {
  const button = event.target.closest('.preview-toggle');
  if (!button || !songList.contains(button)) return;
  const song = songs.find((candidate) => songId(candidate) === button.dataset.songId);
  if (song) playPreview(song);
});
previewToggle.addEventListener('click', () => {
  if (previewSong) playPreview(previewSong);
});
document.querySelector('#preview-stop').addEventListener('click', () => {
  ++previewRequest;
  previewStopped = true;
  previewAudio.pause();
  previewAudio.currentTime = 0;
  previewPlaying = false;
  previewLoading = false;
  previewStatus.textContent = 'Reproducción detenida.';
  updatePreviewUI();
});
previewSeek.addEventListener('input', () => {
  if (Number.isFinite(previewAudio.duration)) previewAudio.currentTime = Number(previewSeek.value);
  updatePreviewUI();
});
previewVolume.addEventListener('input', () => {
  previewAudio.volume = Number(previewVolume.value);
  if (previewAudio.volume > 0) previewAudio.muted = false;
  updatePreviewUI();
});
previewMute.addEventListener('click', () => {
  previewAudio.muted = !previewAudio.muted;
});
previewAudio.addEventListener('playing', () => {
  previewPlaying = true;
  previewLoading = false;
  previewFailed = false;
  previewStatus.textContent = `Reproduciendo ${previewSong.title}, ${previewSong.credit}.`;
  updatePreviewUI();
});
previewAudio.addEventListener('pause', () => {
  previewPlaying = false;
  previewLoading = false;
  if (previewSong && !previewFailed && !previewStopped && !previewAudio.ended) {
    previewStatus.textContent = `Reproducción pausada: ${previewSong.title}.`;
  }
  updatePreviewUI();
});
previewAudio.addEventListener('waiting', () => {
  previewPlaying = false;
  previewLoading = !previewAudio.paused;
  updatePreviewUI();
});
previewAudio.addEventListener('ended', () => {
  previewPlaying = false;
  previewLoading = false;
  previewAudio.currentTime = 0;
  previewStatus.textContent = `Fragmento de ${previewSong.title} finalizado. Vuelve a darle play.`;
  updatePreviewUI();
});
previewAudio.addEventListener('error', previewError);
['loadedmetadata', 'durationchange', 'timeupdate', 'volumechange'].forEach((event) => {
  previewAudio.addEventListener(event, updatePreviewUI);
});

function persistSavedSongs() {
  try {
    window.localStorage.setItem(savedSongsKey, JSON.stringify([...savedSongIds]));
  } catch {
    // Favorites remain usable for this visit when browser storage is unavailable.
  }
}

function renderSongs(filter = activeSongFilter) {
  activeSongFilter = filter;
  const query = normalizeSearch(songQuery);
  const selection = songs.filter((song) => {
    const matchesFilter = filter === 'all'
      || (filter === 'saved' ? savedSongIds.has(songId(song)) : song.artist === filter);
    const matchesQuery = normalizeSearch(`${song.title} ${song.credit} ${song.year}`).includes(query);
    return matchesFilter && matchesQuery;
  });
  const list = songList;
  list.replaceChildren();
  selection.forEach((song, index) => {
    const row = element('article', 'song-row');
    const id = songId(song);
    row.dataset.songId = id;
    row.append(
      element('span', 'song-index', String(index + 1).padStart(2, '0')),
    );
    const artwork = element('div', `song-art ${song.artist}`);
    artwork.setAttribute('aria-hidden', 'true');
    const cover = element('img', 'song-cover');
    cover.src = song.cover;
    cover.alt = '';
    cover.width = 76;
    cover.height = 76;
    artwork.append(cover);
    row.append(artwork);
    const title = element('div', 'song-info');
    title.append(element('h3', 'song-title', song.title));
    title.append(element('p', 'song-credit', song.credit));
    row.append(title);
    const chart = externalLink(
      song.chart ? `${chartBase}${song.chart}.json` : song.catalog,
      song.chart ? `HOT 100 · #${song.position}` : (song.catalogLabel || 'EN LA SELECCIÓN'),
      'song-project',
    );
    chart.setAttribute(
      'aria-label',
      song.chart
        ? `${song.title}: puesto ${song.position} en la lista del ${song.chart}, consultar fuente en nueva pestaña`
        : song.catalogLabel
          ? `${song.title}: catálogo de Playboi Carti, consultar fuente en nueva pestaña`
          : `${song.title}: consultar ficha de catálogo en nueva pestaña`,
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
    listen.append(element('span', '', 'Spotify'));
    const play = element('span', 'play-icon', '↗');
    play.setAttribute('aria-hidden', 'true');
    listen.append(play);
    title.append(listen);
    const preview = element('button', 'preview-toggle');
    preview.type = 'button';
    preview.dataset.songId = id;
    const icon = element('span', 'preview-icon');
    icon.setAttribute('aria-hidden', 'true');
    preview.append(icon, element('span', 'preview-label', 'Escuchar'),
      element('span', 'preview-length', formatPreviewTime(song.duration)));
    row.append(preview);
    const saved = savedSongIds.has(id);
    const save = element('button', 'save-song');
    save.type = 'button';
    save.dataset.songId = id;
    save.setAttribute('aria-pressed', String(saved));
    const saveLabel = saved
      ? `Quitar ${song.title}, ${song.credit}, de guardadas`
      : `Guardar ${song.title}, ${song.credit}`;
    save.setAttribute('aria-label', saveLabel);
    save.title = saveLabel;
    const saveIcon = element('span', 'save-icon', saved ? '♥' : '♡');
    saveIcon.setAttribute('aria-hidden', 'true');
    save.append(saveIcon);
    row.append(save);
    list.append(row);
  });
  document.querySelector('#song-count').textContent =
    `${selection.length} ${selection.length === 1 ? 'CANCIÓN EN ROTACIÓN' : 'CANCIONES EN ROTACIÓN'}`;
  document.querySelectorAll('.filter-button').forEach((button) => {
    const selected = button.dataset.filter === filter;
    button.classList.toggle('selected', selected);
    button.setAttribute('aria-pressed', String(selected));
  });
  if (savedCount) savedCount.textContent = String(savedSongIds.size);
  if (clearSearch) clearSearch.hidden = songQuery.length === 0;
  if (songEmpty) songEmpty.hidden = selection.length !== 0;
  updatePreviewUI();
}

document.querySelectorAll('.filter-button').forEach((button) => {
  button.addEventListener('click', () => renderSongs(button.dataset.filter));
});

songSearch?.addEventListener('input', () => {
  songQuery = songSearch.value;
  renderSongs();
});
clearSearch?.addEventListener('click', () => {
  songQuery = '';
  songSearch.value = '';
  renderSongs();
  songSearch.focus();
});
document.querySelector('#reset-songs')?.addEventListener('click', () => {
  songQuery = '';
  if (songSearch) songSearch.value = '';
  renderSongs('all');
  if (songSearch) songSearch.focus();
});
songList.addEventListener('click', (event) => {
  const button = event.target.closest('.save-song');
  if (!button || !songList.contains(button)) return;
  const previousButtons = [...songList.querySelectorAll('.save-song')];
  const previousIndex = previousButtons.indexOf(button);
  const id = button.dataset.songId;
  if (!knownSongIds.has(id)) return;
  if (savedSongIds.has(id)) savedSongIds.delete(id);
  else savedSongIds.add(id);
  persistSavedSongs();
  renderSongs();
  const buttons = [...songList.querySelectorAll('.save-song')];
  const nextFocus = buttons.find((candidate) => candidate.dataset.songId === id)
    || buttons[Math.min(previousIndex, buttons.length - 1)]
    || document.querySelector('.filter-button[data-filter="saved"]');
  nextFocus?.focus();
});
window.addEventListener('storage', (event) => {
  if (event.key !== savedSongsKey && event.key !== null) return;
  const focused = document.activeElement;
  const focusedRow = songList.contains(focused) ? focused.closest('.song-row') : null;
  const focusSelector = ['.listen-link', '.save-song', '.song-project', '.preview-toggle']
    .find((selector) => focused?.matches(selector));
  const previousIndex = focusedRow
    ? [...songList.querySelectorAll('.song-row')].indexOf(focusedRow)
    : -1;
  const focusedId = focusedRow?.dataset.songId;
  savedSongIds = parseSavedSongs(event.newValue);
  renderSongs();
  if (!focusedRow || !focusSelector) return;
  const rows = [...songList.querySelectorAll('.song-row')];
  const nextRow = rows.find((row) => row.dataset.songId === focusedId)
    || rows[Math.min(previousIndex, rows.length - 1)];
  const nextFocus = nextRow?.querySelector(focusSelector)
    || document.querySelector('.filter-button.selected');
  nextFocus?.focus();
});
renderSongs('all');

const comparisonBody = document.querySelector('#comparison-body');
comparisonBody.replaceChildren();
comparisons.forEach(([topic, carti, cochise]) => {
  const row = element('tr');
  const heading = element('th', '', topic);
  heading.scope = 'row';
  row.append(heading, element('td', '', carti), element('td', '', cochise));
  comparisonBody.append(row);
});

const sourceList = document.querySelector('#source-list');
sourceList.replaceChildren();
sourceList.append(
  element(
    'p',
    '',
    'Detrás de cada recorrido hay fechas, discos y colaboraciones que puedes seguir por tu cuenta. Aquí reúno los perfiles, las reseñas y los archivos que me sirven de punto de partida.',
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
    'Archivo independiente consultado el 12 de octubre de 2026. Cada puesto enlaza la semana correspondiente de las listas de Billboard.',
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
  'Los puestos del Hot 100 son una foto de una semana concreta. Las otras fichas te llevan al catálogo: esta selección está pensada para descubrir canciones, no para ordenar carreras por números.';
sourceList.append(scope);
const status = element('p', 'source-item research-status');
status.textContent =
  'El recorrido llega hasta los lanzamientos de 2026. En las fichas encontrarás más referencias para tirar del hilo; las notas de escucha son mi forma de entrar en la música.';
sourceList.append(status);

const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
const siteHeader = document.querySelector('.site-header');
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
document.addEventListener('focusin', (event) => {
  if (!siteHeader.contains(event.target)) closeMenu();
});
const mobileBreakpoint = window.matchMedia('(max-width: 900px)');
mobileBreakpoint.addEventListener('change', () => closeMenu());

const navLinks = [...navigation.querySelectorAll('.nav-link')];
const navSections = navLinks.map((link) => document.querySelector(link.hash));
let scheduled = false;
function updateNavigation() {
  let active = navSections[0];
  navSections.forEach((section) => {
    if (section.getBoundingClientRect().top <= 160) active = section;
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
