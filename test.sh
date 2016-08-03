dSz=$(du -b -s 2gb_file.tar | cut -f -1)

re='^[0-9]+$'
if ! [[ $dSz =~ $re ]] ; then
	   echo "error: Not a number" >&2; exit 1
   fi
