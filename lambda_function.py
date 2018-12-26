import gzip
import json
import base64
import re
from ESLambdaLog import *
import logging
import structlog
import sys
import datetime


def lambda_handler(event, context):
    log = setup_logging()
    log = log.bind(lambda_name="aws-lnkchk-stream-to-es")
    log.critical("starting_log-stream-to-es")


    cw_data = event["awslogs"]["data"]
    compressed_payload = base64.b64decode(cw_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)

    log_events = payload["logEvents"]
    log.critical("event_count", record_count=len(log_events), log_events=log_events)
    print("*** log_events:")
    count = 0
    for log_event in log_events:
        message = log_event["message"]
        if "{" in message and "lambda_name" in message:
            count = count + 1
            print(str(count) + " - " + message)
            json_string = re.sub("^[^{]+", "", message)
            try:
                json_object = json.loads(json_string)
                # Send the log event into Elasticsearch
                index_name = ""
                if "lambda_name" in json_object:
                    index_name = json_object["lambda_name"]
                es = ESLambdaLog(index_name) 
                es.log_event(json_object)
            except Exception as e:
                print(e)
                print("Continuing to next message")
    log.critical("finished_log-stream-to-es")


def extract_json_from_message_line(message):
    print("||| Input: " + message)
    json_string = re.sub("^[^{]+", "", message)
    print("||| Output: " + json_string)
    return json_string


def setup_logging():
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    return structlog.get_logger()
