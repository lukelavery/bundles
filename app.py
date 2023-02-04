import tkinter
from src.models.path_model import PathModel
from src.controller.controller import Controller

from src.views.main_view import View


class App(tkinter.Tk):
    """Main GUI application."""

    def __init__(self):
        super().__init__()

        # Set the window title and dimensions
        self.title('AG Bundle Tool')
        self.geometry('750x625')
        self.resizable(False, False)

        view = View(self)
        view.pack(padx=10, pady=10)

        # create a controller and pass the view and model to it
        controller = Controller(view)

        # set the controller to the view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()
