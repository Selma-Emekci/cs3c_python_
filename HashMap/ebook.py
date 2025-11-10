"""
eBook reader

Based on Prof Eric Reed's implementation
Modified by Zibin Yang
(Mainly, removed sort-by, because there's better alternative)
"""

import xml.etree.ElementTree as ET
from functools import total_ordering


@total_ordering
class eBookEntry:
    def __init__(self, entry):
        self._title = entry[0]
        self._author = entry[1]
        self._subject = entry[2]
        self._id = int(entry[3])

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def subject(self):
        return self._subject

    @property
    def id(self):
        return self._id

    def __str__(self):
        return str(self.id) + ": " + self.author + " -> " + self.title + \
               " (" + self.subject + ")"

    def __lt__(self, other):
        if isinstance(other, eBookEntry):
            return self.id < other.id
        else:
            return self.id < other

    def __eq__(self, other):
        if isinstance(other, eBookEntry):
            return self.id == other.id
        else:
            return self.id == other


class eBookEntryReader:

    def __init__(self, filename):
        self._books = []
        if len(filename) == 0:
            raise FileNotFoundError
        tree = ET.parse(filename)
        root = tree.getroot()

        ns = {'gutenberg': 'http://www.gutenberg.org/rdfterms/',
              'dcmi': 'http://purl.org/dc/elements/1.1/',
              'dcterms': 'http://purl.org/dc/terms/',
              'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}

        for book in root.findall('gutenberg:etext', ns):
            ID = (book.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}ID']).strip("etext")
            title_el = book.find('dcmi:title', ns)
            if title_el is None:
                title = "(No Author)"
            else:
                title = title_el.text.replace('\n', '').replace('\r', '')
            author_el = book.find('dcmi:creator', ns)
            if author_el is None:
                author = "(No Author)"
            else:
                author = author_el.text
            subject = book.find('dcmi:subject', ns)

            if subject is not None:
                bag = subject.find('rdf:Bag', ns)
                if bag is not None:
                    subject = next(iter(bag))
                lcsh = next(iter(subject))
                value = next(iter(lcsh))
                subject_text = value.text
                if subject_text is None:
                    subject_text = "No Subject"
            else:
                subject_text = "No Subject"

            entry = [title, author, subject_text, ID]

            self._books.append(eBookEntry(entry))

        print(len(self._books), "titles loaded")

    @staticmethod
    def _is_data_line(line):
        if len(line) < 1:
            return False
        if line[0] == "#":
            return True
        return False

    def __iter__(self):
        self._pos = 0
        return self

    def __next__(self):
        if self._pos < len(self._books):
            self._pos += 1
            return self._books[self._pos - 1]
        else:
            raise StopIteration

    def __len__(self):
        return len(self._books)


def main():
    my_books = eBookEntryReader("catalog-short4.txt")

    for book in my_books:
        print(book)
    print(f"total number of books: {len(my_books)}")


if __name__ == "__main__":
    main()
