"""
CS3C, Assignment #7 tests, HashMap and Project Gutenberg
Selma Emekci
"""

import unittest
from pathlib import Path

from assignment07 import HashMap

# Try to import Gutenberg helpers in your repo
_HAS_EBOOK = True
try:
    from ebook import eBookEntryReader
except Exception:
    _HAS_EBOOK = False


class HashMapCoreTests(unittest.TestCase):
    def test_basic_set_get_update_and_iter(self):
        m = HashMap()
        self.assertEqual(len(m), 0)

        m["one"] = 1
        m["two"] = 2
        m["three"] = 3
        self.assertEqual(len(m), 3)

        self.assertEqual(m["one"], 1)
        self.assertEqual(m["two"], 2)
        self.assertEqual(m["three"], 3)

        # update existing key
        m["two"] = 22
        self.assertEqual(len(m), 3)
        self.assertEqual(m["two"], 22)

        # iteration yields keys
        keys = set(iter(m))
        self.assertEqual(keys, {"one", "two", "three"})

        # equality
        m2 = HashMap()
        m2["one"] = 1
        m2["two"] = 22
        m2["three"] = 3
        self.assertTrue(m == m2)

        m2["two"] = 2
        self.assertFalse(m == m2)
        self.assertFalse(m == 123)

    def test_missing_key_raises(self):
        m = HashMap()
        m["x"] = 9
        with self.assertRaises(KeyError):
            _ = m["nope"]


@unittest.skipUnless(_HAS_EBOOK, "ebook module not available in this workspace")
class HashMapGutenbergById(unittest.TestCase):
    def test_map_by_id(self):
        here = Path(__file__).resolve().parent
        catalog = (here.parent / "HashMap/catalog-short4.txt").as_posix()

        books = eBookEntryReader(catalog)
        by_id = HashMap()

        for book in books:
            by_id[book.id] = book

        sample = []
        for b in books:
            sample.append(b)
            if len(sample) == 3:
                break

        for b in sample:
            found = by_id[b.id]
            self.assertEqual(found.id, b.id)
            self.assertEqual(found.title, b.title)


@unittest.skipUnless(_HAS_EBOOK, "ebook module not available in this workspace")
class HashMapGutenbergByAuthorTitle(unittest.TestCase):
    def test_map_by_author_title(self):
        here = Path(__file__).resolve().parent
        catalog = (here.parent / "HashMap/catalog-short4.txt").as_posix()

        books = eBookEntryReader(catalog)
        by_pair = HashMap()
        for book in books:
            key = (book.author, book.title)
            by_pair[key] = book
            
        sample_keys = []
        for book in books:
            sample_keys.append((book.author, book.title))
            if len(sample_keys) == 3:
                break

        for k in sample_keys:
            found = by_pair[k]
            self.assertEqual((found.author, found.title), k)


if __name__ == "__main__":
    unittest.main()
