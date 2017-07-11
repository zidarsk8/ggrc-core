/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, $) {
  'use strict';

  /**
   * A component implementing a modal for mapping objects to other objects,
   * taking the object type mapping constraints into account.
   */
  GGRC.Components('objectGenerator', {
    tag: 'object-generator',
    template: can.view(GGRC.mustache_path +
      '/components/object-generator/object-generator.mustache'),
    viewModel: function (attrs, parentViewModel) {
      var data = {
        object: attrs.object,
        join_object_id: attrs.joinObjectId,
        type: attrs.type
      };

      return {
        isLoadingOrSaving: function () {
          return this.attr('mapper.is_saving') ||
          this.attr('mapper.block_type_change') ||
          //  disable changing of object type while loading
          //  to prevent errors while speedily selecting different types
          this.attr('mapper.is_loading');
        },
        mapper: new GGRC.Models.MapperModel(can.extend(data, {
          relevantTo: parentViewModel.attr('relevantTo'),
          callback: parentViewModel.attr('callback'),
          useTemplates: true,
          assessmentGenerator: true
        }))
      };
    },

    events: {
      inserted: function () {
        var self = this;
        this.viewModel.attr('mapper.selected').replace([]);
        this.viewModel.attr('mapper.entries').replace([]);

        this.setModel();

        self.viewModel.attr('mapper').afterShown();
      },
      closeModal: function () {
        this.viewModel.attr('mapper.is_saving', false);
        this.element.find('.modal-dismiss').trigger('click');
      },
      '.modal-footer .btn-map click': function (el, ev) {
        var callback = this.viewModel.attr('mapper.callback');
        var type = this.viewModel.attr('mapper.type');
        var object = this.viewModel.attr('mapper.object');
        var assessmentTemplate =
          this.viewModel.attr('mapper.assessmentTemplate');
        var instance = CMS.Models[object].findInCacheById(
          this.viewModel.attr('mapper.join_object_id'));

        ev.preventDefault();
        if (el.hasClass('disabled') ||
        this.viewModel.attr('mapper.is_saving')) {
          return;
        }

        this.viewModel.attr('mapper.is_saving', true);
        return callback(this.viewModel.attr('mapper.selected'), {
          type: type,
          target: object,
          instance: instance,
          assessmentTemplate: assessmentTemplate,
          context: this
        });
      },
      setModel: function () {
        var type = this.viewModel.attr('mapper.type');

        this.viewModel.attr(
          'mapper.model', this.viewModel.mapper.modelFromType(type));
      },
      '{mapper} type': function () {
        var mapper = this.viewModel.attr('mapper');
        mapper.attr('filter', '');
        mapper.attr('afterSearch', false);

        this.setModel();

        setTimeout(mapper.onSubmit.bind(mapper));
      },
      '{mapper} assessmentTemplate': function (viewModel, ev, val, oldVal) {
        var type;
        if (_.isEmpty(val)) {
          return this.viewModel.attr('mapper.block_type_change', false);
        }

        val = val.split('-');
        type = val[1];
        this.viewModel.attr('mapper.block_type_change', true);
        this.viewModel.attr('mapper.type', type);
      }
    }
  });
})(window.can, window.can.$);
