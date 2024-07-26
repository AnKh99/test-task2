#!/bin/bash

# Check args
if [ $# -ne 3 ]; then
    echo "Usage: $0 <absolute_path_to_file> <first_key> <second_key>"
    exit 1
fi

absolute_path_to_file=$1
first_key=$2
second_key=$3

found_first_key=false

# checking file
return_flag=1
while IFS= read -r line; do
    if [[ "$line" == *"$first_key"* ]]; then
        found_first_key=true
    elif [[ "$line" == *"$second_key"* && "$found_first_key" == true ]]; then
        return_flag=0
        break
    fi
done < "$absolute_path_to_file"

# return code
exit $return_flag
