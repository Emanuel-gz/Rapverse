"""Functional browser checks. Run: python3 tests/smoke.py -v.

Uses the environment's Playwright and Chromium; application has no dependencies.
"""
from functools import partial
from http.server import ThreadingHTTPServer
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import threading
import unittest
from urllib.parse import unquote, urljoin, urlparse

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SAVED_SONGS_KEY = 'rapverse:saved-songs'
MUSIC_MANIFEST = json.loads((ROOT / 'assets/music/manifest.json').read_text())
MUSIC_TRACKS = MUSIC_MANIFEST['tracks']
SERVER_SPEC = spec_from_file_location('rapverse_serve', ROOT / 'tools/serve.py')
SERVER_MODULE = module_from_spec(SERVER_SPEC)
SERVER_SPEC.loader.exec_module(SERVER_MODULE)
HERO_HEADLINE = 'DOS VOCES. NINGÚN MOLDE.'
NARRATIVE_ATTRIBUTION = re.compile(
    r'\b(?:Apple\s+Music|Pitchfork|Billboard)\s+(?:(?:nos|también|lo)\s+)?'
    r'(?:dice|dicen|cuenta|describe|sitúa|menciona|explica|destaca|documenta|habla|'
    r'señala|informa|informó|presenta|afirma|recoge|atribuye|llama)\b'
    r'|\bsegún\b[^.!?;\n]{0,90}\b(?:Apple\s+Music|Pitchfork|Billboard)\b',
    re.IGNORECASE,
)


class QuietHandler(SERVER_MODULE.RangeRequestHandler):
    def log_message(self, *_args):
        pass


class RapverseBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(
            ('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT))
        )
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}'
        cls.playwright = sync_playwright().start()
        executable = os.environ.get('RAPVERSE_BROWSER_PATH') or shutil.which('chromium')
        options = {'headless': True, 'args': ['--no-sandbox']}
        if executable:
            options['executable_path'] = executable
        cls.browser = cls.playwright.chromium.launch(**options)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.context = self.browser.new_context(viewport={'width': 1440, 'height': 1000})
        self.page = self.context.new_page()
        self.errors = []
        self.failed_resources = []
        self.expected_failed_resources = set()
        self.requests = []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))
        self.page.on('response', lambda response: self.failed_resources.append(
            response.url) if response.status >= 400
            and response.url not in self.expected_failed_resources else None)
        self.page.on('request', lambda request: self.requests.append(request.url))
        self.page.goto(self.url, wait_until='networkidle')
        self.page.evaluate('document.fonts.ready')

    def tearDown(self):
        self.assertEqual(self.errors, [], 'JavaScript errors')
        self.assertEqual(self.failed_resources, [], 'Failed local resources')
        self.context.close()

    def song_row(self, title):
        return self.page.locator('.song-row').filter(
            has=self.page.get_by_role('heading', name=title, exact=True))

    def wait_for_playback(self, source=None):
        self.page.wait_for_function('''(source) => {
            const audio = document.querySelector('#preview-audio');
            return !audio.paused && audio.currentTime > 0.05 && audio.readyState >= 2
                && (!source || new URL(audio.currentSrc).pathname === '/' + source);
        }''', arg=source, timeout=15000)

    def assert_direct_editorial_voice(self, page):
        for text in page.locator('main p, main h4, #comparison-body td').all_text_contents():
            self.assertIsNone(NARRATIVE_ATTRIBUTION.search(text),
                              f'Narrative still attributes its voice to a publisher: {text}')

    def test_song_assets_match_verified_archive_manifest(self):
        self.assertEqual(len(MUSIC_TRACKS), 9)
        self.assertEqual(len({track['id'] for track in MUSIC_TRACKS}), 9)
        rendered = self.page.evaluate('''songs.map(song => ({
            title: song.title, credit: song.credit, cover: song.cover, audio: song.audio
        }))''')
        self.assertEqual(len(rendered), 9)
        self.assertEqual({song['title'] for song in rendered},
                         {track['title'] for track in MUSIC_TRACKS})
        for track in MUSIC_TRACKS:
            with self.subTest(song=track['title']):
                song = next(song for song in rendered if song['title'] == track['title'])
                self.assertEqual(song['credit'], track['artist'])
                row = self.song_row(track['title'])
                expect(row).to_have_count(1)
                expect(row.locator('.song-credit')).to_have_text(track['artist'])
                cover = row.locator('.song-art img.song-cover')
                expect(cover).to_have_count(1)
                self.assertEqual(cover.get_attribute('src'), track['cover'])
                cover.scroll_into_view_if_needed()
                self.page.wait_for_function(
                    '(image) => image.complete && image.naturalWidth > 0',
                    arg=cover.element_handle(), timeout=10000)
                for resource in ('cover', 'audio'):
                    self.assertEqual(song[resource], track[resource])
                    path = ROOT / track[resource]
                    self.assertTrue(path.is_file(), f'Missing {resource}: {path}')
                    self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                                     track[f'{resource}Sha256'])
                expect(row.locator('.preview-toggle')).to_have_attribute(
                    'data-song-id', row.get_attribute('data-song-id'))

    def test_every_preview_really_plays_and_pauses_with_correct_artwork(self):
        audio = self.page.locator('#preview-audio')
        self.assertEqual(self.page.locator('audio').count(), 1)
        for track in MUSIC_TRACKS:
            with self.subTest(song=track['title']):
                row = self.song_row(track['title'])
                toggle = row.locator('.preview-toggle')
                toggle.click()
                self.wait_for_playback(track['audio'])
                expect(row).to_have_class(re.compile(r'\bis-playing\b'))
                expect(row.locator('.song-art')).to_have_css('animation-play-state', 'running')
                expect(toggle).to_have_attribute('aria-pressed', 'true')
                expect(self.page.locator('#preview-toggle')).to_have_attribute('aria-pressed', 'true')
                expect(self.page.locator('#now-title')).to_have_text(track['title'])
                expect(self.page.locator('#now-credit')).to_have_text(track['artist'])
                expect(self.page.locator('#now-cover')).to_have_attribute('src', track['cover'])
                self.assertAlmostEqual(audio.evaluate('(audio) => audio.duration'),
                                       track['durationSeconds'], delta=0.5)
                self.assertEqual(self.page.locator('.song-row.is-playing').count(), 1)
                toggle.click()
                self.assertTrue(audio.evaluate('(audio) => audio.paused'))
                expect(toggle).to_have_attribute('aria-pressed', 'false')
                expect(self.page.locator('.song-row.is-playing')).to_have_count(0)
                expect(row.locator('.song-art')).to_have_css('animation-play-state', 'paused')

    def test_preview_switching_uses_one_audio_and_replaces_track(self):
        first = self.song_row('Magnolia')
        second = self.song_row('Location')
        first.locator('.preview-toggle').click()
        self.wait_for_playback('assets/music/magnolia.mp3')
        second.locator('.preview-toggle').click()
        self.wait_for_playback('assets/music/location.mp3')
        self.assertEqual(self.page.locator('audio').count(), 1)
        expect(first.locator('.preview-toggle')).to_have_attribute('aria-pressed', 'false')
        expect(second.locator('.preview-toggle')).to_have_attribute('aria-pressed', 'true')
        expect(self.page.locator('.song-row.is-playing')).to_have_count(1)
        self.assertLess(self.page.locator('#preview-audio').evaluate('(audio) => audio.currentTime'), 5)
        self.page.locator('#preview-stop').click()
        self.assertTrue(self.page.locator('#preview-audio').evaluate('(audio) => audio.paused'))
        self.assertEqual(self.page.locator('#preview-audio').evaluate('(audio) => audio.currentTime'), 0)
        expect(self.page.locator('.song-row.is-playing')).to_have_count(0)

    def test_preview_controls_seek_volume_mute_and_keyboard(self):
        self.song_row('Location').locator('.preview-toggle').focus()
        self.page.keyboard.press('Enter')
        self.wait_for_playback('assets/music/location.mp3')
        toggle = self.page.locator('#preview-toggle')
        toggle.focus()
        self.page.keyboard.press('Space')
        self.assertTrue(self.page.locator('#preview-audio').evaluate('(audio) => audio.paused'))
        seek = self.page.locator('#preview-seek')
        seek.evaluate('''(input) => {
            input.value = '8';
            input.dispatchEvent(new Event('input', {bubbles: true}));
        }''')
        self.assertAlmostEqual(self.page.locator('#preview-audio').evaluate(
            '(audio) => audio.currentTime'), 8, delta=0.3)
        self.assertIn('0:08', self.page.locator('#preview-current').inner_text())
        self.assertNotEqual(self.page.locator('#preview-duration').inner_text(), '0:00')
        self.assertTrue(seek.get_attribute('aria-valuetext'))
        seek.focus()
        self.page.keyboard.press('ArrowRight')
        self.assertGreater(self.page.locator('#preview-audio').evaluate('(audio) => audio.currentTime'), 8)
        volume = self.page.locator('#preview-volume')
        volume.evaluate('''(input) => {
            input.value = '0.35';
            input.dispatchEvent(new Event('input', {bubbles: true}));
        }''')
        self.assertAlmostEqual(self.page.locator('#preview-audio').evaluate('(audio) => audio.volume'), .35)
        mute = self.page.locator('#preview-mute')
        mute.click()
        self.assertTrue(self.page.locator('#preview-audio').evaluate('(audio) => audio.muted'))
        expect(mute).to_have_attribute('aria-pressed', 'true')
        mute.click()
        self.assertFalse(self.page.locator('#preview-audio').evaluate('(audio) => audio.muted'))
        expect(mute).to_have_attribute('aria-pressed', 'false')
        toggle.focus()
        self.page.keyboard.press('Enter')
        self.wait_for_playback('assets/music/location.mp3')
        self.assertGreater(self.page.locator('#preview-audio').evaluate('(audio) => audio.currentTime'), 8)

    def test_preview_survives_filters_search_and_saving(self):
        self.song_row('Magnolia').locator('.preview-toggle').click()
        self.wait_for_playback('assets/music/magnolia.mp3')
        audio = self.page.locator('#preview-audio')
        initial_time = audio.evaluate('(audio) => audio.currentTime')
        self.page.locator('.song-filters [data-filter="cochise"]').click()
        expect(self.song_row('Magnolia')).to_have_count(0)
        expect(self.page.locator('#now-title')).to_have_text('Magnolia')
        self.wait_for_playback('assets/music/magnolia.mp3')
        self.page.locator('#song-search').fill('Hatchback')
        self.song_row('Hatchback').locator('.save-song').click()
        self.wait_for_playback('assets/music/magnolia.mp3')
        self.assertGreaterEqual(audio.evaluate('(audio) => audio.currentTime'), initial_time)
        self.page.locator('#preview-toggle').click()
        self.assertTrue(audio.evaluate('(audio) => audio.paused'))
        self.page.locator('#preview-toggle').click()
        self.wait_for_playback('assets/music/magnolia.mp3')
        self.page.locator('#clear-search').click()
        self.page.locator('.song-filters [data-filter="all"]').click()
        magnolia = self.song_row('Magnolia')
        expect(magnolia.locator('.preview-toggle')).to_have_attribute('aria-pressed', 'true')
        magnolia.locator('.save-song').click()
        self.wait_for_playback('assets/music/magnolia.mp3')
        expect(magnolia.locator('.preview-toggle')).to_have_attribute('aria-pressed', 'true')

    def test_preview_error_is_announced_and_can_retry(self):
        resource_url = f'{self.url}/assets/music/magnolia.mp3'
        self.expected_failed_resources.add(resource_url)
        self.page.route(resource_url, lambda route: route.fulfill(status=404, body='Missing test preview'))
        toggle = self.song_row('Magnolia').locator('.preview-toggle')
        toggle.click()
        expect(self.page.locator('#preview-status')).to_contain_text('No se pudo reproducir')
        expect(self.page.locator('#preview-status')).to_have_attribute('role', 'status')
        self.assertTrue(self.page.locator('#preview-audio').evaluate('(audio) => audio.paused'))
        expect(toggle).to_have_attribute('aria-pressed', 'false')
        expect(self.page.locator('.song-row.is-playing')).to_have_count(0)
        self.page.unroute(resource_url)
        self.page.locator('#preview-toggle').click()
        self.wait_for_playback('assets/music/magnolia.mp3')
        expect(toggle).to_have_attribute('aria-pressed', 'true')

    def test_preview_waits_for_real_playback_before_spinning(self):
        resource_url = f'{self.url}/assets/music/location.mp3'
        pending = []
        self.page.route(resource_url, lambda route: pending.append(route))
        row = self.song_row('Location')
        toggle = row.locator('.preview-toggle')
        try:
            toggle.click()
            expect(toggle).to_have_attribute('aria-busy', 'true')
            expect(toggle).to_have_attribute('aria-pressed', 'false')
            expect(self.page.locator('#preview-status')).to_contain_text('Cargando')
            expect(self.page.locator('.song-row.is-playing')).to_have_count(0)
            expect(row.locator('.song-art')).to_have_css('animation-play-state', 'paused')
            initial_transform = row.locator('.song-art').evaluate('(art) => getComputedStyle(art).transform')
            self.assertTrue(pending, 'The audio request must actually be pending')
            pending.pop().continue_()
            self.wait_for_playback('assets/music/location.mp3')
            expect(toggle).to_have_attribute('aria-busy', 'false')
            expect(toggle).to_have_attribute('aria-pressed', 'true')
            self.page.wait_for_function('''([art, initial]) =>
                getComputedStyle(art).transform !== initial''',
                arg=[row.locator('.song-art').element_handle(), initial_transform])
        finally:
            for route in pending:
                route.continue_()
            self.page.unroute(resource_url)

    def test_preview_ends_resets_and_can_replay(self):
        self.song_row('POCKET ROCKET').locator('.preview-toggle').click()
        self.wait_for_playback('assets/music/pocket-rocket.mp3')
        self.page.locator('#preview-audio').evaluate('(audio) => { audio.currentTime = audio.duration - 0.15; }')
        self.page.wait_for_function('''() => {
            const audio = document.querySelector('#preview-audio');
            return audio.paused && audio.currentTime === 0;
        }''', timeout=5000)
        expect(self.page.locator('.song-row.is-playing')).to_have_count(0)
        expect(self.page.locator('#preview-toggle')).to_have_attribute('aria-pressed', 'false')
        expect(self.page.locator('#preview-status')).to_contain_text('finalizado')
        expect(self.page.locator('#preview-current')).to_have_text('0:00')
        self.page.locator('#preview-toggle').click()
        self.wait_for_playback('assets/music/pocket-rocket.mp3')

    def test_local_resources_and_document(self):
        self.assertEqual(self.page.locator('html').get_attribute('lang'), 'es')
        self.assertEqual(self.page.locator('h1').count(), 1)
        self.assertEqual(self.page.locator('.artist-card').count(), 2)
        self.assertEqual(self.page.locator('.song-row').count(), 9)
        self.assertTrue(self.page.evaluate("document.fonts.check('16px Anton')"))
        self.assertTrue(self.page.evaluate("document.fonts.check('16px \"Space Grotesk\"')"))
        self.assertTrue(all(url.startswith(self.url) for url in self.requests))
        self.assertEqual(self.page.locator('audio').count(), 1)
        self.assertEqual(self.page.locator('#preview-audio').count(), 1)
        self.assertEqual(self.page.locator('video, iframe').count(), 0)
        self.assertTrue(self.page.locator('#preview-audio').evaluate('(audio) => audio.paused'))
        expect(self.page.locator(
            '#source-list a[href="https://github.com/mhollingshead/billboard-hot-100"]'
        )).to_have_count(1)

    def test_artist_tabs_and_keyboard(self):
        for name in ('carti', 'cochise'):
            card = self.page.locator(f'.artist-card[data-artist="{name}"]')
            history = card.locator(f'#{name}-history-tab')
            history.focus()
            self.page.keyboard.press('ArrowRight')
            evolution = card.locator(f'#{name}-evolution-tab')
            self.assertEqual(evolution.get_attribute('aria-selected'), 'true')
            self.assertEqual(self.page.locator(f'#{name}-panel').get_attribute(
                'aria-labelledby'), f'{name}-evolution-tab')
            self.page.keyboard.press('End')
            self.assertEqual(card.locator(f'#{name}-influences-tab').get_attribute(
                'aria-selected'), 'true')
            expect(card.get_by_role('tabpanel').locator('h4')).to_have_count(1)
            self.assertGreater(card.locator('.artist-sources a').count(), 0)
            self.page.keyboard.press('ArrowRight')
            self.assertEqual(history.get_attribute('aria-selected'), 'true')
            self.page.keyboard.press('ArrowLeft')
            self.assertEqual(card.locator(f'#{name}-influences-tab').get_attribute(
                'aria-selected'), 'true')
            card.locator(f'#{name}-style-tab').click()
            self.assertEqual(card.get_by_role('tabpanel').get_attribute(
                'aria-labelledby'), f'{name}-style-tab')
            self.page.keyboard.press('Home')
            self.assertEqual(card.locator('[tabindex="0"][role="tab"]').count(), 1)
            self.assertEqual(history.get_attribute('aria-selected'), 'true')

    def test_artist_editorials_have_substance_sources_and_distinct_perspectives(self):
        # Protect the facts and reading experience without freezing whole paragraphs.
        important_facts = {
            ('carti', 'history'): ('Jordan Carter', 'Atlanta', '2015', '2017', 'Lil Uzi Vert'),
            ('carti', 'evolution'): ('Die Lit', '2018', 'Whole Lotta Red', '2020', 'MUSIC', '2025'),
            ('cochise', 'history'): ('Palm Bay', 'Columbia', '2020', 'Tell Em', '$NOT', '2022'),
            ('cochise', 'influences'): ('The Warriors', '1979', 'videojuego'),
        }
        headings = set()
        stories = set()
        for artist in ('carti', 'cochise'):
            card = self.page.locator(f'.artist-card[data-artist="{artist}"]')
            for view in ('history', 'evolution', 'style', 'influences'):
                with self.subTest(artist=artist, view=view):
                    tab = card.locator(f'#{artist}-{view}-tab')
                    self.assertTrue(tab.inner_text().strip())
                    tab.click()
                    panel = card.get_by_role('tabpanel')
                    heading = panel.locator('h4').inner_text().strip()
                    self.assertGreaterEqual(len(heading.split()), 3)
                    paragraphs = panel.locator(':scope > p').all_text_contents()
                    self.assertGreaterEqual(len(paragraphs), 2)
                    story = ' '.join(paragraphs)
                    self.assertGreaterEqual(len(story.split()), 65)
                    self.assertIsNone(NARRATIVE_ATTRIBUTION.search(story))
                    for fact in important_facts.get((artist, view), ()):
                        self.assertIn(fact, story)
                    if (artist, view) == ('cochise', 'history'):
                        self.assertRegex(story, r'\b(?:2021|al año siguiente)\b')
                    headings.add(heading)
                    stories.add(story)
                    credits = panel.locator('details.artist-sources')
                    expect(credits).to_have_count(1)
                    expect(credits.locator('a')).not_to_have_count(0)
                    credits.locator('summary').click()
                    expect(credits).to_have_attribute('open', '')
                    for link in credits.locator('a').all():
                        expect(link).to_be_visible()
                        self.assertGreater(len(link.inner_text().strip()), 5)
                        self.assertTrue(link.get_attribute('href').startswith('https://'))
                        self.assertEqual(link.get_attribute('target'), '_blank')
                        self.assertIn('noopener', link.get_attribute('rel'))
        self.assertEqual(len(headings), 8)
        self.assertEqual(len(stories), 8)
        expect(self.page.locator('#comparison-body th')).to_have_text(
            ['El recorrido', 'La voz', 'Las raíces', 'La energía'])
        self.assert_direct_editorial_voice(self.page)

    def test_filters_and_track_credits(self):
        filters = self.page.get_by_role('group', name='Filtrar canciones por artista')
        filters.get_by_role('button', name='Cochise', exact=True).click()
        self.assertEqual(self.page.locator('.song-row').count(), 4)
        self.assertIn('Cochise & $NOT', self.page.locator('.song-credit').all_inner_texts())
        self.assertIn('4 CANCIONES EN ROTACIÓN', self.page.locator('#song-count').inner_text())
        filters.get_by_role('button', name='Playboi Carti', exact=True).click()
        self.assertEqual(self.page.locator('.song-row').count(), 5)
        self.assertIn('Travis Scott', self.page.locator(
            '.song-row[data-song-id="carti:fe!n"] .song-credit').inner_text())
        location = self.page.locator('.song-row[data-song-id="carti:location"]')
        self.assertEqual(location.locator('.song-credit').inner_text(), 'Playboi Carti')
        self.assertEqual(location.locator('.song-project').inner_text(), 'PLAYBOI CARTI · 2017')
        self.assertNotIn('Top Songs', location.locator('.song-project').get_attribute('aria-label'))
        filters.get_by_role('button', name='Todos').click()
        self.assertEqual(self.page.locator('.song-row').count(), 9)
        self.assertEqual(self.page.locator('.song-project[href^="https://music.apple.com/"]').count(), 5)
        self.assertEqual(self.page.locator('.song-project[href^="https://github.com/"]').count(), 4)
        self.assertEqual(self.page.locator('.filter-button[aria-pressed="true"]').count(), 1)
        for link in self.page.locator('.listen-link').all():
            self.assertTrue(link.get_attribute('href').startswith('https://open.spotify.com/search/'))
            self.assertEqual(link.get_attribute('target'), '_blank')
            self.assertIn('noopener', link.get_attribute('rel'))
            self.assertIn('nueva pestaña', link.get_attribute('aria-label'))

    def test_song_search_combines_with_artist_filter(self):
        search = self.page.locator('#song-search')
        self.page.locator('.song-filters [data-filter="cochise"]').click()
        search.fill('  rOcKeT  ')
        expect(self.page.locator('.song-title')).to_have_text(['POCKET ROCKET'])
        self.assertIn('1 CANCIÓN EN ROTACIÓN', self.page.locator('#song-count').inner_text())
        self.page.locator('.song-filters [data-filter="carti"]').click()
        expect(self.page.locator('.song-row')).to_have_count(0)
        expect(self.page.locator('#song-empty')).to_be_visible()
        self.page.locator('.song-filters [data-filter="all"]').click()
        expect(self.page.locator('.song-title')).to_have_text(['POCKET ROCKET'])
        self.page.locator('#clear-search').click()
        expect(search).to_have_value('')
        expect(self.page.locator('.song-row')).to_have_count(9)
        search.fill('lil uzi')
        expect(self.page.locator('.song-title')).to_have_text(['Shoota'])
        self.page.locator('#clear-search').click()
        self.page.locator('.song-filters [data-filter="cochise"]').click()
        search.fill('hatchback')
        self.page.locator('#clear-search').click()
        expect(self.page.locator('.song-row')).to_have_count(4)
        expect(self.page.locator('.song-filters [data-filter="cochise"]')).to_have_attribute(
            'aria-pressed', 'true')

    def test_empty_song_results_and_reset(self):
        self.page.locator('.song-filters [data-filter="cochise"]').click()
        self.page.locator('#song-search').fill('Magnolia')
        expect(self.page.locator('.song-row')).to_have_count(0)
        expect(self.page.locator('#song-empty')).to_be_visible()
        self.assertIn('0 CANCIONES EN ROTACIÓN', self.page.locator('#song-count').inner_text())
        self.page.locator('#reset-songs').click()
        expect(self.page.locator('#song-search')).to_have_value('')
        expect(self.page.locator('.song-filters [data-filter="all"]')).to_have_attribute(
            'aria-pressed', 'true')
        expect(self.page.locator('.song-row')).to_have_count(9)
        expect(self.page.locator('#song-empty')).not_to_be_visible()

    def test_saved_songs_persist_and_update_saved_filter(self):
        magnolia = self.page.locator('.song-row[data-song-id="carti:magnolia"]')
        expect(self.page.locator('#saved-count')).to_have_text('0')
        magnolia.locator('.save-song').click()
        expect(magnolia.locator('.save-song')).to_have_attribute('aria-pressed', 'true')
        expect(magnolia.locator('.save-song')).to_be_focused()
        expect(self.page.locator('#saved-count')).to_have_text('1')
        self.page.locator('.song-filters [data-filter="saved"]').click()
        expect(self.page.locator('.song-title')).to_have_text(['Magnolia'])
        self.page.reload(wait_until='networkidle')
        expect(self.page.locator('#saved-count')).to_have_text('1')
        self.page.locator('.song-filters [data-filter="saved"]').click()
        expect(self.page.locator('.song-title')).to_have_text(['Magnolia'])
        expect(magnolia.locator('.save-song')).to_have_attribute('aria-pressed', 'true')
        self.page.locator('#song-search').fill('Hatchback')
        expect(self.page.locator('#song-empty')).to_be_visible()
        self.page.locator('#clear-search').click()
        expect(self.page.locator('.song-title')).to_have_text(['Magnolia'])
        magnolia.locator('.save-song').click()
        expect(self.page.locator('.song-row')).to_have_count(0)
        expect(self.page.locator('#song-empty')).to_be_visible()
        expect(self.page.locator('#saved-count')).to_have_text('0')
        expect(self.page.locator('.song-filters [data-filter="saved"]')).to_be_focused()
        self.page.reload(wait_until='networkidle')
        expect(self.page.locator('#saved-count')).to_have_text('0')

    def test_saved_songs_sync_between_tabs_without_losing_focus(self):
        other = self.page.context.new_page()
        other.on('pageerror', lambda error: self.errors.append(str(error)))
        other.on('response', lambda response: self.failed_resources.append(
            response.url) if response.status >= 400 else None)
        try:
            other.goto(self.url, wait_until='networkidle')
            magnolia = self.page.locator('.song-row[data-song-id="carti:magnolia"]')
            magnolia.locator('.listen-link').focus()
            other.locator('.song-row[data-song-id="carti:magnolia"] .save-song').click()
            expect(self.page.locator('#saved-count')).to_have_text('1')
            expect(magnolia.locator('.listen-link')).to_be_focused()

            magnolia.locator('.save-song').focus()
            other.locator('.song-row[data-song-id="carti:shoota"] .save-song').click()
            expect(self.page.locator('#saved-count')).to_have_text('2')
            expect(magnolia.locator('.save-song')).to_be_focused()

            saved_filter = self.page.locator('.song-filters [data-filter="saved"]')
            saved_filter.click()
            expect(self.page.locator('.song-title')).to_have_text(['Magnolia', 'Shoota'])
            magnolia.locator('.save-song').focus()
            other.locator('.song-row[data-song-id="carti:magnolia"] .save-song').click()
            expect(self.page.locator('#saved-count')).to_have_text('1')
            expect(self.page.locator('.song-title')).to_have_text(['Shoota'])
            expect(self.page.locator(
                '.song-row[data-song-id="carti:shoota"] .save-song'
            )).to_be_focused()

            other.locator('.song-row[data-song-id="carti:shoota"] .save-song').click()
            expect(self.page.locator('#saved-count')).to_have_text('0')
            expect(self.page.locator('#song-empty')).to_be_visible()
            expect(saved_filter).to_be_focused()
        finally:
            other.close()

    def test_invalid_saved_song_storage_recovers(self):
        for value in ('{broken json', '{"carti:magnolia": true}',
                      '["removed:track",null,42]'):
            with self.subTest(value=value):
                self.page.evaluate('([key, value]) => localStorage.setItem(key, value)',
                                   [SAVED_SONGS_KEY, value])
                self.page.reload(wait_until='networkidle')
                expect(self.page.locator('.song-row')).to_have_count(9)
                expect(self.page.locator('#saved-count')).to_have_text('0')
                self.page.locator('.song-row[data-song-id="carti:magnolia"] .save-song').click()
                self.page.reload(wait_until='networkidle')
                expect(self.page.locator('#saved-count')).to_have_text('1')
                expect(self.page.locator(
                    '.song-row[data-song-id="carti:magnolia"] .save-song'
                )).to_have_attribute('aria-pressed', 'true')

    def test_saved_songs_work_when_storage_is_denied(self):
        self.page.add_init_script('''
            for (const method of ['getItem', 'setItem']) {
                Object.defineProperty(Storage.prototype, method, {
                    configurable: true,
                    value() { throw new DOMException('Storage denied', 'SecurityError'); }
                });
            }
        ''')
        self.page.reload(wait_until='networkidle')
        expect(self.page.locator('.song-row')).to_have_count(9)
        self.page.locator('.song-row[data-song-id="carti:magnolia"] .save-song').click()
        expect(self.page.locator('#saved-count')).to_have_text('1')
        self.page.locator('.song-filters [data-filter="saved"]').click()
        expect(self.page.locator('.song-title')).to_have_text(['Magnolia'])
        self.page.locator('.save-song').click()
        expect(self.page.locator('#saved-count')).to_have_text('0')
        expect(self.page.locator('#song-empty')).to_be_visible()

    def test_content_and_mobile_navigation_without_javascript(self):
        context = self.browser.new_context(
            java_script_enabled=False, viewport={'width': 390, 'height': 844})
        page = context.new_page()
        page.on('pageerror', lambda error: self.errors.append(str(error)))
        page.on('response', lambda response: self.failed_resources.append(
            response.url) if response.status >= 400 else None)
        try:
            page.goto(self.url, wait_until='networkidle')
            expect(page.locator('.song-row')).to_have_count(9)
            expect(page.locator('audio.native-preview[controls][preload="none"]')).to_have_count(9)
            for track in MUSIC_TRACKS:
                row = page.locator('.song-row').filter(
                    has=page.get_by_role('heading', name=track['title'], exact=True))
                expect(row.locator('.song-art .song-cover')).to_have_attribute('src', track['cover'])
                audio = row.locator('audio.native-preview')
                source = audio.get_attribute('src') or audio.locator('source').get_attribute('src')
                self.assertEqual(source, track['audio'])
                self.assertTrue(row.locator('.listen-link').get_attribute('href').startswith(
                    'https://open.spotify.com/search/'))
            expect(page.locator('.artist-panel')).to_have_count(2)
            for artist in ('carti', 'cochise'):
                panel = page.locator(f'#{artist}-panel')
                live_panel = self.page.locator(f'#{artist}-panel')
                self.assertEqual(panel.locator('h4').inner_text(), live_panel.locator('h4').inner_text())
                self.assertEqual(panel.locator(':scope > p').all_text_contents(),
                                 live_panel.locator(':scope > p').all_text_contents(),
                                 f'{artist}: fallback must preserve the current introduction')
                self.assertGreaterEqual(len(' '.join(
                    panel.locator(':scope > p').all_text_contents()).split()), 65)
                sources = panel.locator('details.artist-sources')
                sources.locator('summary').click()
                expect(sources.locator('a').first).to_be_visible()
                self.assertEqual(sources.locator('a').evaluate_all('(links) => links.map(link => link.href)'),
                                 live_panel.locator('.artist-sources a').evaluate_all(
                                     '(links) => links.map(link => link.href)'))
            expect(page.locator('#comparison-body tr')).to_have_count(4)
            self.assertEqual(page.locator('#comparison-body th, #comparison-body td').all_text_contents(),
                             self.page.locator('#comparison-body th, #comparison-body td').all_text_contents(),
                             'Fallback comparison must match the interactive version')
            self.assertEqual(page.locator('#source-list p').all_text_contents(),
                             self.page.locator('#source-list p').all_text_contents(),
                             'Fallback credits must match the interactive version')
            self.assert_direct_editorial_voice(page)
            expect(page.locator('#navigation')).to_be_visible()
            expect(page.locator('.menu-toggle')).not_to_be_visible()
            page.locator('#navigation a[href="#artistas"]').click()
            self.assertEqual(page.url.split('#')[-1], 'artistas')
            self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), 390)
        finally:
            context.close()

    def test_photo_gallery_filters_and_dialog(self):
        expect(self.page.locator('#galeria')).to_have_count(1)
        links = self.page.locator('#galeria .photo-link:visible')
        for artist in ('carti', 'cochise'):
            self.page.locator(f'.gallery-filter[data-gallery-filter="{artist}"]').click()
            expect(links).to_have_count(7)
            self.assertEqual(set(links.evaluate_all(
                '(nodes) => nodes.map(node => node.dataset.artist)')), {artist})
            expect(self.page.locator('#gallery-count')).to_have_text('7 FOTOGRAFÍAS')
        self.page.locator('.gallery-filter[data-gallery-filter="all"]').click()
        expect(links).to_have_count(14)
        expect(self.page.locator('#gallery-count')).to_have_text('14 FOTOGRAFÍAS')
        first = links.nth(0)
        first_url = first.evaluate('(node) => node.href')
        second_url = links.nth(1).evaluate('(node) => node.href')
        original_overflow = self.page.evaluate('document.body.style.overflow')
        first.click()
        dialog = self.page.locator('#photo-dialog')
        expect(dialog).to_be_visible()
        expect(self.page.locator('#photo-close')).to_be_focused()
        expect(self.page.locator('#photo-position')).to_have_text('1 / 14')
        self.assertEqual(self.page.locator('#photo-full').evaluate('(node) => node.src'), first_url)
        self.assertEqual(self.page.evaluate('document.body.style.overflow'), 'hidden')
        self.page.locator('#photo-next').click()
        expect(self.page.locator('#photo-position')).to_have_text('2 / 14')
        self.assertEqual(self.page.locator('#photo-full').evaluate('(node) => node.src'), second_url)
        self.page.keyboard.press('ArrowLeft')
        expect(self.page.locator('#photo-position')).to_have_text('1 / 14')
        self.assertEqual(self.page.locator('#photo-full').evaluate('(node) => node.src'), first_url)
        self.page.keyboard.press('Escape')
        expect(dialog).not_to_be_visible()
        expect(first).to_be_focused()
        self.page.wait_for_function('(value) => document.body.style.overflow === value',
                                    arg=original_overflow, timeout=5000)
        self.assertEqual(self.page.evaluate('document.body.style.overflow'), original_overflow)

        first.click()
        expect(dialog).to_be_visible()
        bounds = dialog.bounding_box()
        self.assertIsNotNone(bounds)
        self.assertGreater(bounds['x'], 1, 'Backdrop must be reachable beside the dialog')
        self.page.mouse.click(1, bounds['y'] + bounds['height'] / 2)
        expect(dialog).not_to_be_visible()
        expect(first).to_be_focused()
        self.page.wait_for_function('(value) => document.body.style.overflow === value',
                                    arg=original_overflow, timeout=5000)
        self.assertEqual(self.page.evaluate('document.body.style.overflow'), original_overflow)

    def test_photo_gallery_local_images_and_no_javascript_links(self):
        expect(self.page.locator('#galeria')).to_have_count(1)
        self.page.locator('.gallery-filter[data-gallery-filter="all"]').click()
        links = self.page.locator('#galeria .photo-link')
        expect(links).to_have_count(14)
        for link in links.all():
            image = link.locator('img')
            expect(image).to_have_count(1)
            for reference in (link.get_attribute('href'), image.get_attribute('src')):
                self.assertTrue(reference)
                url = urljoin(self.url, reference)
                self.assertTrue(url.startswith(f'{self.url}/'), 'Gallery photographs must be local')
                path = ROOT / unquote(urlparse(url).path).lstrip('/')
                self.assertTrue(path.is_file(), f'Missing photograph: {path}')
            image.scroll_into_view_if_needed()
            self.page.wait_for_function(
                '(image) => image.complete && image.naturalWidth > 0',
                arg=image.element_handle(), timeout=10000)
            self.assertTrue(image.get_attribute('alt'))

        context = self.browser.new_context(
            java_script_enabled=False, viewport={'width': 390, 'height': 844})
        page = context.new_page()
        page.on('response', lambda response: self.failed_resources.append(
            response.url) if response.status >= 400 else None)
        try:
            page.goto(self.url, wait_until='networkidle')
            no_script_links = page.locator('#galeria .photo-link:visible')
            expect(no_script_links).to_have_count(14)
            first = no_script_links.first
            image_url = first.evaluate('(node) => node.href')
            first.click()
            page.wait_for_load_state('load')
            self.assertEqual(page.url, image_url)
            self.assertGreater(page.locator('img').evaluate('(image) => image.naturalWidth'), 0)
        finally:
            context.close()

    def test_mobile_menu_and_escape(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        button = self.page.get_by_role('button', name='Abrir menú')
        button.click()
        self.assertTrue(self.page.locator('#navigation').is_visible())
        self.page.keyboard.press('Escape')
        self.assertFalse(self.page.locator('#navigation').is_visible())
        self.assertEqual(button.get_attribute('aria-expanded'), 'false')
        button.click()
        self.page.locator('#navigation a[href="#artistas"]').click()
        self.assertEqual(self.page.url.split('#')[-1], 'artistas')
        self.assertFalse(self.page.locator('#navigation').is_visible())
        button.click()
        self.page.set_viewport_size({'width': 1440, 'height': 1000})
        expect(self.page.locator('.menu-toggle')).to_have_attribute('aria-expanded', 'false')
        self.assertTrue(self.page.locator('#navigation').is_visible())

    def test_responsive_layout(self):
        self.song_row('Location').locator('.preview-toggle').click()
        self.wait_for_playback('assets/music/location.mp3')
        for width in (320, 375, 390, 650, 768, 1024, 1440):
            with self.subTest(width=width):
                self.page.set_viewport_size({'width': width, 'height': 900})
                self.assertLessEqual(self.page.evaluate(
                    'document.documentElement.scrollWidth'), width)
                self.assertTrue(self.page.locator('h1').is_visible())
                self.assertTrue(self.page.locator('.artist-card').first.is_visible())
                expect(self.page.locator('#preview-toggle')).to_be_visible()
                expect(self.page.locator('#preview-seek')).to_be_visible()

    def test_anchors_and_disclosures(self):
        for link in self.page.locator('a[href^="#"]').all():
            target = link.get_attribute('href')[1:]
            self.assertEqual(self.page.locator(f'[id="{target}"]').count(), 1)
        licensing = self.page.locator('.sources-details details').filter(
            has=self.page.locator('a[href="assets/fonts/Anton-OFL.txt"]'))
        licensing.locator('summary').click()
        self.assertTrue(self.page.get_by_role('link', name='Anton', exact=True).is_visible())
        self.assertTrue(self.page.get_by_role('link', name='Space Grotesk', exact=True).is_visible())
        self.page.locator('#navigation a[href="#sonido"]').click()
        self.assertEqual(self.page.url.split('#')[-1], 'sonido')

    def test_reduced_motion_and_skip_link(self):
        self.page.emulate_media(reduced_motion='reduce')
        self.assertEqual(self.page.evaluate(
            "getComputedStyle(document.documentElement).scrollBehavior"), 'auto')
        self.page.keyboard.press('Tab')
        self.assertEqual(self.page.locator(':focus').get_attribute('class'), 'skip-link')
        self.page.keyboard.press('Enter')
        self.assertEqual(self.page.url.split('#')[-1], 'contenido')
        self.assertEqual(self.page.locator(':focus').get_attribute('id'), 'contenido')

    def test_unique_identifiers_and_semantics(self):
        ids = self.page.locator('[id]').evaluate_all('(nodes) => nodes.map(node => node.id)')
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(self.page.locator('main').count(), 1)
        self.assertEqual(self.page.locator('table caption').count(), 1)
        self.assertEqual(self.page.locator('tbody th[scope="row"]').count(), 4)
        for image in self.page.locator('img').all():
            self.assertIsNotNone(image.get_attribute('alt'))

    def test_fx_progress_burst_and_headline(self):
        # La barra de progreso existe y avanza con el scroll.
        self.assertEqual(self.page.locator('.fx-progress').count(), 1)
        self.page.evaluate("document.documentElement.style.scrollBehavior='auto'")
        self.page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
        self.page.wait_for_function(
            "getComputedStyle(document.querySelector('.fx-progress')).transform !== 'matrix(0, 0, 0, 1, 0, 0)'")
        # El titular termina con su texto original y sin aria-label temporal.
        self.page.wait_for_function("!document.querySelector('.hero h1').hasAttribute('aria-label')", timeout=5000)
        self.assertEqual(' '.join(self.page.locator('.hero h1').inner_text().split()),
                         HERO_HEADLINE)
        # Al guardar una canción aparece una ráfaga que desaparece sola.
        button = self.page.locator('.song-row[data-song-id="carti:magnolia"] .save-song')
        button.scroll_into_view_if_needed()
        button.click()
        expect(self.page.locator('.fx-burst')).to_have_count(1)
        expect(self.page.locator('.fx-burst')).to_have_count(0, timeout=3000)
        expect(button).to_have_attribute('aria-pressed', 'true')

    def test_fx_reduced_motion_keeps_text_and_skips_burst(self):
        context = self.browser.new_context(reduced_motion='reduce', viewport={'width': 1440, 'height': 1000})
        page = context.new_page()
        page.on('pageerror', lambda error: self.errors.append(str(error)))
        try:
            page.goto(self.url, wait_until='networkidle')
            self.assertEqual(' '.join(page.locator('.hero h1').inner_text().split()),
                             HERO_HEADLINE)
            page.locator('.song-row[data-song-id="carti:magnolia"] .save-song').click()
            expect(page.locator('.fx-burst')).to_have_count(0)
            expect(page.locator('.outline').first).to_have_css('color', 'rgb(255, 58, 46)')
            location = page.locator('.song-row[data-song-id="carti:location"]')
            location.locator('.preview-toggle').click()
            page.wait_for_function('''() => {
                const audio = document.querySelector('#preview-audio');
                return !audio.paused && audio.currentTime > 0.05;
            }''', timeout=15000)
            expect(location.locator('.preview-toggle')).to_have_attribute('aria-pressed', 'true')
            expect(location.locator('.song-art')).to_have_css('animation-name', 'none')
            expect(page.locator('.deck-record')).to_have_css('animation-name', 'none')
        finally:
            context.close()


if __name__ == '__main__':
    unittest.main()
