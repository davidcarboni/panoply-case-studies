#!/usr/bin/env bash


# Prepare

if [ ! -f ./project.txt ]; then
    echo "Please create a file called project.txt containing your GCP project ID."
    exit 1
else
    BASE=$PWD
    PROJECT=`cat project.txt`
fi


# Update frontend
gsutil -m cp -z html -a public-read -r frontend/* gs://${PROJECT}-frontend


# Deploy function
gcloud functions deploy hello --entry-point Hi --runtime go111 --trigger-http --source=./functions --region=europe-west1

# gcloud functions deploy [FUNCTION_NAME] \
--source https://source.developers.google.com/projects/[PROJECT_ID]/repos/[REPOSITORY_ID]/moveable-aliases/master/paths/[SOURCE] \
--trigger-http;

exit 0

# The functions we want
declare -a functions=(
  "authenticate"
  "authenticated"
)

for function in "${functions[@]}"
do
   gcloud functions deploy $function --region=europe-west1 --runtime=python37 --source=gs://${PROJECT}-functions/functions.zip --memory=128MB --trigger-event=google.storage.object.finalize --trigger-resource=${PROJECT}-content --entry-point=$function
done

