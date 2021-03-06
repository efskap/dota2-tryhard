from collections import defaultdict
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from urllib2 import urlopen

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/compute', methods=['POST'])
def compute():
    # fetch enemy heroes from the request, and strip out empty inputs
    enemy_heroes = [x for x in request.form.getlist('heroes') if x != ""]
    counters = {}
    for enemy_hero in enemy_heroes:
        counters[enemy_hero] = get_counters(enemy_hero)  # download counters and cache them
    total_counters = {}
    for enemy_hero in enemy_heroes:
        total_counters = d_sum(total_counters, counters[enemy_hero])  # now add the advantages
    sorted_list = []
    for hero in sorted(total_counters, key=total_counters.get, reverse=True):  # sort by advantages
        if hero not in enemy_heroes:  # can't pick a hero if enemy already picked him!
            col = [hero, str(total_counters[hero]) + "%"] # build first two columns
            for enemy_hero in enemy_heroes:
                col.append(str(counters[enemy_hero][hero]) + "%")  # add per-hero advantage columns
            sorted_list.append(col)
    header = ['Hero', 'Total Advantage']  # headers for first two columns
    for enemy_hero in enemy_heroes:
        header.append('vs. %s' % enemy_hero)  # headers for the rest
    return render_template('results.html', x=sorted_list, header=header)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500


def get_counters(hero):
    url = 'http://dotabuff.com/heroes/%s/matchups' % hero_name_to_url_format(hero)
    soup = BeautifulSoup(urlopen(url).read())
    table = soup.find("tbody")
    counters = {}
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        hero_name = cells[1].find(text=True)
        adv = -1 * float(cells[2].find(text=True).strip('%'))
        counters[hero_name] = adv
    return counters


# from http://stackoverflow.com/questions/877295/python-dict-add-by-valuedict-2
def d_sum(a, b):
    d = defaultdict(int, a)
    for k, v in b.items():
        d[k] += v
    return dict(d)


def hero_name_to_url_format(name):
    return str.lower(str(name)).replace(' ', '-').strip("'")


# unused
def create_hero_a_tag(name):
    return '<a href="http://dotabuff.com/heroes/{0}/">{1}</a>'.format(hero_name_to_url_format(name),name)