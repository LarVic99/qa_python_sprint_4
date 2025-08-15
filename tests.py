import pytest
from main import BooksCollector

class TestBooksCollector:

    @pytest.fixture
    def collector(self):
        return BooksCollector()

    # На добавление двух книг
    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    # Параметризованный тест на добавление книги с разными длинами названия
    @pytest.mark.parametrize("book_name, expected_count", [
        ("A" * 40, 1),
        ("B" * 41, 0),
        ("Valid Book", 1),
        ("", 0)
    ])
    def test_add_new_book_name_length(self, book_name, expected_count, collector):
        collector.add_new_book(book_name)
        assert len(collector.get_books_genre()) == expected_count

     # На установку жанра книги
    def test_set_book_genre(self, collector):
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        collector.set_book_genre("Что делать, если ваш кот хочет вас убить", "Комедии")
        assert collector.get_book_genre("Что делать, если ваш кот хочет вас убить") == "Комедии"

    # Тест на установку жанра для несуществующей книги
    def test_set_book_genre_invalid_book(self, collector):
        collector.set_book_genre("Неизвестная книга", "Комедии")
        assert collector.get_book_genre("Неизвестная книга") is None

    # Тест на получение жанра книги — задаём внутренний словарь напрямую
    def test_get_books_genre_returns_expected_dict(self, collector):
        collector.books_genre = {
            "Гордость и предубеждение и зомби": "Ужасы",
            "Книга без жанра": ""
        }

        books_genre = collector.get_books_genre()

        assert isinstance(books_genre, dict)
        assert books_genre == {
            "Гордость и предубеждение и зомби": "Ужасы",
            "Книга без жанра": ""
        }

    def test_get_book_genre_returns_correct_genre(self, collector):
        collector.add_new_book("Гордость и предубеждение и зомби")
        collector.set_book_genre("Гордость и предубеждение и зомби", "Ужасы")

        genre = collector.get_book_genre("Гордость и предубеждение и зомби")
        assert genre == "Ужасы"

    # Тест: книга без жанра (пустая строка)
    def test_get_book_genre_returns_empty_string_for_book_without_genre(self, collector):
        collector.add_new_book("Книга без жанра")
        # Явно не устанавливаем жанр, чтобы проверить поведение
        genre = collector.get_book_genre("Книга без жанра")
        assert genre == ""

    # Тест: запрос жанра для несуществующей книги возвращает None
    def test_get_book_genre_returns_none_for_unknown_book(self, collector):
        genre = collector.get_book_genre("Неизвестная книга")
        assert genre is None

    # Тест на получение книг с определённым жанром
    def test_get_books_with_specific_genre(self, collector):
        collector.books_genre = {
            "Гордость и предубеждение и зомби": "Ужасы",
            "Что делать, если ваш кот хочет вас убить": "Ужасы",
            "Книга 3": "Фантастика"
        }

        result = collector.get_books_with_specific_genre("Ужасы")
        assert set(result) == {
            "Гордость и предубеждение и зомби",
            "Что делать, если ваш кот хочет вас убить"
        }
        assert "Книга 3" not in result

    # Тест на получение всего словаря жанров
    def test_get_books_genre(self, collector):
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 2")
        assert len(collector.get_books_genre()) == 2

    # Тест на книги для детей (книги без возрастного рейтинга)
    def test_get_books_for_children(self, collector):
        collector.books_genre = {
            "Детская книга": "Комедии",
            "Фильм ужасов": "Ужасы",
            "Мистика": "Ужасы"
        }

        result = collector.get_books_for_children()

        expected = ["Детская книга"]

        assert sorted(result) == sorted(expected)

    # Параметризованный тест для добавления книги в избранное
    @pytest.mark.parametrize("book_name, book_exists, expected", [
        ("Книга в избранное", True, ["Книга в избранное"]),
        ("Неизвестная книга", False, []),
    ])
    def test_add_book_in_favorites(self, book_name, book_exists, expected, collector):
        if book_exists:
            collector.add_new_book(book_name)

        collector.add_book_in_favorites(book_name)
        favorites = collector.get_list_of_favorites_books()

        assert favorites == expected

    def test_get_list_of_favorites_books(self, collector):
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 2")
        collector.add_book_in_favorites("Книга 1")
        collector.add_book_in_favorites("Книга 2")

        assert collector.get_list_of_favorites_books() == ["Книга 1", "Книга 2"]


    # Тест на удаление книги из избранного
    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book("Книга в избранное")
        collector.add_book_in_favorites("Книга в избранное")
        collector.delete_book_from_favorites("Книга в избранное")
        favorites = collector.get_list_of_favorites_books()
        assert "Книга в избранное" not in favorites

    # Тест на попытку удалить несуществующую книгу из избранного
    def test_delete_book_from_favorites_not_existing(self, collector):
        collector.add_new_book("Книга в избранное")
        collector.add_book_in_favorites("Книга в избранное")
        collector.delete_book_from_favorites("Неизвестная книга")
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 1

    # *Исправленный тест* на добавление книги в избранное, если книга не существует в books_genre
    def test_add_book_in_favorites_not_existing(self, collector):
        collector.add_book_in_favorites("Неизвестная книга")
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 0
