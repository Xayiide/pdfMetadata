for file in *,*
do
	if [ -e "${file//,/}" ]
	then
		printf >$2 '$s\n' "Warning, skipping $file as the renamed version\
			already exists"
		continue
	fi

	mv -- "$file" "${file//,/}"
done
