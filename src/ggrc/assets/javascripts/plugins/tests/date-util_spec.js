/*
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import {getClosestWeekday} from '../utils/date-util';

 describe('GGRC.Utils.DateUtil', ()=> {
  describe('adjustToClosestWeekday() method', ()=> {
    it('adjusts to Friday when weekend provided', ()=> {
      let date = new Date(2017, 11, 24);
      let actual;

      actual = getClosestWeekday(date);

      expect(actual.getDate()).toEqual(22);
    });

    it('leaves date as is when week day provided', ()=> {
      let date = new Date(2017, 11, 20);
      let actual;

      actual = getClosestWeekday(date);

      expect(actual.getDate()).toEqual(20);
    });
  });
 });
