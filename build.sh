#!/usr/bin/env bash


# Prepare

if [ ! -f ./project.txt ]; then
    echo "Please create a file called project.txt containing your GCP project ID."
    exit 1
else
    BASE=$PWD
    PROJECT=`cat project.txt`
fi

if [ ! -f ./jwt_key.txt ]; then
    JWT_KEY=justtesting
else 
    JWT_KEY=`cat jwt_key.txt`
fi


# Update frontend
gsutil -m rsync -a public-read -J -d -r frontend gs://${PROJECT}-frontend/


# Deploy function
#gcloud functions deploy hello --entry-point Hi --runtime go112 --trigger-http --source=./functions/go --region=europe-west1 --update-env-vars PROJECT_ID=${PROJECT}

# Deploy Python version 

gcloud functions deploy register --entry-point register --runtime python37 --trigger-http --source=./functions/python --region=europe-west1 --update-env-vars PROJECT_ID=${PROJECT},JWT_KEY=${JWT_KEY}

gcloud functions deploy authenticate --entry-point authenticate --runtime python37 --trigger-http --source=./functions/python --region=europe-west1 --update-env-vars PROJECT_ID=${PROJECT},JWT_KEY=${JWT_KEY}

# ---

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

# gcloud functions deploy [FUNCTION_NAME] \
#--source https://source.developers.google.com/projects/[PROJECT_ID]/repos/[REPOSITORY_ID]/moveable-aliases/master/paths/[SOURCE] \
#--trigger-http;
