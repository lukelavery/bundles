import os
from pathlib import Path


def get_dir(x):
    entries = os.listdir(x)
    return entries


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


def list_docs(bundle_path):
    # todo: handle error
    docs_path = get_documents_path(bundle_path)
    docs_dir = os.listdir(docs_path)
    return docs_dir


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
