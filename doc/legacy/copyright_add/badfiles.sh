# note: initially found 628 non-compliant files
# Did the above search for file endings .scss, .feature, .html. js, .py, .haml, .mako and applied the appropriate header.
for x in `grep -rLI --exclude-dir=tmp "Copyright (C)" . | grep -v --file=doc/copyright_add/excludes.grep | grep "\.haml$"`
do
				#echo $x
				cp $x temporary_file
				cat doc/copyright_add/haml_header.haml temporary_file > $x
				rm temporary_file
done
