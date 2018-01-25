/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import 'jasmine-fixture/dist/jasmine-fixture';
import './spec_setup';
import './spec_helpers';
import '../../ggrc/static/dashboard-templates';
import '../js/entrypoints/vendor';
import '../js/entrypoints/dashboard';

let testsContext = require.context('../', true, /_spec\.js$/);

testsContext.keys().forEach(testsContext);
