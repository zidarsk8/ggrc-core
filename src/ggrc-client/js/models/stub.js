/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

let Stub = can.Map.extend({
  setup(model) {
    let type = (model instanceof can.Model)
      ? model.constructor.shortName
      : model.type;
    let href = model.selfLink || model.href;

    this._super({
      id: model.id,
      type,
      href,
    });
  },
});

Stub.List = can.List.extend({
  Map: Stub,
}, {
  setup(models=[]) {
    let converted = models.map((model) => new Stub(model));
    this._super(converted);
  },
});

can.Observe.prototype.reify = function () {
  let type;
  let model;

  if (this instanceof can.Model) {
    return this;
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

export default Stub;
