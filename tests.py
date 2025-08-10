import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


class TestBooksCollector:

    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    @pytest.mark.parametrize("book_name,expected_count", [
        ("A" * 40, 1),  # ровно 40 символов — допускается
        ("B" * 41, 0),  # 41 символ — не добавляется
        ("Valid Book", 1),  # нормальное название
        ("", 0),  # пустое название
    ])
    def test_add_new_book_name_length_and_uniqueness(self, book_name, expected_count, collector):
        collector.add_new_book(book_name)
        assert len(collector.get_books_genre()) == expected_count

    def test_set_and_get_book_genre(self, collector):
        collector.add_new_book("Book 1")
        collector.set_book_genre("Book 1", "Фантастика")
        assert collector.get_book_genre("Book 1") == "Фантастика"

    def test_set_book_genre(self, collector):
        collector.add_new_book("Книга1")
        collector.set_book_genre("Книга1", "Фантастика")
        assert collector.get_book_genre("Книга1") == "Фантастика"

        # Попытка установить жанр не из списка
        collector.set_book_genre("Книга1", "Неизвестный жанр")
        assert collector.get_book_genre("Книга1") == "Фантастика"

        # Попытка установить жанр для несуществующей книги
        collector.set_book_genre("Неизвестная книга", "Фантастика")
        assert collector.get_book_genre("Неизвестная книга") is None

    def test_get_book_genre(self, collector):
        collector.add_new_book("Книга2")
        assert collector.get_book_genre("Книга2") == ""
        assert collector.get_book_genre("Отсутствует") is None

    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book("Книга3")
        collector.add_new_book("Книга4")
        collector.set_book_genre("Книга3", "Фантастика")
        collector.set_book_genre("Книга4", "Комедии")

        books = collector.get_books_with_specific_genre("Фантастика")
        assert books == ["Книга3"]
        assert collector.get_books_with_specific_genre("Романтика") == []

    def test_get_books_genre(self, collector):
        collector.add_new_book("Книга5")
        collector.set_book_genre("Книга5", "Комедии")
        books_genre = collector.get_books_genre()
        assert isinstance(books_genre, dict)
        assert books_genre.get("Книга5") == "Комедии"

    def test_get_books_for_children(self, collector):
        collector.add_new_book("Детская книга")
        collector.add_new_book("Ужастик")
        collector.set_book_genre("Детская книга", "Комедии")
        collector.set_book_genre("Ужастик", "Ужасы")
        books_for_children = collector.get_books_for_children()
        assert "Детская книга" in books_for_children
        assert "Ужастик" not in books_for_children

    def test_add_book_in_favorites(self, collector):
        collector.add_new_book("Книга в избранное")
        collector.add_book_in_favorites("Книга в избранное")
        collector.add_book_in_favorites("Книга в избранное")  # повторное добавление
        favorites = collector.get_list_of_favorites_books()
        assert favorites == ["Книга в избранное"]

    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book("Книга для удаления")
        collector.add_book_in_favorites("Книга для удаления")
        collector.delete_book_from_favorites("Книга для удаления")
        assert "Книга для удаления" not in collector.get_list_of_favorites_books()
        collector.delete_book_from_favorites("Нет такой книги")

    def test_get_list_of_favorites_books(self, collector):
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 2")
        collector.add_book_in_favorites("Книга 1")
        collector.add_book_in_favorites("Книга 2")
        favorites = collector.get_list_of_favorites_books()
        assert "Книга 1" in favorites
        assert "Книга 2" in favorites

    def test_add_new_book_duplicate_not_added(self, collector):
        collector.add_new_book("Book 1")
        collector.add_new_book("Book 1")  # дубликат
        assert len(collector.get_books_genre()) == 1

    def test_add_new_book_empty_and_too_long_name(self, collector):
        collector.add_new_book("")  # пустая строка — не добавляется
        collector.add_new_book("x" * 41)  # 41 символ — не добавляется
        assert len(collector.get_books_genre()) == 0
