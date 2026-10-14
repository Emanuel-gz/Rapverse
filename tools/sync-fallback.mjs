#!/usr/bin/env node

// Optional authoring helper. The published site does not need Node or a build.
import { readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { runInNewContext } from 'node:vm';

const root = resolve(import.meta.dirname ?? dirname(fileURLToPath(import.meta.url)), '..');
const htmlPath = resolve(root, 'index.html');
const scriptPath = resolve(root, 'script.js');

function escapeHtml(value) {
  const entities = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' };
  return String(value).replace(/[&<>"]/g, (character) => entities[character]);
}

function externalLink(url, text, className = '', ariaLabel = '') {
  const classes = className ? ` class="${escapeHtml(className)}"` : '';
  const label = ariaLabel ? ` aria-label="${escapeHtml(ariaLabel)}"` : '';
  return `<a${classes} href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer"${label}>${escapeHtml(text)}</a>`;
}

function readData(script) {
  const boundary = script.indexOf('function element(');
  if (boundary === -1) {
    throw new Error('No se encuentra el inicio del renderizado: function element(.');
  }
  // Evaluate only this repository's data declarations, without any browser code.
  const declarations = script.slice(0, boundary).replace(
    /^[\t ]*document\.documentElement\.classList\.add\(['"]js['"]\);[\t ]*\r?$/m,
    '',
  );
  return runInNewContext(
    `${declarations}\n({ artistContent, songs, comparisons, chartBase, appleCarti, appleCochise, pitchforkCarti, pitchforkFreshmen });`,
    Object.create(null),
    { filename: scriptPath, timeout: 1000 },
  );
}

function renderArtist(content) {
  const paragraphs = content.paragraphs.map((text) => `<p>${escapeHtml(text)}</p>`).join('');
  const sources = (content.sources ?? []).map(({ label, url }) => externalLink(
    url,
    `${label} ↗`,
    'inline-source',
    `${label}, abrir fuente en nueva pestaña`,
  )).join('');
  return `<span class="content-kind ${escapeHtml(content.kind)}">${escapeHtml(content.label)}</span>`
    + `<h4>${escapeHtml(content.title)}</h4>${paragraphs}`
    + (sources ? `<details class="artist-sources source-disclosures"><summary>Créditos de este lado</summary><div class="source-links">${sources}</div></details>` : '');
}

function renderSongs(songs, chartBase) {
  return songs.map((song, index) => {
    const chartUrl = song.chart ? `${chartBase}${song.chart}.json` : song.catalog;
    const chartText = song.chart ? `HOT 100 · #${song.position}` : (song.catalogLabel || 'EN LA SELECCIÓN');
    const chartLabel = song.chart
      ? `${song.title}: puesto ${song.position} en la lista del ${song.chart}, consultar fuente en nueva pestaña`
      : song.catalogLabel
        ? `${song.title}: catálogo de Playboi Carti, consultar fuente en nueva pestaña`
        : `${song.title}: consultar ficha de catálogo en nueva pestaña`;
    const query = encodeURIComponent(`${song.title} ${song.credit}`);
    const listenLabel = `Buscar ${song.title}, ${song.credit}, en Spotify (nueva pestaña)`;
    return '<article class="song-row">'
      + `<span class="song-index">${escapeHtml(String(index + 1).padStart(2, '0'))}</span>`
      + `<div class="song-art ${escapeHtml(song.artist)}" aria-hidden="true"><img class="song-cover" src="${escapeHtml(song.cover)}" alt="" width="76" height="76" /></div>`
      + `<div class="song-info"><h3 class="song-title">${escapeHtml(song.title)}</h3>`
      + `<p class="song-credit">${escapeHtml(song.credit)}</p>`
      + `<a class="listen-link" href="${escapeHtml(`https://open.spotify.com/search/${query}`)}" target="_blank" rel="noopener noreferrer" aria-label="${escapeHtml(listenLabel)}">`
      + '<span>Spotify</span><span class="play-icon" aria-hidden="true">↗</span></a></div>'
      + externalLink(chartUrl, chartText, 'song-project', chartLabel)
      + `<span class="song-year">${escapeHtml(song.year)}</span>`
      + `<audio class="native-preview" controls preload="none" src="${escapeHtml(song.audio)}" aria-label="Fragmento de ${escapeHtml(song.title)}, ${escapeHtml(song.credit)}"></audio>`
      + '</article>';
  }).join('');
}

function renderComparisons(comparisons) {
  return comparisons.map(([topic, carti, cochise]) => '<tr>'
    + `<th scope="row">${escapeHtml(topic)}</th>`
    + `<td>${escapeHtml(carti)}</td><td>${escapeHtml(cochise)}</td></tr>`).join('');
}

function renderSources({ appleCarti, appleCochise, pitchforkCarti, pitchforkFreshmen }) {
  const overview = 'Detrás de cada recorrido hay fechas, discos y colaboraciones que puedes seguir por tu cuenta. Aquí reúno los perfiles, las reseñas y los archivos que me sirven de punto de partida.';
  const archiveNote = 'Archivo independiente consultado el 12 de octubre de 2026. Cada puesto enlaza la semana correspondiente de las listas de Billboard.';
  const scope = 'Los puestos del Hot 100 son una foto de una semana concreta. Las otras fichas te llevan al catálogo: esta selección está pensada para descubrir canciones, no para ordenar carreras por números.';
  const status = 'El recorrido llega hasta los lanzamientos de 2026. En las fichas encontrarás más referencias para tirar del hilo; las notas de escucha son mi forma de entrar en la música.';
  const links = [
    ['02 / Apple Music · Playboi Carti ↗', appleCarti],
    ['03 / Apple Music · Cochise ↗', appleCochise],
    ['04 / Pitchfork · Playboi Carti ↗', pitchforkCarti],
    ['05 / Pitchfork · XXL Freshmen 2022 ↗', pitchforkFreshmen],
  ];
  return `<p>${escapeHtml(overview)}</p><div class="source-item">`
    + externalLink('https://github.com/mhollingshead/billboard-hot-100', '01 / Archivo independiente del Billboard Hot 100 ↗')
    + `<small>${escapeHtml(archiveNote)}</small></div>`
    + links.map(([label, url]) => `<div class="source-item">${externalLink(url, label)}</div>`).join('')
    + `<p class="source-item">${escapeHtml(scope)}</p>`
    + `<p class="source-item research-status">${escapeHtml(status)}</p>`;
}

function replaceFallback(html, name, content) {
  const start = `<!-- fallback:${name}:start -->`;
  const end = `<!-- fallback:${name}:end -->`;
  const startIndex = html.indexOf(start);
  const endIndex = html.indexOf(end);
  if (startIndex === -1 || endIndex === -1) {
    throw new Error(`Faltan los marcadores fallback:${name}:start / fallback:${name}:end en index.html.`);
  }
  if (html.indexOf(start, startIndex + start.length) !== -1
      || html.indexOf(end, endIndex + end.length) !== -1
      || endIndex < startIndex + start.length) {
    throw new Error(`Los marcadores fallback:${name} están duplicados o desordenados en index.html.`);
  }
  return html.slice(0, startIndex + start.length) + content + html.slice(endIndex);
}

function updateSongCount(html, count) {
  // Read whole quoted attributes so text inside another attribute cannot match id.
  const tags = /<!--[\s\S]*?-->|<([a-z][\w:-]*)\b((?:[^>"']|"[^"]*"|'[^']*')*)>/gi;
  const attributes = /(?:^|\s)([^\s"'<>/=]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?/g;
  const matches = [];
  let tag;
  while ((tag = tags.exec(html))) {
    if (!tag[1]) continue; // Comments may contain example markup.
    const id = [...tag[2].matchAll(attributes)].find((attribute) => attribute[1].toLowerCase() === 'id');
    if (id && (id[2] ?? id[3] ?? id[4]) === 'song-count') matches.push(tag);
    if (['script', 'style', 'textarea', 'title'].includes(tag[1].toLowerCase())) {
      const closing = new RegExp(`</${tag[1]}\\s*>`, 'gi');
      closing.lastIndex = tags.lastIndex;
      const end = closing.exec(html);
      tags.lastIndex = end ? closing.lastIndex : html.length;
    }
  }
  if (matches.length !== 1) {
    throw new Error('Se necesita un único elemento #song-count con contenido de texto en index.html.');
  }
  const opening = matches[0];
  const textStart = opening.index + opening[0].length;
  const contents = html.slice(textStart).match(new RegExp(`^([^<]*)(</${opening[1]}\\s*>)`, 'i'));
  if (!contents) throw new Error('#song-count debe contener solamente texto en index.html.');
  const text = `${count} ${count === 1 ? 'CANCIÓN EN ROTACIÓN' : 'CANCIONES EN ROTACIÓN'}`;
  return html.slice(0, textStart) + escapeHtml(text) + html.slice(textStart + contents[1].length);
}

async function main() {
  const [script, originalHtml] = await Promise.all([
    readFile(scriptPath, 'utf8'),
    readFile(htmlPath, 'utf8'),
  ]);
  const data = readData(script);
  const sections = [
    ['carti-panel', renderArtist(data.artistContent.carti.history)],
    ['cochise-panel', renderArtist(data.artistContent.cochise.history)],
    ['songs', renderSongs(data.songs, data.chartBase)],
    ['comparison-body', renderComparisons(data.comparisons)],
    ['source-list', renderSources(data)],
  ];
  let html = originalHtml;
  for (const [name, content] of sections) html = replaceFallback(html, name, content);
  html = updateSongCount(html, data.songs.length);
  // Validate every section before writing; never regenerate the surrounding page.
  if (html !== originalHtml) await writeFile(htmlPath, html, 'utf8');
  console.log(`Fallback sincronizado: ${data.songs.length} canciones, ${data.comparisons.length} filas comparativas.`);
}

main().catch((error) => {
  console.error(`sync-fallback: ${error.message}`);
  process.exitCode = 1;
});
