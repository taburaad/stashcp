eck=$(md5sum 2gb_filetar | awk '{print $1;}')
string="7d05ef0790d891f918eeafec40185fd8"
      if [ "$check" != "$string" ]
      then
              echo "FILE_NOT_EQUAL"
      else
      echo "GOOD"
      fi

      ls -l 2gb_file.tar
      rm -f 2gb_file.tar.
