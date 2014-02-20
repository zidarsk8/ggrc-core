# cache/utils/profiles.py
#
# This module collects profiles for any expression, python statement
#
# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: chandramouliv@google.com
# Maintained By: chandramouliv@google.com
#
import cProfile, pstats, StringIO

def create_profile():
     return cProfile.Profile()

def enable_profile(profile):
	profile.enable()

def disable_profile(profile):
	profile.enable()
	
def collect_profiles(expr):
	profile=create_profile()
	enable_profile(profile)
	expr
	disable_profile(profile)
	s = StringIO.StringIO()
	sortby = 'time'

	ps = pstats.Stats(prsc, stream=s).sort_stats(sortby)
	ps.print_stats()

	return s.getvalue()

