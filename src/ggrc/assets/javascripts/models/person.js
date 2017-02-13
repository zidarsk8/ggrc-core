/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

// require can.jquery-all
// require models/cacheable

(function (ns, can) {
  can.Model.Cacheable('CMS.Models.Person', {
    root_object: 'person',
    root_collection: 'people',
    category: 'entities',
    findAll: 'GET /api/people',
    findOne: 'GET /api/people/{id}',
    create: 'POST /api/people',
    update: 'PUT /api/people/{id}',
    destroy: 'DELETE /api/people/{id}',
    search: function (request, response) {
      return can.ajax({
        type: 'get',
        url: '/api/people',
        dataType: 'json',
        data: {s: request.term},
        success: function (data) {
          response(can.$.map(data, function (item) {
            return can.extend({}, item.person, {
              label: item.person.email,
              value: item.person.id
            });
          }));
        }
      });
    },
    is_custom_attributable: true,
    attributes: {
      context: 'CMS.Models.Context.stub',
      modified_by: 'CMS.Models.Person.stub',
      object_people: 'CMS.Models.ObjectPerson.stubs',
      language: 'CMS.Models.Option.stub',
      user_roles: 'CMS.Models.UserRole.stubs',
      name: 'trimmed',
      email: 'trimmedLower',
      custom_attribute_values: 'CMS.Models.CustomAttributeValue.stubs'
    },
    mixins: ['ca_update'],
    defaults: {
      name: '',
      email: '',
      contact: null,
      owners: null
    },
    convert: {
      trimmed: function (val) {
        return (val && val.trim) ? val.trim() : val;
      },
      trimmedLower: function (val) {
        return ((val && val.trim) ? val.trim() : val).toLowerCase();
      }
    },
    serialize: {
      trimmed: function (val) {
        return (val && val.trim) ? val.trim() : val;
      },
      trimmedLower: function (val) {
        return ((val && val.trim) ? val.trim() : val).toLowerCase();
      }
    },
    findInCacheByEmail: function (email) {
      var result = null;
      var that = this;
      can.each(Object.keys(this.cache || {}), function (k) {
        if (that.cache[k].email === email) {
          result = that.cache[k];
          return false;
        }
      });
      return result;
    },
    tree_view_options: {
      show_view: GGRC.mustache_path + '/people/tree.mustache',
      attr_view: GGRC.mustache_path + '/people/tree-item-attr.mustache',
      header_view: GGRC.mustache_path + '/people/tree_header.mustache',
      footer_view: GGRC.mustache_path + '/base_objects/tree_footer.mustache',
      add_item_view: GGRC.mustache_path + '/people/tree_add_item.mustache',
      mapper_attr_list: [
        {attr_title: 'Title', attr_name: 'title'},
        {attr_title: 'Email', attr_name: 'email'}
      ],
      disable_columns_configuration: true
    },
    list_view_options: {
      find_params: {__sort: 'name,email'}
    },
    init: function () {
      var rEmail =
        /^[-!#$%&*+\\.\/0-9=?A-Z^_`{|}~]+@([-0-9A-Z]+\.)+([0-9A-Z]){2,4}$/i;
      this._super.apply(this, arguments);

      this.validateNonBlank('email');
      this.validateFormatOf('email', rEmail);
    },
    getUserRoles: function (instance, person) {
      var result = $.Deferred();
      var refreshQueue = new RefreshQueue();
      var userRoles;

      can.each(person.user_roles, function (ur) {
        refreshQueue.enqueue(ur.getInstance());
      });

      refreshQueue.trigger().then(function (roles) {
        userRoles = _.filter(roles, function (role) {
          return instance.context && role.context &&
            role.context.id === instance.context.id;
        });
        result.resolve(userRoles);
      });
      return result.promise();
    },
    getPersonMappings: function (instance, person, specificOject) {
      var result = $.Deferred();
      var mappingObject = instance[specificOject];
      var mappingsRQ = new RefreshQueue();
      var userRolesRQ = new RefreshQueue();

      can.each(mappingObject, function (obj) {
        mappingsRQ.enqueue(obj);
      });

      mappingsRQ.trigger().then(function (objects) {
        var userRoles;
        var objectPeopleFiltered = _.filter(objects, function (item) {
          return item.person && item.person.id === person.id;
        });

        userRoles = _.filter(person.user_roles, function (item) {
          item = item.getInstance();
          return instance.context && item.context_id === instance.context.id;
        }).map(function (item) {
          return item.reify();
        });

        userRoles = userRoles.concat(objectPeopleFiltered);

        can.each(userRoles, function (obj) {
          userRolesRQ.enqueue(obj);
        });

        return userRolesRQ.trigger();
      }).then(function (userRoles) {
        result.resolve(userRoles);
      });
      return result.promise();
    }
  }, {
    display_name: function () {
      return this.email;
    },
    autocomplete_label: function () {
      return this.name ?
      this.name + '<span class="url-link">' + this.email + '</span>' :
        this.email;
    }
  });
})(window, can);
