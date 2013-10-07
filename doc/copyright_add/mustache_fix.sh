# arg1 is grep file that lists regexes for files you want to match
# good test file: src/ggrc/static/mustache/sections/control_selector.mustache
#for x in `grep -rlI --exclude-dir=tmp "Created By: *$" . | grep -v --file=doc/copyright_add/excludes.grep | egrep --file=$1`
# save the seventh line on (tail -n +7), do swap on lines before that (head -6)
for x in "src/ggrc/static/mustache/sections/control_selector.mustache"
do
    tail -n +7 $x > temporary_file
    head -6 $x \
    | sed -e 's/<!--/{{!/' \
    | sed -e 's/-->/}}/' \
    > temporary_file2
    cat temporary_file2 temporary_file
    rm temporary_file
    rm temporary_file2
done

