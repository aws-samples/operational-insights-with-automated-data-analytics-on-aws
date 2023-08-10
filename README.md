# Derive Application Log Insights Using Amazon CloudWatch Connector for Automated Data Analytics on AWS

## Background
 This repository provides an AWS CDK solution that is used to demonstrate the capabilities of ADA on AWS Solution as describe in the blog [here](link). [Automated Data Analytics on AWS (ADA)](https://aws.amazon.com/solutions/implementations/automated-data-analytics-on-aws/) is an AWS Solution that enables users to derive meaningful insights from data in a matter of minutes through a simple and intuitive user interface. ADA offers an AWS-native data analytics platform that is ready to use out-of-the-box by data analysts for a variety of use cases. Using ADA, teams can ingest, transform, govern and query diverse datasets from a range of data sources without requiring specialist technical skills. ADA provides a set of [pre-built connectors](https://docs.aws.amazon.com/solutions/latest/automated-data-analytics-on-aws/data-connectors-guide.html) to ingest data from a wide range of sources including Amazon Simple Storage Service (S3), Amazon Kinesis Stream, Amazon CloudWatch, Amazon CloudTrail, and Amazon DynamoDB. 

Using this repository, we will demonstrate how an Application Developer or an Application Tester is able to leverage ADA to derive operational insights of applications running in AWS. We will also demonstrate how ADA solution can be used to connect to different data sources in AWS without having to copy the data from the source. We will first [deploy the ADA solution](https://docs.aws.amazon.com/solutions/latest/automated-data-analytics-on-aws/deploy-the-solution.html) into an AWS account and [set up the ADA solution](https://docs.aws.amazon.com/solutions/latest/automated-data-analytics-on-aws/setting-up-automated-data-analytics-on-aws.html) by creating [data products](https://docs.aws.amazon.com/solutions/latest/automated-data-analytics-on-aws/creating-data-products.html) using data connectors. ADA’s data products allows users to connect to a wide range of data sources so that users can query the datasets as if they are querying Relational Database Tables. We then use ADA’s query workbench to join the separate datasets and query the correlated data to get insights. We will also demonstrate how ADA can be integrated with BI tools such as Tableau to visualise the data and to build reports. 

## Solution overview

In this section, we will present the Solution Architecture for the demo and explain the workflow. For the purposes of demonstration, the bespoke application is simulated using an Amazon Lambda function that emits logs in [Apache Log Format](https://httpd.apache.org/docs/2.4/logs.html#accesslog) at a preset interval using Amazon EventBridge. This standard format can be produced by many different web servers and be read by many log analysis programs. The application (Amazon Lambda) logs are sent to a CloudWatch Log Group. The historical application logs are stored in an Amazon S3 bucket for reference and for querying purposes. A lookup table with a list of [HTTP status codes](https://httpd.apache.org/docs/2.4/logs.html#accesslog) along with the description is stored in an Amazon DynamoDB table. These three will serve as sources from which data will be ingested into ADA for correlation, query and analysis. We will [deploy ADA Solution](https://docs.aws.amazon.com/solutions/latest/automated-data-analytics-on-aws/deploy-the-solution.html) into an AWS account and setup ADA. We will then create the data products within ADA for the Amazon CloudWatch Log Group, Amazon S3 bucket, and Amazon DynamoDB. Once the data products are configured, ADA provisions the data pipeline to ingest the data from the sources into the ADA platform. Using ADA’s Query Workbench, users can query the ingested data using plain SQL for application troubleshooting or issue diagnosis. 

Refer to the diagram below to get an overview of the architecture and workflow of using ADA to gain insights into application logs.
![Demo Solution Architecture.](./image/SA.png "Demo Solution Architecture.")

The workflow includes the following steps:
1. An Amazon Lambda function is scheduled to be triggered at a 2-minute interval using Amazon EventBridge.
1. The Amazon Lambda function emits logs that are stored at a specified Amazon CloudWatch Log Group under /aws/lambda/CdkStack-AdaLogGenLambdaFunction. The application logs are generated using the Apache Log Format schema but stored in the Amazon CloudWatch Log Group in JSON format.
1. The Data Products for Amazon CloudWatch, Amazon S3 and Amazon DynamoDB, are created in ADA, respectively. The Amazon CloudWatch data product connects to the Amazon CloudWatch Log Group where the application (AWS Lambda) logs are stored. The Amazon S3 connector connects to an Amazon S3 bucket folder where the historical logs are stored. The Amazon DynamoDB connector connects to an Amazon DynamoDB table where the status code that are referred by the application and historical logs are stored.
1. For each of three data products, ADA deploys the data pipeline infrastructure to ingest data from the sources. Once the data ingestion is complete, user will be able to write queries using SQL via the ADA’s Query Workbench.
1. User logs in to the ADA portal and composes SQL queries from the query workbench to gain insights in to the application logs. User can optionally save the query and share the query with other ADA users in the same domain. ADA’s query feature is powered by Amazon Athena, which is a serverless, interactive analytics service that provides a simplified, flexible way to analyze petabytes of data.
1. Tableau is configured to access the ADA Data Products via ADA’s Egress EndPoints. User creates a dashboard with two charts. The first chart is a heat map that shows the prevalence of HTTP Error codes correlated with the Application API EndPoints. The second chart is a bar chart that shows the top 10 application APIs with a total count of HTTP error codes from the historical data.

## Prerequisites

To perform this demo end to end as described in the [blog](link), the user needs the following prerequisites:

1. Install the [AWS Command Line Interface](https://aws.amazon.com/cli/), AWS CDK [prerequisites](https://docs.aws.amazon.com/cdk/v2/guide/work-with.html), TypeScript-specific [prerequisites](https://docs.aws.amazon.com/cdk/v2/guide/work-with-cdk-typescript.html) and [git] (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
1. [Deploy](https://docs.aws.amazon.com/solutions/latest/automated-data-analytics-on-aws/deploy-the-solution.html) ADA Solution in the user’s AWS Account in the North Virgina (us-east-1) region.
    1. Provide an admin email while launching the ADA CloudFormation stack. It is needed for ADA to send the root user password. An admin phone number is required to receive One-Time Password (OTP) messages if Multi-Factor Authentication (MFA) is enabled. For this demo, MFA is not enabled.
1. Build and Deploy the sample application ([AWS Cloud Development Kit](https://github.com/aws-samples/operational-insights-with-automated-data-analytics-on-aws)) solution so that the following resources can be provisioned in the user’s AWS Account in the North Virginia (us-east-1) region:
    1. An Amazon Lambda Function that simulates the logging application and an Amazon EventBridge rule that invokes the Application Amazon Lambda function at a 2-minute interval.
    1. An Amazon S3 Bucket with the relevant bucket policies and a .csv file that contains the historical application logs.
    1. An Amazon DynamoDB table with the lookup data.
    1. Relevant IAM roles and permissions required for the services.
1. (Optional) Install Tableau [desktop](https://www.tableau.com/products/desktop), a third party Business Intelligence provider. We are using Tableau Desktop version 2021.2. There is a cost involved in using a licensed version of Tableau Desktop application. For additional details, please refer to Tableau licensing documentation.

## Setting up the Sample Application Infrastructure using AWS CDK
The steps to clone the repo and to set up AWS CDK project are listed below. Before running the commands below, be sure to [configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) your AWS Credentials. Create a folder, open Terminal and navigate to the folder where the AWS CDK solution needs to be installed. 

```
* `gh repo clone vaijusson/ADALogInsights`  clone the project in a local folder
* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template
```

These steps perform the following:
1. Install the library dependencies 
1. Build the project
1. Generate a valid AWS CloudFormation template
1. Deploy the stack using AWS CloudFormation in the user’s AWS account.

The deployment takes about 1-2 minutes and creates the Amazon DynamoDB lookup table, Application Lambda function and Amazon S3 bucket containing the historical log files as outputs.
![CDK Deployment.](./image/cdk_deploy.jpg "CDK Deployment.")

## Tear Down

Tearing down the sample application infrastructure is a two-step process. First, to remove the infrastructure provisioned for the purposes of this demo, execute the following command in the Terminal.

```
cdk destroy
```

For the following question, enter ‘y’ and CDK will delete the resources deployed for the demo. 

```
Are you sure you want to delete: CdkStack (y/n)? y
```

Alternatively, the resources can be removed from the AWS Console by navigating the ‘CloudFormation’ service, selecting the ‘CdkStack’ and selecting ‘Delete’ option. 
![CloudFormation Destroy.](./image/cf_destroy.jpg "CloudFormation Destroy.")


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.