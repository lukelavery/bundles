import PyPDF2

pdf = "C:/Users/lukel/Desktop/bundle/A. Section A/2003.03.03 - Example Document 3.pdf"
pdf_file = PyPDF2.PdfFileReader(pdf)
p0 = pdf_file.getPage(0)
p0.scale(2, 2)
pdf_writer = PyPDF2.PdfFileWriter()
pdf_writer.addPage(p0)
with open("C:/Users/lukel/Desktop/bundle/A. Section A/resizedpdffile.pdf", "wb+") as f:
    pdf_writer.write(f)
