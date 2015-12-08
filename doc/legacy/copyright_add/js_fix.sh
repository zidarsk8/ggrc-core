# good test file: src/ggrc/assets/javascripts/application.js
# replace comments that look like this:
#/*
# * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# * Created By: brad@reciprocitylabs.com
# * Maintained By: brad@reciprocitylabs.com
# */
# with this:
#/*!
#    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
#    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
#    Created By: 
#    Maintained By:
#*/
for x in `grep -rlI --include=*.js --exclude-dir=tmp "*" . | grep -v --file=doc/copyright_add/excludes.grep`
# save the seventh line on (tail -n +7), do swap on lines before that (head -6)
do
    tail -n +7 $x > temporary_file
    head -6 $x \
    | sed -e 's/^\/\*!*/\/\*!/' \
    | sed -e 's/^ \* /    /' \
    | sed -e 's/^ \*\//*\//' \
    > temporary_file2
    cat temporary_file2 temporary_file > $x
    rm temporary_file
    rm temporary_file2
done

