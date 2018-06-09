Access Control
==============

Role Based Access Control & Access Control List
-----------------------------------------------

⚠️ GGRC is currently in the process of refactoring the role based access control
permission system (RBAC) to access control list (ACL).

The progress is tracked in the `ACL technical design document
<https://docs.google.com/document/d/1i-iutQOHzfgAIizgRzTGGMUb7PyS7LfwUTAvcPiTFwg/edit#heading=h.xgjl2srtytjt>`_.


Roles
-----

Below is a complete list of roles a user can have in GGRC

- **Global Roles** No access, Creator, Reader, Editor, Administrator, Superuser
- **Program roles** Program Manager, Program Editor, Program Reader
- **Workflows roles** Workflow Manager, Workflow Member
- **Assessment Object roles** Assignees (Creator, Assessor, Verifier)
- **Object Roles** Object Admins, Primary contacts, Secondary contacts, Primary Assessors, Secondary Assessors

Global Roles
~~~~~~~~~~~~

GGRC has 6 global roles:

- **No Role** - users with no access are not allowed to get passed the login page. They are marked as Inactive users inside the app.
- **Creator** users are allowed to create any GGRC object, but they are only allowed to see their own objects or objects where they were explicitly given access to by another role (object owner, program manager, assignee, …).
- **Reader** users have READ access to all the objects in GGRC. In addition to this, they also have the ability to CREATE any object much like users with the Creator role. Currently there is no way to give a user READ only access to the app. Every user (except for the ones with No access role) are allowed to create their own objects.
- **Editor** users can READ & EDIT all objects in GGRC and similar to Reader and Creator roles they can also CREATE their own objects.
- **Administrator** users can do all of the above plus they are granted access to the admin dashboard where they can grant System wide roles to other users. They can also add global custom attributes to GGRC objects.
- **Superuser** that is set in the app config (GGRC_BOOTSTRAP_ADMIN_USERS). It behaves completely the same as the Administrator role, but it can’t be unassigned through the application interface (a change in the config is required).

RBAC Implementation
-------------------

All the roles described above are scattered through multiple database tables.

Database Tables
~~~~~~~~~~~~~~~

- `roles` table stores all the possible system wide roles. The permissions that the roles grant are stored in the code, where each role in the database has a corresponding python file with a list of permissions that the role grants, e.g. creator.
- `user_roles`  connects users in the system to a specific role

ACL Implementation
------------------

The idea behind the new ACL system is to greatly simplify the implementation by reducing the number of places where roles are defined and stored. All necessary state is stored in a single table (`access_control_list`). The table is optimized for READ access because it will be queried on almost every request.

We accomplish this by sacrificing some performance on object creation (e.g. creating a mapping will have to add one or multiple rows to the access_control_list table), but by so doing we will not have to compute those permissions on every GET request.

Object level permissions will give the user access to one particular object. In the `access_control_list` table these permissions will have a valid object set in the resource_id and resource_type columns. The permissions granted will depend on the role specified e.g. object owner role will grant read/write/delete access on the object, while object contact role might only grant read access.

Database Tables
~~~~~~~~~~~~~~~

- `access_control_roles` stores role definitions.
- `access_control_list` stores user <-> role <-> object mappings.
