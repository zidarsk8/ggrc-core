/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC, CMS) {
  'use strict';

  var mapper = {
    createRelationship: function (source, destination) {
      return new CMS.Models.Relationship({
        context: source.context,
        source: source,
        destination: destination
      });
    },
    mapObjects: function (source, destination, type) {
      return this.createRelationship(source, destination);
    }
  };

  GGRC.Components('reusableObjectsList', {
    tag: 'reusable-objects-list',
    viewModel: {
      define: {
        baseInstanceDocuments: {
          get: function () {
            return this.attr('urls').concat(this.attr('evidences'));
          }
        },
        hasSelected: {
          get: function () {
            return !!this.attr('documentList.length');
          }
        }
      },
      evidences: [],
      urls: [],
      baseInstance: {},
      documentList: [],
      isSaving: false,
      baseInstanceDocuments: [],
      getMapObjects: function (source, list, mapperType) {
        return Array.prototype.filter
        // Get Array of unique items
          .call(list, function (item, index) {
            return index === list.indexOf(item);
          })
          // Get Array of mapped models
          .map(function (destination) {
            return mapper
              .mapObjects(source, destination, mapperType)
              .save();
          });
      },
      getReusedObjectList: function () {
        var source = this.attr('baseInstance');
        var documentList =
          this.getMapObjects(source, this.attr('documentList'), 'documents');
        return documentList;
      },
      reuseSelected: function () {
        var reusedObjectList = this.getReusedObjectList();

        this.attr('isSaving', true);

        can.when.apply(can, reusedObjectList)
          .done(function () {
            can.$(document.body).trigger('ajax:flash', {
              success: 'Selected evidences are reused'
            });
          })
          .fail(function () {
            can.$(document.body).trigger('ajax:flash', {
              error: 'Selected evidences were not reused'
            });
          })
          .always(this.restoreDefaults.bind(this));
      },
      restoreDefaults: function () {
        this.attr('documentList').replace([]);
        this.attr('isSaving', false);
        this.attr('baseInstance').dispatch('refreshInstance');
      }
    }
  });
})(window.can, window.GGRC, window.CMS);
