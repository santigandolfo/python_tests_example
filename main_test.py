import pytest

from main import SomeClass, SomePydanticClass, SomeRepositoryClass, other_function


@pytest.fixture
def cursor_mock(mocker):
    cursor_mock = mocker.MagicMock()
    cursor_mock.execute = mocker.MagicMock()
    yield cursor_mock


@pytest.fixture
def connection_mock(mocker, cursor_mock):
    connection_mock = mocker.MagicMock()
    connection_mock.cursor.return_value.__enter__ = mocker.MagicMock(return_value=cursor_mock)
    yield connection_mock


@pytest.fixture
def some_repository_class(mocker, connection_mock):
    some_repository_class = SomeRepositoryClass(connection_mock)
    yield some_repository_class


@pytest.fixture
def some_class(mocker):
    some_class = mocker.MagicMock()
    some_class.some_attribute = True
    some_class.some_method = mocker.MagicMock(return_value=True)
    yield some_class


class MockSomePydanticClass(SomePydanticClass):
    some_method_return_value: bool

    def some_method(self):
        return self.some_method_return_value


def test_fully_mock_some_class(mocker):
    some_class = mocker.MagicMock()
    some_class.some_attribute = True
    some_class.some_method = mocker.MagicMock(return_value=True)

    some_attribute = some_class.some_attribute
    some_method_value = some_class.some_method()

    assert some_attribute
    assert some_method_value

    some_class.some_method.assert_called_once()


def test_mock_methods_of_some_class(mocker):
    some_class = SomeClass(True)
    some_class.some_method = mocker.MagicMock(return_value=True)
    some_class.other_method = mocker.MagicMock(return_value=True)
    some_class.another_method = mocker.MagicMock(return_value=True)

    some_class.some_method()

    some_class.other_method(True)
    some_class.other_method(False)

    some_class.some_method.assert_called_once()
    some_class.other_method.assert_has_calls([
        mocker.call(True),
        mocker.call(False)
    ])
    some_class.another_method.assert_not_called


def test_mock_some_pydantic_class(mocker):
    some_pydantic_class = MockSomePydanticClass(some_method_return_value=True)

    some_method_value = some_pydantic_class.some_method()

    assert some_method_value


def test_mock_using_fixture(mocker, some_class):
    some_attribute = some_class.some_attribute
    some_method_value = some_class.some_method()

    assert some_attribute
    assert some_method_value

    some_class.some_method.assert_called_once()


def test_some_repository_class_method(mocker, some_repository_class, connection_mock, cursor_mock):
    querty = "SELECT * FROM TABLE"
    some_method_value = some_repository_class.some_method(querty)

    assert some_method_value
    connection_mock.cursor.assert_called_once()
    cursor_mock.execute.assert_called_once_with(querty)


def test_mock_some_function(mocker):
    mocker.patch('main.some_function', return_value=True)

    other_function_value = other_function()

    assert other_function_value
