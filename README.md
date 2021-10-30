
<h1 align="center">
  <br>
  <img src="https://github.com/Shreyas-l/DataSec.AI/blob/main/Documentation/logo_.png" alt="Markdownify" width="400">
</h1>


<p align="center">
 <div align="center"><img width="55" src="https://github.com/Shreyas-l/DataSec.AI/blob/main/Documentation/python.png.png"/><img width="55" src="https://github.com/Shreyas-l/DataSec.AI/blob/main/Documentation/docker.png"/><img width="55" src="https://github.com/Shreyas-l/DataSec.AI/blob/main/Documentation/squid.png"/><img width="55" src="https://github.com/Shreyas-l/DataSec.AI/blob/main/Documentation/spacy.png"/><img width="55" src="https://github.com/Shreyas-l/DataSec.AI/blob/main/Documentation/gcp_.png"/><img width="55" src="https://github.com/Shreyas-l/DataSec.AI/blob/main/Documentation/redis.png"/><img width="55" src="https://github.com/Shreyas-l/DataSec.AI/blob/main/Documentation/postgres.png"/><img width="55" src="https://github.com/Shreyas-l/DataSec.AI/blob/main/Documentation/k8_.png"/></div>
</p>

<p align="center">
  <a href="#intro">Introduction</a> •
  <a href="#desc">Description</a> •
  <a href="#arch">Architecture</a> •
  <a href="#demo">Demonstration</a>
</p>

<div id="intro"></div>

## Introduction

https://user-images.githubusercontent.com/58290353/137585333-99d3607e-4337-474f-8fd3-e903dc5d3ef5.mp4

<div id="desc"></div>

## Description

<p> DataSec.AI aims to tackle data privacy issues of the 21st century by leveraging cutting-edge technologies integrated with state-of-the-art Artificial Intelligence Algorithms <p>

* DataSec.AI masks all the sensitive Personally Identifiable Information (PII) on the web
* The masking logic works real-time, connects to the company VPN & intercepts all the network traffic
* The masking logic can be configured by our clients, once their accounts are authorized by the admin
* Several types of masks are configured to ensure that DataSec covers all PII, especially pharma industry
* The software can be deployed as both Cloud and On-Premise setup 
* Containerized deployment on Google Kubernetes Engine speeds up anonymization, scaling, healing
* The CI/CD pipeline helps to push and deploy new code modifications with great ease
* Leveraged Service Mesh Architecture to deploy DataSec on Google Kubernetes Engine
* Squid Proxy acts as Reverse Proxy & intercepts all the traffic on a given network
* Squid Proxy acts as sidecar to Python ICAP Server which Masks/Unmasks PII from intercepted traffic
* Redis used for in-memory caching of Masking logic, Request Configurations, UserID Management
* Flask framework is used to develop the Configuration Software
* PostgreSQL Database is used for the purpose of RDBMS
* SpaCy's Presidio Analyzer Engine is leveraged to detect & anonymize PII from requests and responses
	
<div id="arch"></div>

## Architecture

<p align="center">
 <div align="center"><img src="https://github.com/Shreyas-l/DataSec.AI/blob/main/Documentation/DMS.png"/>
</div>
</p>

<div id="demo"></div>

## Demonstration
	
![ezgif com-gif-maker](https://user-images.githubusercontent.com/58290353/137585762-4755f0c2-5b54-468b-8127-b377d3939f2c.gif)

## License

MIT

