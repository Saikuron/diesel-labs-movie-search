from app import open_file, whole_names

def test_open_file():
    test_file = open_file("data/links.csv")
    assert len(test_file) > 0
    assert len(test_file[1]) == 3

def test_whole_names():
    assert type(whole_names[1]) == str