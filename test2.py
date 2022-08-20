from pathlib import Path
from typing import Iterable, Any

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTPage

from text_model import TextObject

index = -1


def get_bbox_dict(index_path):
    text_objects = []
    path = Path(index_path).expanduser()

    def show_ltitem_hierarchy(o: Any, depth=0):
        """Show location and text of LTItem and all its descendants"""
        # if depth == 0:
        #     print('element                        x1  y1  x2  y2   text')
        #     print('------------------------------ --- --- --- ---- -----')

        # print(
        #     f'{get_indented_name(o, depth):<30.30s} '
        #     f'{get_optional_bbox(o)} '
        #     f'{get_optional_text(o)}'
        # )
        global index

        if isinstance(o, Iterable):
            for i in o:
                if isinstance(i, LTPage):
                    index += 1
                    print("page")
                if isinstance(i, LTTextBoxHorizontal):
                    x1, y1, x2, y2 = i.bbox
                    text_object = TextObject(
                        i.get_text().strip(), x1, y1, x2, y2, index)
                    text_objects.append(text_object)
                show_ltitem_hierarchy(i, depth=depth + 1)

    pages = extract_pages(path)

    show_ltitem_hierarchy(pages)

    return sort_list(text_objects)


def sort_list(list):
    list.sort(key=lambda x: (x.page, 1/x.y1))
    y1_dict = {}
    for li in list:
        y1 = li.y1

        if y1 in y1_dict:
            y1_dict[y1].append(li)
        else:
            y1_dict[y1] = [li]
    return y1_dict
