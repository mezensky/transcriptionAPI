import json
import os
import uuid

import boto3

transcribe_client = boto3.client("transcribe")


def success_response(response):
    body = response
    return_response = {
        "headers": {"Access-Control-Allow-Origin": "*"},
        "statusCode": 200,
        "body": json.dumps(body),
    }
    return return_response


def error_response(error_message):
    response = {
        "statusCode": 410,
        "body": json.dumps(error_message),
        "headers": {"Access-Control-Allow-Origin": "*"},
    }
    print(f"Error: {error_message}")
    return response


def format_api_request(event):
    body = json.loads(event["body"])
    request = {
        "job_name": "{}_{}".format(uuid.uuid4(), body.get("external-id")),
        "media": {"MediaFileUri": body.get("file-location")},
        "media_format": "mp3",
        "language_code": "en-US",
        "output_bucket": os.environ.get("TRANSCRIBE_BUCKET"),
    }
    print(request)
    return request


def run_transcribe(transcribe_params):
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=transcribe_params.get("job_name"),
        Media=transcribe_params.get("media"),
        MediaFormat=transcribe_params.get("media_format"),
        LanguageCode=transcribe_params.get("language_code"),
        OutputBucketName=transcribe_params.get("output_bucket"),
    )
    print(f"run_transcribe: {response}")
    return response


def api_handler(event, context):
    # format incoming data and env data
    request = format_api_request(event)

    try:
        # perform function
        response = run_transcribe(request)
    except Exception as ex:
        return error_response(str(ex))

    # format response
    return success_response(response)
