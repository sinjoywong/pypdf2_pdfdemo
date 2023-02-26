from PyPDF2 import PdfReader, PdfWriter, Transformation, PaperSize
import math,os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# https://pypdf2.readthedocs.io/en/latest/user/cropping-and-transforming.html

def merge_every_two_page_in_one_page():
    op_translate_to_right_half_of_a4_paper = Transformation().translate(PaperSize.A5.height / 2, 0)
    op_scale_to_half = Transformation().scale(sx=0.5, sy=0.5)
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

original_pdf_name = ""
tmp_pdf_name = original_pdf_name + ".tmp"
final_pdf_name = original_pdf_name + "_final.pdf"
def main():
    merge_every_two_page_in_one_page()
    finalize()
    messagebox.showinfo('处理完成', '请在源文件相同目录下找到以_final.pdf结尾的同名文件，并仔细检查是否符合预期！')
    open_directory()

original_pdf_name = ""
def get_file_path():
    global original_pdf_name
    global tmp_pdf_name
    global final_pdf_name
    original_pdf_name = filedialog.askopenfilename(title="Select A File", filetypes=(("pdf", "*.pdf"),))
    tmp_pdf_name = original_pdf_name + ".tmp"
    final_pdf_name = original_pdf_name + "_final.pdf"
    l1 = tk.Label(text="已选文件: " + original_pdf_name).pack()

def open_directory():
    global final_pdf_name
    dir_name = os.path.dirname(final_pdf_name)
    print(final_pdf_name)
    print(dir_name)
    #os.system('start ' + dir_name)
    if os.sys.platform == "win32":
        os.startfile(dir_name)
    elif os.sys.platform == "darwin":
        print("not supported in mac system")
    else:
        print("not support in system: " + os.sys.platform)


window = tk.Tk()
window.title("PDF处理小工具 v0.1")
label = tk.Label(text="功能：将每两页A4纸pdf横向放置合并为一页A4纸.")
label.pack()

button = tk.Button(text="打开pdf文件", command=get_file_path).pack(pady=10)
button = tk.Button(text="开始处理", command=main).pack()
window.mainloop()
