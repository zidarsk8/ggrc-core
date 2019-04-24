/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {
  getTruncatedList,
  getOnlyAnchorTags,
} from '../ggrc_utils';

describe('getTruncatedList() util', () => {
  it('returns string which includes 5 lines without last line with count of ' +
  'remaining items if count of items less then 6', () => {
    const items = [
      'email2@something.com',
      'email1@something.com',
      'email3@something.com',
      'email4@something.com',
    ];
    const expected = items.join('\n');

    const result = getTruncatedList(items);

    expect(result).toBe(expected);
  });

  it('returns first 5 items with last line with count of remaining items ' +
  'if count of items less then 6', () => {
    const items = [
      'email2@something.com',
      'email1@something.com',
      'email3@something.com',
      'email4@something.com',
      'email12@something.com',
    ];
    const overflowedItems = [
      ...items,
      'email11@something.com',
      'email13@something.com',
      'email14@something.com',
    ];
    const itemsLimit = 5;
    const expected = items.join('\n') +
      `\n and ${overflowedItems.length - itemsLimit} more`;

    const result = getTruncatedList(overflowedItems);

    expect(result).toBe(expected);
  });
});

describe('getOnlyAnchorTags() util', () => {
  it('returns transformed html content having only anchor tags', () => {
    const html = '<p>my <a href="https://www.example.com">example</a></p>';
    const result = getOnlyAnchorTags(html);

    expect(result)
      .toBe('my <a href="https://www.example.com">example</a>');
  });

  it('returns transformed html with no html tags', () => {
    const html = '<p><strong>sample text</strong></p>';
    const result = getOnlyAnchorTags(html);

    expect(result)
      .toBe('sample text');
  });
});
