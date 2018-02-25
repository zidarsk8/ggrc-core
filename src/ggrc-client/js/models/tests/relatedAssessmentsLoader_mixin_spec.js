/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

const ENDPOINT = '/api/related_assessments';

describe('relatedAssessmentsLoader mixin', () => {
  beforeEach(() => {
    spyOn($, 'get');
  });

  describe('for Assessment model', () => {
    it('should contain getRelatedAssessments method', () => {
      const model = new CMS.Models.Assessment({});

      expect(model.getRelatedAssessments).toBeTruthy();
    });
  });

  describe('for Control model', () => {
    it('should contain getRelatedAssessments method', () => {
      const model = new CMS.Models.Control({});

      expect(model.getRelatedAssessments).toBeTruthy();
    });
  });

  describe('for Objective model', () => {
    it('should contain getRelatedAssessments method', () => {
      const model = new CMS.Models.Objective({});

      expect(model.getRelatedAssessments).toBeTruthy();
    });
  });

  describe('for Snapshot model', () => {
    it('should build correct response', () => {
      const model = new CMS.Models.Control({
        id: 1,
        type: 'Control',
        snapshot: {
          child_type: 'Control',
          child_id: 13,
          type: 'Snapshot',
        },
      });

      model.getRelatedAssessments();

      expect($.get).toHaveBeenCalledWith(ENDPOINT, {
        object_id: 13,
        object_type: 'Control',
        limit: '0,5',
      });
    });
  });

  describe('for other models', () => {
    it('should not contain getRelatedAssessments method', () => {
      const audit = new CMS.Models.Audit({});
      const program = new CMS.Models.Program({});
      const reg = new CMS.Models.Regulation({});
      const system = new CMS.Models.System({});
      const issue = new CMS.Models.Issue({});
      const section = new CMS.Models.Section({});

      expect(audit.getRelatedAssessments).toBeFalsy();
      expect(program.getRelatedAssessments).toBeFalsy();
      expect(reg.getRelatedAssessments).toBeFalsy();
      expect(system.getRelatedAssessments).toBeFalsy();
      expect(issue.getRelatedAssessments).toBeFalsy();
      expect(section.getRelatedAssessments).toBeFalsy();
    });
  });

  it('should send default limit as "0,5"', () => {
    const model = new CMS.Models.Assessment({id: 1, type: 'Assessment'});

    model.getRelatedAssessments();

    expect($.get).toHaveBeenCalledWith(ENDPOINT, {
      object_id: 1,
      object_type: 'Assessment',
      limit: '0,5',
    });
  });

  it('should send correct limit values', () => {
    const model = new CMS.Models.Assessment({id: 1, type: 'Assessment'});

    model.getRelatedAssessments([0, 10]);

    expect($.get).toHaveBeenCalledWith(ENDPOINT, {
      object_id: 1,
      object_type: 'Assessment',
      limit: '0,10',
    });
  });

  it('should send correct order_by value', () => {
    const model = new CMS.Models.Assessment({id: 1, type: 'Assessment'});

    model.getRelatedAssessments([0, 10], [{field: 'foo', direction: 'asc'}]);

    expect($.get).toHaveBeenCalledWith(ENDPOINT, {
      object_id: 1,
      object_type: 'Assessment',
      limit: '0,10',
      order_by: 'foo,asc',
    });
  });

  it('should send correct order_by value for multiple fields', () => {
    const model = new CMS.Models.Assessment({id: 1, type: 'Assessment'});

    model.getRelatedAssessments([0, 10], [
      {field: 'foo', direction: 'asc'},
      {field: 'bar', direction: 'desc'},
    ]);

    expect($.get).toHaveBeenCalledWith(ENDPOINT, {
      object_id: 1,
      object_type: 'Assessment',
      limit: '0,10',
      order_by: 'foo,asc,bar,desc',
    });
  });
});
