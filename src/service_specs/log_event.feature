# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: brad@reciprocitylabs.com
# Maintained By: brad@reciprocitylabs.com

Feature: Log Javascript client events to syslog
  Background:
    Given service description

  Scenario: HTTP Post of log event
    Given HTTP POST to endpoint "log_event"
      """
      { "log_event": {
          "severity": "ERROR"
          , "description": "This was a test error."
        }
      }
      """
    Then a "200" status code is received
