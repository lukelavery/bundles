from src.models.path_model import PathModel
from src.models.path_type import PathType
from src.models.bundle_model import BundleModel
from src.models.exceptions import BundleError, PathError


class Controller:
    def __init__(self, view):
        self.view = view
        self.path_model = None
        self.bundle = None

    def handle_get_data_button_click(self, input_path: str) -> None:
        try:
            self.path_model = PathModel(value=input_path)
        except PathError as error:
            self.view.show_input_error(error)
        except BundleError as error:
            self.view.show_error(error)

    def handle_generate_button_click(self):
        try:
            self._gen_bundle
        except BundleError as error:
            self.view.show_error(error)

    def _gen_bundle(self):
        """Create a temporary directory, try to generate the index and documents, then delete the temporary directory."""

        if self.bundle == None:
            raise BundleError('Bundle is empty.')

        self.bundle.get_tmp_dir()

        try:
            self.gen_index()
            self.gen_documents()
        finally:
            self.bundle.del_tmp_dir()

    def gen_index(self):
        """Generate the index and update the progress bar in the View."""
        self.view.update_pb(10)
        self.bundle.index.input_table_data()
        self.bundle.index.save(
            self.bundle.paths['index_doc_path'])
        self.bundle.index.convert(
            self.bundle.paths['index_pdf_path'])
        self.view.update_pb(33)
        self.bundle.index.input_pag_nums()
        self.bundle.index.save(
            self.bundle.paths['index_doc_path'])
        self.bundle.index.convert(
            self.bundle.paths['index_pdf_path'])
        self.view.update_pb(66)

    def gen_documents(self):
        """Generate the documents and update the progress bar in the View."""

        self.bundle.documents.merge_documents(
            self.bundle.paths['merged_path'])
        self.view.update_pb(80)
        self.bundle.documents.paginate(self.bundle.paths['pag_input_path'],
                                       self.bundle.paths['pag_output_path'])
        self.view.update_pb(90)
        self.bundle.documents.hyperlink(self.bundle.paths['index_pdf_path'],
                                        self.bundle.paths['pag_output_path'], self.bundle.paths['link_path'])
        self.view.update_pb(100)
