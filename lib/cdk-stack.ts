// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import { Duration, Stack, StackProps, RemovalPolicy } from 'aws-cdk-lib';
import { AwsCustomResource, AwsCustomResourcePolicy, PhysicalResourceId } from 'aws-cdk-lib/custom-resources';
import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';
import { EventbridgeToLambdaProps, EventbridgeToLambda } from '@aws-solutions-constructs/aws-eventbridge-lambda';
import { Construct } from 'constructs';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as events from 'aws-cdk-lib/aws-events';
import { CloudWatchLogGroup } from 'aws-cdk-lib/aws-events-targets';

export class CdkStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) 
  {
    super(scope, id, props);

    // Create an Amazon S3 bucket to store Historical Application Logs
    const s3Bucket = new s3.Bucket(this, 'ada_logs', {
      objectOwnership: s3.ObjectOwnership.BUCKET_OWNER_ENFORCED,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      versioned: false,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      enforceSSL:true,
      //encryptionKey: new kms.Key(this, 's3BucketKMSKey'),
    });

    // Copy the logs in to the Amazon S3 bucket
    const histLog = new s3deploy.BucketDeployment(this, 'deploy_files', {
      sources: [s3deploy.Source.asset('./asset/historical_logs/')],
      destinationBucket: s3Bucket,
      destinationKeyPrefix: 'logs/',
    });
    histLog.node.addDependency(s3Bucket);

    // const logGenRole = new iam.Role(this, 'Log Gen Lambda Role', {
    //   assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com')
    // });

    //logGenRole.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName("service-role/AWSLambdaBasicExecutionRole"));
  
    // Create a Amazon Lambda function that writes logs in Apache Log Format to a CloudWatch Log Group
    // Trigger the Amazon Lambda function every 2 minutes using AWS EventsBridge rule
    const constructProps: EventbridgeToLambdaProps = {
      lambdaFunctionProps: {
        runtime: lambda.Runtime.PYTHON_3_10,
        handler: 'log_generator.lambda_handler',
        //role: logGenRole,
        code: lambda.Code.fromAsset('./asset/current_logs/')
      },
      eventRuleProps: {
        schedule: events.Schedule.rate(Duration.minutes(2))
      }
    };
    
    const LambdaEvent = new EventbridgeToLambda(this, 'AdaLogGen', constructProps);
   
    const tableName = 'ADALookUp';

    // Create an Amazon DynamoDB table to store the HTTP Status Codes
    const table = new dynamodb.Table(this, 'ADALookUpTable', {
      tableName,
      partitionKey: { name: 'key', type: dynamodb.AttributeType.STRING },
      removalPolicy: RemovalPolicy.DESTROY,
    });
    

    const myRole = new iam.Role(this, 'Lambda Role', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
    });

    myRole.node.addDependency(table);
    table.grantWriteData(myRole);

    // Get the Amazon DynamoDB table output
    new cdk.CfnOutput(this, 'DynamoDBTable', {
      value: table.tableArn,
      description: 'DyanmoDB Table',
      exportName: 'DyanmoDBTableName',
    });

    // Get the Amazon S3 bucket ARN
    new cdk.CfnOutput(this, 'S3', {
      value: s3Bucket.bucketArn,
      description: 'S3 Bucket',
      exportName: 'S3Bucket',
    });

    // Get the Amazon Lambda function ARN
    new cdk.CfnOutput(this, 'Lambda Function', {
      //value: CloudWatchLogGroup.nam,
      value: LambdaEvent.lambdaFunction.functionArn,
      description: 'Logging Application',
      exportName: 'LoggerLambda',
    });

     // Create a Amazon Lambda function to write the HTTP Status codes in to the Amazon DynamoDB lookup table
     const lookupLambda = new lambda.Function(this, 'LambdaNodeStack', {
      code: lambda.Code.fromAsset('./asset/lookup/'),
      functionName: "lookupLambda",
      handler: 'ddb_writer.handler',
      role: myRole,
      memorySize: 512,
      runtime: lambda.Runtime.NODEJS_14_X,
      timeout: cdk.Duration.seconds(60),
    });
    myRole.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName("service-role/AWSLambdaBasicExecutionRole"));
    //myRole.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName("AmazonDynamoDBFullAccess"));
    lookupLambda.node.addDependency(table);



    // Set up a trigger to invoke the Amazon Lambda function to insert the records in to the look up table
    const lambdaTrigger = new AwsCustomResource(this, 'StatefunctionTrigger', {
      policy: AwsCustomResourcePolicy.fromStatements([new iam.PolicyStatement({
        actions: ['lambda:InvokeFunction'],
        effect: iam.Effect.ALLOW,
        resources: [lookupLambda.functionArn]
      })]),
      timeout: cdk.Duration.minutes(1),
      onCreate: {
        service: 'Lambda',
        action: 'invoke',
        parameters: {
          FunctionName: lookupLambda.functionName,
          InvocationType: 'Event'
        },
        physicalResourceId: PhysicalResourceId.of(Date.now().toString())
      }
    });
    lambdaTrigger.node.addDependency(table, lookupLambda)
  }
}
