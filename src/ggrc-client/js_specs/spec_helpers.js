/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

// This is primarily useful for passing as the fail case for
//  promises, since every item passed to it will show up in
//  the jasmine output.
function failAll(done) {
  return function (...args) {
    args.forEach(function (arg) {
      fail(JSON.stringify(arg));
    });
    if (done) {
      done();
    }
  };
}

function getComponentVM(Component) {
  const viewModelConfig = Component.prototype.viewModel;

  if (_.isFunction(viewModelConfig)) {
    return new viewModelConfig();
  }
  return new (can.Map.extend(viewModelConfig));
}

function makeFakeModel({model, staticProps = {}, instanceProps = {}} = {}) {
  const attrsForBaseModel = model.attributes;
  const staticPresetup = {
    // "attributes" isn't inherited from base model.
    // We should explicitly set the same "attributes" for derived models from
    // base model.
    attributes: {...attrsForBaseModel},
    ...staticProps,
  };

  return model.extend(staticPresetup, instanceProps);
}

function makeFakeInstance({
  model,
  staticProps = {},
  instanceProps = {},
} = {}) {
  const fakeModel = makeFakeModel({model, staticProps, instanceProps});
  return (...instanceArgs) => new fakeModel(...instanceArgs);
}

export {
  failAll,
  getComponentVM,
  makeFakeModel,
  makeFakeInstance,
};
