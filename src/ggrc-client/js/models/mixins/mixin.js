/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import loIncludes from 'lodash/includes';
import loIsFunction from 'lodash/isFunction';

export default class Mixin {
  constructor() {
    throw new Error('Mixins cannot be directly instantiated');
  }

  static add_to(cls) {
    if (this === Mixin) {
      throw new Error('Must only add a subclass of Mixin to an object,' +
        ' not Mixin itself');
    }
    function setupFns(obj) {
      return function (fn, key) {
        let blockedKeys = ['constructor', 'length', 'name', 'prototype'];
        let aspect;
        let index = key.indexOf(':');
        if (index !== -1) {
          aspect = key.substr(0, index);
          key = key.substr(index + 1);
        } else {
          aspect = 'after';
        }

        if (!blockedKeys.includes(key)) {
          let oldfn = obj[key];
          // TODO support other ways of adding functions.
          //  E.g. "override" (doesn't call super fn at all)
          //       "sub" (sets this._super for mixin function)
          //       "chain" (pushes result of oldfn onto args)
          //       "before"/"after" (overridden function)
          // TODO support extension for objects.
          //   Necessary for "attributes"/"serialize"/"convert"
          // Defaults will always be "after" for functions
          //  and "override" for non-function values
          if (loIsFunction(oldfn)) {
            switch (aspect) {
              case 'before':
                obj[key] = function () {
                  fn.apply(this, arguments);
                  return oldfn.apply(this, arguments);
                };
                break;
              case 'after':
                obj[key] = function () {
                  let result;
                  result = oldfn.apply(this, arguments);
                  fn.apply(this, arguments);
                  return result;
                };
                break;
              default:
                break;
            }
          } else if (aspect === 'extend') {
            obj[key] = Object.assign(obj[key], fn);
          } else {
            obj[key] = fn;
          }
        }
      };
    }

    if (!loIncludes(cls._mixins, this)) {
      cls._mixins = cls._mixins || [];
      cls._mixins.push(this);
      Object.getOwnPropertyNames(this).forEach((key) => {
        setupFns(cls)(this[key], key);
      });
      Object.getOwnPropertyNames(this.prototype).forEach((key) => {
        setupFns(cls.prototype)(this.prototype[key], key);
      });
    }
  }
}
