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
