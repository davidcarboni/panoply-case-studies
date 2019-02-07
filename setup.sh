#!/usr/bin/env bash


# Prepare

if [ ! -f ./project.txt ]; then
    echo "Please create a file called project.txt containing your GCP project ID."
    exit 1
else
    BASE=$PWD
    PROJECT=`cat project.txt`
fi


# Buckets

storage_class=multi_regional
location=eu

declare -a buckets=(
  "${PROJECT}-content"
  "${PROJECT}-frontend"
)

for bucket in "${buckets[@]}"
do
   echo Bucket: $bucket
   gsutil ls -b gs://${bucket} || gsutil mb -p $PROJECT -c $storage_class -l $location gs://${bucket}/
done

