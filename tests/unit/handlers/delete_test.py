import os
import time
import json

import yaml
import pytest
import boto3

from functions.handlers.create import create
from functions.handlers.delete import delete
from tests.unit import config
from tests.unit import http_event


# Module scoped variables for simple unit testing.
# @todo How can we point at the local DynamoDB local instance for testing handler?
test_globals = {
    "note_id": None,
    "user_id": "azrael",
    "notebook": "system",
    "text": "Rest API test task",
    "created_at": None,
    "updated_at": None
}


def test_delete_returns_valid_response_structure_when_valid_data(monkeypatch, http_event, config):
    monkeypatch.delenv("AWS_DEFAULT_REGION", raising=False)
    monkeypatch.delenv("DYNAMODB_TABLE", raising=False)
    
    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

    response = create(http_event, {})
    created = json.loads(response["body"])

    test_globals["note_id"] = created["noteId"]
    test_globals["user_id"] = created["userId"]
    test_globals["notebook"] = created["notebook"]
    test_globals["text"] = created["text"]
    test_globals["created_at"] = created["createdAt"]
    test_globals["updated_at"] = created["updatedAt"]
    
    http_event["pathParameters"]["id"] = test_globals["note_id"]
    response = delete(http_event, {})
    payload = json.loads(response["body"])

    assert "isBase64Encoded" in response and response["isBase64Encoded"] == False
    assert "statusCode" in response and response["statusCode"] == 200
    assert "headers" in response
    assert "body" in response

    assert "noteId" not in payload
    assert "userId" not in payload
    assert "notebook" not in payload
    assert "text" not in payload

    assert "updatedAt" not in payload
    assert "createdAt" not in payload


def test_delete_returns_valid_response_structure_when_invalid_data(monkeypatch, http_event, config):
    monkeypatch.delenv("AWS_DEFAULT_REGION", raising=False)
    monkeypatch.delenv("DYNAMODB_TABLE", raising=False)

    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

    http_event["pathParameters"]["id"] = test_globals["note_id"] + "_badid"
    response = delete(http_event, {})
    payload = json.loads(response["body"])

    assert "isBase64Encoded" in response and response["isBase64Encoded"] == False
    assert "statusCode" in response and response["statusCode"] == 200
    assert "headers" in response
    assert "body" in response

    assert "noteId" not in payload
    assert "userId" not in payload
    assert "notebook" not in payload
    assert "text" not in payload

    assert "updatedAt" not in payload
    assert "createdAt" not in payload


def test_delete_returns_status_code_500_when_aws_region_not_set(monkeypatch, http_event, config):
    monkeypatch.delenv("AWS_DEFAULT_REGION", raising=False)
    monkeypatch.delenv("DYNAMODB_TABLE", raising=False)

    response = delete(http_event, {})
    
    assert "statusCode" in response and response["statusCode"] == 500


def test_delete_returns_status_code_500_when_dynamodb_table_not_set(monkeypatch, http_event, config):
    monkeypatch.delenv("DYNAMODB_TABLE", raising=False)
    
    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    response = delete(http_event, {})
    
    assert "statusCode" in response and response["statusCode"] == 500


def test_delete_returns_status_code_400_when_request_id_not_set(monkeypatch, http_event, config):
    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

    http_event["pathParameters"]["id"] = None
    response = delete(http_event, {})
    
    assert "statusCode" in response and response["statusCode"] == 400

    http_event["pathParameters"]["id"] = ""
    response = delete(http_event, {})

    assert "statusCode" in response and response["statusCode"] == 400

    http_event["pathParameters"] = ""
    response = delete(http_event, {})

    assert "statusCode" in response and response["statusCode"] == 400
