# GGRC_BENCHMARK=true ipython

import cgi

import bleach
from HTMLParser import HTMLParser
parser = HTMLParser()

from lxml.html.clean import Cleaner
cleaner = Cleaner()

import ggrc
from ggrc import app
from ggrc.utils import benchmark


html1 = '''
 <html>
  <head>
    <script type="text/javascript" src="evil-site"></script>
    <link rel="alternate" type="text/rss" src="evil-rss">
    <style>
      body {background-image: url(javascript:do_evil)};
      div {color: expression(evil)};
    </style>
    <script>alert("hiya");</script>
  </head>
  <body onload="evil_function()">
    <!-- I am interpreted for EVIL! -->
    <a href="javascript:evil_function()">a link</a>
    <a href="#" onclick="evil_function()">another link</a>
    <p onclick="evil_function()">a paragraph</p>
    <div style="display: none">secret EVIL!</div>
    <object> of EVIL! </object>
    <iframe src="evil-site"></iframe>
    <form action="evil-site">
      Password: <input type="password" name="password">
    </form>
    <blink>annoying EVIL!</blink>
    <a href="evil-site">spam spam SPAM!</a>
    <image src="evil!">
  </body>
 </html>
'''

with benchmark('bleach'):
    for _ in range(0, 10000):
        parser.unescape(bleach.clean(html1, strip=True))

with benchmark('bleach no unescape'):
    for _ in range(0, 10000):
        bleach.clean(html1, strip=True)

with benchmark('lxml'):
    for _ in range(0, 100000):
        cleaner.clean_html(html1)

with benchmark('cgi'):
    for _ in range(0, 100000):
        cgi.escape(html1)

# RESULTS
# --------------------------------------------
# sum:  20.53816  - count:    1.00000  - avg 20.53816 - max: 20.53816  - min: 20.53816  - bleach
# sum:   9.28157  - count:    1.00000  - avg  9.28157 - max:  9.28157  - min:  9.28157  - bleach no unescape
# sum:   3.54578  - count:    1.00000  - avg  3.54578 - max:  3.54578  - min:  3.54578  - lxml
# sum:   0.02205  - count:    1.00000  - avg  0.02205 - max:  0.02205  - min:  0.02205  - cgi
