/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

window.CMS = window.CMS || {};
window.CMS.Models = window.CMS.Models || {};

CMS.Models.get_instance = function (objectType, objectId, paramsOrObject) {
  let model;
  let params = {};
  let instance;
  let href;

  if (typeof objectType === 'object' || objectType instanceof can.Stub) {
    // assume we only passed in params_or_object
    paramsOrObject = objectType;
    if (!paramsOrObject) {
      return null;
    }
    if (paramsOrObject instanceof can.Model) {
      objectType = paramsOrObject.constructor.shortName;
    } else if (paramsOrObject instanceof can.Stub) {
      objectType = paramsOrObject.type;
    } else if (!paramsOrObject.selfLink && paramsOrObject.type) {
      objectType = paramsOrObject.type;
    } else {
      href = paramsOrObject.selfLink || paramsOrObject.href;
      objectType = can.map(
        window.cms_singularize(/^\/api\/(\w+)\//.exec(href)[1]).split('_'),
        can.capitalize
      ).join('');
    }
    objectId = paramsOrObject.id;
  }

  model = CMS.Models[objectType];

  if (!model) {
    return null;
  }

  if (!objectId) {
    return null;
  }

  if (paramsOrObject) {
    if ($.isFunction(paramsOrObject.serialize)) {
      $.extend(params, paramsOrObject.serialize());
    } else {
      $.extend(params, paramsOrObject || {});
    }
  }

  instance = model.findInCacheById(objectId);
  if (!instance) {
    if (params.selfLink) {
      params.id = objectId;
      instance = new model(params);
    } else {
      instance = new model({
        id: objectId,
        type: objectType,
        href: (paramsOrObject || {}).href,
      });
    }
  }
  return instance;
};

CMS.Models.get_stub = function (object) {
  let instance = CMS.Models.get_instance(object);
  if (!instance) {
    return;
  }
  return instance.stub();
};

CMS.Models.get_stubs = function (objects) {
  return new can.Stub.List(
    can.map(CMS.Models.get_instances(objects), function (obj) {
      if (!obj || !obj.stub) {
        console.warn('`Models.get_stubs` instance has no stubs ', arguments);
        return;
      }
      return obj.stub();
    }));
};

CMS.Models.get_instances = function (objects) {
  let i;
  let instances = [];
  if (!objects) {
    return [];
  }
  for (i = 0; i < objects.length; i++) {
    instances[i] = CMS.Models.get_instance(objects[i]);
  }
  return instances;
};

CMS.Models.get_link_type = function (instance, attr) {
  let type;
  let model;

  type = instance[attr + '_type'];
  if (!type) {
    model = instance[attr] && instance[attr].constructor;
    if (model) {
      type = model.shortName;
    } else if (instance[attr]) {
      type = instance[attr].type;
    }
  }
  return type;
};
