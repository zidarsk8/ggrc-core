/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

export default can.Observe('can.Stub', {
  get_or_create: function (obj) {
    let id = obj.id;
    let stub;
    let type = obj.type;

    CMS.Models.stub_cache = CMS.Models.stub_cache || {};
    CMS.Models.stub_cache[type] = CMS.Models.stub_cache[type] || {};
    if (!CMS.Models.stub_cache[type][id]) {
      stub = new can.Stub(obj);
      CMS.Models.stub_cache[type][id] = stub;
    }
    return CMS.Models.stub_cache[type][id];
  },
}, {});

can.Observe.prototype.stub = function () {
  let type;
  let id;

  if (!(this instanceof can.Model || this instanceof can.Stub)) {
    console.debug('.stub() called on non-stub, non-instance object', this);
  }

  if (this instanceof can.Stub) {
    return this;
  }

  if (this instanceof can.Model) {
    type = this.constructor.shortName;
  } else {
    type = this.type;
  }

  if (this.constructor.id) {
    id = this[this.constructor.id];
  } else {
    id = this.id;
  }

  if (!id && id !== 0) {
    return null;
  }

  return can.Stub.get_or_create({
    id: id,
    href: this.selfLink || this.href,
    type: type,
  });
};

can.Observe.List.prototype.stubs = function () {
  return new can.Observe.List(can.map(this, function (obj) {
    return obj.stub();
  }));
};

can.Observe.prototype.reify = function () {
  let type;
  let model;

  if (this instanceof can.Model) {
    return this;
  }
  if (!(this instanceof can.Stub)) {
    // console.debug('`reify()` called on non-stub, non-instance object', this);
  }

  type = this.type;
  model = CMS.Models[type] || GGRC.Models[type];

  if (!model) {
    console.debug('`reify()` called with unrecognized type', this);
  } else {
    return model.model(this);
  }
};

can.Observe.List.prototype.reify = function () {
  return new can.Observe.List(can.map(this, function (obj) {
    return obj.reify();
  }));
};
