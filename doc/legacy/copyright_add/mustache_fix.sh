# good test file: src/ggrc/static/mustache/sections/control_selector.mustache
for x in `grep -rlI --include=*.mustache --exclude-dir=tmp "<\!--" . | grep -v --file=doc/copyright_add/excludes.grep`
# save the seventh line on (tail -n +7), do swap on lines before that (head -6)
do
    tail -n +7 $x > temporary_file
    head -6 $x \
    | sed -e 's/<!--/{{!/' \
    | sed -e 's/-->/}}/' \
    > temporary_file2
    cat temporary_file2 temporary_file > $x
    rm temporary_file
    rm temporary_file2
done

