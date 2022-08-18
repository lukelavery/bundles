from pathlib import Path
from typing import Iterable, Any

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal


def get_bbox_dict(index_path):
    xy_dict = {}
    path = Path(path).expanduser()

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

        if isinstance(o, Iterable):
            for i in o:
                show_ltitem_hierarchy(i, depth=depth + 1)
                if isinstance(i, LTTextBoxHorizontal):
                    xy_dict[i.get_text().strip()] = i.bbox

    pages = extract_pages(path)

    show_ltitem_hierarchy(pages)

    return xy_dict
