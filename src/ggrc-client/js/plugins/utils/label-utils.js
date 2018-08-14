/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

const sortByName = (labels) => {
  const sortedLabels = _.orderBy(
    labels,
    (label) => {
      return label.name && label.name.toLowerCase ?
        label.name.toLowerCase() :
        label.name;
    }
  );

  return sortedLabels;
};

export {
  sortByName,
};
