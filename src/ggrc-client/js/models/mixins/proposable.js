/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Mixin from './mixin';
import {REFRESH_PROPOSAL_DIFF} from '../../events/eventTypes';

export default class Proposable extends Mixin {
  after_update() {
    this.dispatch({
      ...REFRESH_PROPOSAL_DIFF,
    });
  }
}

Proposable.isProposable = true;
