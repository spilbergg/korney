from .models import Book


def discont(book_set):
    full_price = 0
    if len(book_set) == 1:
        for f in book_set:
            full_price += Book.objects.get(name_book_rus=f).price_one_day_period * 30
    elif len(book_set) == 2 or len(book_set) == 3:
        for f in book_set:
            full_price += Book.objects.get(name_book_rus=f).price_one_day_period * 30 * 0.9
    elif len(book_set) == 4:
        for f in book_set:
            full_price += Book.objects.get(name_book_rus=f).price_one_day_period * 30 * 0.85
    return full_price
