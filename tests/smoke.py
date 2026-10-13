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

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]


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
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 1000})
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
        self.page.close()

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
        self.assertEqual(self.page.locator('[aria-pressed="true"]').count(), 1)
        for link in self.page.locator('.listen-link').all():
            self.assertTrue(link.get_attribute('href').startswith('https://open.spotify.com/search/'))
            self.assertEqual(link.get_attribute('target'), '_blank')
            self.assertIn('noopener', link.get_attribute('rel'))
            self.assertIn('nueva pestaña', link.get_attribute('aria-label'))

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
