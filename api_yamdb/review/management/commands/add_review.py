import csv
from django.core.management import BaseCommand


from review.models import Comment, Review, TITLES
from users.models import User

CSV_Comment = '/Users/natalliaakhromenka/Dev/api_yamdb/api_yamdb/static/data/comments.csv'
CSV_Review = '/Users/natalliaakhromenka/Dev/api_yamdb/api_yamdb/static/data/review.csv'
CSV_Titles = '/Users/natalliaakhromenka/Dev/api_yamdb/api_yamdb/static/data/titles.csv'
CSV_User = '/Users/natalliaakhromenka/Dev/api_yamdb/api_yamdb/static/data/users.csv'


class Command(BaseCommand):
    help = "Loads products and product categories from CSV file."

    def handle(self, *args, **options):

        with open(CSV_User, "r") as csv_file:
            data = csv.reader(csv_file, delimiter=",")

            for row in data:
                User.objects.create(email=row[2], first_name=row[1], role=row[3])

