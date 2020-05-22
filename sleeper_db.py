import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.request import Request
import numpy as np
import time

#web scrape 1st table on the page below
#.decode() added because of py3
year = 2019
url = 'https://www.pro-football-reference.com/years/2019/receiving.htm'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
time.sleep(1)
table = soup.findAll('table')[0].decode()
dfs = pd.read_html(table, header=0)
df = dfs[0]

#filter
df['Player'] = df['Player'].str.rstrip('*, +')
pos = ['WR', 'RB', 'TE']
df_rec = df[df.Pos.str.contains('|'.join(pos), na=False)]

#Export to html
html_string = '''
<html>
  <head><title>Sleeper_DB</title></head>
  <link rel="stylesheet" type="text/css" href="df_style.scss"/>
  <script src="app.js"></script>
  <body>
    <h1>NFL Top Receptions</h1>
    <input type="text" id="myInput" onkeyup="myFunction()" placeholder="Search for names.." title="Type in a name">
    {table}
  </body>
</html>
'''
# OUTPUT AN HTML FILE
with open('index.html', 'w') as f:
    # f.write(html_string.format(table=df_rec.to_html(classes='mystyle')))
    f.write(html_string.format(table=df_rec.to_html(classes='mystyle', table_id='dataframe')))
