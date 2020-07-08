import json

from src import add_transcription
from src.add_transcription import error_response, success_response

success = {"headers": {"Access-Control-Allow-Origin": "*"}, "statusCode": 200}

error = {
    "statusCode": 410,
    "body": "error_message",
    "headers": {"Access-Control-Allow-Origin": "*"},
}


def test_api_handler(mocker):
    # arrange
    event = {"event": "values"}
    context = {"context": "value"}
    mapped_event = {"mapped": "values"}
    mocker.patch.object(add_transcription, "format_api_request")
    mocker.patch.object(add_transcription, "run_transcribe")
    add_transcription.format_api_request.return_value = mapped_event
    add_transcription.run_transcribe.return_value = {"transcribe": "return"}

    # act
    add_transcription.api_handler(event, context)

    # assert
    add_transcription.format_api_request.assert_called_with(event)
    add_transcription.run_transcribe.assert_called_with(mapped_event)


def test_api_handler_fail(mocker):
    # arrange
    error_message = "fail"
    event = {"event": "values"}
    context = {"context": "value"}
    mapped_event = {"mapped": "values"}
    mocker.patch.object(add_transcription, "format_api_request")
    mocker.patch.object(add_transcription, "run_transcribe", side_effect=Exception(error_message))
    add_transcription.format_api_request.return_value = mapped_event
    add_transcription.run_transcribe.return_value = {"transcribe": "return"}

    # act
    result = add_transcription.api_handler(event, context)

    # assert
    # add_transcription.format_api_request.assert_called_with(event)
    # Sadd_transcription.run_transcribe.assert_called_with(mapped_event)
    assert result == error_response(error_message)


def test_run_transcribe(mocker):
    # arrange
    transcribe_params = {
        "job_name": "job_name",
        "media": "media",
        "media_format": "media_format",
        "language_code": "language_code",
        "output_bucket": "output_bucket",
    }
    transcribe_return = {"transcribe": "return"}
    mocker.patch.object(add_transcription.transcribe_client, "start_transcription_job")
    add_transcription.transcribe_client.start_transcription_job.return_value = transcribe_return

    # act
    add_transcription.run_transcribe(transcribe_params)

    # assert
    add_transcription.transcribe_client.start_transcription_job.assert_called_with(
        TranscriptionJobName=transcribe_params.get("job_name"),
        Media=transcribe_params.get("media"),
        MediaFormat=transcribe_params.get("media_format"),
        LanguageCode=transcribe_params.get("language_code"),
        OutputBucketName=transcribe_params.get("output_bucket"),
    )


def test_success_response():
    # arrange
    response_input = "test"
    expected = success
    expected["body"] = json.dumps(response_input)

    # act
    response = success_response(response_input)

    # assert
    assert response == expected


def test_error_response():
    # arrange
    response_input = "test"
    expected = error
    expected["body"] = json.dumps(response_input)

    # act
    response = error_response(response_input)

    # assert
    assert response == expected
