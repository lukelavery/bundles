
from dir.directory import get_dir, get_documents_path, list_docs


bundle_path = 'C:/Users/lukel/Desktop/bundle/'
docs = list_docs(bundle_path)
docs_path = get_documents_path(bundle_path)
docs_dir = get_dir(docs_path)

print(docs)
# print(docs_path)
# print(docs_dir)
