#
# This fixes the kicad lib paths in OSX used by python... sorry I don't have more documentation right now
#

for i in `ls -1`
do
  otool -L $i | grep exec | awk '{print $1}' | awk -F/ -v file="$i" '{print "install_name_tool -change @executable_path/../Frameworks/" $4 " /usr/local/kicad/Frameworks/"$4" " file}'
done

