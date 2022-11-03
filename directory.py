import os
from pathlib import Path
from dt import short_string_to_long_string
from models import BundleEntry, BundleSection


def get_dir(x):
    entries = os.listdir(x)
    return entries


def get_dir_dict(path):
    dir_dict = {}
    tab = 1

    for d in os.listdir(path):
        entry_list = []
        sub_dir = os.path.join(path, d)

        if os.path.isdir(sub_dir):
            section = BundleSection(sub_dir)

            for f in os.listdir(sub_dir):
                entry_list.append(BundleEntry(
                    path=os.path.join(sub_dir, f), tab=tab))
                tab = tab + 1

            dir_dict[section] = entry_list

    return dir_dict


def scrape_file_names(docs):
    my_tuples = []
    for doc in docs:
        date = get_date_from_file(doc)
        date = short_string_to_long_string(date)

        name = get_name_from_file(doc)

        my_tuple = (date, name)
        my_tuples.append(my_tuple)
    return my_tuples


def get_parent_dir(path):
    path1 = Path(path)
    return path1.parent


def get_documents_path(bundle_path):
    docs_path = os.path.join(bundle_path, "Documents")
    return docs_path


def path_exists(path):
    result = os.path.exists(path)
    return result

# return list of documents in bundle


def list_docs(path):
    # todo: handle error
    docs_dir = []

    for d in os.listdir(path):
        sub_dir_path = os.path.join(path, d)
        if os.path.isdir(sub_dir_path):
            sub_dir = os.listdir(sub_dir_path)
            for s in sub_dir:
                docs_dir.append(s)

    return docs_dir


def list_doc_paths(path):
    doc_paths = []

    for d in os.listdir(path):
        sub_dir_path = os.path.join(path, d)
        if os.path.isdir(sub_dir_path):
            sub_dir = os.listdir(sub_dir_path)
            for li in sub_dir:
                doc_path = os.path.join(sub_dir_path, li)
                doc_paths.append(doc_path)

    return (doc_paths)


def delete_file(path):
    os.remove(path)


def get_date_from_file(file_name):
    date = file_name[0:10]
    return date


def get_name_from_file(file_name):
    name = file_name[13:]
    # only works when len(file_extension) = 3
    name = name[:-4]
    return name


def join_paths(path1, path2):
    new_path = os.path.join(path1, path2)
    return new_path


def is_custom_index(input_path):
    for li in os.listdir(input_path):
        if li == 'index_template.docx':
            print("Index!")
            return True


def is_title_page(input_path):
    for li in os.listdir(input_path):
        if li == 'title_page.docx':
            return True
