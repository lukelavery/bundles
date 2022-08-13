from dir.directory import get_date_from_file, get_name_from_file
from dt import short_string_to_long_string


def scrape_file_names(docs):
    my_tuples = []
    for doc in docs:
        date = get_date_from_file(doc)
        date = short_string_to_long_string(date)

        name = get_name_from_file(doc)

        my_tuple = (date, name)
        my_tuples.append(my_tuple)
    return my_tuples
