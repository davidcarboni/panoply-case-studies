#!/usr/bin/env bash

gcloud config set project panoply-case-studies
base=$PWD

# Update functions
cd functions && zip -r functions.zip . && mv functions.zip $base/static/
cd $base

# Update bucket
gsutil -m cp -r static/* gs://panoply-case-studies
rm static/functions.zip

# Deploy functions
# TODO: deploy from a source repo?
declare -a functions=("authenticate" "authenticated")

## Deploy the list of functions
options="--region=europe-west1 --runtime=python37 --source=gs://panoply-case-studies/functions.zip --memory=128MB --trigger-http"
for function in "${functions[@]}"
do
   echo Deploying function: "$i"
   gcloud functions deploy $i --entry-point=$i ${options}
done

# gcloud functions deploy authenticate   ${region} ${options} --entry-point=authenticate
# gcloud functions deploy authenticated  ${region} ${options} --entry-point=authenticated
