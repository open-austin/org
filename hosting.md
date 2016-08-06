# Hosting

Your project may need hosting, servers, or something like that.

Often times, you might think that you need to use a paid service to deploy your project. But there are usually free alternatives (that aren't inferior).

This document will cover some basic instructions on how to get setup with some of the paid resources Code for America provides to Open Austin like AWS and Azure. It will also suggest a few ways to avoid using a paid service.

## Containers

An easy way to package and deploy and application is to use a container, like Docker, to run your application. You need to write a Dockerfile that describes your application's environment, and then you can run it on a container service with minimal effort. Amazon, Azure and Google cloud all have container platforms.

## Amazon Web Services

AWS has several options for hosting. You can use a more traditional setup, or try using one of their cloud platforms.

You can always provision and manage a cloud sever by yourself. This is a very manual process, and we don't recommend it. The option always exists if you specifically need a server for a project.

For a simple Node or Python application, ElasticBeanstalk might be the best option. It manages server instances, and provides support for databases. In addition, application and deployment is handled by a CLI+configuration files in the project repository, making it easy for multiple people to deploy the project.

Finally, consider using AWS Lambda. Lambda is "Serverless Compute" and allows you to run code without provisioning a server. You can execute code on external triggers. Several OA members have used it in projects. If you have code that runs once a day at a set time, consider using Lambda instead of a cronjob on a server

## Azure

## Heroku

Heroku is a Platform as a Service application that will manage an application for you. Heroku only supports several languages, Node, Ruby, Java, PHP, Python, Go, Scala and Clojure. Heroku will also manage a database for you. Deployment is managed by git, so it's a fairly simple process 

## GitHub Pages

Depending on your application, you might not even need a server! You can host a static site on github, which makes deployment and maintanince very simple. If your application is mostly a front end site, consider hosting it on github pages

# AWS Account Setup Instructions

1. Go to AWS
2. Go to IAM https://console.aws.amazon.com/iam/home?region=us-west-2#home
3. Create a new user
4. Note the Username, Access Key ID, and Secret Access Key
6. Click on the user details
5. Add the user to the Group `open-austin-members`
6. Assign the user a password
  ![image](https://cloud.githubusercontent.com/assets/1275831/17458330/0308f9f2-5bd3-11e6-98d3-a5e176369afe.png)

  ![image](https://cloud.githubusercontent.com/assets/1275831/17458332/1915240a-5bd3-11e6-8c48-06571f90f2b3.png)

  ![image](https://cloud.githubusercontent.com/assets/1275831/17458333/21938fb8-5bd3-11e6-98c3-d884c7ec1a85.png)

6. Finally, email the login information to the user:
  ```
  https://open-austin.signin.aws.amazon.com/console
  
  User: helloworld
  Password: $&$(@*U(#*U(*U@)))
  
  Access Key ID: AKIAIEIEJF4IE31JF3
  Secret Access Key: woi323ej81jj3st123r523
  ```
