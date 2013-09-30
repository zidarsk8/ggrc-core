# note: initially found 628 non-compliant files
for x in `grep -rLI --exclude-dir=tmp "Copyright (C)" . | grep -v --file=doc/copyright_add/excludes.grep | grep "\.scss$"`
do
				#echo $x
				cp $x temporary_file
				cat doc/copyright_add/js_header.js temporary_file > $x
				rm temporary_file
done
