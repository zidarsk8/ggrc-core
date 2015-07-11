# note: initially found 628 non-compliant files
# Did the above search for file endings .scss, .feature, .html. js, .py, .haml, .mako and applied the appropriate header.
for x in `grep -rLI --exclude-dir=tmp "Copyright (C)" . | grep -v --file=doc/legacy/copyright_add/excludes.grep | grep "\.html$"`
do
				#echo $x
				cp $x temporary_file
				cat doc/legacy/copyright_add/html_header.html temporary_file > $x
				rm temporary_file
done
