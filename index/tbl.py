from docx.enum.text import WD_ALIGN_PARAGRAPH


def get_table(doc):
    # implement search for table
    tables = doc.tables
    table = tables[3]
    return table


def add_text(cell, text, alignment):
    cell.text = text
    para = cell.paragraphs[0]
    para_fmt = para.paragraph_format
    para_fmt.space_before = 76200
    para_fmt.space_after = 76200

    if alignment == 'centre':
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
