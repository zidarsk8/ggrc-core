/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE- 0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (GGRC, _) {
  var FIRST_NAMES = "James Christopher Ronald Mary Lisa Michelle John Daniel Anthony Patricia Nancy Laura Robert Paul Kevin Linda Karen Sarah Michael Mark Jason Barbara Betty Kimberly William Donald Jeff Elizabeth Helen Deborah David George Jennifer Sandra Richard Kenneth Maria Donna Charles Steven Susan Carol Joseph Edward Margaret Ruth Thomas Brian Dorothy Sharon".split(" "),
      LAST_NAMES = "Smith Anderson Clark Wright Mitchell Johnson Thomas Rodriguez Lopez Perez Williams Jackson Lewis Hill Roberts Jones White Lee Scott Turner Brown Harris Walker Green Phillips Davis Martin Hall Adams Campbell Miller Thompson Allen Baker Parker Wilson Garcia Young Gonzalez Evans Moore Martinez Hernandez Nelson Edwards Taylor Robinson King Carter Collins".split(" "),
      WORDS = "all undertaken by government market network over family tribe formal informal organization territory through laws norms power language relates processes interaction decision-making among actors involved collective problem that lead creation reinforcement reproduction social norms institutions distinguish term governance from government government formal body invested with authority make decisions given political system this case governance process which includes all actors involved influencing decision-making process such as lobbies parties medias centered on relevant governing body whether organization geopolitical entity nation-state corporation business organization incorporated as legal entity socio-political entity chiefdom tribe family etc an informal one its governance way rules norms actions are produced sustained regulated held accountable degree formality depends on internal rules given organization absence actors administer affecting aimed already also among analysed analytical any apply applying approaches are article articulated as associated assure at authority authors banks based be becht beginning being best between board boards bolton both business by called can century citizens clear coherent collective community complex concept connections consists contrast control corporate corporation corporation creating customers customs deals decisions defined denote describe describes differences direct directioncorporate directors documented edit eells empirical employees environment environmental equals especially established example exercise exist explicit fiduciary finance first five focus focuses for form formal found framework free from functioning gaf generate global goal goals governance governancecorporate governanceglobal governanceinformation governanceinternet governanceit governance government group has have however in include includes independent industry informal information institutions inter- interact interchangeable interdependent interests international internet investigating investment involved is issues it itself james large laws lenders like logically main make management manner many markets meaning mechanisms mediated methodology mission mitigate need needs nodal non-governmental non-normative non-profit norms obligations observed of often older on or organization organizations other over overarching people perspective pg plane players points policies policy political polity postulated practical primarily principal problems processes project projects proposes public regarding regular regulation regulators reinforcing relations relationship relationships research respect responsibility richard right risks rules sector serves set shareholders social society some sometimes stakeholders states structure successful suppliers system technology term terms textbooks their these those through thus tool traditional trust trustees understood units unlike up use used value various was way where wherever which whom with word".split(" ");

  function g() {
    return this;
  }
  g.user = function () {
    return {
      name: g.get_random(FIRST_NAMES) + " " + g.get_random(LAST_NAMES)
    };
  };
  g.users = function (count) {
    return _.times(count || 1, g.user);
  };
  g.get_random = function (arr) {
    return arr[_.random(0, arr.length - 1)];
  };
  g.get_words = function (count, join, arr) {
    count = count || 1;
    arr = arr || WORDS;
    join = join || " ";
    return _.map(_.times(count, _.partial(_.random, 0, arr.length - 1, false)), function (num) {
      return arr[num];
    }).join(join);
  };
  g.title = function (len) {
    return _.startCase(g.get_words(_.random(3, 7)));
  };
  g.sentence = function (len) {
    var punctuation = ".",
        sentence = g.get_words(_.random(3, len || 15));
    return _.capitalize(sentence) + punctuation;
  };
  g.paragraph = function (count) {
    if (count === 0) {
      return "";
    }
    return _.trim(_.times(count || 1, g.sentence).join(" "));
  };
  g.file = function () {
    var types = "pdf txt xls doc img zip url ".split(" "),
        name = g.get_words(_.random(3, 7), "_"),
        extension = g.get_random(types);

    return {
      name: name + (extension ? "." + extension : ""),
      icon: extension || "",
      date: g.get_date(),
      url: "http:/google.com"
    };
  };
  g.get_date = function (data) {
    data = data || {};
    data.month = data.month || _.random(1, 12);
    data.day = data.day || _.random(1, 31);
    data.year = data.year || _.random(2003, 2015);

    // TODO: Moment knows how to handle invalid dates, so I don't care
    return moment(data.month + "-" + data.day + "-" + data.year).format(data.format || "MM/DD/YYYY");
  };
  g.files = function (count, options) {
    if (count === 0) {
      return [];
    }
    options = options || {};
    var files = _.times(count || 1, g.file);
    if (options.sort === "date") {
      return g._sort_by_date(files);
    }
    return files;
  };
  g.comment = function () {
    var types = "assignee requester verifier".split(" ");
    return {
      type: g.get_random(types),
      author: g.user(),
      date: g.get_date({year: 2015}),
      comment: g.paragraph(_.random(0, 10)),
      attachments: g.files(_.random(0, 3))
    };
  },
  g.comments = function (count, options) {
    options = options || {};
    var comments = _.times(count || 1, g.comment);
    if (options.sort === "date") {
      return g._sort_by_date(comments);
    }
    return comments;
  };
  g.request = function () {
    return {
      date: g.get_date({year: 2015}),
      title: g.title(),
      files: g.files(_.random(1, 5))
    };
  };
  g.requests = function (count) {
    return _.times(count || 1, g.request);
  }
  g._sort_by_date = function (arr) {
    return _.sortBy(arr, function (item) {
      return moment(item.date).unix();
    }).reverse();
  };
  GGRC.Mockup = GGRC.Mockup || {};
  GGRC.Mockup.Generator = GGRC.Mockup.Generator || g;
})(this.GGRC, this._);
