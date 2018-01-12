/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('GGRC.query_parser', function () {
  'use strict';

  var parserStructure = {
    parse: jasmine.any(Function),
    join_queries: jasmine.any(Function),
    generated: {
      parse: jasmine.any(Function),
      SyntaxError: jasmine.any(Function),
    },
  };

  it('should exist', function () {
    expect(GGRC.query_parser).toEqual(parserStructure);
  });

  describe('parse', function () {
    it('parses an empty query', function () {
      var emptyResult = {
        expression: {},
        keys: [],
        order_by: {keys: [], order: '', compare: null},
      };

      expect(GGRC.query_parser.parse('')).toEqual(emptyResult);
      expect(GGRC.query_parser.parse(' ')).toEqual(emptyResult);
      expect(GGRC.query_parser.parse(' \t ')).toEqual(emptyResult);
      expect(GGRC.query_parser.parse('\t')).toEqual(emptyResult);
      expect(GGRC.query_parser.parse('    \t')).toEqual(emptyResult);
    });

    it('parses exclude text search queries', function () {
      var textSearchQueries = [
        '!~a',
        '!~word',
        '!~ --this --is',
        '!~ order by something',
        '!~ order by s,thing',
        '!~ order by s,thin  "elese" g',
        '!~7531902 468',
      ];

      can.each(textSearchQueries, function (queryStr) {
        var text = queryStr.replace('!~', '').trim();
        expect(GGRC.query_parser.parse(queryStr)).toEqual({
          expression: {
            text: text,
            op: {name: 'exclude_text_search'},
          },
          order_by: {keys: [], order: '', compare: null},
          keys: [],
        });
      });
    });

    it('parses text search queries', function () {
      var textSearchQueries = [
        'a',
        'word',
        ' --this --is',
        ' order by s,thin  "elese" g',
        '~a',
        '~word',
        '~ --this --is',
        '~ order by something',
        '~ order by s,thing',
        '~ order by s,thin  "elese" g',
        '~7531902 468',
      ];

      can.each(textSearchQueries, function (queryStr) {
        var text = queryStr.replace('~', '').trim();
        expect(GGRC.query_parser.parse(queryStr)).toEqual({
          expression: {
            text: text,
            op: {name: 'text_search'},
          },
          order_by: {keys: [], order: '', compare: null},
          keys: [],
        });
      });
    });

    it('parses simple queries', () => {
      const operators = [
        '=',
        '!=',
        '<',
        '<=',
        '>',
        '>=',
        '~',
        '!~',
      ];

      can.each(operators, (op) => {
        let simpleQueries = [
          `a${op}b`,
          ` with ${op} spaces`,
          `but${op} not_all_spaces  `,
          `"last updated"${op} 01/03/2018  `,
          `"last updated"${op} "with spaces"  `,
        ];

        can.each(simpleQueries, function (queryStr) {
          var query = queryStr.split(op);
          expect(GGRC.query_parser.parse(queryStr)).toEqual({
            expression: {
              left: query[0].trim().replace(/"/g, ''),
              op: {name: op},
              right: query[1].trim().replace(/"/g, ''),
            },
            order_by: {keys: [], order: '', compare: null},
            keys: [query[0].trim().replace(/"/g, '')],
          });
        });
      });
    });

    it('parses \'is\' queries', function () {
      expect(GGRC.query_parser.parse('5words is empty')).toEqual({
        expression: {
          left: '5words',
          op: {name: 'is'},
          right: 'empty',
        },
        order_by: {keys: [], order: '', compare: null},
        keys: ['5words'],
      });
    });
    it('works with order by statement', function () {
      expect(GGRC.query_parser
        .parse('5words ~ just order by some,"name with spaces" desc'))
        .toEqual({
          expression: {
            left: '5words',
            op: {name: '~'},
            right: 'just',
          },
          order_by: {
            keys: ['some', 'name with spaces'],
            order: 'desc',
            compare: jasmine.any(Function),
          },
          keys: ['5words'],
        });
    });

    it('parses \'or\' queries', () => {
      let queries = [
        ' (n = 22 or n = 5)',
        'n = 22 OR n = 5  ',
        'n = 22 || n = 5 ',
        'n = 22||n = 5 ',
        'n = "22"||"n" = 5 ',
        'n = "22"    or ("n" = 5) ',
      ];

      can.each(queries, (query) => {
        expect(GGRC.query_parser.parse(query))
          .toEqual({
            expression: {
              left: {left: 'n', op: {name: '='}, right: '22'},
              op: {name: 'OR'},
              right: {left: 'n', op: {name: '='}, right: '5'},
            },
            order_by: {keys: [], order: '', compare: null},
            keys: ['n'],
          });
      });
    });

    it('parses \'and\' queries', () => {
      let queries = [
        ' (n = 22 and n = 5)',
        'n = 22 AND n = 5  ',
        'n = 22 && n = 5 ',
        'n = 22&&n = 5 ',
        'n = "22"&&"n" = 5 ',
        'n = "22"    and ("n" = 5) ',
      ];

      can.each(queries, (query) => {
        expect(GGRC.query_parser.parse(query))
          .toEqual({
            expression: {
              left: {left: 'n', op: {name: '='}, right: '22'},
              op: {name: 'AND'},
              right: {left: 'n', op: {name: '='}, right: '5'},
            },
            order_by: {keys: [], order: '', compare: null},
            keys: ['n'],
          });
      });
    });

    it('parses relevant queries', function () {
      expect(GGRC.query_parser.parse('#SomeClass,1,2,3,4#'))
        .toEqual({
          expression: {
            object_name: 'SomeClass',
            op: {name: 'relevant'},
            ids: ['1', '2', '3', '4'],
          },
          order_by: {keys: [], order: '', compare: null},
          keys: [],
        });

      expect(GGRC.query_parser.parse('#SomeClass,1,2,3,4# or #A,1# and #B,2#'))
        .toEqual({
          expression: {
            left: {
              object_name: 'SomeClass',
              op: {name: 'relevant'},
              ids: ['1', '2', '3', '4'],
            },
            op: {name: 'OR'},
            right: {
              left: {
                object_name: 'A',
                op: {name: 'relevant'},
                ids: ['1'],
              },
              op: {name: 'AND'},
              right: {
                object_name: 'B',
                op: {name: 'relevant'},
                ids: ['2'],
              },
            },
          },
          order_by: {keys: [], order: '', compare: null},
          keys: [],
        });

      expect(GGRC.query_parser.parse('#SomeClass,1,2,3,4# or #A,1#'))
        .toEqual({
          expression: {
            left: {
              object_name: 'SomeClass',
              op: {name: 'relevant'},
              ids: ['1', '2', '3', '4'],
            },
            op: {name: 'OR'},
            right: {
              object_name: 'A',
              op: {name: 'relevant'},
              ids: ['1'],
            },
          },
          order_by: {keys: [], order: '', compare: null},
          keys: [],
        });
    });

    it('parses complex queries', () => {
      expect(GGRC.query_parser
        .parse('(n = 22 and n = 5) and ("bacon ipsum" !~ bacon)'))
        .toEqual({
          expression: {
            left: {
              left: {left: 'n', op: {name: '='}, right: '22'},
              op: {name: 'AND'},
              right: {left: 'n', op: {name: '='}, right: '5'},
            },
            op: {name: 'AND'},
            right: {left: 'bacon ipsum', op: {name: '!~'}, right: 'bacon'},
          },
          order_by: {keys: [], order: '', compare: null},
          keys: ['bacon ipsum', 'n'],
        });

      expect(GGRC.query_parser
        .parse('(n = 22 or n = 5) and ("bacon ipsum" !~ bacon)'))
        .toEqual({
          expression: {
            left: {
              left: {left: 'n', op: {name: '='}, right: '22'},
              op: {name: 'OR'},
              right: {left: 'n', op: {name: '='}, right: '5'},
            },
            op: {name: 'AND'},
            right: {left: 'bacon ipsum', op: {name: '!~'}, right: 'bacon'},
          },
          order_by: {keys: [], order: '', compare: null},
          keys: ['bacon ipsum', 'n'],
        });

      expect(GGRC.query_parser
        .parse('n = 22 or n = 5 and "bacon ipsum" ~ bacon'))
        .toEqual({
          expression: {
            left: {left: 'n', op: {name: '='}, right: '22'},
            op: {name: 'OR'},
            right: {
              left: {left: 'n', op: {name: '='}, right: '5'},
              op: {name: 'AND'},
              right: {left: 'bacon ipsum', op: {name: '~'}, right: 'bacon'},
            },
          },
          order_by: {keys: [], order: '', compare: null},
          keys: ['bacon ipsum', 'n'],
        });

      expect(GGRC.query_parser
        .parse('("bacon ipsum" ~ bacon) and ("bacon ipsum" !~ bacon)'))
        .toEqual({
          expression: {
            left: {left: 'bacon ipsum', op: {name: '~'}, right: 'bacon'},
            op: {name: 'AND'},
            right: {left: 'bacon ipsum', op: {name: '!~'}, right: 'bacon'},
          },
          order_by: {keys: [], order: '', compare: null},
          keys: ['bacon ipsum'],
        });

      expect(GGRC.query_parser
        .parse('hello=worldoo or ~ bacon ipsum'))
        .toEqual({
          expression: {
            left: {left: 'hello', op: {name: '='}, right: 'worldoo'},
            op: {name: 'OR'},
            right: {text: 'bacon ipsum', op: {name: 'text_search'}},
          },
          order_by: {keys: [], order: '', compare: null},
          keys: ['hello'],
        });
    });

    it('correctly handles escaped symbols inside quotes', function () {
      var queries = [
        'title ~ "test\\\\"',
        'title ~ "test\\%"',
        'title ~ "test\\_"',
        'title ~ "test\\""',
      ];

      _.each(queries, function (query) {
        var value = query.split('~')[1].trim().replace(/^"|"$/g, '');
        var result = GGRC.query_parser.parse(query);

        expect(result.expression.right).toEqual(value);
      });
    });

    it('correctly handles escaped symbols outside quotes', function () {
      var queries = [
        'title ~ test\\\\',
        'title ~ test\\%',
        'title ~ test\\_',
        'title ~ test\\"',
      ];

      _.each(queries, function (query) {
        var value = query.split('~')[1].trim();
        var result = GGRC.query_parser.parse(query);

        expect(result.expression.right).toEqual(value);
      });
    });

    it('does not change escaped symbols in case of text search', function () {
      var query = 'some \\\\ test \\% \\_ query';

      var result = GGRC.query_parser.parse(query);

      expect(result.expression.op.name).toBe('text_search');
      expect(result.expression.text).toBe(query);
    });

    it('correctly handles escaped symbol inside attribute name', function () {
      var query = '"my \\" quote" ~ aaa';
      var result = GGRC.query_parser.parse(query);

      expect(result.expression.left).toEqual('my \\" quote');
    });
  });

  describe('join_queries', function () {
    it('joins two queries with AND by default', function () {
      var sameQueries = [
        ['a=b and c=d', 'a=b', 'c=d'],
        ['(a=b) and (c=d)', 'a=b', 'c=d'],
        ['(a=b or c=A) and (c=d)', 'a=b or c=A', 'c=d'],
        ['(a=b or c=A) and (c=d)', '(a=b or c=A) and (c=d)', ''],
        ['(a=b or c=A) and (c=d)', '', '(a=b or c=A) and (c=d)'],
        ['hello=worldoo and ~ bacon ipsum',
          'hello=worldoo',
          '~ bacon ipsum'],
      ];

      can.each(sameQueries, function (queries) {
        expect(
          JSON.stringify(GGRC.query_parser.parse(queries[0]))
        ).toEqual(
          JSON.stringify(
            GGRC.query_parser.join_queries(
              GGRC.query_parser.parse(queries[1]),
              GGRC.query_parser.parse(queries[2])
            )
          )
        );
      });
    });

    it('joins two queries with OR', function () {
      var sameQueries = [
        ['a=b or c=d', 'a=b', 'c=d'],
        ['(a=b) or (c=d)', 'a=b', 'c=d'],
        ['(a=b and c=A) or (c=d)', 'a=b and c=A', 'c=d'],
        ['(hello=worldoo or n=22 ) or ~ bacon ipsum',
          '(hello=worldoo or n=22 )',
          '  ~ bacon ipsum'],
      ];

      can.each(sameQueries, function (queries) {
        expect(
          JSON.stringify(GGRC.query_parser.parse(queries[0]))
        ).toEqual(
          JSON.stringify(
            GGRC.query_parser.join_queries(
              GGRC.query_parser.parse(queries[1]),
              GGRC.query_parser.parse(queries[2]),
              'OR'
            )
          )
        );
      });
    });
  });
});
