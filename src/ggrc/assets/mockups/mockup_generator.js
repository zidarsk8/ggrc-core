/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE- 0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (GGRC, _) {
  var FIRST_NAMES = 'James Christopher Ronald Mary Lisa Michelle John Daniel Anthony Patricia Nancy Laura Robert Paul Kevin Linda Karen Sarah Michael Mark Jason Barbara Betty Kimberly William Donald Jeff Elizabeth Helen Deborah David George Jennifer Sandra Richard Kenneth Maria Donna Charles Steven Susan Carol Joseph Edward Margaret Ruth Thomas Brian Dorothy Sharon'.split(' ');
  var LAST_NAMES = 'Smith Anderson Clark Wright Mitchell Johnson Thomas Rodriguez Lopez Perez Williams Jackson Lewis Hill Roberts Jones White Lee Scott Turner Brown Harris Walker Green Phillips Davis Martin Hall Adams Campbell Miller Thompson Allen Baker Parker Wilson Garcia Young Gonzalez Evans Moore Martinez Hernandez Nelson Edwards Taylor Robinson King Carter Collins'.split(' ');
  var WORDS = 'all undertaken by government market network over family tribe formal informal organization territory through laws norms power language relates processes interaction decision-making among actors involved collective problem that lead creation reinforcement reproduction social norms institutions distinguish term governance from government government formal body invested with authority make decisions given political system this case governance process which includes all actors involved influencing decision-making process such as lobbies parties medias centered on relevant governing body whether organization geopolitical entity nation-state corporation business organization incorporated as legal entity socio-political entity chiefdom tribe family etc an informal one its governance way rules norms actions are produced sustained regulated held accountable degree formality depends on internal rules given organization absence actors administer affecting aimed already also among analysed analytical any apply applying approaches are article articulated as associated assure at authority authors banks based be becht beginning being best between board boards bolton both business by called can century citizens clear coherent collective community complex concept connections consists contrast control corporate corporation corporation creating customers customs deals decisions defined denote describe describes differences direct directioncorporate directors documented edit eells empirical employees environment environmental equals especially established example exercise exist explicit fiduciary finance first five focus focuses for form formal found framework free from functioning gaf generate global goal goals governance governancecorporate governanceglobal governanceinformation governanceinternet governanceit governance government group has have however in include includes independent industry informal information institutions inter- interact interchangeable interdependent interests international internet investigating investment involved is issues it itself james large laws lenders like logically main make management manner many markets meaning mechanisms mediated methodology mission mitigate need needs nodal non-governmental non-normative non-profit norms obligations observed of often older on or organization organizations other over overarching people perspective pg plane players points policies policy political polity postulated practical primarily principal problems processes project projects proposes public regarding regular regulation regulators reinforcing relations relationship relationships research respect responsibility richard right risks rules sector serves set shareholders social society some sometimes stakeholders states structure successful suppliers system technology term terms textbooks their these those through thus tool traditional trust trustees understood units unlike up use used value various was way where wherever which whom with word'.split(' ');
  var SITES = [{
    title: 'AdMob',
    domain: 'admob.com'
  }, {
    title: 'AdSense',
    domain: 'adsense.com'
  }, {
    title: 'AdWords',
    domain: 'adwords.com'
  }, {
    title: 'Android',
    domain: 'android.com'
  }, {
    title: 'Blogger',
    domain: 'blogger.com'
  }, {
    title: 'Chromium',
    domain: 'chromium.org'
  }, {
    title: 'Google Chrome',
    domain: 'chrome.com'
  }, {
    title: 'Chromebook',
    domain: 'chromebook.com'
  }, {
    title: 'Google Member',
    domain: 'googlemember.com'
  }, {
    title: 'Google Members',
    domain: 'googlemembers.com'
  }, {
    title: 'elgooG',
    domain: 'com.google'
  }, {
    title: 'FeedBurner',
    domain: 'feedburner.com'
  }, {
    title: 'DoubleClick',
    domain: 'doubleclick.com'
  }, {
    title: 'iGoogle',
    domain: 'igoogle.com'
  }, {
    title: 'Froogle',
    domain: 'froogle.com'
  }, {
    title: 'Google Analytics',
    domain: 'googleanalytics.com'
  }, {
    title: 'Google Code',
    domain: 'googlecode.com'
  }, {
    title: 'Google Developer Source',
    domain: 'googlesource.com'
  }, {
    title: 'Google Drive',
    domain: 'googledrive.com'
  }, {
    title: 'Google Earth',
    domain: 'googlearth.com'
  }, {
    title: 'Google Maps',
    domain: 'googlemaps.com'
  }, {
    title: 'Google Page Creator',
    domain: 'googlepagecreator.com'
  }, {
    title: 'Google Scholar',
    domain: 'googlescholar.com'
  }, {
    title: 'Gmail',
    domain: 'gmail.com'
  }, {
    title: 'Keyhole',
    domain: 'keyhole.com'
  }, {
    title: 'Made with Code',
    domain: 'madewithcode.com'
  }, {
    title: 'Panoramio',
    domain: 'panoramio.com'
  }, {
    title: 'Picasa',
    domain: 'picasa.com'
  }, {
    title: 'SketchUp',
    domain: 'sketchup.com'
  }, {
    title: 'Google Analytics',
    domain: 'urchin.com'
  }, {
    title: 'Waze',
    domain: 'waze.com'
  }, {
    title: 'YouTube',
    domain: 'youtube.com'
  }, {
    title: 'Google.org',
    domain: 'google.org'
  }, {
    title: 'Google',
    domain: 'goolge.com'
  }, {
    title: 'Google URL Shortener',
    domain: 'goo.gl'
  }];

  var g = function () {
    this.u = g.user();
    this.d = g.get_date({today: true});
    return this;
  };
  g.user = function (options) {
    var types;
    options = options || {};
    types = 'assignee requester verifier assessor'.split(' ');
    return {
      name: g.get_random(FIRST_NAMES) + ' ' + g.get_random(LAST_NAMES),
      type: options.type || g.get_random(options.types || types)
    };
  };
  g.url = function () {
    var site = g.get_random(SITES);
    return {
      icon: 'url',
      extension: 'url',
      timestamp: g.get_date({year: 2015}),
      name: site.title,
      url: 'http://' + site.domain
    };
  };
  g.get_random = function (arr) {
    return arr[_.random(0, arr.length - 1)];
  };
  g.get_words = function (count, join, arr) {
    count = count || 1;
    arr = arr || WORDS;
    join = join || ' ';
    return _.map(_.times(count, _.partial(_.random, 0, arr.length - 1, false)), function (num) {
      return arr[num];
    }).join(join);
  };
  g.title = function (len) {
    return _.startCase(g.get_words(_.random(3, 7)));
  };
  g.sentence = function (len) {
    var punctuation = '.';
    var sentence = g.get_words(_.random(3, len || 15));
    return _.capitalize(sentence) + punctuation;
  };
  g.paragraph = function (count) {
    if (count === 0) {
      return '';
    }
    return _.trim(_.times(count || 1, g.sentence).join(' '));
  };
  g.file = function (options) {
    var types;
    var name;
    var extension;
    options = options || {};
    types = 'pdf txt xls doc jpg zip '.split(' ');
    name = g.get_words(_.random(3, 7), '_');
    extension = g.get_random(types);

    return {
      name: name + (extension ? '.' + extension : ''),
      extension: extension || '',
      icon: extension || '',
      timestamp: g.get_date(),
      url: 'http:/google.com'
    };
  };
  g.get_date = function (data) {
    data = data || {};
    if (data.today) {
      return moment().format(data.format || 'MM/DD/YYYY');
    }
    data.month = data.month || _.random(1, 12);
    data.day = data.day || _.random(1, 31);
    data.year = data.year || _.random(2003, 2015);

    // TODO: Moment knows how to handle invalid dates, so I don't care
    return moment(data.month + '-' + data.day + '-' + data.year)
      .format(data.format || 'MM/DD/YYYY');
  };
  g.get_id = function (data) {
    data = data || {};

    return Number(_.uniqueId());
  };
  g.comment = function (options) {
    options = options || {};
    return {
      author: g.user({types: options.type || options.types}),
      timestamp: g.get_date({year: 2015}),
      comment: g.paragraph(_.random(0, 10)),
      attachments: g.get('file|url', _.random(0, 3))
    };
  };
  g.request = function () {
    return {
      timestamp: g.get_date({year: 2015}),
      title: g.title(),
      files: g.get('file', _.random(1, 5))
    };
  };
  g._sort_by_date = function (arr) {
    return _.sortBy(arr, function (item) {
      return moment(item.date).unix();
    }).reverse();
  };
  g.get = function (types, count, options) {
    var values;
    function getTypeFn(type) {
      var fn = g[type] || g[type.slice(0, -1)] || g['get_' + type];
      if (!type || !fn) {
        return;
      }
      return fn;
    }
    types = _.map(types.split('|'), getTypeFn);
    options = options || {};
    if (count === 'random') {
      count = _.random(0, 5);
    }
    if (count === 0) {
      return [];
    }
    values = _.times(count || 1, _.partial(g.get_random(types), options));
    if (options.sort === 'date') {
      return g._sort_by_date(values);
    }
    return values;
  };
  g._create_single = function (data, options) {
    var alias = {
      date: 'get_date',
      id: 'get_id',
      title: 'title',
      timestamp: 'get_date',
      text: 'paragraph',
      user: 'user',
      files: 'file'
    };
    var rGenerator = /^\%\S+$/i;
    var result = {};

    _.each(data, function (val, prop) {
      if (_.isArray(options.randomize) ? _.indexOf(options.randomize, prop) !== -1 : options.randomize === prop) {
        if (_.every(val, _.isString)) {
          result[prop] = g.get_random(val);
          return;
        }
        result[prop] = g._create_single(g.get_random(val), options);
        return;
      }
      if (rGenerator.test(val)) {
        result[prop] = g[alias[val.substr(1)]]();
      } else if (_.isObject(val) && !_.isEmpty(val)) {
        result[prop] = g._create_single(val, options);
      } else if (!_.isNumber(prop)) {
        result[prop] = val;
      }
    });
    return result;
  };
  g.create = function (data, options) {
    options = options || {};
    return _.times(options.count || 1, _.partial(this._create_single, data, options));
  };

  GGRC.Mockup = GGRC.Mockup || {};
  GGRC.Mockup.Generator = GGRC.Mockup.Generator || g;
  GGRC.Mockup.Generator.current = GGRC.Mockup.Generator.current || new g();
})(this.GGRC, this._);
