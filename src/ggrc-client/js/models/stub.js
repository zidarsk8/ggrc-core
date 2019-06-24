/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import canModel from 'can-model';
import canList from 'can-list';
import CanMap from 'can-map';
let Stub = CanMap.extend({
  setup(model) {
    let type = (model instanceof canModel)
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

Stub.List = canList.extend({
  Map: Stub,
}, {
  setup(models=[]) {
    let converted = models.map((model) => new Stub(model));
    this._super(converted);
  },
});

export default Stub;
