/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

function Proxy(optionModelName, joinOptionAttr, joinModelName,
  joinObjectAttr, instanceJoinAttr) {
  return new GGRC.ListLoaders.ProxyListLoader(
    joinModelName, joinObjectAttr, joinOptionAttr,
    instanceJoinAttr, optionModelName);
}

function Direct(
  optionModelName, instanceJoinAttr, remoteJoinAttr) {
  return new GGRC.ListLoaders.DirectListLoader(
    optionModelName, instanceJoinAttr, remoteJoinAttr);
}

function Indirect(instModelName, joinAttr) {
  return new GGRC.ListLoaders.IndirectListLoader(instModelName, joinAttr);
}

function Search(queryFunction, observeTypes) {
  return new GGRC.ListLoaders.SearchListLoader(queryFunction, observeTypes);
}

function Multi(sources) {
  return new GGRC.ListLoaders.MultiListLoader(sources);
}

function TypeFilter(source, modelName) {
  return new GGRC.ListLoaders.TypeFilteredListLoader(source, [modelName]);
}

function CustomFilter(source, filterFn) {
  return new GGRC.ListLoaders.CustomFilteredListLoader(source, filterFn);
}

function Cross(localMapping, remoteMapping) {
  return new GGRC.ListLoaders.CrossListLoader(localMapping, remoteMapping);
}

export {
  Proxy,
  Direct,
  Indirect,
  Search,
  Multi,
  TypeFilter,
  CustomFilter,
  Cross,
};

