..
  Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: david@reciprocitylabs.com
  Maintained By: vraj@reciprocitylabs.com


.. _EventLogResource:

*********************
Event Log Resource
*********************

An event log resource represents changes made to GGRC resources resulting
from an atomic HTTP POST, PUT, or DELETE request. The event log resource
is intended to provide a feed of events that occur in GGRC for display to
users.

An event log resource has a media type of ``application/json`` and is an
object containing an :ref:`EventLog` object.

Example
=======

.. sourcecode:: javascript

    {
        "events_collection": {
            "selfLink": "/api/events",
            "events": [
                {
                    "selfLink": "/api/events/6",
                    "http_method": "POST",
                    "modified_by": {
                        "href": "/api/people/79",
                        "type": "Person",
                        "id": 79
                    },
                    "resource_id": 1457,
                    "created_at": "2013-07-29T14:51:52",
                    "updated_at": "2013-07-29T14:51:52",
                    "resource_type": "Section",
                    "context": null,
                    "id": 6,
                    "revisions": [
                        {
                            "href": "/api/revisions/6",
                            "type": "Revision",
                            "id": 6
                        }
                    ]
                }
            ]
        }
    }


Event Log Content
====================

.. list-table::
   :widths: 20 10 70
   :header-rows: 1

   * - Property
     - Type
     - Description
   * - ``activitylog``
     - object
     - Root property for the event log resource, an :ref:`EventLog`
       object.

.. _EventLog:

EventLog
===========

.. list-table::
   :widths: 30 10 60
   :header-rows: 1

   * - Property
     - Type
     - Description
   * - ``selfLink``
     - string
     - The url of this resource.
   * - ``entries``
     - array
     - A list of :ref:`ActivityEntry`.

.. _ActivityEntry:

ActivityEntry
-------------

.. list-table::
   :widths: 20 10 70
   :header-rows: 1

   * - Property
     - Type
     - Description
   * - ``selfLink``
     - string
     - URL of the activity entry resource.
   * - ``http_method``
     - string
     - The HTTP method for the recorded activity.
   * - ``resourceLink``
     - string
     - URL of the resource to which the request was made.
   * - ``resource_id``
     - string
     - ID of the target resource.
   * - ``resource_type``
     - string
     - Type name of the target resource.
   * - ``timestamp``
     - string
     - ISO 8601 formatted UTC timestamp indicating the time this activity was
       performed.
   * - ``userid``
     - string
     - Authenticated User ID on whose behalf the request was performed.
   * - ``revisions``
     - array
     - List of :ref:`RevisionEntry` for resources modified as part of the
       transaction satisfying the request.

