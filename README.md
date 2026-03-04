# Melody Journal — Serverless Backend

A minimal journaling app for tracking daily music practice sessions.
Built to learn AWS serverless architecture hands-on.

## Stack
Python · AWS Lambda · API Gateway · DynamoDB · S3 · CloudFront  
SAM (Infrastructure as Code) · CodePipeline · Google OAuth

## Architecture
- Each Lambda function handles a single CRUD operation on journal entries
- SAM templates for infrastructure definition and deployment
- Google OAuth for authentication
- CI/CD pipeline via CodePipeline
