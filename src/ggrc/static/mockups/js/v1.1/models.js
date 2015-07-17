/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

var Assessment = can.Model.LocalStorage.extend({
},{
  init: function(){
    this.name = "workflow";
    this.on('change', function(ev, prop){
      if(prop === 'text' || prop === 'complete'){
        ev.target.save();
      }
    });
  },
});

var Workflow = can.Model.LocalStorage.extend({
},{
  init: function(){
    this.name = "assessmentWorkflows-v3";
    this.on('change', function(ev, prop){
      if(prop === 'text' || prop === 'complete'){
        ev.target.save();
      }
    });
  }
});

var Task = can.Model.LocalStorage.extend({
},{
  init: function(){
    this.name = "task";
    this.on('change', function(ev, prop){
      if(prop === 'text' || prop === 'complete'){
        ev.target.save();
      }
    });
  }
});


var ProgramList = [{
  name: 'program',
  title: 'Google Fiber',
  description: '<p><b>ISO/IEC 27001</b>, part of the growing&nbsp;<a href="http://en.wikipedia.org/wiki/ISO/IEC_27000-series">ISO/IEC 27000 family of standards</a>, is an&nbsp;<a href="http://en.wikipedia.org/wiki/Information_security_management_system">information security management system</a>&nbsp;(ISMS) standard published in October 2005 by the&nbsp;<a href="http://en.wikipedia.org/wiki/International_Organization_for_Standardization">International Organization for Standardization</a>&nbsp;(ISO) and the&nbsp;<a href="http://en.wikipedia.org/wiki/International_Electrotechnical_Commission">International Electrotechnical Commission</a>&nbsp;(IEC). Its full name is&nbsp;<i>ISO/IEC 27001:2005 – Information technology – Security techniques – Information security management systems – Requirements</i>.</p><p>ISO/IEC 27001 formally specifies a management system that is intended to bring information security under explicit management control. Being a formal specification means that it mandates specific requirements. Organizations that claim to have adopted ISO/IEC 27001 can therefore be formally audited and certified compliant with the standard (more below).</p>',
  owner: 'liz@reciprocitylbas.com',
  contact: 'ken@reciprocitylbas.com'
}];
var Objects = {
  controls: [
    {type: "control", name: "Secure Backups"},
    {type: "control", name: "Data Storage"},
    {type: "control", name: "Password Security"},
    {type: "control", name: "Access Control"},
    {type: "control", name: "Stability and Perpetuability"}
  ],
  objectives: [
    {type: "objective", name: "Establish a schedule"}
  ],
  standards: [
    {type: "standard", name: "ASHRAE 90.1"}
  ],
  policies: [
    {type: "policy", name: "Probationary Terms"},
    {type: "policy", name: "Medical Leave"}
  ],
  contracts: [
    {type: "contract", name: "Master Service Agreement"},
    {type: "contract", name: "SaaS Vendor Contract"},
    {type: "contract", name: "Company X Contract"}
  ],
  regulations: [
    {type: "regulation", name: "SOX"},
    {type: "regulation", name: "PCI DSS v2.0"}
  ],
};
var People = [
  {type: "person", name: "Vladan Mitevski"},
  {type: "person", name: "Predrag Kanazir"},
  {type: "person", name: "Dan Ring"},
  {type: "person", name: "Silas Barta"},
  {type: "person", name: "Cassius Clay"},
];



var taskList = new Task.List({});
var assessmentList = new Assessment.List({});
create_seed();
