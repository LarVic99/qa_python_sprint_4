import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()

class TestBooksCollector:

    @pytest.mark.parametrize('book_name, expected_len', [
        ("A" * 40, 1),        # допустимая длина
        ("B" * 41, 0),        # превышает лимит
        ("Книга", 1),         # обычное название
        ("", 0),              # пустое название
    ])
    def test_add_new_book_name_length(self, collector, book_name, expected_len):
        collector.add_new_book(book_name)
        assert len(collector.get_books_genre()) == expected_len

    def test_set_and_get_book_genre(self, collector):
        collector.add_new_book("Book 1")
        collector.set_book_genre("Book 1", "Фантастика")
        assert collector.get_book_genre("Book 1") == "Фантастика"

        # Попытка установить жанр не из списка
        collector.set_book_genre("Book 1", "Неизвестный жанр")
        assert collector.get_book_genre("Book 1") == "Фантастика"

        # Попытка установить жанр для несуществующей книги
        collector.set_book_genre("Неизвестная книга", "Фантастика")
        assert collector.get_book_genre("Неизвестная книга") is None

    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book("Book 1")
        collector.set_book_genre("Book 1", "Фантастика")
        collector.add_new_book("Book 2")
        collector.set_book_genre("Book 2", "Ужасы")

        assert set(collector.get_books_with_specific_genre("Фантастика")) == {"Book 1"}
        assert set(collector.get_books_with_specific_genre("Ужасы")) == {"Book 2"}
        assert collector.get_books_with_specific_genre("Детективы") == []

    def test_get_books_genre_returns_dict(self, collector):
        collector.add_new_book("Book 1")
        collector.add_new_book("Book 2")
        collector.set_book_genre("Book 1", "Фантастика")
        expected = {"Book 1": "Фантастика", "Book 2": ""}
        assert collector.get_books_genre() == expected

    def test_get_books_for_children_excludes_age_rated(self, collector):
        collector.add_new_book("Book 1")
        collector.add_new_book("Book 2")
        collector.add_new_book("Book 3")
        collector.set_book_genre("Book 1", "Фантастика")   # детский жанр
        collector.set_book_genre("Book 2", "Ужасы")        # возрастной
        collector.set_book_genre("Book 3", "Комедии")      # детский жанр

        books_for_children = collector.get_books_for_children()
        assert "Book 1" in books_for_children
        assert "Book 3" in books_for_children
        assert "Book 2" not in books_for_children

    def test_add_book_in_favorites_and_get_list_of_favorites(self, collector):
        collector.add_new_book("Book 1")
        collector.add_new_book("Book 2")

        collector.add_book_in_favorites("Book 1")
        collector.add_book_in_favorites("Book 1")  # повторное добавление не должно быть
        collector.add_book_in_favorites("Book 3")  # несуществующая книга — не добавится

        favorites = collector.get_list_of_favorites_books()
        assert favorites == ["Book 1"]

    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book("Book 1")
        collector.add_book_in_favorites("Book 1")
        assert "Book 1" in collector.get_list_of_favorites_books()

        collector.delete_book_from_favorites("Book 1")
        assert "Book 1" not in collector.get_list_of_favorites_books()

        # удаление книги, которой нет в избранном — ничего не ломает
        collector.delete_book_from_favorites("Book 2")

    def test_add_new_book_duplicate_not_added(self, collector):
        collector.add_new_book("Book 1")
        collector.add_new_book("Book 1")  # дубликат
        assert len(collector.get_books_genre()) == 1

    def test_add_new_book_empty_and_too_long_name(self, collector):
        collector.add_new_book("")  # пустая строка — не добавляется
        collector.add_new_book("x" * 41)  # 41 символ — не добавляется
        assert len(collector.get_books_genre()) == 0
