/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import 'jasmine-fixture/dist/jasmine-fixture';
import './spec_setup';
import './spec_helpers';
import '../../static/dashboard-templates';
import '../javascripts/entrypoints/vendor';
import '../javascripts/entrypoints/dashboard';

var testsContext = require.context('../../..', true, /_spec\.js$/);
testsContext.keys().forEach(testsContext);
