from PyPDF2 import PdfReader, PdfMerger, PdfWriter, Transformation, PaperSize
import math,os

# https://pypdf2.readthedocs.io/en/latest/user/cropping-and-transforming.html

os.makedirs("tmp",exist_ok=True)
original_pdf_name = "EVEN.pdf"
tmp_pdf_name = "tmp/tmp_" + original_pdf_name
final_pdf_name = "final." + original_pdf_name

# common:
op_translate_to_right_half_of_a4_paper = Transformation().translate(PaperSize.A5.height / 2, 0)
op_scale_to_half = Transformation().scale(sx=0.5, sy=0.5)


def merge_every_two_page_in_one_page():
    pdf = PdfReader(original_pdf_name)
    num_pages = len(pdf.pages)
    pdf_writer = PdfWriter()

    last_part_index = -1
    print("num_pages=%d", num_pages)
    index = 0
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
            # pdf_writer.add_page(blank_page)
            pdf_writer.insert_page(blank_page, index)
            index = index + 1
        else:
            last_part_index = num_pages - 1
            break

    if last_part_index > 0:
        page_last_part = pdf.pages[last_part_index]
        blank_page.merge_page(page_last_part)
        pdf_writer.insert_page(blank_page, index)
    with open(tmp_pdf_name, 'wb') as f:
        pdf_writer.write(f)

def finalize():
    pdf = PdfReader(tmp_pdf_name)
    num_pages = len(pdf.pages)
    half_num_pages_ceil_up = math.ceil(num_pages / 2)
    pdf_writer = PdfWriter()

    pdf_writer.append(tmp_pdf_name, (0, half_num_pages_ceil_up))
    with open(final_pdf_name, 'wb') as f:
        pdf_writer.write(f)
    os.remove(tmp_pdf_name)


def main():
    merge_every_two_page_in_one_page()
    finalize()


main()
