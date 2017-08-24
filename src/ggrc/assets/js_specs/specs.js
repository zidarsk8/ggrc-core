/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import 'jasmine-fixture/dist/jasmine-fixture';
import './spec_setup';
import './spec_helpers';
import '../../static/dashboard-templates';
import '../javascripts/entrypoints/vendor';
import '../javascripts/entrypoints/dashboard';
import '../../../ggrc_basic_permissions/assets/javascripts';
import '../../../ggrc_gdrive_integration/assets/javascripts';
import '../../../ggrc_risk_assessments/assets/javascripts';
import '../../../ggrc_risks/assets/javascripts';
import '../../../ggrc_workflows/assets/javascripts';

var testsContext = require.context('../../..', true, /_spec\.js$/);
testsContext.keys().forEach(testsContext);
