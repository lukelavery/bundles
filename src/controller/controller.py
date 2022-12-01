from src.models.exceptions import BundleError, ValidationError
from models.bundle_model import BundleModel


class Controller:
    def __init__(self, view, validation_model):
        self.view = view
        self.validation_model = validation_model
        self.bundle = None

    def set_input_path(self, value):
        """Try to validate the input path, if successful then create a BundleModel and update the tree view."""
        try:

            # set the input path
            self.validation_model.input_path = value
            self.set_bundle_model(value)

        except ValidationError as error:
            # show an error message
            self.view.show_input_error(error)
        except BundleError as error:
            self.view.show_error(error)

    def set_output_path(self, value):
        """Try to validate the output path, if successful then generate the bundle."""
        try:
            # set the input path
            self.validation_model.output_path = value
            self.bundle.paths.update({
                'output_path': value
            })
            self.gen()

        except ValueError as error:
            # show an error message
            self.view.show_output_error(error)
        except BundleError as error:
            self.view.show_error(error)

    def set_bundle_model(self, input_path):
        self.bundle = BundleModel(input_path)
        self.view.update_tree_view(self.bundle.data)

    def gen(self):
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
