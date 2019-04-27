
# coding: utf-8

# In[33]:


import os
from .PyPDF3 import PdfFileReader, PdfFileWriter
from django.conf import settings
from .fpdf import FPDF
from django.core.exceptions import ValidationError
def pdf_splitter(path,start_page,end_page,chapter_name,book_name):
    print('path: ',path,'no: ',type(start_page))
    fname = os.path.splitext(os.path.basename(path))[0]
    pdf = PdfFileReader(path)
    print(pdf.getNumPages())
    i=0
    print(type(start_page))
    print(type(end_page))
    start_page=int(start_page)
    end_page=int(end_page)
    pdf_writer = PdfFileWriter()
    for k in range(start_page-1,end_page):
        pdf_writer.addPage(pdf.getPage(k))
    chapter_name=book_name.replace(".pdf", "_")+chapter_name+'.pdf'
    path=settings.MEDIA_ROOT+'\\'+chapter_name
    with open(path, 'wb') as out:
        pdf_writer.write(out)
    print('Created: {}'.format(chapter_name))
    return chapter_name,path

def pdf_cat(ref_no,input_files):
    input_streams = []
    try:
        for input_file in input_files:
            input_streams.append(open(input_file, 'rb'))
        pdf_writer = PdfFileWriter()
        for reader in map(PdfFileReader, input_streams):
            for n in range(reader.getNumPages()):
                pdf_writer.addPage(reader.getPage(n))

        path = settings.MEDIA_ROOT + '\\' + ref_no+'.pdf'
        with open(path, 'wb') as out:
            pdf_writer.write(out)

        print('Created combined file')

    finally:
        for f in input_streams:
            f.close()



def make_Introduction(book_name,data):
    spacing = 1
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Times", size=36)
    col_width = pdf.w/2
    row_height = pdf.font_size
    pdf.cell(col_width, row_height * spacing,
             txt=book_name, border=0, align='R')
    pdf.ln(row_height * spacing)
    pdf.ln(row_height * spacing)

    pdf.set_font("Times", size=24)
    pdf.cell(col_width, row_height * spacing,
             txt='Index', border=0, align='R')
    pdf.ln(row_height * spacing)
    pdf.ln(row_height * spacing)

    col_width = pdf.w / 3
    pdf.set_font("Times", size=12)
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height * spacing,
                     txt=item, border=0)
        pdf.ln(row_height * spacing)

    pdf.output(settings.MEDIA_ROOT+'\\'+'simple_table.pdf')
