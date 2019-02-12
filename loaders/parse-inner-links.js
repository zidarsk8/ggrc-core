/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

module.exports = function(html) {
  let linkRegexp = /<a href="(.*)">(.*)<\/a>/g;
  let linkMatches = [];
  let result;

  // find all links
  while ((result = linkRegexp.exec(html)) !== null) {
    linkMatches.push(result);
  }

  linkMatches.forEach((match, index) => {
    let hash = (Date.now() * Math.random()).toFixed();
    let innerText = match[2];
    let headerStr = `<h3>${innerText}<\/h3>`;
    let linkStr = `<a href="${match[1]}">${innerText}<\/a>`;

    if (html.indexOf(headerStr) > -1) {
      // set hash as id for header
      html = html.replace(headerStr,
        `<h3 id="${hash}">${innerText}<\/h3>`);

      // set hash as href for link
      html = html.replace(linkStr,
        `<a href="#${hash}">${innerText}<\/a>`);
    }
  });

  return html;
}
