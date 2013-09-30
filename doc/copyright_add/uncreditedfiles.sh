# arg1 is grep file that lists regexes for files you want to match
# arg2 is email address of person you want to credit
for x in `grep -rlI --exclude-dir=tmp "Created By: *$" . | grep -v --file=doc/copyright_add/excludes.grep | egrep --file=$1`
do
    cp $x temporary_file
    sed "s/Created By: *$/Created By: $2/" temporary_file > $x
    rm temporary_file
done

for x in `grep -rlI --exclude-dir=tmp "Maintained By: *$" . | grep -v --file=doc/copyright_add/excludes.grep | egrep --file=$1`
do
    cp $x temporary_file
    sed "s/Maintained By: *$/Maintained By: $2/" temporary_file > $x
    rm temporary_file
done
