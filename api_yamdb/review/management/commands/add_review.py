import csv
from django.core.management import BaseCommand


from review.models import Comment, Review, TITLES, CATEGORIES, GENRES
from users.models import User

CSV_Category = '/Users/natalliaakhromenka/Dev/api_yamdb/api_yamdb/static/data/category.csv'
CSV_Genre = '/Users/natalliaakhromenka/Dev/api_yamdb/api_yamdb/static/data/genre.csv'
CSV_Comment = '/Users/natalliaakhromenka/Dev/api_yamdb/api_yamdb/static/data/comments.csv'
CSV_Review = '/Users/natalliaakhromenka/Dev/api_yamdb/api_yamdb/static/data/review.csv'
CSV_Titles = '/Users/natalliaakhromenka/Dev/api_yamdb/api_yamdb/static/data/titles.csv'
CSV_User = '/Users/natalliaakhromenka/Dev/api_yamdb/api_yamdb/static/data/users.csv'


class Command(BaseCommand):
    help = "Loads DB from CSV file."

    def handle(self, *args, **options):

        with open(CSV_User, "r") as csv_User,\
                open(CSV_Category, "r") as csv_Category, \
                open(CSV_Genre, "r") as csv_Genre, \
                open(CSV_Titles, "r") as csv_Title:

            data_Title = csv.reader(csv_Title, delimiter=",")
            data_Genre = csv.reader(csv_Genre, delimiter=",")
            data_Category = csv.reader(csv_Category, delimiter=",")
            data_User = csv.reader(csv_User, delimiter=",")
            title = [field.name for field in TITLES.objects.all()]
            genre = [field.slug for field in GENRES.objects.all()]
            cat = [field.slug for field in CATEGORIES.objects.all()]
            user = [field.username for field in User.objects.all()]
            for row in list(data_User)[1:]:
                if row[1] not in user:
                    User.objects.create(email=row[2], username=row[1], role=row[3])
            for row in list(data_Category)[1:]:
                if row[2] not in cat:
                    CATEGORIES.objects.create(name=row[1], slug=row[2])
            for row in list(data_Genre)[1:]:
                if row[2] not in genre:
                    GENRES.objects.create(name=row[1], slug=row[2])
            for row in list(data_Title)[1:]:
                if row[1] not in title:
                    TITLES.objects.create(name=row[1], slug=row[2])
