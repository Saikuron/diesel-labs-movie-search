from app import open_file, whole_names, avg_ratings, whole_table
from random import randint

# Function used to check that a string contains a float
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

# Testing the open_file function
def test_open_file():
  test_file = open_file("data/links.csv")
  assert len(test_file) > 0
  assert len(test_file[1]) == 3

# Testing the whole_names list
def test_whole_names():
  assert len(whole_names) > 0
  assert type(whole_names[1]) == str
  assert len(whole_names[1]) > 0

# Testing the result of the make_average_ratings function
def test_average_ratings():
  assert len(avg_ratings) > 0
  rand_int = randint(1, len(avg_ratings)-1)
  assert type(avg_ratings[rand_int][0]) == int
  assert type(avg_ratings[rand_int][1]) == float

# Testing the result of the make_whole function
def test_whole():
  rand_int = randint(0, len(whole_table)-1)
  rand_movie = whole_table[rand_int]
  assert rand_movie[0].isdigit()
  assert rand_movie[4].isdigit()
  assert rand_movie[5].isdigit()
  assert isfloat(rand_movie[6])
  assert isinstance(rand_movie[7], list)