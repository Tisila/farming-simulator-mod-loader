import re
import os
import unittest
from datetime import datetime
from fsmodloader import Mod

class TestMod(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._mod = Mod('https://farming-simulator.com/mod.php?lang=en&country=us&mod_id=148173&title=fs2019')
        os.remove('FS19_DairyBarn.zip')

    def test_mod_webpage(self):
        self.assertEqual(self._mod._webpage, 'https://farming-simulator.com/mod.php?lang=en&country=us&mod_id=148173&title=fs2019')

    #def test_mod_link(self):
    #    regex_pattern = re.compile('https://cdn*.giants-software.com/modHub/storage/00148173/FS19_DairyBarn.zip')
    #    self.assertTrue(regex_pattern.fullmatch(self._mod._link))

    def test_mod_size(self):
        self.assertEqual(self._mod._size, 13.53)

    def test_mod_unit(self):
        self.assertEqual(self._mod._unit, 'MB') 

    def test_mod_filename(self):
        self.assertEqual(self._mod._filename, 'FS19_DairyBarn.zip')

    def test_mod_is_downloaded(self):
        self.assertFalse(self._mod.is_downloaded()) 

    def test_mod_is_updated(self):
        self.assertFalse(self._mod.is_updated())

class  TestModPriorToDownload(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._mod = Mod('https://farming-simulator.com/mod.php?lang=en&country=us&mod_id=148173&title=fs2019')
        cls._mod.download()

    def test_mod_is_updated(self):
        self.assertTrue(self._mod.is_updated())

    def test_mod_is_downloaded(self):
        self.assertTrue(self._mod.is_downloaded())

    def test_mod_is_size_ok(self):
        self.assertTrue(self._mod.is_size_ok())

if __name__ == '__main__':
    unittest.main()
