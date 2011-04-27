import random
import unittest
import blgr

class BlgrTest(unittest.TestCase):

    def setUp(self):
		pass

    def test_slugify(self):
        self.assertEqual("my-nice-slug", blgr.slugify("My nice ..(Slug)"))

    def test_load_tpl(self):
        self.assertEqual("TEST %(VALUE)s\n", blgr.load_tpl("test"))

    def test_get_tpl(self):
        self.assertEqual("TEST %(VALUE)s\n", blgr.load_tpl("test"))

    def test_get_tpl__MEMO(self):
        self.assertEqual("TEST %(VALUE)s\n", blgr.load_tpl("test"))
        self.assertEqual({ "tpltest": "TEST %(VALUE)s\n"}, blgr.MEMO)
         
    def test_templatize(self):
        self.assertEqual("TEST 222\n", blgr.templatize("test", { "VALUE": "222" }))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(BlgrTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

