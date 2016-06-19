# Copyright (C) 2016 Google Inc., authors, and contributors
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Benchmark context managers."""

import os
import inspect
import logging
import time
from collections import defaultdict

from flask import current_app


class BenchmarkContextManager(object):
  """Default benchmark context manager.

  This should be used used on appengine instances and by default on dev
  instances.
  """
  # pylint: disable=too-few-public-methods

  def __init__(self, message):
    self.message = message
    self.start = 0

  def __enter__(self):
    self.start = time.time()

  def __exit__(self, exc_type, exc_value, exc_trace):
    end = time.time()
    current_app.logger.info("{:.4f} {}".format(end - self.start, self.message))


class WithNop(object):
  """Nop benchmark context manager.

  This is a dummy context manager that can be used in place of default or debug
  context managers, you can disable them without removing lines of code.
  """
  # pylint: disable=too-few-public-methods

  def __init__(self, message):
    pass

  def __enter__(self):
    pass

  def __exit__(self, exc_type, exc_value, exc_trace):
    pass


class DebugBenchmark(object):
  """Debug benchmark context manager.

  This benchmark should be used when debugging performance issues. It has the
  most comprehensive output of all context managers.

  To enable this, just set GGRC_BENCHMARK env var on the server.

  Note that this benchmark is useful inside for loops with quiet set to True.
  The benchmark itself has some overhead. It's about 10 times slower than
  simple addition with func_name given. If func name is not given the it will
  run about 200 times slower than simple addition.

  For more precise measurements uncomment the c profiler in ggrc.__main__.
  """

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
    """Initialize a new instance of this benchmark.

    Args:
      message: String containing the message that will be display with the
        benchmark results. It should be unique for all instances.
      func_name: Name of the function where this benchmark has been
        initialized. If none is given, it will be populated automatically.
        Note that this is a slow process.
      form: String containing the format of the benchmark results. Two given
        options are COMPACT_FORM and FULL_FORM.
    """
    self.message = message
    self.quiet = quiet
    self.form = form
    self.start = 0
    if func_name is None:
      curframe = inspect.currentframe()
      calframe = inspect.getouterframes(curframe, 0)
      func_name = calframe[1][3]
    self.func_name = func_name

  def __enter__(self):
    """Start the benchmark timer."""
    if not self.quiet:
      msg = "{}{}: {}".format(
          self.PREFIX * DebugBenchmark._depth, self.func_name, self.message)
      logging.info(msg)
    if DebugBenchmark._depth == 0:
      self._reset_stats()
    DebugBenchmark._depth += 1
    self.start = time.time()

  def __exit__(self, exc_type, exc_value, exc_trace):
    """Stop the benchmark timer.

    This function gets the duration of the benchmark and stores it. If this is
    the outer most benchmark, the summary of all calls will be printed.
    """
    duration = time.time() - self.start
    DebugBenchmark._depth -= 1
    self.update_stats(duration)
    if not self.quiet:
      msg = self.form.format(
          prefix=self.PREFIX * DebugBenchmark._depth,
          **self._stats[self.message]
      )
      logging.fatal(msg)
    if DebugBenchmark._depth == 0:
      self._print_stats(self._stats)

  def _update_stats(self, stats, duration):
    """Add duration data to stats.

    Args:
      stats: mutable dict containing data that will be updated.
      duration: time measured by the benchmark.
    """
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
    """Print stats summary."""
    sorted_ = sorted(stats.values(), key=lambda item: item[sort_key],
                     reverse=True)
    for stat in sorted_:
      msg = cls.PRINT_FORM.format(
          prefix=stat["message"] + " - ",
          avg=stat["sum"] / stat["count"] if stat["count"] else 0,
          **stat
      )
      logging.info(msg)


def get_benchmark():
  """Get a benchmark context manager."""
  if os.environ.get("GGRC_BENCHMARK"):
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    return DebugBenchmark
  else:
    return BenchmarkContextManager
