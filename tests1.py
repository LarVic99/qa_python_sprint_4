import pytest
from main import BooksCollector

# Тестовый класс, который включает все необходимые тесты для BooksCollector
class TestBooksCollector:

    # Фикстура для подготовки объекта BooksCollector с некоторыми книгами
    @pytest.fixture
    def setup_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')
        collector.set_book_genre('Что делать, если ваш кот хочет вас убить', 'Ужасы')
        return collector

    # Тест на добавление двух книг
    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    # Параметризованный тест на добавление книги с разными длинами названия
    @pytest.mark.parametrize("book_name, expected_count", [
        ("A" * 40, 1),  # название ровно 40 символов
        ("B" * 41, 0),  # название 41 символ
        ("Valid Book", 1),  # нормальная книга
        ("", 0)  # пустое название
    ])
    def test_add_new_book_name_length(self, book_name, expected_count):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert len(collector.get_books_genre()) == expected_count

    # Тест на установку жанра книги
    def test_set_book_genre(self, setup_books):
        collector = setup_books
        collector.set_book_genre("Что делать, если ваш кот хочет вас убить", "Комедии")
        assert collector.get_book_genre("Что делать, если ваш кот хочет вас убить") == "Комедии"

    # Тест на установку жанра для несуществующей книги
    def test_set_book_genre_invalid_book(self, setup_books):
        collector = setup_books
        collector.set_book_genre("Неизвестная книга", "Комедии")
        assert collector.get_book_genre("Неизвестная книга") is None

    # Тест на получение жанра книги
    def test_get_book_genre(self, setup_books):
        collector = setup_books
        assert collector.get_book_genre("Гордость и предубеждение и зомби") == "Ужасы"
        assert collector.get_book_genre("Отсутствует") is None

    # Тест на получение книг с определённым жанром
    def test_get_books_with_specific_genre(self, setup_books):
        collector = setup_books
        books = collector.get_books_with_specific_genre("Ужасы")
        assert "Гордость и предубеждение и зомби" in books
        assert "Что делать, если ваш кот хочет вас убить" in books
        assert len(books) == 2

    # Тест на получение всех жанров книг
    def test_get_books_genre(self, setup_books):
        collector = setup_books
        books_genre = collector.get_books_genre()
        assert isinstance(books_genre, dict)
        assert books_genre.get("Гордость и предубеждение и зомби") == "Ужасы"

    # Тест на книги для детей (книги без возрастного рейтинга)
    def test_get_books_for_children(self, setup_books):
        collector = setup_books
        collector.add_new_book("Детская книга")
        collector.set_book_genre("Детская книга", "Комедии")
        books_for_children = collector.get_books_for_children()
        assert "Детская книга" in books_for_children
        assert len(books_for_children) == 1

    # Параметризованный тест для добавления книги в избранное
    @pytest.mark.parametrize("book_name, expected", [
        ("Книга в избранное", ["Книга в избранное"]),
        ("Неизвестная книга", []),  # книга не добавляется, если её нет в books_genre
    ])
    def test_add_book_in_favorites(self, book_name, expected):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        favorites = collector.get_list_of_favorites_books()
        assert favorites == expected

    # Тест на удаление книги из избранного
    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book("Книга в избранное")
        collector.add_book_in_favorites("Книга в избранное")
        collector.delete_book_from_favorites("Книга в избранное")
        favorites = collector.get_list_of_favorites_books()
        assert "Книга в избранное" not in favorites

    # Тест на попытку удалить несуществующую книгу из избранного
    def test_delete_book_from_favorites_not_existing(self):
        collector = BooksCollector()
        collector.add_new_book("Книга в избранное")
        collector.add_book_in_favorites("Книга в избранное")
        collector.delete_book_from_favorites("Неизвестная книга")  # попытка удалить несуществующую книгу
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 1  # Изменений не будет

    # *Исправленный тест* на добавление книги в избранное, если книга не существует в books_genre
    def test_add_book_in_favorites_not_existing(self):
        collector = BooksCollector()
        collector.add_new_book("Книга в избранное")
        # Пытаемся добавить книгу, которой нет в books_genre
        collector.add_book_in_favorites("Неизвестная книга")
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 0  # Книга НЕ добавляется в избранное, так как её нет в books_genre

