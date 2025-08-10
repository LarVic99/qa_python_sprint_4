import pytest
from main import BooksCollector

class TestBooksCollector:

    @pytest.fixture
    def setup_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')
        collector.set_book_genre('Что делать, если ваш кот хочет вас убить', 'Ужасы')
        return collector

    @pytest.fixture
    def setup_favorites(self):
        collector = BooksCollector()
        collector.add_new_book("Книга в избранное")
        collector.add_book_in_favorites("Книга в избранное")
        return collector

    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    @pytest.mark.parametrize("book_name,expected_count", [
        ("A" * 40, 1),         # ровно 40 символов — допускается
        ("B" * 41, 0),         # 41 символ — не добавляется
        ("Valid Book", 1),     # нормальное название
        ("", 0),               # пустое название
    ])
    def test_add_new_book_name_length_and_uniqueness(self, book_name, expected_count):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert len(collector.get_books_genre()) == expected_count

    def test_set_book_genre(self, setup_books):
        collector = setup_books
        collector.set_book_genre("Что делать, если ваш кот хочет вас убить", "Комедии")
        assert collector.get_book_genre("Что делать, если ваш кот хочет вас убить") == "Комедии"

    def test_set_book_genre_invalid_book(self, setup_books):
        collector = setup_books
        collector.set_book_genre("Неизвестная книга", "Комедии")
        assert collector.get_book_genre("Неизвестная книга") is None

    def test_get_book_genre(self, setup_books):
        collector = setup_books
        assert collector.get_book_genre("Гордость и предубеждение и зомби") == "Ужасы"
        assert collector.get_book_genre("Отсутствует") is None

    def test_get_books_with_specific_genre(self, setup_books):
        collector = setup_books
        books = collector.get_books_with_specific_genre("Ужасы")
        assert "Гордость и предубеждение и зомби" in books
        assert "Что делать, если ваш кот хочет вас убить" in books
        assert len(books) == 2

    def test_get_books_genre(self, setup_books):
        collector = setup_books
        books_genre = collector.get_books_genre()
        assert isinstance(books_genre, dict)
        assert books_genre.get("Гордость и предубеждение и зомби") == "Ужасы"

    def test_get_books_genre_empty(self):
        collector = BooksCollector()
        books_genre = collector.get_books_genre()
        assert books_genre == {}

    def test_get_books_for_children(self):
        collector = BooksCollector()
        collector.add_new_book("Детская книга")
        collector.add_new_book("Ужастик")
        collector.set_book_genre("Детская книга", "Комедии")
        collector.set_book_genre("Ужастик", "Ужасы")
        books_for_children = collector.get_books_for_children()
        assert "Детская книга" in books_for_children
        assert "Ужастик" not in books_for_children

    @pytest.mark.parametrize("book, expected", [
        ("Книга в избранное", ["Книга в избранное"]),
        ("Неизвестная книга", []),  # книга не добавляется
    ])
    def test_add_book_in_favorites(self, book, expected):
        collector = BooksCollector()
        collector.add_new_book("Книга в избранное")  # Добавляем книгу в books_genre
        collector.add_book_in_favorites(book)         # Попытка добавить в избранное
        favorites = collector.get_list_of_favorites_books()
        assert favorites == expected

    def test_add_book_in_favorites_duplicate(self, setup_favorites):
        collector = setup_favorites
        collector.add_book_in_favorites("Книга в избранное")  # повторное добавление
        favorites = collector.get_list_of_favorites_books()
        assert favorites == ["Книга в избранное"]

    def test_delete_book_from_favorites(self, setup_favorites):
        collector = setup_favorites
        collector.delete_book_from_favorites("Книга в избранное")
        favorites = collector.get_list_of_favorites_books()
        assert "Книга в избранное" not in favorites

    def test_delete_book_from_favorites_not_existing(self, setup_favorites):
        collector = setup_favorites
        collector.delete_book_from_favorites("Нет такой книги")
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 1  # ничего не изменилось

    def test_get_list_of_favorites_books(self, setup_favorites):
        collector = setup_favorites
        collector.add_new_book("Еще одна книга")
        collector.add_book_in_favorites("Еще одна книга")
        favorites = collector.get_list_of_favorites_books()
        assert favorites == ["Книга в избранное", "Еще одна книга"]

