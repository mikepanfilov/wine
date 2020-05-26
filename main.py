from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime as dt
import pandas as pd
import collections

years_since = dt.date.today().year - 1920

df = pd.read_excel('wine3.xlsx').fillna('')
wines = df.to_dict(orient='record')

grouped_by_category_wines = collections.defaultdict(list)
for wine in wines:
  grouped_by_category_wines[wine['Категория']].append(wine)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    grouped_by_category_wines = grouped_by_category_wines,
    years = years_since,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()