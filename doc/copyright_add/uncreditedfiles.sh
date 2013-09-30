counter=1
for x in `grep -rlI --exclude-dir=tmp "Created By: *$" . | grep -v --file=doc/copyright_add/excludes.grep | grep --file=$1`
do
				cp $x temporary_file
				cat $x | sed "s/Created By: *$/Created By: $2/" > $x
				rm temporary_file
				break
done
