import json
import os

import boto3

import functions.log as log
import functions.exceptions as ex
import functions.validator as val
from functions.beacon import respond
from functions.models.note import NoteModel


# Get our module logger.
logger = log.setup_custom_logger("notes")


def search_by_user(event, context):
    """Return the collection of items based on query."""

    try:

        # Determine if required env var for region is present.
        val.check_region()

        # Determine if required env var for DynamoDB table is present.
        val.check_dynamodb()

        # Check for the url {id}.
        user_id = val.check_id(event)

        # Set up resource and environment. This is where we keep
        # *aaS provider resources away from biz logic.
        region = os.environ["AWS_DEFAULT_REGION"]
        table = os.environ["DYNAMODB_TABLE"]

        # Determine which DynamoDB host we need (local/remote)?
        host = val.check_dynamodb_host()
        conn = boto3.resource("dynamodb", region, endpoint_url=host)
        conn_table = conn.Table(table)

        # Build our model and read.
        note = NoteModel(conn_table)
        items = note.search_by_user(user_id)

        logger.info("Notes for user found: {} [{}]".format(
            user_id, len(items)))
        return respond(200, items)

    except ex.AwsRegionNotSetException as exc:
        return respond(500, {"error": str(exc)})

    except ex.DynamoDbTableNotSetException as exc:
        return respond(500, {"error": str(exc)})

    except ex.RequestUrlIdNotSetException as exc:
        return respond(400, {"error": str(exc)})

    except Exception as exc:
        return respond(500, {"error": str(exc)})


def search_by_notebook(event, context):
    """Return the collection of items based on query."""

    try:

        # Determine if required env var for region is present.
        val.check_region()

        # Determine if required env var for DynamoDB table is present.
        val.check_dynamodb()

        # Check for the url {id}.
        notebook = val.check_id(event)

        # Set up resource and environment. This is where we keep
        # *aaS provider resources away from biz logic.
        region = os.environ["AWS_DEFAULT_REGION"]
        table = os.environ["DYNAMODB_TABLE"]

        # Determine which DynamoDB host we need (local/remote)?
        host = val.check_dynamodb_host()
        conn = boto3.resource("dynamodb", region, endpoint_url=host)
        conn_table = conn.Table(table)

        # Build our model and read.
        note = NoteModel(conn_table)
        items = note.search_by_notebook(notebook)

        logger.info("Notes for notebook found: {} [{}]".format(
            notebook, len(items)))
        return respond(200, items)

    except ex.AwsRegionNotSetException as exc:
        return respond(500, {"error": str(exc)})

    except ex.DynamoDbTableNotSetException as exc:
        return respond(500, {"error": str(exc)})

    except ex.RequestUrlIdNotSetException as exc:
        return respond(400, {"error": str(exc)})

    except Exception as exc:
        return respond(500, {"error": str(exc)})
