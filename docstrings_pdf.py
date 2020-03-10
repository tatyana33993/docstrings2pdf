#!/usr/bin/env python3
import sys
import re
import pyFPDF
from PyPDF2 import PdfFileReader, PdfFileWriter
import docstrings


def get_pdf(filename):
    d = docstrings.get_docstrings(filename)
    pdf = pyFPDF.FPDF(format='letter')
    pdf.add_page()
    for i, j in d.items():
        pdf.set_font("Arial", size=14)
        pdf.cell(0, 5, 'class.def: {0}'.format(i), border=1, ln=1, align='C')
        arr = j.split('\n')
        pdf.cell(0, 5, 'comm:', border=0, ln=1)
        pdf.set_font("Arial", size=12)
        for el in arr:
            pdf.cell(0, 5, el, border=0, ln=1)
    name_pdf = '{0}.pdf'.format(filename.split('.')[0])
    pdf.output(name_pdf)

    f_pdf_read = open(name_pdf, 'rb')
    read = PdfFileReader(f_pdf_read)
    write = PdfFileWriter()
    for i in range(read.getNumPages()):
        page = read.getPage(i)
        page_content = page.extractText()
        names = re.findall(r'(class\.def: [\w()]*\.\w*)', page_content)
        write.addPage(read.getPage(i))
        for name in names:
            write.addBookmark(re.sub(r'(class\.def: )|(comm)', '', name),
                              i, bold=True)
    f_pdf_write = open(name_pdf, 'wb')
    write.write(f_pdf_write)
    f_pdf_read.close()
    f_pdf_write.close()


if __name__ == '__main__':
    if (len(sys.argv) > 1) and (sys.argv[1] == 'help'):
        print("""Программа переводит docstrings функций
         python в документацию в pdf файле""")
    elif len(sys.argv) == 1:
        print("Аргумент для проверки отсутствует. Посмотрите help.")
    else:
        get_pdf(sys.argv[1])
