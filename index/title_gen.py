from docxtpl import DocxTemplate


def gen_title(template_doc, context, output_path):

    doc = DocxTemplate(template_doc)

    doc.render(context)

    doc.save(output_path)
