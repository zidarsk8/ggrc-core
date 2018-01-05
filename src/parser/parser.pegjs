/*
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/


start
  = _* only_order_by:only_order_by _*
    {
      return {
        expression: {},
        keys: [],
        order_by: only_order_by,
      };
    }
  / _* or_exp:or_exp order_by:order_by _*
    {
      var keys = jQuery.unique(or_exp.keys.sort());
      delete or_exp.keys;
      return {
        expression: or_exp,
        keys: keys,
        order_by: order_by,
      };
    }
  / _*
    {
      return {
        expression: {},
        keys: [],
        order_by: {
          keys: [],
          order: '',
          compare: null
        },
      };
    }
  / .*
    {
      return false;
    }

order_by
  = ' ' only_order_by:only_order_by
    {
      return only_order_by;
    }
  / _*
    {
      return {
        keys: [],
        order: '',
        compare: null
      };
    }

only_order_by
  = _* 'order by'i _+ word_list:word_list order:order
    {
      return {
        keys: word_list,
        order: order,
        compare: function(val1, val2){
          for (var i=0 ; i < word_list.length; i++){
            var key = word_list[i];
            if (val1[key] !== val2[key]){
              var a = parseFloat(val1[key]) || val1[key],
                  b = parseFloat(val2[key]) || val2[key];
              return (a < b) ^ (order !== 'asc')
            }
          }
          return false;
        }
      };
    }

word_list
  = word:word ',' word_list:word_list
    {
      return [word].concat(word_list);
    }

  / word:word
    {
      return [word];
    }

order
  = _+ 'desc'i _*
    {
      return 'desc';
    }
  / _+ 'asc'i _*
    {
      return 'asc';
    }
  / _*
    {
      return 'asc';
    }


or_exp
  = left:and_exp op:OR right:or_exp
    {
      var keys = left.keys.concat(right.keys);
      delete right.keys;
      delete left.keys;
      return {
        left: left,
        op: op,
        right: right,
        keys: keys,
      };
    }
  / and_exp


and_exp
  = left:simple_exp op:AND right:and_exp
    {
      var keys = left.keys.concat(right.keys);
      delete right.keys;
      delete left.keys;
      return {
        left:left,
        op: op,
        right: right,
        keys: keys,
      };
    }
  / simple_exp


simple_exp
  = left:word op:OP right:word
    {
      var lleft = left.toLowerCase();
      return {
        left: lleft,
        op: op,
        right: right,
        keys: [lleft],
      };
    }
  / relevant_exp
  / paren_exp
  / text_exp

relevant_exp
  = _* "#" relevant:word_list "#"
    {
      return {
        object_name: relevant[0],
        op: {name: "relevant"},
        ids: relevant.slice(1),
        keys: [],
      };
    }

text_exp
  = _* "~" characters:.*
    {
      return {
        text: characters.join("").trim(),
        op: {name:'text_search'},
        keys: [],
      };
    }
  / _* "!~" characters:.*
    {
      return {
        text: characters.join("").trim(),
        op: {name: 'exclude_text_search'},
        keys: [],
      };
    }

paren_exp
  = LEFT_P or_exp:or_exp RIGHT_P
    {
      return or_exp;
    }


word
  = unquoted_word
  / quoted_word


unquoted_word
  = word:unqoted_char+
    {
      return word.join('');
    }


quoted_word
  = '"' word:quoted_char* '"'
    {
      return word.join('');
    }

unqoted_char
  = escaped_symbol
  / [a-zA-Z0-9_\-./%]


quoted_char
  = escaped_symbol
  / [^"]


escaped_symbol
  = escape:'\\' symbol:.
    {
      return escape + symbol;
    }


AND
  = _+ 'AND'i _+
    {
      return {
        name: 'AND',
      };
    }
  / _* '&&'   _*
    {
      return {
        name: 'AND',
      };
    }


OR
  = _+ 'OR'i  _+
    {
      return {
        name: 'OR',
      };
    }
  / _* '||'   _*
    {
      return {
        name: 'OR',
      };
    }


OP
  = _* op:('=' / '!=' / '<=' / '<' / '>=' / '>' / '~' / '!~') _*
    {
      return {
        name: op,
      };
    }
  / _+ op:'is' _+
    {
      return {
        name: op,
      };
    }


LEFT_P = '(' _*

RIGHT_P = _* ')'

_ = [ \t\r\n\f]+
