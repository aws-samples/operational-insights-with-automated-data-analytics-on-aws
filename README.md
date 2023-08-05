## Derive Application Log Insights Using Amazon CloudWatch Connector for Automated Data Analytics on AWS

### <ins> Background </ins>
 This repository aims at providing CDK solution that is used to demonstrate the capabilities of AWS ADA Solution. Automated Data Analytics (ADA) is an AWS Solution that enables users to derive meaningful insights from data in a matter of minutes through a simple and intuitive user interface. ADA provides a AWS-native, production-ready data platform to enable businesses analyse datasets, manage the data ingestion and data transformation. ADA provides a foundational platform that can be used by data analysts in use cases such as IT, Finance, Marketing, Sales and Security. Using ADA, teams can ingest, transform, govern and query diverse datasets from a range of data sources without requiring specialist technical skills. ADA provides a set of pre-built connectors to ingest data from a wide range of sources including Amazon Simple Storage Service, Amazon Kinesis Stream, Amazon CloudWatch, Amazon CloudTrail, and Amazon DynamoDB. The Amazon CloudWatch data connector allows data ingestion from the Amazon CloudWatch logs in the same AWS account in which ADA has been deployed, or an external AWS Account. Amazon Athena is a serverless, interactive analytics service that provides a simplified, flexible way to analyze petabytes of data.

In this repository, we demonstrate how ADA Solution can be used to derive application insights in the AWS. We will first deploy ADA Solution into an AWS account and configure ADAby creating data products using the data connectors. We then use ADA’s query workbench to query and join the separate data sources to gain insights. We will also demonstrate how ADA can be integrated with BI tools such as Tableau to create rich visualisation and create reports.

### <ins> Solution overview </ins>

The following are deployed:

    1. A Amazon Lambda Function that simulates an application emitting logs in Apache Log Format and 
    2. An Amazon EventBridge rule that invokes the Application Amazon Lambda function at a 2-minute interval.
    3. An Amazon S3 Bucket with the relevant bucket policies and a .csv file that contains the historical application logs.
    4. A Amazon DynamoDB table with the lookup data.
    5. Relevant IAM roles and permissions required for the services.

### <ins> Instructions </ins>

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Steps to setting up the solution:
## Prerequisites: Install the AWS CDK prerequisites, TypeScript-specific prerequisites and git.

* `gh repo clone vaijusson/ADALogInsights`  clone the project in a local folder
* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.