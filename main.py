from PyPDF2 import PdfReader, PdfMerger, PdfWriter, Transformation, PaperSize

# https://pypdf2.readthedocs.io/en/latest/user/cropping-and-transforming.html

pdf = PdfReader(r'./CR.pdf')
num_pages = len(pdf.pages)

pdf_writer = PdfWriter()
# pdf_writer.add_page(pdf.pages[0].rotate(90))


pdf_write_merge = PdfMerger()

# common:
op_translate_to_right_half_of_a4_paper = Transformation().translate(PaperSize.A5.height / 2, 0)
op_scale_to_half = Transformation().scale(sx=0.5, sy=0.5)


def merge_every_two_page_in_one_page(num_pages):
    last_part_index = -1
    blank_page = pdf_writer.add_blank_page(PaperSize.A5.height, PaperSize.A5.width)
    print("num_pages=%d", num_pages)
    for i in range(0, num_pages, 2):
        blank_page = pdf_writer.add_blank_page(PaperSize.A5.height, PaperSize.A5.width)
        print("-----%d", i)
        page_odd = pdf.pages[i]
        page_odd.add_transformation(op_scale_to_half)
        print("======%d", i + 1)
        if i + 1 < num_pages:
            page_even = pdf.pages[i + 1]
            page_even.add_transformation(op_scale_to_half)
            page_even.add_transformation(op_translate_to_right_half_of_a4_paper)

            blank_page.merge_page(page_odd)
            blank_page.merge_page(page_even)
            pdf_writer.add_page(blank_page)
        else:
            last_part_index = num_pages - 1
            break

    if last_part_index > 0:
        #blank_page = pdf_writer.add_blank_page(PaperSize.A5.height, PaperSize.A5.width)
        page_last_part = pdf.pages[last_part_index]
        #page_last_part.add_transformation(op_scale_to_half)
        blank_page.merge_page(page_last_part)
        pdf_writer.add_page(blank_page)



# page_even_rotated = page_even.rotate(0)

# add blank page of A4 size:

# num_pages = 2
merge_every_two_page_in_one_page(num_pages)

with open(r'CR-new.pdf', 'wb') as f:
    pdf_writer.write(f)
