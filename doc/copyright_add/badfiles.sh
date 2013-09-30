# note: initially found 628 non-compliant files
for x in `grep -rLI --exclude-dir=tmp "Copyright (C)" . | grep -v --file=doc/copyright_add/excludes.grep | grep "\.feature$"`
do
				#echo $x
				cp $x temporary_file
				cat doc/copyright_add/py_header.py temporary_file > $x
				rm temporary_file
done
