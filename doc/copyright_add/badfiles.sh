# note: initially found 628 non-compliant files
for x in `grep -rLI --exclude-dir=tmp "Copyright (C)" . | grep -v --file=doc/copyright_add/excludes.grep | grep "\.html$"`
do
				#echo $x
				mv $x temporary_file
				cat doc/copyright_add/html_header.html temporary_file > $x
				rm temporary_file
done
