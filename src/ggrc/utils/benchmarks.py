# Copyright (C) 2016 Google Inc., authors, and contributors
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Benchmark context managers."""

import inspect
import logging
import time
from collections import defaultdict

from flask import current_app


class BenchmarkContextManager(object):

  def __init__(self, message):
    self.message = message

  def __enter__(self):
    self.start = time.time()

  def __exit__(self, exc_type, exc_value, exc_trace):
    end = time.time()
    current_app.logger.info("{:.4f} {}".format(end - self.start, self.message))


class WithNop(object):

  def __init__(self, message):
    pass

  def __enter__(self):
    pass

  def __exit__(self, exc_type, exc_value, exc_trace):
    pass


class DebugBenchmark(object):

  _depth = 0
  PREFIX = "|   "
  COMPACT_FORM = "{prefix}{last:.4f}"
  FULL_FORM = ("{prefix}current: {last:.4f} - max: {max:.4f} - min: "
               "{min:.4f} - sum: {sum:.4f} - count: {count:.4f}")
  PRINT_FORM = ("sum: {sum:>9.5f}  - count: {count:>10.5f}  - avg {avg:8.5f}"
                " - max: {max:8.5f}  - min: {min:8.5f}  - {message}")

  _stats = defaultdict(lambda: defaultdict(float))
  _all_stats = defaultdict(lambda: defaultdict(float))

  def __init__(self, message, func_name=None, form=COMPACT_FORM, quiet=False):
    self.message = message
    self.quiet = quiet
    self.form = form
    if func_name is None:
      curframe = inspect.currentframe()
      calframe = inspect.getouterframes(curframe, 0)
      func_name = calframe[1][3]
    self.func_name = func_name

  def __enter__(self):
    if not self.quiet:
      logging.info("{}{}: {}".format(
          self.PREFIX * DebugBenchmark._depth, self.func_name, self.message))
    if DebugBenchmark._depth == 0:
      self._reset_stats()
    DebugBenchmark._depth += 1
    self.start = time.time()

  def __exit__(self, exc_type, exc_value, exc_trace):
    duration = time.time() - self.start
    DebugBenchmark._depth -= 1
    self.update_stats(duration)
    if not self.quiet:
      logging.fatal(self.form.format(
          prefix=self.PREFIX * DebugBenchmark._depth,
          **self._stats[self.message]
      ))
    if DebugBenchmark._depth == 0:
      self._print_stats(self._stats)

  def _update_stats(self, stats, duration):
    stats[self.message]["message"] = self.message
    stats[self.message]["count"] += 1
    stats[self.message]["sum"] += duration
    stats[self.message]["last"] = duration
    stats[self.message]["max"] = max(stats[self.message]["max"], duration)
    stats[self.message]["min"] = min(
        stats[self.message]["min"] or duration,  # ignore initial zero
        duration
    )

  def update_stats(self, duration):
    self._update_stats(self._all_stats, duration)
    self._update_stats(self._stats, duration)

  @classmethod
  def print_stats(cls):
    cls._print_stats(cls._all_stats)

  @classmethod
  def _reset_stats(cls):
    cls._stats = defaultdict(lambda: defaultdict(float))

  @classmethod
  def _print_stats(cls, stats, sort_key="sum"):
    sorted_ = sorted(stats.values(), key=lambda item: item[sort_key],
                     reverse=True)
    for stat in sorted_:
      logging.fatal(cls.PRINT_FORM.format(
          prefix=stat["message"] + " - ",
          avg=stat["sum"] / stat["count"] if stat["count"] else 0,
          **stat
      ))
