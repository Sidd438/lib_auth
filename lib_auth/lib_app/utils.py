from lib_app.models import Book, Issue, Rating, Renew, Review

def process_ratings(ratingform, book, current_user):
    ratingform.save()
    rating = Rating.objects.latest('id')
    rate = rating.rating
    rating.user = current_user
    rating.book = book
    rating.save()
    book.brating = round(
        (book.brating*book.bratings + rate)/(book.bratings+1), 2)
    book.bratings += 1
    book.save()
