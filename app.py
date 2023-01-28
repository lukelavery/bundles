import tkinter
from src.controller.controller import Controller
from src.models.validation_model import ValidationModel
from src.views.main_view import View


class App(tkinter.Tk):
    """Main GUI application."""

    def __init__(self):
        super().__init__()

        # Set the window title and dimensions
        self.title('AG Bundle Tool')
        self.geometry('750x625')
        self.resizable(False, False)

        # Create instances of the model and view
        validation_model = ValidationModel()
        view = View(self)
        view.pack(padx=10, pady=10)

        # create a controller and pass the view and model to it
        controller = Controller(view, validation_model)

        # set the controller to the view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()
