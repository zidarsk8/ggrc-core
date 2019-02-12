/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

let Stub = can.Map.extend({
  setup(model) {
    let type = (model instanceof can.Model)
      ? model.constructor.model_singular
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

export default Stub;
