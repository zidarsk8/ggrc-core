/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

GGRC.Templates = GGRC.Templates || {};

let mustacheTemplates = require.context('./mustache/', true, /\.mustache/);

mustacheTemplates.keys().forEach((key) => {
  let newKey = key.match(/(?<=\.\/)(.*?)(?=\.mustache)/g);
  if (newKey[0]) {
    GGRC.Templates[newKey[0]] = mustacheTemplates(key);
  }
});
