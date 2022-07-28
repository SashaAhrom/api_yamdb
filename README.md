## Description
```
The YaMDb project collects reviews (Review) of users on works (Titles).
The works are divided into categories: "Books", "Films", "Music".
The list of categories (Category) can be expanded by the administrator
(for example, you can add the category "Fine Arts" or "Jewellery").
The works themselves are not stored in YaMDb; you cannot watch a movie or listen to music here.
In each category there are works: books, films or music.
For example, in the category "Books" there may be works "Winnie the Pooh and All-All-All"
and "The Martian Chronicles", and in the category "Music"
- the song "Now" by the group "Insects" and the second suite of Bach.
A work can be assigned a genre (Genre) from the list of preset ones (for example,
"Fairy Tale", "Rock" or "Arthouse"). New genres can only be created by the administrator.
Grateful or indignant users leave text reviews (Review) for the works
and rate the work in the range from one to ten (an integer);
from user ratings, an average rating of the work is formed
- rating (integer). A user can leave only one review per work..
For a detailed description of the project in
  http://127.0.0.1:8000/redoc/
```
## Running a project in dev mode
```
- Install and activate the virtual environment
- Install dependencies from requirements.txt file
- pip install -r requirements.txt
- In the folder with the manage.py, run the command:
  python3 manage.py runserver
- python3 manage.py migrate 
```
## System requirements
```
Python 3.7
Django 2.2.19
Djangorestframework 3.12.4
```
## The authors
Aliaksandr Akhromenka
Valentin Nemanov
Igor Ryabov

