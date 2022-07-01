from pydantic import BaseModel


class SomeClass:

    def __init__(self, some_attribute):
        self.some_attribute = some_attribute

    def some_method(self):
        return False

    def other_method(self, param):
        return param

    def another_method(self):
        return False


class SomeRepositoryClass:

    def __init__(self, connection):
        self.connection = connection

    def some_method(self, query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return True


class SomePydanticClass(BaseModel):

    def some_method(self):
        return False


def some_function():
    return False


def other_function():
    return some_function()
