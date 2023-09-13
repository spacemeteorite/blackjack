from typing import Protocol


class Model:
    def __init__(self):
        ...

    def create(self):
        ...

    def read(self):
        ...

    def update(self):
        ...

    def delete(self):
        ...


class View:
    def some_fun(self):
        ...


class Presenter:
    def __init_(self, model: Model, view: View):
        ...