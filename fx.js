'use strict';

/*
 * Rapverse · interacciones.
 * Capa opcional: la página funciona igual sin este archivo. No modifica los
 * datos ni el estado de script.js y gallery.js; sólo añade respuesta visual.
 * Respeta prefers-reduced-motion y no hace peticiones de red.
 */
(() => {
  const reduceQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  const fineQuery = window.matchMedia('(hover: hover) and (pointer: fine)');
  const reduced = () => reduceQuery.matches;
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

  /* 1 · Barra de progreso: el "volumen" de la página. */
  const progress = document.createElement('div');
  progress.className = 'fx-progress';
  progress.setAttribute('aria-hidden', 'true');
  document.body.prepend(progress);

  function updateProgress() {
    const root = document.documentElement;
    const range = root.scrollHeight - root.clientHeight;
    const ratio = range > 0 ? clamp(window.scrollY / range, 0, 1) : 0;
    progress.style.transform = `scaleX(${ratio})`;
  }

  /* 2 · Marquesina: la velocidad responde al scroll y se invierte al subir. */
  const track = document.querySelector('.marquee > div');
  let rate = 1;
  let targetRate = 1;
  let lastY = window.scrollY;
  let lastTime = performance.now();
  let idleTimer = 0;
  let marqueeFrame = 0;

  function marqueeAnimation() {
    if (!track || typeof track.getAnimations !== 'function') return null;
    return track.getAnimations()[0] || null;
  }

  function stepMarquee() {
    marqueeFrame = 0;
    const animation = marqueeAnimation();
    if (!animation) return;
    rate += (targetRate - rate) * 0.12;
    if (Math.abs(targetRate - rate) < 0.01) rate = targetRate;
    animation.updatePlaybackRate(rate || 0.001);
    if (rate !== targetRate) marqueeFrame = requestAnimationFrame(stepMarquee);
  }

  function onScrollMarquee() {
    if (!track || reduced()) return;
    const now = performance.now();
    const distance = window.scrollY - lastY;
    const velocity = Math.abs(distance) / Math.max(now - lastTime, 16);
    if (distance !== 0) {
      const direction = distance > 0 ? 1 : -1;
      targetRate = direction * clamp(1 + velocity * 3.2, 1, 7);
    }
    lastY = window.scrollY;
    lastTime = now;
    clearTimeout(idleTimer);
    idleTimer = setTimeout(() => {
      targetRate = 1;
      if (!marqueeFrame) marqueeFrame = requestAnimationFrame(stepMarquee);
    }, 140);
    if (!marqueeFrame) marqueeFrame = requestAnimationFrame(stepMarquee);
  }

  let scrollScheduled = false;
  window.addEventListener(
    'scroll',
    () => {
      onScrollMarquee();
      if (scrollScheduled) return;
      scrollScheduled = true;
      requestAnimationFrame(() => {
        updateProgress();
        scrollScheduled = false;
      });
    },
    { passive: true },
  );
  window.addEventListener('resize', updateProgress);
  updateProgress();

  /* 3 · Luz de escenario: sigue al puntero en el póster, las fichas y la galería. */
  function trackLight(container, selector, tilt) {
    if (!container) return;
    let frame = 0;
    let pending = null;
    function apply() {
      frame = 0;
      if (!pending) return;
      const { target, x, y } = pending;
      pending = null;
      const rect = target.getBoundingClientRect();
      const px = clamp((x - rect.left) / rect.width, 0, 1);
      const py = clamp((y - rect.top) / rect.height, 0, 1);
      target.style.setProperty('--mx', `${(px * 100).toFixed(1)}%`);
      target.style.setProperty('--my', `${(py * 100).toFixed(1)}%`);
      if (tilt) {
        target.style.setProperty('--ry', `${((px - 0.5) * 9).toFixed(2)}deg`);
        target.style.setProperty('--rx', `${((0.5 - py) * 7).toFixed(2)}deg`);
      }
    }
    container.addEventListener('pointermove', (event) => {
      if (reduced() || !fineQuery.matches || event.pointerType === 'touch') return;
      const target = event.target.closest(selector);
      if (!target || !container.contains(target)) return;
      pending = { target, x: event.clientX, y: event.clientY };
      if (!frame) frame = requestAnimationFrame(apply);
    });
    if (tilt) {
      container.addEventListener('pointerleave', () => {
        container.style.setProperty('--rx', '0deg');
        container.style.setProperty('--ry', '0deg');
      });
    }
  }

  const heroArt = document.querySelector('.hero-art');
  trackLight(heroArt, '.hero-art', true);
  trackLight(document.querySelector('.artist-grid'), '.artist-visual', false);
  trackLight(document.querySelector('.photo-grid'), '.photo-link', false);

  /* 4 · Titulares en contorno: se "encienden" en rojo al entrar en pantalla. */
  const outlines = [...document.querySelectorAll('.outline')];
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-lit');
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.6 },
    );
    outlines.forEach((node) => observer.observe(node));
  } else {
    outlines.forEach((node) => node.classList.add('is-lit'));
  }

  /* 5 · Titular del hero: se "decodifica" una sola vez al cargar. */
  function decodeHeadline() {
    const heading = document.querySelector('.hero h1');
    if (!heading || reduced() || window.scrollY > 120) return;
    const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#%&';
    const nodes = [];
    const walker = document.createTreeWalker(heading, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      if (walker.currentNode.nodeValue.trim()) {
        nodes.push({ node: walker.currentNode, text: walker.currentNode.nodeValue });
      }
    }
    if (!nodes.length) return;
    const label = heading.textContent.replace(/\s+/g, ' ').trim();
    heading.setAttribute('aria-label', label);
    const total = nodes.reduce((sum, item) => sum + item.text.length, 0);
    const duration = 1100;
    const start = performance.now();

    function frame(now) {
      const progressValue = clamp((now - start) / duration, 0, 1);
      const revealed = Math.floor(progressValue * total * 1.15);
      let seen = 0;
      nodes.forEach((item) => {
        let output = '';
        for (const character of item.text) {
          const index = seen++;
          const isLetter = /[A-ZÁÉÍÓÚÑ0-9]/i.test(character);
          output += !isLetter || index < revealed
            ? character
            : letters[Math.floor(Math.random() * letters.length)];
        }
        item.node.nodeValue = output;
      });
      if (progressValue < 1) {
        requestAnimationFrame(frame);
      } else {
        nodes.forEach((item) => {
          item.node.nodeValue = item.text;
        });
        heading.removeAttribute('aria-label');
      }
    }
    requestAnimationFrame(frame);
  }
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(decodeHeadline, decodeHeadline);
  } else {
    decodeHeadline();
  }

  /* 6 · Confirmación al guardar: ráfaga de partículas desde el corazón. */
  document.addEventListener(
    'click',
    (event) => {
      const button = event.target.closest?.('.save-song');
      if (!button || reduced() || button.getAttribute('aria-pressed') === 'true') return;
      const rect = button.getBoundingClientRect();
      const burst = document.createElement('div');
      burst.className = 'fx-burst';
      burst.setAttribute('aria-hidden', 'true');
      burst.style.left = `${rect.left + rect.width / 2}px`;
      burst.style.top = `${rect.top + rect.height / 2}px`;
      const pieces = 16;
      for (let index = 0; index < pieces; index += 1) {
        const piece = document.createElement('i');
        const angle = (Math.PI * 2 * index) / pieces + Math.random() * 0.4;
        const distance = 34 + Math.random() * 48;
        piece.style.setProperty('--dx', `${Math.cos(angle) * distance}px`);
        piece.style.setProperty('--dy', `${Math.sin(angle) * distance}px`);
        piece.style.setProperty('--rot', `${Math.round(Math.random() * 360)}deg`);
        burst.append(piece);
      }
      document.body.append(burst);
      setTimeout(() => burst.remove(), 900);
    },
    true,
  );
})();
