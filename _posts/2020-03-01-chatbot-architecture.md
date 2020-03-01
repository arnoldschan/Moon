---
layout: post
title: "Penniless Chatbot Architecture"
date: 2020-03-01
excerpt: "Create your 24/7 chatbot for free with this architecture!"
tags: [tutorial, aws, chatbot]
comments: true
---
[Check on dev.to](https://dev.to/arnoldschan/penniless-chatbot-architecture-2g81)

Everybody loves free stuff, programmers as well!
Running an advanced cloud service without paying a penny sounds not possible. By utilizing AWS free-tier offers, I've managed to create a  simple cloud-powered chatbot for [LINE Messenger](http://line.me)
##### ** Please note that this architecture mostly suitable for a chatbot in general use to keep the bill low **
#### ** [check the source code on github](https://github.com/arnoldschan/chatbot-demo)**
## AWS free tier
If we carefully check on always free [AWS Free-Tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=tier%23always-free) offers, there are a complete service set to create a simple chatbot: 
- Script executor ([AWS Lambda](https://aws.amazon.com/lambda/)) *free 1 million requests per month*
- Storage ([AWS DynamoDB](https://aws.amazon.com/dynamodb/) : NoSQL-styled storage) *free 25 GB storage*
- Message webhook handler ([AWS API Gateway](https://aws.amazon.com/api-gateway/)) *free 1 million calls per month, for 12 months*

## Structure 
![Simple Chatbot Structure](https://dev-to-uploads.s3.amazonaws.com/i/4nae6nwmvi72rw5i8ugl.png)

Basically, there are 4 steps to process the user's incoming message in LINE messenger:
1. LINE messenger server receive and transfer the message to registered webhook (door)
2. The door finds the correct function (gears) that responsible to handle the message
3. The function sends a reply message to [LINE Messenger](http://line.me), and stores necessary log to the database (memory card)
4. LINE messenger transmits the reply message to the user

Pretty simple, isn't it? 😄
There are 3 AWS resources:
* **[AWS API Gateway](https://aws.amazon.com/api-gateway/)** serves as the **door** to receive and executes the function
* **[AWS Lambda](https://aws.amazon.com/lambda/)** serves as the **function** to execute the code to process the message
* **[AWS DynamoDB](https://aws.amazon.com/dynamodb/)** handles message logs and records the logs as [JSON](https://en.wikipedia.org/wiki/JSON)-styled information. This resource is portrayed as **memory card** in the picture

#### Why Lambda?
TL;DR 
Cheaper for low traffic usage.

Unlike the common way of computing information, it's not necessary to rent one computing resource the whole 24/7.  AWS Lambda lets us rent the computing resource only at the necessary event, in this case: processing the incoming message.

AWS suggests the use of [AWS Lambda](https://aws.amazon.com/lambda/) only if the computing resource time short ([below 15 minutes](https://aws.amazon.com/about-aws/whats-new/2018/10/aws-lambda-supports-functions-that-can-run-up-to-15-minutes/)) and the service has a low-traffic, periodic activity, otherwise, there'll be a hole in your wallet 😅.
Therefore, [AWS Lambda](https://aws.amazon.com/lambda/) is suitable in general-use chatbots and side-projects computing needs.


Enough the theory. Let's dive in the technical stuff!

## Directory Structures
```
.
├── app.py
├── dynamodb.py
├── template.yml
└── requirements.txt
```

## Contents
-------------------
`app.py`

```python
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage
import json
import requests
from dynamodb import DynamoDB


access_token = <<PUT YOUR ACCESS TOKEN HERE>>  #replace with your access token
channel_secret= <<PUT YOUR CHANNEL SECRET HERE>> #replace with your channel secret
table_name = 'echobot' #DynamoDB table name
key_name = 'userID' #database's primary key
sec_key_name = 'timestamp' #databse's secondary key

def lambda_handler(event,context):

    # create BotEcho object with parameters
    line_bot = BotEcho(
        event,
        access_token = access_token ,
        channel_secret = channel_secret)

    # check the signature (originality of source)
    if line_bot.signature_check != 200:
        print("fail to signature check")
        return {'statusCode': line_bot.signature_check}

    # send the message back to the user
    response = line_bot.send_reply(line_bot.text_message)
    if response != 200:
        print('fail to send reply')
        return {'statusCode': response}

    return {'statusCode':200}

```
The main file is `app.py`. it's the first script that is executed each time there's a received message by [AWS Lambda](https://aws.amazon.com/lambda/). [AWS Lambda](https://aws.amazon.com/lambda/) will call `lambda_handler` function with 2 parameters as input: event and context. Both contain message information sent by [LINE Messenger](http://line.me).
There are 3 steps in echo back the message:
1. Create the BotEcho class with the LINE messenger credentials and event
2. Validate the [message signature](https://developers.line.biz/en/reference/messaging-api/#signature-validation)
3. Echo the message back to the sender

------
In the same file (`app.py`), BotEcho class is also defined:
  

```python

class BotEcho:
    def __init__(self,event,access_token,channel_secret):
        self.event = event
        self.bot = LineBotApi(access_token)
        self.handler = WebhookHandler(channel_secret)
        self.body = json.loads(event['body'])['events'][0]
        self.sender_id = self.body['source']['userId']
        self.text_message = self.body['message']['text']
        self.log(sender=self.sender_id,to='self',message=self.text_message)

    @property
    def signature_check(self):
        signature = self.event['headers']['X-Line-Signature']
        try:
            self.handler.handle(self.event['body'], signature)
            return 200
        except InvalidSignatureError:
            return 400

    def send_reply(self,message):
        self.log(sender='self',to=self.sender_id,message=message)
        response = self.bot.reply_message(self.body['replyToken'], \
                                    TextSendMessage(text=message))
        return response

    def log(self,sender,to,message):
        log_head = ['to','message']
        log_value = [to, message]
        response = DynamoDB(table_name, key_name, sec_key_name)\
                                .put(sender,log_head,log_value)
        print(response)
        return response
```
BotEcho receives `event`,`access_token`, and `channel_secret`. This class utilizes a [LINE Bot API python package](https://github.com/line/line-bot-sdk-python). 
There are 2 functions:
* `send_reply`: calls [LINE Bot API](https://github.com/line/line-bot-sdk-python) to send message
* `log`: record the information to [AWS DynamoDB](https://aws.amazon.com/dynamodb/)

Of course, you can add the bot's ability rather than echoing back the message. Just use your creativity in it!

`requirements.txt`
1. Create a new virtual environment
2. Install [LINE Bot API package](https://github.com/line/line-bot-sdk-python)
3. `pip freeze > requirements.txt`
4. Voila!

## SAM
[Serverless Application Model](https://aws.amazon.com/serverless/sam/) offered by AWS.
I'll cover this part in detail in another post.
Basically it's a convenient way to deploy your app to AWS services in a script configuration. It's easy and traceable. 

You need to:
1. Have an [AWS account](https://aws.amazon.com/) (obviously)
2. [Install aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) and [login to your AWS account](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
3. [Install SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
4. Create a `template.yml` file in your folder.

Here's the `template.yml` contents:
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: >
  Chatbot Echo demo
# More info about Globals: https://github.com/awslabs/serverless-application-model/blob/master/docs/globals.rst
Globals: #shared configuration
  Function:
    Timeout: 3 
  Api:
    OpenApiVersion: 3.0.1 ### to remove the stage name deployment bug
Parameters: #shared parameters
  StageName: # version staging config
      Default: 'prod'
      Type: String
Resources: #AWS services list
  ChatbotAPI: # API Gateway https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html
    Type: AWS::Serverless::Api
    Properties:
      EndpointConfiguration: REGIONAL
      StageName: !Ref StageName
      DefinitionBody:
        swagger: "2.0"
        info:
          title: "ChatbotAPI"
        schemes:
        - "https"
        paths:
          /:
            post:
              produces:
              - "application/json"
              responses:
                "200":
                  description: "200 response"
                  schema:
                    $ref: "#/definitions/Empty"
              x-amazon-apigateway-integration:
                uri:
                  Fn::Sub: arn:${AWS::Partition}:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${ChatbotFunction.Arn}/invocations 
                responses:
                  default:
                    statusCode: "200"
                passthroughBehavior: "when_no_match"
                httpMethod: "POST"
                contentHandling: "CONVERT_TO_TEXT"
                type: "aws_proxy"
        definitions:
          Empty:
            type: "object"
            title: "Empty Schema"
  DynamoDBTable: #DynamoDB Table https://docs.aws.amazon.com/lambda/latest/dg/kinesis-tutorial-spec.html
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: echobot #change to your table name
      AttributeDefinitions:
        - AttributeName: userID #change to db primary key and type
          AttributeType: S
        - AttributeName: timestamp #change to db secondary key and type
          AttributeType: S
      KeySchema:
        - AttributeName: userID #change to db primary key
          KeyType: HASH
        - AttributeName: timestamp #change to db primary key
          KeyType: RANGE
      ProvisionedThroughput: 
        ReadCapacityUnits: 1 
        WriteCapacityUnits: 1


  ChatbotFunction: # Lambda Function https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
    Type: AWS::Serverless::Function 
    Properties:
      Handler: app.lambda_handler
      Runtime: python3.7
      Events: 
        endpoint:
          Type: Api
          Properties: #connect to our API Gateway
            RestApiId: !Ref ChatbotAPI
            Path: /
            Method: Post
      Policies:
        - Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action: #only allowed to put the record
                - dynamodb:Put
              Resource: !GetAtt DynamoDBTable.Arn

```

## Deploy!

Simple commands:
1. `sam build`
2. `sam deploy --guided`
3. Attach your [AWS API Gateway](https://aws.amazon.com/api-gateway/) invoke URL to LINEWebhook URL
4. And your EchoBot is good to go!

All [SAM's](https://aws.amazon.com/serverless/sam/) deployed app can be checked on [AWS Cloudformation](https://aws.amazon.com/cloudformation/)

## Pricings

Refer to our AWS Services usage:
* [AWS Lambda](https://aws.amazon.com/lambda/) *free 1 million requests per month*
* [AWS DynamoDB](https://aws.amazon.com/dynamodb/) *free 25 GB storage*
* [AWS API Gateway](https://aws.amazon.com/api-gateway/) *free 1 million calls per month, for 12 months*

The chatbot most likely free in the first 12 months and costs some penny for the [AWS API Gateway](https://aws.amazon.com/api-gateway/) usage. love it <3

## Conclusions
With the wonderful [AWS Free-Tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=tier%23always-free) offers, developers can manage to create a chatbot that'll cost very few or even free.

[Serverless Application Model](https://aws.amazon.com/serverless/sam/) or SAM makes developers' life easy with a simple deployment configuration.

Finally, you can modify the chatbot's ability to do more than echo back the message! *[check the source code on github](https://github.com/arnoldschan/chatbot-demo)*
Feel free to drop me a message to improve my work.

Thanks!

*"Whatever you do, work heartily, as for the Lord and not for men" - Colossians 3:23*
