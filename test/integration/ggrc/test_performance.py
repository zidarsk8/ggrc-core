# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import time

from ggrc.app import app
from integration.ggrc import TestCase


class TestApiCalls(TestCase):

  def setUp(self):
    self.client.get("/login")
    self.headers = {
        "Content-Type": "application/json",
        "X-Requested-By": "gGRC",
        "X-Requested-With": "XMLHttpRequest",
    }

  def _get(self, url):
    return self.client.get(url, headers=self.headers)

  def test_id_in_calls(self):
    self._get("http://localhost:8080/api/sections?id__in=1292%2C1294%2C1295"
              "%2C1296%2C1297%2C1298%2C1300%2C1301%2C1304%2C1305%2C1311%2C1312"
              "%2C1315%2C1316%2C1317%2C1318%2C1320%2C1321%2C1322%2C1323%2C1325"
              "%2C1326%2C1327%2C1328%2C1329%2C1330%2C1339%2C1341%2C1351%2C1352"
              "%2C1484%2C1496%2C1497%2C1499%2C1500%2C1501%2C1504%2C1505%2C1508"
              "%2C1512%2C1516%2C1517%2C1533%2C1535%2C1541%2C1545%2C1566%2C1568"
              "%2C1581%2C1582%2C1584%2C1585%2C1706%2C1861%2C1055%2C1726%2C1832"
              "%2C1738%2C1737%2C1862%2C44%2C72%2C73%2C75%2C71%2C78%2C55%2C1846"
              "%2C60%2C68%2C69%2C61%2C112%2C113%2C115%2C62%2C63%2C64%2C65%2C66"
              "%2C67%2C59%2C788%2C1235%2C892%2C809%2C167%2C710%2C744%2C1010"
              "%2C1022%2C1838%2C1550%2C1632%2C694%2C878%2C879%2C887%2C939"
              "%2C1069%2C1072%2C1427%2C1050%2C1105%2C1429%2C789%2C790%2C791"
              "%2C792%2C1073%2C916%2C121%2C1747%2C1428%2C1421%2C1422%2C1083"
              "%2C1084%2C1085%2C915%2C1234%2C1863%2C1814%2C1052%2C1041%2C95"
              "%2C96%2C1815%2C105%2C111%2C114%2C1079%2C1151%2C1830%2C1807%2C7"
              "%2C516%2C1209&_={}".format(time.time()))
    import ipdb; ipdb.set_trace()
    from ggrc.utils import benchmark
    print benchmark.results
    self.assertTrue(False)
