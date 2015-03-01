/*!
 Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 Created By: anze@reciprocitylabs.com
 Maintained By: anze@reciprocitylabs.com
*/


(function (can) {
  can.Model.Cacheable("CMS.Models.ThreatActor", {
    root_object: "threat_actor",
    root_collection: "threat_actors",
    category: "risk",
    findAll: "GET /api/threat_actors",
    findOne: "GET /api/threat_actors/{id}",
    create: "POST /api/threat_actors",
    update: "PUT /api/threat_actors/{id}",
    destroy: "DELETE /api/threat_actors/{id}",
    mixins: ["ownable", "contactable", "unique_title"],
    is_custom_attributable: true,
    attributes: {
      context: "CMS.Models.Context.stub",
      contact: "CMS.Models.Person.stub",
      owners: "CMS.Models.Person.stubs",
      modified_by: "CMS.Models.Person.stub",
      object_people: "CMS.Models.ObjectPerson.stubs",
      people: "CMS.Models.Person.stubs",
      object_documents: "CMS.Models.ObjectDocument.stubs",
      documents: "CMS.Models.Document.stubs",
      related_sources: "CMS.Models.Relationship.stubs",
      related_destinations: "CMS.Models.Relationship.stubs",
      object_objectives: "CMS.Models.ObjectObjective.stubs",
      objectives: "CMS.Models.Objective.stubs",
      object_controls: "CMS.Models.ObjectControl.stubs",
      controls: "CMS.Models.Control.stubs",
      object_sections: "CMS.Models.ObjectSection.stubs",
      sections: "CMS.Models.get_stubs"
    },
    tree_view_options: {},
    init: function () {
      this._super && this._super.apply(this, arguments);
      this.validatePresenceOf("title");
    }
  }, {});
})(window.can);
