import unittest
from lambda_function import *
import time
from Event import *


cloudwatch_event = {
  "awslogs": {
    "data": "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"
  }
}


class TestMethods(unittest.TestCase):
	def test_process_cloud_watch_messages__no_structlog_events__zero_results_processed(self):
		# Arrange
		cloudwatch_events = [{"message" : "test one"}]

		# Act
		result = process_cloud_watch_messages(cloudwatch_events)

		# Assert
		self.assertEqual(result, 0)


	def test_process_cloud_watch_messages__one_structlog_events__zero_results_processed(self):
		# Arrange
		cloudwatch_events = [{"message" : "[CRITICAL] 2018-12-26T22:00:17.246Z a0a6b576-0959-11e9-a	{\"lambda_name\" : \"super_lambda\"}"}]

		# Act
		result = process_cloud_watch_messages(cloudwatch_events)

		# Assert
		self.assertEqual(result, 1)

	def test_create_es_event__simple_event_data__s3_file_created(self):
		# Arrange
		input = {
			"hello" : "world"
			}

		# Act
		s3_url = create_es_event(input)
		print("*** s3_url: " + s3_url)

		# Assert
		s3_array = [1]
		s3_array[0] = s3_url
		s3 = boto3.resource("s3")
		written_text = get_file_text_from_s3_urls(s3_array, s3)
		event_json = json.loads(written_text[s3_url])
		self.assertEqual(event_json["_index"], "aws_lambda_log_")
		self.assertEqual(event_json["data"]["hello"], "world")
		self.assertTrue("@timestamp" in event_json["data"])
		self.assertTrue("@timestamp_local" in event_json["data"])


	def test_create_es_event__simple_event_data__s3_file_created(self):
		# Arrange
		input = {
			"hello" : "world",
			"lambda_name" : "test-log-stream-to-es",
			"@timestamp" : "1776-07-04T09:17:07.00000"
			}

		# Act
		s3_url = create_es_event(input)
		print("*** s3_url: " + s3_url)

		# Assert
		s3_array = [1]
		s3_array[0] = s3_url
		s3 = boto3.resource("s3")
		written_text = get_file_text_from_s3_urls(s3_array, s3)
		event_json = json.loads(written_text[s3_url])
		self.assertEqual(event_json["_index"], "aws_lambda_log_test-log-stream-to-es")
		self.assertEqual(event_json["data"]["hello"], "world")
		self.assertEqual(event_json["data"]["@timestamp"], "1776-07-04T09:17:07.00000")
		self.assertTrue("@timestamp_local" in event_json["data"])


if __name__ == '__main__':
	unittest.main()		

