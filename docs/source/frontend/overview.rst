Overview
========

This document is a reference for anyone interested in understanding how
GGRC is constructed. The goal for this document is to explain how
everything works in moderate detail with references to source code which
can be used to understand in exact detail how GGRC works.

Client Side
-----------


Overview
~~~~~~~~

The client-side of GGRC is initially constructed from templates and/or
views defined and rendered on the server. The templates and views
provide a scaffolding for the UI. Rendering those elements invokes
JavaScript code which bootstraps the majority of the client-side of GGRC
which is constructed from CanJS Controls, Components and Mustache templates.

Once the Controls are rendered, they take control of generating the
remainder of the UI and attaching all relevant logic and user
interaction handlers.

There are two main objects that are useful in managing the data model:

-  ``GGRC``
-  ``CMS``

For example, ``GGRC.page_instance()`` returns the current page instance,
and ``GGRC.page_object`` is the object rendered by the current page
(e.g. a Program), as it was received from the server (mapped objects are
stubs).

``CMS.Models.<MODEL>.cache`` stores the loaded objects. For example,
``CMS.Models.Program.cache`` will have an array of all the loaded
programs.

Client-side File Manifests
~~~~~~~~~~~~~~~~~~~~~~~~~~

Mustache templates need to be referenced
from a manifest file in order for it to be usable in constructing the
UI.

These manifest files live in ``src/<module>/assets/assets.yaml``.

Javascript resources are bundled together using webpack.

Page Structure
~~~~~~~~~~~~~~

**TODO**: Show and talk about diagram with Title, LHN, Dashboard,
Dashboard Widget, Info Widget, TreeView & TreeNode.

.. figure:: /_static/res/page_structure.png
   :alt: Page structure

   Page structure


View Logic
^^^^^^^^^^

View logic is defined within the control (as functions on the control
itself).

Widgets (tabs)
~~~~~~~~~~~~~~

Which widgets (or tabs) are shown on the object page is defined in
``business_objects.js``.
This is where we state which controller or component should be used
for each tab:

-  ``InfoWidget Controller``, is used as first tab on the page and contain
    context of one (content of object for objects related pages
    (Program, Audit etc.) or active workflows statistics on My Work page)
-  ``Summary Controller``,
    is used on Audit page and shows statistics of status related Assessments.
-  Tree view tabs use ``tree-widget-container`` in order for wrap
    all inner logic of the tab (:ref:`tree-view-widget`).
-  ``TreeView/ListView Controllers`` are used only on the Admin Dashboard page.
    ListViews have pagination.

.. _tree-view-widget:

Tree view widget
~~~~~~~~~~~~~~~~

Tree view widget has a ``tree-widget-container`` as a wrapper,
that has a three major parts:

1) Filter
    a) The filter input where you can enter an arbitrary filter(corresponding to the rules for :ref:`filter-expressions`) as a string
    b) Multi-select dropdown with statuses
    c) :ref:`advanced-search`

2) Tree view grid
    a) Tree view grid
        ``tree-view`` component uses the :ref:`advanced-query-api` in order for
        fetch data for grid.
        The default query for first level of grid will looks like it:

        ..  code:: json

            {
                "object_name": "<tab model name>",
                "limit": "[0, 10]",
                "filters": {"expression": {
                    "object_name": "<page context model name>",
                    "op": {"name":"relevant"},
                    "ids": ["<id of context object>"]
                    }
                }
            }
    b) Pagination component (at the filter line and under the grid)
    c) Tree item action components (edit, preview, map logic and etc.)
    d) Sub-level of tree item
        Sub-level of tree item has limitation in 20 items. If object has
        more than 20 mapped object is shown link on this object in order to
        look at all related objects.

3) Info pane (preview of object)

.. figure:: /_static/res/tree-widget.png

.. _advanced-search:

Advanced search
~~~~~~~~~~~~~~~

``Advanced Search`` feature in GGRC provides a user simple way to perform
complicated search across required data. The feature allows to search objects
both by attributes and mappings.
Search by attributes include possibility to find object by any attributes
it has with “Contains”, “Equals”, “Does not contain”, “Is not equal”,
“Lesser than”, “Greater than” attributes.
Search by mappings allows to search objects by any level of mappings
(for example, “I would like to find a Control that is mapped to Program A,
where Program A is mapped to Regulation B and etc.). User is also able to
construct complex group expression with “AND”, “OR” conditions
(for example, “I would like to find a Control that is mapped to Program A
AND that is mapped to Regulation B and etc.)
``Advanced Search`` except tree view also integrated with Mapping and Global
search modals (:ref:`mapping-and-global-search`)
``Advanced Search`` UI generate a complex query to :ref:`advanced-query-api`
in order to fetch data from server side.

.. figure:: /_static/res/advanced-search.png


QuickFormController
~~~~~~~~~~~~~~~~~~~

This controller derives from the Modals controller in that it takes form
input, converts it into properties on model instances, and saves the
changes back to the server. A primary difference in QuickForm is that
any update to the instance triggered by QuickForm results in an
immediate save(). Also, QuickForm was created with the expectation that
the instance already exists on the server; attempts to work with new
model instances before first save may result in unexpected behavior.

-  How do controllers interact with controls?
-  How do controllers interact with the backend?

Model
~~~~~

View models (defined in JavaScript) are in
``src/<module>/assets/javascripts/models/``

The models define:

-  how a type of model relates to other types
-  behaviors relevant to the model

   -  validation rules
   -  event listeners
   -  default values
   -  default view templates
   -  initialization logic

-  metadata that allows the model to integrate with frameworks and other
   conventions

Stubs vs. Full-form Models
^^^^^^^^^^^^^^^^^^^^^^^^^^

All models have a stub and a full form. All collection attributes of a
full form object are stubs.

A stub is a lightweight representation of a full-form model. A stub has
references to complex attributes such as collections or other complex
models. But those references have to be “traded in” for either stubs or
full-form objects in order to walk through the data model. This approach
is somewhat analogous to “lazy-loading”.

In contrast, all of the models referenced by a full-form model are not
just placeholders, but are true model instances themselves. This
approach is more analogous to “eager-loading”.

A stub can be converted into a full-form instance by calling ``reify()``
on the stub. See also ``builder.json``.

Lifecycle of a Model
^^^^^^^^^^^^^^^^^^^^

-  Primary Operations
-  Saving

Saving is either done as an update or create operation. See Updating and
Creating below. \* Updating

Updating happens when an instance is known to exist on the server (the
determinant is whether the id property is set on the instance) and
``save()`` is called on the instance. The update is executed with a PUT
request to the object endpoint. \* Creating

Creating happens when an instance is known not to exist on the server
(id property is not set) and ``save()`` is called on the instance. The
create is executed with a POST request to the collection endpoint. \*
Deleting Deleting can only happen on an instance which is known to exist
on the server (see Updating above), when ``destroy()`` is called on a
model instance. The delete is executed with a DELETE request to the
object endpoint. Deletion may execute immediately on the server, in
which case the former data of the deleted object is returned, or
deletion may be offloaded to a background task, in which case the
returned content from the operation will reference the background_task
object. On the client side, the deferred returned from ``destroy()``
will not resolve until the background task completes.

-  Non-lifecycle Model Interactions
-  _transient property

This property is set on instances during modal operation. *transient is
meant to hold data that is not sent to the server and does not need to
be kept after the modal completes or is canceled. This is useful for
intermediary values for validation, or calculated default values for a
property. \* _pending*\ joins() / "deferred bindings"

Model instances can be joined to other objects as part of their regular
update cycles. After an update completes successfully, any deferred
binding operations contained in ``<instance>._pending_joins`` are
resolved by adding or removing join objects. These deferred bindings are
usually created by using ``<instance>.mark_for_addition()`` and
``<instance>.mark_for_deletion()`` \* other modal-based ops

The modal includes a connector widget that allows pending join object
creation and destruction. Since the connector widget automates the
deferred bindings for an instance in deferred mode, no action is taken
until the modal is saved.

Are they cached?

-  Server-side:

   -  Memcache

      -  Added to memcache *only* on “collection GET” requests, and
         expired on any “object PUT” or “object DELETE” requests.
      -  [The current locking mechanism (to avoid un-ordered operations
         from simultaneous requests) is broken and subject to race
         conditions. In its place, a more standard form of distributed
         locking should be used, paying attention to the constraints and
         guarantees made by App Engine's memcache service.]

-  Client-side:

   -  can.Model.Cacheable

      -  Once a model is retrieved to the browser, it is stored in
         ``CMS.Models.<model_name>.cache[<id>]``.  Once present, it is
         only requested again via the ``<instance>.refresh()`` method.
      -  A model can be conditionally pulled from the server (if it only
         exists on the client in stub form) by enqueueing it into a
         RefreshQueue, and then subsequently triggering the
         RefreshQueue. If an enqueued model has already been synched
         (i.e. if the selfLink property exists on the instance), it will
         not be re-fetched by the RefreshQueue.

How/when are they validated?

-  Server-side:

   -  In-database constraints
   -  SQLAlchemy validations (using ``@validates``)

-  Client-side:

   -  Defined in class ``init()`` method on Model classes, and uses Can
      Validations (http://canjs.com/docs/can.Map.validations.html)
   -  Includes a custom ``validateNonBlank()`` validation function that
      trims strings before checking for empty strings.

View
~~~~

View templates are implemented all in JavaScript with the help of Mustache.

Components
~~~~~~~~~~

In order to build the UI we are using components,
that are placed in the directory ``assets/javascripts/components``

Standard view templates
^^^^^^^^^^^^^^^^^^^^^^^

Several standard view fragments are defined for each type of entity
within GGRC. Additional fragments can be created and utilized as needed.
But these templates are the main templates from which the majority of
the UI is created.

-  ``info.mustache`` - Defines the “Info” widget on each object’s page.
    Defined per-widget in GGRC.Controllers.InfoWidget as the
   ``widget_view`` option, and specified using ``GGRC.WidgetList``
   definitions.
-  ``extended_info.mustache`` - Defines the content of an object’s
   tooltip/popover in the LHN lists.  Specified as the ``tooltip_view``
   parameter when rendering
   :src:`ggrc/assets/mustache/dashboard/lhn.mustache`.
-  ``modal_content.mustache`` - Defines the view for modal “create” or
   “edit” form functionality.  For most objects, this path is
   automatically generated using the ``data-template`` or
   ``data-object-plural`` attributes of the invoking element (see
   ``bootstrap/modal-ajax.js``.

Where to find view templates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The view files are in the following folder within a module
``src/<module>/assets/mustache/``.

For example, the ``ggrc_workflow`` views are in the following folder
:src:`ggrc_workflows/assets/mustache/`

View Helpers
^^^^^^^^^^^^

View helpers are defined using the Mustache `helper mechanism provided
by CanJS <http://canjs.com/docs/can.mustache.Helpers.html>`_.  Core
helpers are specified in
:src:`ggrc/assets/javascripts/mustache_helpers.js`,
and extension helpers should be specified in a file named similar to
``src/<module_name>/assets/javascripts/<class_name>_mustache_helpers.js``.

Extensions
~~~~~~~~~~

An extension is a bundle of code and assets packaged into a folder
hierarchy similar to ggrc-core. Extensions have at minimum a startup
script at <extension-folder>/__init__.py and a settings file in
<extension-folder>/settings

The extensions which are used in any GGRC instance are determined by the
GGRC_SETTINGS_MODULE shell variable. To add an extension to a GGRC
deployment, append a space separator and the Python path to the settings
file (e.g. " ggrc_some_extension.settings.development") to this shell
variable, and restart or redeploy the GGRC server.

The minimum that the extension settings file must contain is
``EXTENSIONS = ['<name_of_extension>']``. Additionally, global settings
can be provided; any variable set at the top level in this file will be
added to the ``ggrc.settings`` object and later accessible through
``from ggrc import settings``. Setting ``exports =`` to an array of key
names in the extension settings file will make those keys and their
values available to the client side through the ``GGRC.config`` object.

The minimum that __init__.py must contain is:

.. code:: python

    from flask import Blueprint

    blueprint = Blueprint(
        '<name_of_extension>',
        __name__,
        template_folder='templates',
        static_folder='static',
        static_url_path='/static/<name_of_extension>',
        )

This will set up an extension to be recognized by Flask.

Asset hierarchies in extensions should follow the ggrc-core model:
assets.yaml should define the bundles for dashboard-js,
dashboard-templates, and dashboard-js-specs; The folder naming
convention for these bundles (``assets/javascripts``,
``assets/mustache``, and ``assets/js_specs``, respectively) should be
followed for each extension. An important caveat is that the assets
bundler can only bundle one asset with a given path over all base
folders, so you should avoid re-using paths known to exist in ggrc-core
or other extensions (e.g. "mustache_helper.js" and "models/mixins.js"
already exist in ggrc-core, so don't name your files the same as these).

DB migrations should be set up in ``migrations/versions`` as in
ggrc-core. Once the extension is created and the settings path added to
GGRC_SETTINGS_MODULE, db_migrate should pick up any migrations
automatically. To completely undo the migrations from an extension (in
order to remove it without possible database breakage), use the command
``db_downgrade <name_of_extension> -1``

Extension contributions
^^^^^^^^^^^^^^^^^^^^^^^

-  Models

Define models in your ``<extension_name>/models/`` folder, and use the
same patterns for implementing them as ggrc-core does (derive from
ggrc.db.Model, use provided mixins, make association proxy tables and
models, etc.). Be sure to import all files from models as part of the
extension's __init__.py

-  Services

Services provide the CRUD object endpoints over REST to allow instances
of your extension models. ggrc-core provides a contributions mechanism
for defining more services from your extension at startup time. The
services contribution is done as such:

\`\`\`python from . import models from ggrc.services.registry import
service

def contributed_services(): return [ service(m.\ **table**.name, m) for
m in models.\ **dict**.values() if isinstance(m, type) and issubclass(m,
db.Model) ] \`\`\`

-  Views
-  Any special templates should be placed under
   <extension_module_name>/templates/ and called as normal.
-  To set up an object page for one of the contributed model classes,
   declare a function similar to this (this function will work as long
   as your module hierarchy is flat with all models at the first level
   and you want all of your objects to have pages):

\`\`\`python from ggrc.views.registry import object_view from . import
models from ggrc import db

def contributed_object_views(): return [ object_view(m) for m in
models.\ **dict**.values() if isinstance(m, type) and issubclass(m,
db.Model) ] \`\`\`

-  Roles
-  ROLE_CONTRIBUTIONS: at module level, subclass ``RoleContributions``,
   overriding ``contributions``, and set this property to an instance of
   the subclass.
-  ROLE_DECLARATIONS: at module level, subclass ``RoleDeclarations``,
   overriding ``roles()``, and set this property to an instance of the
   subclass.

Modals
~~~~~~

The core logic and functionality related to modals is defined in the
following files:

-  ``ggrc/assets/javascripts/bootstrap/modal-ajax.js``
-  ``ggrc/assets/javascripts/bootstrap/modal-form.js``
-  ``ggrc/assets/javascripts/controllers/modals_controller.js``

The view for a modal is defined in
``/src/<module>/assets/mustache/<class_name>/modal_content.mustache``.

More about modals in `modals.md <modals.md>`_.

Events
~~~~~~

Client-side event firing/handling is handled through CanJS, which is
primarily based on jQuery event handling.

Program Flow
~~~~~~~~~~~~

Legacy part of client-side logic is implemented in Controls. Much of this logic is
implemented using asynchronous callbacks via
`can.Deferred <http://canjs.com/docs/can.Deferred.html>`_.
All new features are written in component-based approach.

Error Handling
~~~~~~~~~~~~~~

Most errors are reported to the system with a ``window.onerror`` handler
that generates flash messages at the top of the page and reports the
exception back to Tracker. For maximum coverage, the script that defines
this handler is inlined into base.haml.

AJAX failures that happen while a modal is active are reported back to a
flash handler at the modal level (so that the flash messages are not
covered by modals or overlays).

Because the error handler at the window level handles most of our needs,
try/catch blocks are rare in GGRC. However, it is worth noting that
errors in Deferred callbacks may not fire the onerror handler, *and*
"break the chain" inasmuch as the state of the deferred never changes
from "pending" after that, and other deferreds waiting for the result of
that deferred will never run. This is a failure of the jQuery Deferred
object to sensibly handle uncaught errors (they should reject the
deferred instead). In the case where it's possible that a callback will
throw an error, it is recommended to wrap the content of the callback in
``try/catch`` and return a rejected deferred when an error happens.


Mappings
~~~~~~~~

Mappings are best thought of as **links**. (“Mapping”
`often means <http://www.merriam-webster.com/dictionary/mapping>`_ a 1-to-1
correspondence, and for historical reasons is the term adopted by GGRC
users; but in actuality; we have links between objects - e.g. a
Directive is **linked** to a Section, or a Programs **references** zero
or more Controls.) “Mappings” are a way to relate any model instance to
another model instance in a way that is flexible, and doesn't require
modifying the relational structure in the underlying data store used for
persistence (database). They're essentially just an abstraction over our
database, so that you don't have to care about which tables the
relationships are stored in.

Mappings essentially turn the entire system into a
`property graph <https://github.com/tinkerpop/gremlin/wiki/Defining-a-Property-Graph>`_.

Mappings are defined in :src:`ggrc/assets/javascripts/models/mappings-ggrc.js`.

We don't have a function that gets all the objects mapped to a given
object. You can get the mappings of an instance by calling
``instance.get_mappings('_mapping_')`` if the mappings are already
loaded, or by calling
``instance.get_binding('_mapping_').refresh_list()`` if they are not.

Types of Mappings
^^^^^^^^^^^^^^^^^

There are 8 types of mappings. The types of mappings are defined with
Mappers. Mappers are defined in :src:`ggrc/assets/javascripts/models/mappers.js`

Each type of mapping is defined below:

-  **Proxy** :src:`ggrc/assets/javascripts/models/mappers/proxy-list-loader.js`:
   A proxy mapping is a relationship where one model
   references another through another “join” or “proxy” model.  E.g.,
   Programs reference Controls via the ProgramControl join/proxy model.
    The Proxy mapping specifies the attributes and models involved in
   the relationship, e.g.:

-  **Direct** :src:`ggrc/assets/javascripts/models/mappers/direct-list-loader.js`:
   A direct mapping is a relationship where one model
   directly references another model.  E.g., Sections contain a
   ``directive`` attribute, so Section has a Direct mapping to
   Directive.

-  **Indirect** :src:`ggrc/assets/javascripts/models/mappers/indirect-list-loader.js`:
   An indirect mapping is the reverse of ``Direct``, but
   the implementation is inconsistent with the rest of the mappers.

-  **Search** :src:`ggrc/assets/javascripts/models/mappers/search-list-loader.js`:
   A search mapping is a relationship where results are
   produced by a function returning a deferred. This mapping is f
   foremost used by the Advanced Search feature and for getting owned
   objects for a Person, but other uses are also possible. Note that the
   search function is run at attach time and also when a new object of
   any type is created, so it is recommended to use this mapper
   sparingly in the system if it makes a number of large AJAX calls.

-  **Multi** :src:`ggrc/assets/javascripts/models/mappers/multi-list-loader.js`:
   Constructs a mapping which is the union of zero or more
   other mappings.  Specifically, the set of ``result.instance`` values
   is the union of ``result.instance`` from the contributing mappings.

-  **TypeFilter** :src:`ggrc/assets/javascripts/models/mappers/type-filtered-list-loader.js`:
   A TypeFiltered mapping takes the result of another
   mapping and returns only the results which are instances of a
   specified type. This is useful for filtering polymorphic proxies.

-  **CustomFilter** :src:`ggrc/assets/javascripts/models/mappers/custom-filtered-list-loader.js`:
   A custom filtered mapping runs a filter function on
   every result coming from a source mapping and returns all results
   where the function returns either a truthy value or a deferred that
   resolves to a truthy value. The filter function is re-run whenever an
   instance in the source mapping changes, and adds and removes a
   mapping to that instance accordingly.

-  **Cross** :src:`ggrc/assets/javascripts/models/mappers/cross-list-loader.js`:
   Similar to Proxy mapping, but joins across other mappings.
   For example, the result of ``m = Cross("a", "b")`` would be the
   union of the “b” mappings for every instance in the root object’s “a”
   result set.
