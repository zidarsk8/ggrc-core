/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC, CMS) {
  'use strict';

  var mapper = {
    createRelationship: function (source, destination) {
      return new CMS.Models.Relationship({
        context: source.context,
        source: source.stub(),
        destination: destination
      });
    },
    createObjectRelationship: function (source, destination) {
      return new CMS.Models.ObjectDocument({
        context: source.context,
        documentable: source,
        document: destination
      });
    },
    isObjectDocument: function (object) {
      var isObjectDocument;
      if (object.attr('reuseMapperType')) {
        isObjectDocument =
          object.attr('reuseMapperType') === 'all_documents';
      } else {
        isObjectDocument =
          object.object_documents && object.object_documents.length;
      }
      return isObjectDocument;
    },
    mapObjects: function (source, destination) {
      return this.isObjectDocument(destination) ?
        this.createObjectRelationship(source, destination) :
        this.createRelationship(source, destination);
    }
  };

  can.Component.extend({
    tag: 'reusable-objects-list',
    scope: {
      baseInstance: null,
      checkReusedStatus: false,
      selectedList: [],
      isSaving: false,
      reuseSelected: function () {
        var reusedList = this.attr('selectedList');
        var source = this.attr('baseInstance');
        var models;
        this.attr('isSaving', true);
        this.attr('checkReusedStatus', false);
        models = Array.prototype.filter
        // Get Array of unique items
          .call(reusedList, function (item, index) {
            return index === reusedList.indexOf(item);
          })
          // Get Array of mapped models
          .map(function (destination) {
            return mapper
              .mapObjects(source, destination)
              .save();
          });
        can.when.apply(can, models)
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
          .always(function () {
            reusedList.replace([]);
            this.attr('isSaving', false);
            this.attr('checkReusedStatus', true);
          }.bind(this));
      }
    },
    events: {
      '{scope.selectedList} length': function (arr, ev, length) {
        this.scope.attr('hasSelected', length > 0);
      }
    }
  });
})(window.can, window.GGRC, window.CMS);
