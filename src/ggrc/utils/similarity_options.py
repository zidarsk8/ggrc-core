# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Defines similarity_options for classes implementing WithSimilarityScore."""

ASSESSMENT = {
    "relevant_types": {
        "Objective": {"weight": 2},
        "Control": {"weight": 2},
    },
    "threshold": 1,
}

# similarity_options for assessment and request are the same at the moment
REQUEST = ASSESSMENT
