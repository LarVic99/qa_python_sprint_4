import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


class TestBooksCollector:

    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book('Книга1')
        collector.add_new_book('Книга2')
        assert len(collector.books_genre) == 2

    @pytest.mark.parametrize("book_name,expected_count", [
        ("A" * 40, 1),
        ("B" * 41, 0),
        ("Valid Book", 1),
        ("", 0),
    ])
    def test_add_new_book_name_length(self, collector, book_name, expected_count):
        collector.add_new_book(book_name)
        assert len(collector.books_genre) == expected_count

    def test_set_book_genre_success_and_fail(self, collector):
        collector.add_new_book("Книга1")
        collector.set_book_genre("Книга1", "Фантастика")
        assert collector.get_book_genre("Книга1") == "Фантастика"

        collector.set_book_genre("Неизвестная книга", "Фантастика")
        assert collector.get_book_genre("Неизвестная книга") is None

        collector.set_book_genre("Книга1", "Романтика")
        assert collector.get_book_genre("Книга1") == "Фантастика"

    def test_get_book_genre_positive_and_negative(self, collector):
        collector.add_new_book("Книга2")

        assert collector.get_book_genre("Книга2") == ""

        assert collector.get_book_genre("Отсутствует") is None

    def test_get_books_with_specific_genre_positive_and_empty(self, collector):
        collector.add_new_book("Книга3")
        collector.add_new_book("Книга4")
        collector.set_book_genre("Книга3", "Фантастика")
        collector.set_book_genre("Книга4", "Комедии")

        books = collector.get_books_with_specific_genre("Фантастика")
        assert books == ["Книга3"]

        assert collector.get_books_with_specific_genre("Романтика") == []

    def test_get_books_genre_returns_dict(self, collector):
        collector.add_new_book("Книга5")
        collector.set_book_genre("Книга5", "Комедии")
        books_genre = collector.get_books_genre()
        assert isinstance(books_genre, dict)
        assert books_genre.get("Книга5") == "Комедии"

    def test_get_books_for_children_filters_age_rating(self, collector):
        collector.add_new_book("Детская книга")
        collector.add_new_book("Ужастик")
        collector.set_book_genre("Детская книга", "Комедии")
        collector.set_book_genre("Ужастик", "Ужасы")

        books_for_children = collector.get_books_for_children()
        assert "Детская книга" in books_for_children
        assert "Ужастик" not in books_for_children

    def test_add_book_in_favorites_success(self, collector):
        collector.add_new_book("Книга в избранное")
        collector.add_book_in_favorites("Книга в избранное")
        assert collector.get_list_of_favorites_books() == ["Книга в избранное"]

    def test_add_book_in_favorites_unknown_book(self, collector):
        collector.add_book_in_favorites("Неизвестная книга")
        assert collector.get_list_of_favorites_books() == []

    def test_add_book_in_favorites_no_duplicates(self, collector):
        collector.add_new_book("Дубликат")
        collector.add_book_in_favorites("Дубликат")
        collector.add_book_in_favorites("Дубликат")
        assert collector.get_list_of_favorites_books() == ["Дубликат"]

    def test_delete_book_from_favorites_success(self, collector):
        collector.add_new_book("Книга для удаления")
        collector.add_book_in_favorites("Книга для удаления")
        collector.delete_book_from_favorites("Книга для удаления")
        assert "Книга для удаления" not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_non_existent(self, collector):
        collector.add_new_book("Книга для удаления")
        collector.add_book_in_favorites("Книга для удаления")
        collector.delete_book_from_favorites("Нет такой книги")
        # Избранное не изменилось
        assert collector.get_list_of_favorites_books() == ["Книга для удаления"]

    def test_get_list_of_favorites_books(self, collector):
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 2")
        collector.add_book_in_favorites("Книга 1")
        collector.add_book_in_favorites("Книга 2")
        favorites = collector.get_list_of_favorites_books()
        assert favorites == ["Книга 1", "Книга 2"]