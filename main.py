from PyPDF2 import PdfReader, PdfMerger, PdfWriter, Transformation

# https://pypdf2.readthedocs.io/en/latest/user/cropping-and-transforming.html

pdf = PdfReader(r'./report-dec2021.pdf')
num_pages = len(pdf.pages)

pdf_writer = PdfWriter()
#pdf_writer.add_page(pdf.pages[0].rotate(90))


pdf_write_merge = PdfMerger()

# common:
op_translate_to_right_half_of_a4_paper = Transformation().translate(149,0)
op_scale_to_half = Transformation().scale(sx=0.25, sy=0.25)

def merge_every_two_page_in_one_page(num_pages):
    for i in range(num_pages):
        if i % 2 == 0:
            print ("-----%d",i)
        else:
            print ("======%d",i)

page_odd = pdf.pages[0]
page_odd.add_transformation(op_scale_to_half)

page_even = pdf.pages[1]
page_even.add_transformation(op_scale_to_half)
page_even.add_transformation(op_translate_to_right_half_of_a4_paper)
#page_even_rotated = page_even.rotate(0)

# add blank page of A4 size:
blank_page = pdf_writer.add_blank_page(297,210)
blank_page.merge_page(page_odd)
blank_page.merge_page(page_even)

merge_every_two_page_in_one_page(num_pages)

#pdf_writer.add_page(blank_page)
pdf_writer.add_page(blank_page)
with open(r'report-dec2021-new.pdf', 'wb') as f:
    pdf_writer.write(f)



