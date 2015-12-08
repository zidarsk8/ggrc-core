#!/usr/bin/env node
/*
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: miha@reciprocitylabs.com
    Maintained By: miha@reciprocitylabs.com
*/

/*
Script used to generate ggrc_filter_query_parser.js 

-- updating dev enviroment by running: 

  vagrant provision 

-- manual dev env setup:

to run this script you need node.js and peg.js
  sudo apt-get install nodejs npm
  npm install pegjs
  npm install mkdirp

if npm install returns a 404 just run the next command and try again.
  npm config set registry http://registry.npmjs.org/


then edit the parser.pegjs file and run the generator
  ./generate_parser.js
 
to run the tests first install nodeunit
  npm install -g nodeunit

and run with the test folder
  nodeunit test
  
*/


var parser,
    parser_src,
    ggrc_parser,
    parser_grammar = '/vagrant/src/parser/parser.pegjs',
    parser_template_file = '/vagrant/src/parser/parser_template.js', 
    ggrc_parser_folder = '/vagrant/src/ggrc/assets/javascripts/generated/',
    ggrc_parser_js_file = 'ggrc_filter_query_parser.js',
    peg = require('pegjs'),
    fs = require('fs'),
    mkdirp = require('mkdirp'),
    parser_string = fs.readFileSync(parser_grammar, 'utf8'),
    filter_template = fs.readFileSync(parser_template_file, 'utf8');

// dirty way of making the parser work in node.js without jquery
root.jQuery = {
  unique : function(k) {
    return Object.keys(k.reduce(function(o,v,i) {o[v] = true; return o;}, {}));
  },
  type : function(o) {
    return typeof o;
  }
}


console.log('building parser');
parser = peg.buildParser(parser_string);
parser_src = peg.buildParser(parser_string, {output: "source"});

console.log('saving parser to js files');
ggrc_parser = filter_template.replace('"GENERATED_PLACEHOLDER"', parser_src);

mkdirp.sync(ggrc_parser_folder);
fs.writeFileSync(ggrc_parser_folder + ggrc_parser_js_file, ggrc_parser);

console.log('\ndone :)');
