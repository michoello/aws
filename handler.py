# Test 2
import json

import boto3
from botocore.exceptions import ClientError


def hello(event, context):
  SENDER = "michael.dolinin@gmail.com"
  RECIPIENT = "michael.dolinin@gmail.com"

  CONFIGURATION_SET = "ConfigSet"
  AWS_REGION = "us-west-2"
  SUBJECT = "Amazon SES Test (SDK for Python)"
  BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )
            
  # The HTML body of the email.
  body_html = """<html>
<head></head>
<body>
  <h1>Amazon SES Test (SDK for Python)</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.</p>"""

  output = event
  for k in output:
      body_html = body_html + "<b>" + k + "</b>:<i>" + output[k] + "</i><br>"
    
      
  body_html = body_html + """  
</body>
</html>"""            
  output = {}
  CHARSET = "UTF-8"

  client = boto3.client('ses',region_name=AWS_REGION)

  # Try to send the email.
  try:
    #Provide the contents of the email.
    response = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': body_html,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
        # If you are not using a configuration set, comment or delete the
        # following line
     #   ConfigurationSetName=CONFIGURATION_SET,
    )
  # Display an error if something goes wrong.	
  except ClientError as e:
    output['error_message'] = e.response['Error']['Message']
  else:
    output['ok_message'] = response['MessageId']
    
  return {
        'statusCode': 200,
        'body': json.dumps(output)
  }


