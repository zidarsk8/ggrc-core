/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
describe('CMS.Models.Relationship ', function () {
  describe('unmap() method', function () {
    let model;

    beforeEach(function () {
      model = new CMS.Models.Relationship({id: 'testId'});
    });

    it('sends correct request if not cascade', function () {
      spyOn($, 'ajax').and.returnValue(jasmine.createSpyObj(['done']));

      model.unmap(false);

      expect($.ajax).toHaveBeenCalledWith({
        type: 'DELETE',
        url: '/api/relationships/testId?cascade=false',
      });
    });

    it('sends correct request if cascade', function () {
      spyOn($, 'ajax').and.returnValue(jasmine.createSpyObj(['done']));

      model.unmap(true);

      expect($.ajax).toHaveBeenCalledWith({
        type: 'DELETE',
        url: '/api/relationships/testId?cascade=true',
      });
    });

    it('triggers "destroyed" event', function () {
      spyOn($, 'ajax').and.returnValue(can.Deferred().resolve());
      spyOn(can, 'trigger');

      model.unmap(true);

      expect(can.trigger)
        .toHaveBeenCalledWith(model.constructor, 'destroyed', model);
    });
  });
});
