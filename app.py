from itertools import count
import os
from flask import Flask, abort, render_template, request, send_from_directory, url_for
from capsdata import CapsData
from os.path import exists
import urllib.parse

app = Flask(__name__)
data = CapsData()


test = '<ul>'
test += f'<li><a href="/wyswietl/">Wszystkie kapsle ({data.count_caps()})</a>'
for country_name in data.country_names:
    test += f'<li><a href="/wyswietl/{urllib.parse.quote(country_name)}/">{country_name} ({data.count_caps(country_name)})</a>'
    if data.companies_by_country(country_name):
        test += '<ul>'
        for company_name in data.companies_by_country(country_name):
            test += f'<li><a href="/wyswietl/{urllib.parse.quote(country_name)}/{urllib.parse.quote(company_name)}/">{company_name} ({data.count_caps(country_name, company_name)})</a>'
            if data.breweries_by_company(country_name, company_name):
                test += '<ul>'
                for brewery_name in data.breweries_by_company(country_name, company_name):
                    test += f'<li><a href="/wyswietl/{urllib.parse.quote(country_name)}/{urllib.parse.quote(company_name)}/{urllib.parse.quote(brewery_name)}/">{brewery_name} ({data.count_caps(country_name, company_name, brewery_name)})</a></li>'
                test += '</ul>'
            test += '</li>'
        test += '</ul>'
test += '</li></ul>'
with open('templates/list.html', 'w', encoding='UTF8') as f:
    f.write(test)

test = '<ul>'
test += f'<li><a href="/wymiana/wyswietl/">Wszystkie kapsle ({data.count_caps(only_trade=True)})</a>'
for country_name in data.country_names:
    c = data.count_caps(country_name, only_trade=True)
    if c > 0:
        test += f'<li><a href="/wymiana/wyswietl/{urllib.parse.quote(country_name)}/">{country_name} ({c})</a>'
        if data.companies_by_country(country_name):
            test += '<ul>'
            for company_name in data.companies_by_country(country_name):
                c = data.count_caps(country_name, company_name, only_trade=True)
                if c > 0:
                    test += f'<li><a href="/wymiana/wyswietl/{urllib.parse.quote(country_name)}/{urllib.parse.quote(company_name)}/">{company_name} ({c})</a>'
                    if data.breweries_by_company(country_name, company_name):
                        test += '<ul>'
                        for brewery_name in data.breweries_by_company(country_name, company_name):
                            c = data.count_caps(country_name, company_name, brewery_name, only_trade=True)
                            if c > 0:
                                test += f'<li><a href="/wymiana/wyswietl/{urllib.parse.quote(country_name)}/{urllib.parse.quote(company_name)}/{urllib.parse.quote(brewery_name)}/">{brewery_name} ({c})</a></li>'
                        test += '</ul>'
                    test += '</li>'
            test += '</ul>'
test += '</li></ul>'
with open('templates/list-trade.html', 'w', encoding='UTF8') as f:
    f.write(test)

def image_url(image_id):
    if exists(f'static/img/{image_id}.png'):
        return url_for('static', filename=f'img/{image_id}.png')
    if exists(f'static/img/{image_id}.gif'):
        return url_for('static', filename=f'img/{image_id}.gif')
    return url_for('static', filename=f'img/{image_id}.jpg')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wyswietl/')
def show_all():
    country = 'ALL'
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    if limit is None or int(limit) > 500:
        limit = 500
    elif int(limit) < 1:
        limit = 1
    else:
        limit = int(limit)
    if offset is None:
        offset = 0
    else:
        offset = int(offset)
    if offset < 0:
        abort(500)
    ids = data.ids_by_country(country)
    count = len(ids)
    ids = ids[offset:limit + offset]
    urls = {}
    for i in ids:
        urls[i] = image_url(i)
    if len(ids) == 0:
        abort(500)
    page = offset//limit+1
    pages = count//limit+1
    return render_template('show.html', ids=ids, urls=urls, page=page, pages=pages, limit=limit, results=len(ids))

@app.route('/missingdata/<name>/<country>')
def show_missing(name, country):
    name = urllib.parse.unquote(name)
    country = urllib.parse.unquote(country)
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    if limit is None or int(limit) > 500:
        limit = 500
    elif int(limit) < 1:
        limit = 1
    else:
        limit = int(limit)
    if offset is None:
        offset = 0
    else:
        offset = int(offset)
    if offset < 0:
        abort(500)
    ids2 = data.ids_by_country(country)
    ids = []
    if len(ids2) == 0:
        abort(500)
    big = []
    for id in ids2:
        details = data.details_by_id(id)
        if 'd' in details['info']:
            big.append(id)
        if  not name in details:
            ids.append(id)
    urls = {}
    for i in ids:
        urls[i] = image_url(i)
    count = len(ids)
    ids = ids[offset:limit + offset]
    page = offset//limit+1
    pages = count//limit+1
    return render_template('show.html', ids=ids, urls=urls, page=page, pages=pages, limit=limit, results=len(ids), big=big)

@app.route('/wyswietl/<country>/')
def show_country(country):
    country = urllib.parse.unquote(country)
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    if limit is None or int(limit) > 500:
        limit = 500
    elif int(limit) < 1:
        limit = 1
    else:
        limit = int(limit)
    if offset is None:
        offset = 0
    else:
        offset = int(offset)
    if offset < 0:
        abort(500)
    ids = data.ids_by_country(country)
    count = len(ids)
    ids = ids[offset:limit + offset]
    if len(ids) == 0:
        abort(500)
    big = []
    for id in ids:
        if 'd' in data.details_by_id(id)['info']:
            big.append(id)
    urls = {}
    for i in ids:
        urls[i] = image_url(i)
    page = offset//limit+1
    pages = count//limit+1
    return render_template('show.html', ids=ids, urls=urls, page=page, pages=pages, limit=limit, results=data.count_caps(country), big=big)


@app.route('/wyswietl/<country>/<company>/')
def show_company(country, company):
    country = urllib.parse.unquote(country)
    company = urllib.parse.unquote(company)
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    if limit is None or int(limit) > 500:
        limit = 500
    elif int(limit) < 1:
        limit = 1
    else:
        limit = int(limit)
    if offset is None:
        offset = 0
    else:
        offset = int(offset)
    if offset < 0:
        abort(500)
    ids = data.ids_by_company(country, company)
    count = len(ids)
    ids = ids[offset:limit + offset]
    urls = {}
    for i in ids:
        urls[i] = image_url(i)
    if len(ids) == 0:
        abort(500)
    page = offset//limit+1
    pages = count//limit+1
    big = []
    for id in ids:
        if 'd' in data.details_by_id(id)['info']:
            big.append(id)
    return render_template('show.html', ids=ids, urls=urls, page=page, pages=pages, limit=limit, results=data.count_caps(country, company), big=big)


@app.route('/wyswietl/<country>/<company>/<brewery>/')
def show_brewery(country, company, brewery):
    country = urllib.parse.unquote(country)
    company = urllib.parse.unquote(company)
    brewery = urllib.parse.unquote(brewery)
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    if limit is None or int(limit) > 500:
        limit = 500
    else:
        limit = int(limit)
    if offset is None:
        offset = 0
    else:
        offset = int(offset)
    if offset < 0:
        abort(500)
    ids = data.ids_by_brewery(country, company, brewery)
    count = len(ids)
    ids = ids[offset:limit + offset]
    urls = {}
    for i in ids:
        urls[i] = image_url(i)
    if len(ids) == 0:
        abort(500)
    page = offset//limit+1
    pages = count//limit+1
    big = []
    for id in ids:
        if 'd' in data.details_by_id(id)['info']:
            big.append(id)
    return render_template('show.html', ids=ids, urls=urls, page=page, pages=pages, limit=limit, results=data.count_caps(country, company, brewery), big=big)


@app.route('/kapsel/<cap_id>')
def cap_details(cap_id):
    details = data.details_by_id(int(cap_id))
    images = []
    if 'x' in details['info']:
        images.append(image_url(cap_id+'p'))
        images.append(image_url(cap_id+'t'))
    else:
        images.append(image_url(cap_id))
    country = details['country'].replace(' ', '%20')
    try:
        company = details['company'].replace(' ', '%20')
    except KeyError:
        company = ''
    try:
        brewery = details['brewery'].replace(' ', '%20')
    except KeyError:
        brewery = ''
    return render_template('details.html', id=cap_id, details=details, images=images, country=country, company=company, brewery=brewery)


@app.route('/wymiana/')
def trade():
    return render_template('trade.html')

@app.route('/wymiana/wyswietl/')
def show_all_trade():
    country = 'ALL'
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    if limit is None or int(limit) > 500:
        limit = 500
    elif int(limit) < 1:
        limit = 1
    else:
        limit = int(limit)
    if offset is None or int(offset) < 0:
        offset = 0
    else:
        offset = int(offset)
    ids = data.ids_by_country(country, only_trade=True)
    count = len(ids)
    ids = ids[offset:limit + offset]
    urls = {}
    for i in ids:
        urls[i] = image_url(i)
    if len(ids) == 0:
        abort(500)
    page = offset//limit+1
    pages = count//limit+1
    return render_template('show-trade.html', ids=ids, urls=urls, page=page, pages=pages, limit=limit, results=count)


@app.route('/wymiana/wyswietl/<country>/')
def show_country_trade(country):
    country = urllib.parse.unquote(country)
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    if limit is None or int(limit) > 500:
        limit = 500
    elif int(limit) < 1:
        limit = 1
    else:
        limit = int(limit)
    if offset is None:
        offset = 0
    else:
        offset = int(offset)
    if offset < 0:
        abort(500)
    ids = data.ids_by_country(country, only_trade=True)
    count = len(ids)
    ids = ids[offset:limit + offset]
    urls = {}
    for i in ids:
        urls[i] = image_url(i)
    if len(ids) == 0:
        abort(500)
    page = offset//limit+1
    pages = count//limit+1
    return render_template('show-trade.html', ids=ids, urls=urls, page=page, pages=pages, limit=limit, results=count)


@app.route('/wymiana/wyswietl/<country>/<company>/')
def show_company_trade(country, company):
    country = urllib.parse.unquote(country)
    company = urllib.parse.unquote(company)
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    if limit is None or int(limit) > 500:
        limit = 500
    elif int(limit) < 1:
        limit = 1
    else:
        limit = int(limit)
    if offset is None:
        offset = 0
    else:
        offset = int(offset)
    if offset < 0:
        abort(500)
    ids = data.ids_by_company(country, company, only_trade=True)
    count = len(ids)
    ids = ids[offset:limit + offset]
    urls = {}
    for i in ids:
        urls[i] = image_url(i)
    if len(ids) == 0:
        abort(500)
    page = offset//limit+1
    pages = count//limit+1
    return render_template('show-trade.html', ids=ids, urls=urls, page=page, pages=pages, limit=limit, results=count)


@app.route('/wymiana/wyswietl/<country>/<company>/<brewery>/')
def show_brewery_trade(country, company, brewery):
    country = urllib.parse.unquote(country)
    company = urllib.parse.unquote(company)
    brewery = urllib.parse.unquote(brewery)
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    if limit is None or int(limit) > 500:
        limit = 500
    elif int(limit) < 1:
        limit = 1
    else:
        limit = int(limit)
    if offset is None:
        offset = 0
    else:
        offset = int(offset)
    if offset < 0:
        abort(500)
    ids = data.ids_by_brewery(country, company, brewery, only_trade=True)
    count = len(ids)
    ids = ids[offset:limit + offset]
    urls = {}
    for i in ids:
        urls[i] = image_url(i)
    if len(ids) == 0:
        abort(500)
    page = offset//limit+1
    pages = count//limit+1
    return render_template('show-trade.html', ids=ids, urls=urls, page=page, pages=pages, limit=limit, results=count)


@app.route('/kontakt')
def contact():
    return render_template('kontakt.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run()
