#!/usr/bin/env python34
import unittest
import re
import docstrings as d
import docstrings_pdf as p
from PyPDF2 import PdfFileReader


class Testdocstrings_pdf(unittest.TestCase):
    def test_get_docstrings_pdf_pages(self):
        f_pdf_read = open('example.pdf', 'rb')
        read = PdfFileReader(f_pdf_read)
        num = read.getNumPages()
        self.assertTrue(num != 0)
        f_pdf_read.close()

    def test_get_docstrings_pdf_def(self):
        docstrings = d.get_docstrings('example.txt')
        f_pdf_read = open('example.pdf', 'rb')
        read = PdfFileReader(f_pdf_read)
        res = []
        for i in range(read.getNumPages()):
            page = read.getPage(i)
            page_content = page.extractText()
            names = re.findall(r'(class\.def: [\w()]*\.\w*)', page_content)
            for name in names:
                newname = name.replace('comm', '')
                newname = newname[newname.find('class.def: ') + 11:]
                res.append(newname)
        self.assertTrue(len(res) == len(docstrings))
        for e in res:
            self.assertTrue(e in docstrings)
        f_pdf_read.close()

    def test_get_docstrings_pdf_comm(self):
        docstrings = d.get_docstrings('example.txt')
        f_pdf_read = open('example.pdf', 'rb')
        read = PdfFileReader(f_pdf_read)
        res = ''
        for i in range(read.getNumPages()):
            page = read.getPage(i)
            page_content = page.extractText()
            res += page_content
        for e in docstrings:
            self.assertTrue(res.find(e) != -1)
        f_pdf_read.close()

    def test_get_docstrings_pdf_none(self):
        p.get_pdf('example.txt')
        f = open('example.pdf', 'r')
        self.assertIsNotNone(f)
        f.close()


if __name__ == '__main__':
    unittest.main()
