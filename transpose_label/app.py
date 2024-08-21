import PyPDF2
from tkinter import Tk, filedialog, Label, Button, Radiobutton, IntVar, messagebox
import os

from PyPDF2 import Transformation


def get_pdf_filename():
    filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    return filename

def transpose_label(input_pdf, output_pdf, position):
    reader = PyPDF2.PdfReader(input_pdf)
    writer = PyPDF2.PdfWriter()

    # get first page
    page = reader.pages[0]

    media_box = page.mediabox

    width = media_box.width
    height = media_box.height

    # Define the target position based on user input
    if position == 2:  # Top right
        target_x = width / 2
        target_y = 0
    elif position == 3:  # Bottom left
        target_x = 0
        target_y = -(height / 2)
    elif position == 4:  # Bottom right
        target_x = width / 2
        target_y = -(height / 2)
    else:
        raise ValueError("Invalid position selected")

    # Move the content to the selected position
    page.add_transformation(Transformation().translate(tx=target_x, ty=target_y))
    writer.add_page(page)

    # Save the new PDF
    with open(output_pdf, 'wb') as out_file:
        writer.write(out_file)

def select_position_and_process():
    input_pdf = get_pdf_filename()
    if not input_pdf:
        messagebox.showerror("Error", "No file selected. Exiting.")
        return

    position = position_var.get()
    if position not in [2, 3, 4]:
        messagebox.showerror("Error", "Invalid position selected.")
        return

    suffix = ['top_right', 'bottom_left', 'bottom_right'][position - 2]

    output_pdf = input_pdf.replace('.pdf', f'_{suffix}.pdf')
    transpose_label(input_pdf, output_pdf, position)
    # Open the output PDF in the default PDF viewer
    os.system(f'open {output_pdf}')
    # Exit
    exit(0)
    # messagebox.showinfo("Success", f"Label transposed to position {position} and saved as {output_pdf}.")

def create_gui():
    root = Tk()
    root.title("PDF Label Transposer")

    Label(root, text="Select the position to transpose the top-left label to:").pack(pady=10)

    global position_var
    position_var = IntVar()
    position_var.set(2)

    Radiobutton(root, text="2: Top Right", variable=position_var, value=2).pack(anchor='w')
    Radiobutton(root, text="3: Bottom Left", variable=position_var, value=3).pack(anchor='w')
    Radiobutton(root, text="4: Bottom Right", variable=position_var, value=4).pack(anchor='w')

    Button(root, text="Select PDF and Transpose Label", command=select_position_and_process).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()

