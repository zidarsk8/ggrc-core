# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Defines similarity_options for classes implementing WithSimilarityScore."""

ASSESSMENT = {
    "relevant_types": {
        "Audit": {"weight": 5},
        "Regulation": {"weight": 3},
        "Control": {"weight": 10},
    },
    "threshold": 5,
}

# similarity_options for assessment and request are the same at the moment
REQUEST = ASSESSMENT
