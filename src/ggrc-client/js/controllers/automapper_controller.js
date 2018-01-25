/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import RefreshQueue from '../models/refresh_queue';

(function (CMS, GGRC, can, $) {
  let MIN_WAIT = 2000;
  let MAX_WAIT = 5000;

  let refresher = {
    instanceQueue: [],
    lastRefresh: Date.now(),
    refreshInstance: function (instance) {
      this.instanceQueue.push(instance);
      setTimeout(this.tick(instance), MIN_WAIT);
    },
    tick: function (instance) {
      return (function () {
        let isCurrent =
          this.instanceQueue[this.instanceQueue.length - 1] === instance;
        let isOverdue = (this.lastRefresh + MAX_WAIT) < Date.now();
        if (isCurrent || isOverdue) {
          this.go();
        }
      }).bind(this);
    },
    go: function () {
      let instances = this.instanceQueue;
      let rq = new RefreshQueue();
      this.lastRefresh = Date.now();
      this.instanceQueue = [];
      can.each(instances, function (refreshInstance) {
        rq.enqueue(getRefreshableObjects(refreshInstance));
      });
      rq.trigger();
    },
  };

  let flashWarning = function () {
    // timeout is required because a 'mapping created' success flash will show up
    // and we do not currently support multiple simultaneous flashes
    setTimeout(function () {
      $(document.body).trigger('ajax:flash', {
        warning: 'Automatic mappings were not created because that would ' +
        'result in too many new mappings',
      });
    }, 2000); // 2000 is a magic number that feels nice in the UI
  };

  let Controller = can.Control({
    '{CMS.Models.Relationship} created': function (model, ev, instance) {
      let limitExceeded;
      let rq;
      if (instance instanceof CMS.Models.Relationship) {
        limitExceeded = instance.extras &&
          instance.extras.automapping_limit_exceeded;
        if (limitExceeded) {
          flashWarning();
        } else {
          refresher.refreshInstance(instance);
        }
      } else if (instance instanceof CMS.Models.ObjectPerson) {
        rq = new RefreshQueue();
        rq.enqueue(instance.personable);
        rq.trigger();
      }
    },
  });

  function isPersonInstance(instance) {
    return instance instanceof CMS.Models.ObjectPerson;
  }

  function getRefreshableObjects(instance) {
    let result = [];

    if (isPersonInstance(instance) && instance.personable) {
      result.push(instance.personable);
    } else {
      result.push(instance.source);
      result.push(instance.destination);
    }

    return result;
  }

  $(function () {
    new Controller();
  });
})(window.CMS, window.GGRC, window.can, window.can.$);

