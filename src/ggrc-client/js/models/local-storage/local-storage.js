/* eslint no-invalid-this: 0 */
/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

// LocalStorage model, stubs AJAX requests to storage instead of going to the server.  Useful when a REST resource hasn't yet been implemented
// Adapted from an example in the CanJS documentation.  http://canjs.us/recipes.html
// Base model to handle reading / writing to local storage
export default can.Model('can.Model.LocalStorage', {
  makeFindOne(findOne) {
    if (typeof findOne === 'function' && this !== can.Model.LocalStorage) {
      return findOne;
    } else {
      return function (params, success, error) {
        let instance;
        let def = new can.Deferred();
        // Key to be used for local storage
        let key = [this._shortName, params.id].join(':');
        // Grab the current data, if any
        let data = window.localStorage.getItem( key );

        params = params || {};


        // Bind success and error callbacks to the deferred
        def.then(success, error);

        // If we had existing local storage data...
        if ( data ) {
          // Create our model instance
          instance = this.store[params.id] || this.model( JSON.parse( data ));

          // Resolve the deferred with our instance
          def.resolve( instance );

        // Otherwise hand off the deferred to the ajax request
        } else {
          def.reject({
            status: 404,
            responseText: 'Object with id ' + params.id + ' was not found',
          });
        }
        return def;
      };
    }
  },
  makeFindAll: function (findAll) {
    if (typeof findAll === 'function' && this !== can.Model.LocalStorage) {
      return findAll;
    } else {
      return function (params, success, error) {
        let def = new can.Deferred();
        let allData = window.localStorage.getItem(`${this._shortName}:ids`);
        let returns = new can.Model.List();
        let that = this;
        params = params || {};

        if (allData) {
          can.each(JSON.parse(allData), function (id) {
            let data;
            let pkeys;
            if (!params.id || params.id === id) {
              data = window.localStorage.getItem(`${that._shortName}:${id}`);

              if (data) {
                data = that.store[id] || JSON.parse(data);
                pkeys = Object.keys(params);
                if (pkeys.length < 1 || can.filter(pkeys, function (key) {
                  return params[key] !== data[key];
                }).length < 1) {
                  returns.push(that.model(data));
                }
              }
            }
          });
        }

        def.resolve(returns);
        return def;
      };
    }
  },
  makeCreate: function (create) {
    if (typeof create === 'function' && this !== can.Model.LocalStorage) {
      return create;
    } else {
      return function (params) {
        let item;
        let key = [this._shortName, 'ids'].join(':');
        let data = window.localStorage.getItem( key );
        let newkey = 1;
        let def = new can.Deferred();


        // add to list
        if (data) {
          data = JSON.parse(data);
          // newkey = Math.max.apply(Math, data.concat([0])) + 1;
          newkey = Math.max(0, ...data) + 1;
          data.push(newkey);
        } else {
          data = [newkey];
        }
        window.localStorage.setItem(key, JSON.stringify(data));

        // create new
        key = [this._shortName, newkey].join(':');
        item = this.model(can.extend({id: newkey}, params));
        window.localStorage.setItem(key, JSON.stringify(item.serialize()));

        def.resolve(item);
        this.created && this.created(item);
        return def;
      };
    }
  },
  makeUpdate: function (update) {
    if (typeof update === 'function' && this !== can.Model.LocalStorage) {
      return update;
    } else {
      return function (id, params) {
        let item;
        let key = [this._shortName, id].join(':');
        let data = window.localStorage.getItem( key );
        let def = new can.Deferred();

        if (data) {
          data = JSON.parse(data);

          if (params._removedKeys) {
            can.each(params._removedKeys, function (key) {
              if (!params[key]) {
                delete data[key];
              }
            });
          }

          delete params._removedKeys;
          can.extend(data, params);
          item = this.model({}).attr(data);

          window.localStorage.setItem(key, JSON.stringify(item.serialize()));
          def.resolve(item);
          this.updated && this.updated(item);
        } else {
          def.reject({
            status: 404,
            responseText: 'The object with id ' + id + ' was not found.',
          });
        }
        return def;
      };
    }
  },
  makeDestroy: function (destroy) {
    if (typeof destroy === 'function' && this !== can.Model.LocalStorage) {
      return destroy;
    } else {
      return function (id) {
        let def = new can.Deferred();
        let key = [this._shortName, id].join(':');
        let item = this.model({id: id});
        let data;

        if (window.localStorage.getItem(key)) {
          window.localStorage.removeItem(key);

          // remove from list
          key = [this._shortName, 'ids'].join(':');
          data = window.localStorage.getItem( key );

          data = JSON.parse(data);
          data.splice(can.inArray(id, data), 1);
          window.localStorage.setItem(key, JSON.stringify(data));

          def.resolve(item);
          this.destroyed && this.destroyed(item);
        } else {
          def.reject({
            status: 404,
            responseText: 'Object with id ' + id + ' was not found',
          });
        }
        return def;
      };
    }
  },
  clearAll: function () {
    window.localStorage.clear();
  },
}, {
  removeAttr: function (attr) {
    this._super(attr);
    this._removedKeys || (this._data._removedKeys = this._removedKeys = []);
    this._removedKeys.push(attr);
    return this;
  },
});
