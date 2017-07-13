/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.SnapshotScopeUpdater', function () {
  'use strict';

  var Component;  // the component under test
  var scope;
  var originalHtml;
  var original;
  var containerVM;

  beforeAll(function () {
    Component = GGRC.Components.get('SnapshotScopeUpdater');
    scope = Component.prototype.scope;
    originalHtml = document.body.innerHTML;
    original = {
      instance: scope.instance,
      snapshotModels: scope.snapshotModels
    };
  });

  afterAll(function () {
    document.body.innerHTML = originalHtml;
    _.extend(scope, original);
  });

  beforeEach(function () {
    document.body.innerHTML =
      '<tree-widget-container><tree-widget-container>' +
      '<tree-widget-container><tree-widget-container>';
    containerVM = {
      setRefreshFlag: jasmine.createSpy('setRefreshFlag'),
      display: jasmine.createSpy('display'),
      model: {
        model_singular: 'A'
      }
    };
    _.extend(scope, {
      instance: new can.Map({
        title: 'TITLE',
        refresh: jasmine
          .createSpy('refresh'),
        save: jasmine.createSpy('save')
      }),
      snapshotModels: ['A', 'B']
    });
    spyOn($.prototype, 'viewModel').and.returnValue(containerVM);
  });

  describe('upsertIt() method', function () {
    var method;

    beforeAll(function () {
      method = scope.upsertIt.bind(scope);
    });

    beforeEach(function () {
      spyOn(GGRC.Controllers.Modals, 'confirm').and.callThrough();
    });

    describe('calls confirm method', function () {
      it('one time', function () {
        method(scope);

        expect(GGRC.Controllers.Modals.confirm).toHaveBeenCalled();
      });

      it('with given params', function () {
        method(scope);

        expect(GGRC.Controllers.Modals.confirm.calls.argsFor(0)).toEqual([
          jasmine.objectContaining({
            instance: scope.instance,
            button_view: GGRC.Controllers.Modals.BUTTON_VIEW_OK_CLOSE,
            skip_refresh: true
          }),
          jasmine.any(Function),
          jasmine.any(Function)
        ]);
      });
    });
  });

/**
 * Next are tests depended on upsertIt() method
 * Begin
 */
  describe('_refreshContainers() method', function () {
    var method;

    beforeAll(function () {
      method = scope._refreshContainers.bind(scope);
      spyOn(GGRC.Utils.CurrentPage, 'refreshCounts');
    });

    it('refreshes all page counters', function () {
      method();
      expect(GGRC.Utils.CurrentPage.refreshCounts).toHaveBeenCalled();
    });

    it('sets refresh flag for each tree-widget-container that contains' +
    ' snapshots', function () {
      method();

      $('tree-widget-container').each(function () {
        var viewModel = $(this).viewModel();
        expect(viewModel.setRefreshFlag).toHaveBeenCalledWith(true);
      });
    });

    it('does not set refresh flag for each tree-widget-container that does ' +
    'not contain snapshots', function () {
      _.extend(containerVM.model, {model_singular: 'C'});
      method();
      $('tree-widget-container').each(function () {
        var viewModel = $(this).viewModel();
        expect(viewModel.setRefreshFlag).not.toHaveBeenCalled();
      });
    });
  });

  describe('_success() method', function () {
    var method;
    var refreshDfd;

    beforeAll(function () {
      method = scope._success.bind(scope);
    });

    beforeEach(function () {
      refreshDfd = new $.Deferred();
      scope.instance.refresh.and.returnValue(refreshDfd);
      spyOn(GGRC.Errors, 'notifier');
    });

    it('refreshes the instance attached to the component', function () {
      method();
      expect(scope.instance.refresh).toHaveBeenCalled();
    });

    describe('after instance refresh', function () {
      it('saves the instance attached to the component', function () {
        method();
        refreshDfd.resolve();
        expect(scope.instance.save).toHaveBeenCalled();
      });

      it('sets snapshots attr for the instance', function () {
        method();
        refreshDfd.resolve();

        expect(scope.instance.attr('snapshots'))
          .toEqual(
            jasmine.objectContaining({
              operation: 'upsert'
            })
          );
      });

      it('sets snapshots attr for the instance', function () {
        method();
        refreshDfd.resolve();

        expect(scope.instance.attr('snapshots'))
          .toEqual(
            jasmine.objectContaining({
              operation: 'upsert'
            })
          );
      });
    });
  });
/**
 * End
 */
});
