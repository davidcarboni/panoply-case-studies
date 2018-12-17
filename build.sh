#!/usr/bin/env bash

gcloud config set project panoply-case-studies
base=$PWD

# Update functions
cd functions && zip -r functions.zip . && mv functions.zip $base/static/
cd $base

# Update bucket
gsutil -m cp -r static/* gs://casestudies.noducksgiven.com
rm static/functions.zip

# Deploy functions
# TODO: deploy from a source repo?
declare -a functions=("authenticate" "authenticated")

## Deploy the list of functions
options="--region=europe-west1 --runtime=python37 --source=gs://casestudies.noducksgiven.com/functions.zip --memory=128MB --trigger-http"
for function in "${functions[@]}"
do
   echo Deploying function: "$function"
   gcloud functions deploy $function --entry-point=$function ${options}
done

# gcloud functions deploy authenticate   ${region} ${options} --entry-point=authenticate
# gcloud functions deploy authenticated  ${region} ${options} --entry-point=authenticated
