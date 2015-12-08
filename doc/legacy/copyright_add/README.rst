..
  Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: silas@reciprocitylabs.com
  Maintained By: silas@reciprocitylabs.com


This is the write-up for how I added the copyright notice to the missing files.

First step, adding notice
-------------------

This step added the notice where it was not present, but left the Created/Maintained fileds blank.  I used ``badfiles.sh``, which had to be tweaked for each kind of syntax.  Different file types required different headers (due to how comments are added for the various file times), and those are saved in this directory in the form <file_type>_header.<file_type>.  Not every file type is mentioned, since some had the same comment syntax (e.g. the html header could be used for mustache).

Second step: filling in created/maintained fields
-------------------

In this, the Created/Maintained fields, where empty, were populated with names, using the rule of thumb that frontend files are credited to ``brad@reciprocitylabs.com`` and backend files to ``dan@reciprocitylabs.com``.  The list of regexes for matching the different types of files are in ``frontend.grep`` and ``backend.grep``.

(This part did not need to distinguish between the different types of commenting syntax for the different file types because it just had to swap out the already-in-comments entry for Created By and Maintained By.)

I then used the script ``uncreditedfiles.sh``, which I wrote to be more generalized than ``badfiles.sh`` above. It takes the regex matcher file as the first argument and the person to credit as the second argument. I then just had to run it with the argument sets (``frontend.grep``, ``brad@reciprocitylabs.com``) and (``backend.grep``, ``dan@reciprocitylabs.com``).

Note: some file types did not exist in large enough number to automate, and for these I manually added the notice using best judgment as to who to credit.
