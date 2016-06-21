# good test file: src/ggrc/assets/javascripts/application.js
# replace comments that look like this:
#/*
# * Copyright (C) 2016 Google Inc.
# * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# */
# with this:
#/*!
#    Copyright (C) 2016 Google Inc.
#    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
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

