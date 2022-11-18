from app import open_file

def test_open_file():
    test_file = open_file("data/links.csv")
    assert len(test_file) > 0