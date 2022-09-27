import sqlite3

from flask import Flask, json


app = Flask(__name__)


def get_data_by_sql(sql):
    with sqlite3.connect('netflix.db') as connection:
        connection.row_factory = sqlite3.Row

        result = connection.execute(sql).fetchall()

    return result


@app.get('/movie/<title>/')
def step_1(title):
    result = {}
    for item in get_data_by_sql(sql=f"""
            SELECT title, country, release_year, listed_in as genre, description
            FROM netflix
            WHERE title = '{title}'
            ORDER BY release_year DESC
            LIMIT 1
            """):
        result = dict(item)

    return app.response_class(
        json.dumps(result, ensure_ascii=False, indent=8),
        # minetype="application/json",
        status=200
    )


@app.get('/movie/<int:year1>/to/<int:year2>/')
def step_2(year1, year2):
    sql = f"""
        SELECT title, release_year
        FROM netflix
        WHERE release_year BETWEEN {year1} AND {year2}
        LIMIT 100
        """
    result = []

    for item in get_data_by_sql(sql):
        result.append(
                dict(item)
        )

    return app.response_class(
        json.dumps(result, ensure_ascii=False, indent=8),
        # minetype="application/json",
        status=200
    )


@app.get('/rating/<rating>/')
def step_3(rating):
    my_rating = {
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }
    sql = f"""
        SELECT title, rating, release_year
        FROM netflix
        WHERE rating in {my_rating.get(rating)}
        LIMIT 100
        """
    result = []

    for item in get_data_by_sql(sql):
        result.append(
                dict(item)
        )

    return app.response_class(
        json.dumps(result, ensure_ascii=False, indent=8),
        # minetype="application/json",
        status=200
    )


@app.get('/genre/<genre>/')
def step_4(genre):
    my_rating = {
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }
    sql = f"""
        SELECT show_id, title
        FROM netflix
        WHERE listed_in LIKE "%{str(genre).title()}%"
        LIMIT 10
        """
    result = []

    for item in get_data_by_sql(sql):
        result.append(
                dict(item)
        )

    return app.response_class(
        json.dumps(result, ensure_ascii=False, indent=8),
        # minetype="application/json",
        status=200
    )


def step_5(name_1, named_2):
    sql = f"""
            SELECT *
            FROM netflix
            WHERE "cast" LIKE "%{name_1}%"
            AND "cast" LIKE "%{named_2}%"
            """

    names_dict = {}

    for item in get_data_by_sql(sql):
        result = dict(item)

        names = set(result.get("cast").split(", "))-set([name_1, named_2])

        for name in names:
            names_dict[name.strip()] = names_dict.get(name.strip(), 0) + 1

    print(names_dict)

    for key, value in names_dict.items():
        if value > 2:
            print(key)


def step_6(types, release_year, genre):
    sql = f"""
            SELECT *
            FROM netflix
            WHERE type like '{types.title()}' AND release_year like '{release_year}' AND listed_in like '%{genre.title()}%'
            """

    result = []

    for item in get_data_by_sql(sql):
        result.append(
            dict(item)
        )

    return json.dumps(result, ensure_ascii=False, indent=8)


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)

