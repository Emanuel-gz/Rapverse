"""Functional browser checks. Run: python3 tests/smoke.py -v.

Uses the environment's Playwright and Chromium; application has no dependencies.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
import shutil
import threading
import unittest
from urllib.parse import unquote, urljoin, urlparse

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SAVED_SONGS_KEY = 'rapverse:saved-songs'


class QuietHandler(SimpleHTTPRequestHandler):
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
        self.requests = []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))
        self.page.on('response', lambda response: self.failed_resources.append(
            response.url) if response.status >= 400 else None)
        self.page.on('request', lambda request: self.requests.append(request.url))
        self.page.goto(self.url, wait_until='networkidle')
        self.page.evaluate('document.fonts.ready')

    def tearDown(self):
        self.assertEqual(self.errors, [], 'JavaScript errors')
        self.assertEqual(self.failed_resources, [], 'Failed local resources')
        self.context.close()

    def test_local_resources_and_document(self):
        self.assertEqual(self.page.locator('html').get_attribute('lang'), 'es')
        self.assertEqual(self.page.locator('h1').count(), 1)
        self.assertEqual(self.page.locator('.artist-card').count(), 2)
        self.assertEqual(self.page.locator('.song-row').count(), 8)
        self.assertTrue(self.page.evaluate("document.fonts.check('16px Anton')"))
        self.assertTrue(self.page.evaluate("document.fonts.check('16px \"Space Grotesk\"')"))
        self.assertTrue(all(url.startswith(self.url) for url in self.requests))
        self.assertEqual(self.page.locator('audio, video, iframe').count(), 0)
        self.assertIn('Archivo de terceros', self.page.locator('#source-list').inner_text())

    def test_artist_tabs_and_keyboard(self):
        for name in ('carti', 'cochise'):
            card = self.page.locator(f'[data-artist="{name}"]')
            history = card.get_by_role('tab', name='Historia', exact=True)
            history.focus()
            self.page.keyboard.press('ArrowRight')
            evolution = card.get_by_role('tab', name='Evolución', exact=True)
            self.assertEqual(evolution.get_attribute('aria-selected'), 'true')
            self.assertEqual(self.page.locator(f'#{name}-panel').get_attribute(
                'aria-labelledby'), f'{name}-evolution-tab')
            self.page.keyboard.press('End')
            self.assertEqual(card.get_by_role('tab', name='Influencias').get_attribute(
                'aria-selected'), 'true')
            self.assertIn('INFLUENCIAS', card.get_by_role('tabpanel').inner_text())
            self.assertGreater(card.locator('.artist-sources a').count(), 0)
            self.page.keyboard.press('ArrowRight')
            self.assertEqual(history.get_attribute('aria-selected'), 'true')
            self.page.keyboard.press('ArrowLeft')
            self.assertEqual(card.get_by_role('tab', name='Influencias').get_attribute(
                'aria-selected'), 'true')
            card.get_by_role('tab', name='Estilo y actitud').click()
            self.assertIn('LECTURA EDITORIAL', card.get_by_role('tabpanel').inner_text())
            self.page.keyboard.press('Home')
            self.assertEqual(card.locator('[tabindex="0"][role="tab"]').count(), 1)
            self.assertEqual(history.get_attribute('aria-selected'), 'true')

    def test_filters_and_track_credits(self):
        self.page.get_by_role('button', name='Cochise', exact=True).click()
        self.assertEqual(self.page.locator('.song-row').count(), 4)
        self.assertIn('Cochise & $NOT', self.page.locator('.song-credit').all_inner_texts())
        self.assertIn('4 CANCIONES DOCUMENTADAS', self.page.locator('#song-count').inner_text())
        self.page.get_by_role('button', name='Playboi Carti', exact=True).click()
        self.assertEqual(self.page.locator('.song-row').count(), 4)
        self.assertIn('Travis Scott', self.page.locator('.song-credit').all_inner_texts()[-1])
        self.page.get_by_role('button', name='Todos').click()
        self.assertEqual(self.page.locator('.song-row').count(), 8)
        self.assertEqual(self.page.locator('.song-project[href^="https://music.apple.com/"]').count(), 4)
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
        self.assertIn('1 CANCIÓN DOCUMENTADA', self.page.locator('#song-count').inner_text())
        self.page.locator('.song-filters [data-filter="carti"]').click()
        expect(self.page.locator('.song-row')).to_have_count(0)
        expect(self.page.locator('#song-empty')).to_be_visible()
        self.page.locator('.song-filters [data-filter="all"]').click()
        expect(self.page.locator('.song-title')).to_have_text(['POCKET ROCKET'])
        self.page.locator('#clear-search').click()
        expect(search).to_have_value('')
        expect(self.page.locator('.song-row')).to_have_count(8)
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
        self.assertIn('0 CANCIONES DOCUMENTADAS', self.page.locator('#song-count').inner_text())
        self.page.locator('#reset-songs').click()
        expect(self.page.locator('#song-search')).to_have_value('')
        expect(self.page.locator('.song-filters [data-filter="all"]')).to_have_attribute(
            'aria-pressed', 'true')
        expect(self.page.locator('.song-row')).to_have_count(8)
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
                expect(self.page.locator('.song-row')).to_have_count(8)
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
        expect(self.page.locator('.song-row')).to_have_count(8)
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
            expect(page.locator('.song-row')).to_have_count(8)
            expect(page.locator('.artist-panel')).to_have_count(2)
            for panel in page.locator('.artist-panel').all():
                self.assertIn('BIOGRAFÍA DOCUMENTADA', panel.inner_text())
                self.assertGreater(panel.locator('p').count(), 0)
                self.assertGreater(panel.locator('.artist-sources a').count(), 0)
            expect(page.locator('#comparison-body tr')).to_have_count(4)
            expect(page.locator('#navigation')).to_be_visible()
            expect(page.locator('.menu-toggle')).not_to_be_visible()
            page.locator('#navigation').get_by_role('link', name='Los artistas').click()
            self.assertEqual(page.url.split('#')[-1], 'artistas')
            self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), 390)
        finally:
            context.close()

    def test_photo_gallery_filters_and_dialog(self):
        if not self.page.locator('#galeria').count():
            self.skipTest('Photographs have not been imported')
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
        if not self.page.locator('#galeria').count():
            self.skipTest('Photographs have not been imported')
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
        self.page.locator('#navigation').get_by_role('link', name='Los artistas').click()
        self.assertEqual(self.page.url.split('#')[-1], 'artistas')
        self.assertFalse(self.page.locator('#navigation').is_visible())
        button.click()
        self.page.set_viewport_size({'width': 1440, 'height': 1000})
        expect(self.page.locator('.menu-toggle')).to_have_attribute('aria-expanded', 'false')
        self.assertTrue(self.page.locator('#navigation').is_visible())

    def test_responsive_layout(self):
        for width in (320, 375, 390, 650, 768, 1024, 1440):
            with self.subTest(width=width):
                self.page.set_viewport_size({'width': width, 'height': 900})
                self.assertLessEqual(self.page.evaluate(
                    'document.documentElement.scrollWidth'), width)
                self.assertTrue(self.page.locator('h1').is_visible())
                self.assertTrue(self.page.locator('.artist-card').first.is_visible())

    def test_anchors_and_disclosures(self):
        for link in self.page.locator('a[href^="#"]').all():
            target = link.get_attribute('href')[1:]
            self.assertEqual(self.page.locator(f'[id="{target}"]').count(), 1)
        summary = self.page.get_by_text('Imágenes, audio y licencias', exact=False)
        summary.click()
        self.assertTrue(self.page.get_by_role('link', name='Anton', exact=True).is_visible())
        self.assertTrue(self.page.get_by_role('link', name='Space Grotesk', exact=True).is_visible())
        self.page.locator('#navigation').get_by_role('link', name='El sonido').click()
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


if __name__ == '__main__':
    unittest.main()
