import tkinter
from src.controller.controller import Controller
from models.bundle_model import ValidationModel
from src.views.main_view import View


class App(tkinter.Tk):
    """Main GUI application."""

    def __init__(self):
        super().__init__()

        self.title('AG Bundle Tool')
        self.geometry('750x625')
        self.resizable(False, False)

        validation_model = ValidationModel()

        # create a view and place it on the root window
        view = View(self)
        view.pack(padx=10, pady=10)

        # create a controller
        controller = Controller(view, validation_model)

        # set the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()
