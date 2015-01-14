from datetime import date, datetime, timedelta
# import monthdelta

'''
All dates are calculated raw. They are not adjusted for holidays or workdays.
Use WorkflowDateCalculator.nearest_work_day() to get a date adjusted for
weekends & holidays.
'''
class WorkflowDateCalculator(object):

    def __init__(self, workflow=None):
        self.workflow = workflow

    '''
    direction = 1  indicates FORWARD
    direction = -1 indicates BACKWARD
    '''
    @staticmethod
    def nearest_work_day(date_, direction):
        holidays = []
        while date_.weekday() > 4 or date_ in holidays:
            date_ = date_ + datetime.timedelta(direction)
        return date_

    def calc_nearest_start_date_after_basedate(self, basedate):
        import monthdelta
        frequency = self.workflow.frequency
        min_relative_start_day = self._calc_min_relative_start_day_from_tasks()
        min_relative_start_month=self._calc_min_relative_start_month_from_tasks()
        print "(min_rel_start_month, min_rel_start_day) = ({m}, {d})"\
          .format(d=min_relative_start_day, m=min_relative_start_month)

        basedate_day_of_week = basedate.weekday()
        basedate_day_of_month = basedate.day
        basedate_month_of_year = basedate.month

        if "one_time" == frequency:
            return basedate
        elif "weekly" == frequency:
            if min_relative_start_day == basedate_day_of_week:
                return basedate
            elif min_relative_start_day > basedate_day_of_week:
                day_delta = min_relative_start_day - basedate_day_of_week
                return basedate + timedelta(days = day_delta)
            elif min_relative_start_day < basedate_day_of_week:
                day_delta = basedate_day_of_week - min_relative_start_day
                return basedate + timedelta(days = 7 - day_delta)
        elif "monthly" == frequency:
            if min_relative_start_day == basedate_day_of_month:
                return basedate
            elif min_relative_start_day > basedate_day_of_month:
                day_delta = min_relative_start_day - basedate_day_of_month
                return basedate + timedelta(days = day_delta)
            elif min_relative_start_day < basedate_day_of_month:
                return basedate + monthdelta(1)
                # next_month = basedate.month + 1
                # year = basedate.year
                # if 13 == next_month:
                #     year = basedate.year + 1
                # month = next_month % 12
                # day = basedate.day
                # return date(year=year, month=month, day=day)
        elif "quarterly" == frequency:
            base_quarter_month = (basedate_month_of_year % 3) + 1
            min_relative_start_quarter_month = min_relative_start_month
            if min_relative_start_quarter_month == base_quarter_month:
                if min_relative_start_day == basedate_day_of_month:
                    return basedate # Start today
                elif min_relative_start_day < basedate_day_of_month:
                    # We missed this cycle. Start the following quarter.
                    tmp_month = basedate_month_of_year
                    while ((tmp_month % 3) + 1) != min_relative_start_quarter_month:
                        tmp_month += 1
                    tmp_year = basedate.year
                    if tmp_month > 12:
                        tmp_year += 1
                        tmp_month -= 12
                    return date(year=tmp_year, month=tmp_month, day=min_relative_start_day)
                else:
                    return date(year=basedate.year, month=basedate_month_of_year, day=min_relative_start_day)
            elif min_relative_start_quarter_month < base_quarter_month:
                '''
                    2 < 3, where base actual month is Jun (6). Need to get Aug (8).
                    1 < 2, where base actual month is Feb (2). Need to get Apr (4).
                    1 < 3, where base actual month is Sep (9). Need to get Oct (10).

                    Need to compute the actual start date.
                '''
                # Brute force it. Couldn't figure out a reliable algorithm that I could guarantee works.
                # This isn't ideal in terms of performance. But number if iterations to find the correct date
                # will be less than 3. So it won't make a noticeable difference.
                tmp_month = basedate_month_of_year
                while ((tmp_month % 3) + 1) != min_relative_start_quarter_month:
                    tmp_month += 1
                tmp_year = basedate.year
                if tmp_month > 12:
                    tmp_year += 1
                    tmp_month -= 12
                #return
                return date(year=tmp_year, month=tmp_month, day=min_relative_start_day)
            else: #min_relative_start_quarter_month > base_quarter_month: Walk forward to a valid month
                return basedate + monthdelta(min_relative_start_quarter_month) - base_quarter_month
                # tmp_month = basedate_month_of_year + min_relative_start_quarter_month - base_quarter_month
                # tmp_year = basedate.year
                # if tmp_month > 12:
                #     tmp_year += 1
                #     tmp_month -= 12
                # return date(year=tmp_year, month=tmp_month, day=min_relative_start_day)
        elif "annually" == frequency:
            if basedate_month_of_year == min_relative_start_month:
                if basedate_day_of_month == min_relative_start_day:
                    return basedate
                elif basedate_day_of_month > min_relative_start_day:
                    return date(year=basedate.year+1, month=min_relative_start_month, day=min_relative_start_day)
                elif basedate_day_of_month < min_relative_start_day:
                    return date(year=basedate.year, month=min_relative_start_month, day=min_relative_start_day)
            elif basedate_month_of_year > min_relative_start_month:
                return date(year=basedate.year+1, month=min_relative_start_month, day=min_relative_start_day)
            else:
                return date(year=basedate.year, month=min_relative_start_month, day=min_relative_start_day)
        else:
            pass

    def calc_nearest_end_date_after_start_date(self, start_date):
        frequency = self.workflow.frequency
        max_relative_end_day = self._calc_max_relative_end_day_from_tasks()
        max_relative_end_month=self._calc_max_relative_end_month_from_tasks()

        start_date_day_of_week = start_date.weekday()
        start_date_day_of_month = start_date.day
        start_date_month_of_year = start_date.month
        start_date_year = start_date.year

        if "one_time" == frequency:
            if max_relative_end_month == start_date_month_of_year:
                if max_relative_end_day == start_date_day_of_month:
                    return start_date
                elif max_relative_end_day > start_date_day_of_month:
                    return date(year=start_date_year, month=max_relative_end_month, day=max_relative_end_day)
                else:
                    return date(year=start_date_year+1, month=max_relative_end_month, day=max_relative_end_day)
            elif max_relative_end_month < start_date_month_of_year:
                return date(year=start_date_year+1, month=max_relative_end_month, day=max_relative_end_day)
            else:
                return date(year=start_date_year, month=max_relative_end_month, day=max_relative_end_day)
        elif "weekly" == frequency:
            if max_relative_end_day == start_date_day_of_week:
                return start_date
            elif max_relative_end_day < start_date_day_of_week:
                import ipdb; ipdb.set_trace()
                return start_date + timedelta(days = max_relative_end_day + (6 - start_date_day_of_week))
            else:
                return start_date + timedelta(days = (max_relative_end_day - start_date_day_of_week))
        elif "monthly" == frequency:
            if max_relative_end_day == start_date_day_of_month:
                return start_date
            elif max_relative_end_day < start_date_day_of_month:
                _y = start_date_year
                _m = start_date_month_of_year
                if 12 == _m:
                    _m = 1
                    _y += 1
                return date(year=_y, month=_m, day=max_relative_end_day)
            else:
                return start_date + timedelta(days = (max_relative_end_day - start_date_day_of_month))
        elif "quarterly" == frequency:
            start_quarter_month = (start_date_month_of_year % 3) + 1
            if start_quarter_month == max_relative_end_month:
                if start_date_day_of_month == max_relative_end_day:
                    return start_date
                elif start_date_day_of_month < max_relative_end_day:
                    return date(year=start_date_year, month=start_date_month_of_year, day=max_relative_end_day)
                else:
                    _end_month = start_date_month_of_year + 3
                    _year = start_date_year
                    if _end_month > 12:
                        _year += _end_month / 12
                        _end_month = (_end_month % 12)
                    return date(year=_year, month=_end_month, day=max_relative_end_day)
            elif start_quarter_month < max_relative_end_month:
                return date(
                    year=start_date_year,
                    month=start_date_month_of_year+(max_relative_end_month-start_quarter_month),
                    day=max_relative_end_day)
            else:
                tmp_month = start_date_month_of_year
                while ((tmp_month % 3) + 1) != max_relative_end_month:
                    tmp_month += 1
                tmp_year = start_date_year
                if tmp_month > 12:
                    tmp_year += 1
                    tmp_month -= 12
                return date(year=tmp_year, month=tmp_month, day=max_relative_end_day)
        elif "annually" == frequency:
            if start_date_month_of_year == max_relative_end_month:
                if start_date_day_of_month == max_relative_end_day:
                    return start_date
                elif start_date_day_of_month < max_relative_end_day:
                    return date(year=start_date_year, month=start_date_month_of_year, day=max_relative_end_day)
                else:
                    return date(year=start_date_year+1, month=start_date_month_of_year, day=max_relative_end_day)
            elif start_date_month_of_year < max_relative_end_month:
                return date(year=start_date_year, month=max_relative_end_month, day=max_relative_end_day)
            else:
                return date(year=start_date_year+1, month=max_relative_end_month, day=max_relative_end_day)
        else:
            pass

    def calc_next_cycle_start_date_after_basedate(self, basedate):
        start_date = self.calc_nearest_start_date_after_basedate(basedate)
        frequency = self.workflow.frequency
        if "one_time" == frequency:
            return start_date
        elif "weekly" == frequency:
            return start_date + timedelta(days=7)
        elif "monthly" == frequency:
            _tmp_month = start_date.month + 1
            _year = start_date.year
            if _tmp_month > 12:
                _year += 1
                _tmp_month -= 12
            return date(year=_year, month=_tmp_month, day=start_date.day)
        elif "quarterly" == frequency:
            _tmp_month = start_date.month + 3
            _year = start_date.year
            if _tmp_month > 12:
                _year += 1
                _tmp_month -= 12
            return date(year=_year, month=_tmp_month, day=start_date.day)
        elif "annually" == frequency:
            return date(year=start_date.year + 1, month=start_date.month, day=start_date.day)
        else:
            pass

    def calc_previous_cycle_start_date_before_basedate(self, basedate):
        start_date = self.calc_nearest_start_date_after_basedate(basedate)
        frequency = self.workflow.frequency
        if "one_time" == frequency:
            return start_date
        elif "weekly" == frequency:
            return start_date - timedelta(days=7)
        elif "monthly" == frequency:
            _tmp_month = start_date.month - 1
            _year = start_date.year
            if _tmp_month < 1:
                _year -= 1
                _tmp_month += 12
            return date(year=_year, month=_tmp_month, day=start_date.day)
        elif "quarterly" == frequency:
            _tmp_month = start_date.month - 3
            _year = start_date.year
            if _tmp_month < 1:
                _year -= 1
                _tmp_month += 12
            return date(year=_year, month=_tmp_month, day=start_date.day)
        elif "annually" == frequency:
            #return start_date + timedelta(weeks=-365)
            return date(year=start_date.year - 1, month=start_date.month, day=start_date.day)
        else:
            pass

    def _calc_min_relative_start_month_from_tasks(self):
        # import ipdb; ipdb.set_trace()
        min_start_month = None
        for tg in self.workflow.task_groups:
            for t in tg.task_group_tasks:
                relative_start_month = t.relative_start_month
                if min_start_month is None or relative_start_month < min_start_month:
                    min_start_month = relative_start_month
        return min_start_month

    def _calc_min_relative_start_day_from_tasks(self):
        # import ipdb; ipdb.set_trace()
        min_start_day = None
        for tg in self.workflow.task_groups:
            for t in tg.task_group_tasks:
                relative_start_day = t.relative_start_day
                if min_start_day is None or relative_start_day < min_start_day:
                    min_start_day = relative_start_day
        return min_start_day

    def _calc_max_relative_end_day_from_tasks(self):
        # import ipdb; ipdb.set_trace()
        max_end_day = None
        for tg in self.workflow.task_groups:
            for t in tg.task_group_tasks:
                relative_end_day = t.relative_end_day
                if max_end_day is None or relative_end_day > max_end_day:
                    max_end_day = relative_end_day
        return max_end_day

    def _calc_max_relative_end_month_from_tasks(self):
        # import ipdb; ipdb.set_trace()
        max_end_month = None
        for tg in self.workflow.task_groups:
            for t in tg.task_group_tasks:
                relative_end_month = t.relative_end_month
                if max_end_month is None or relative_end_month > max_end_month:
                    max_end_month = relative_end_month
        return max_end_month
