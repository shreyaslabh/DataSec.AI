
<h1 align="center">
  <br>
  <img src="https://github.com/Shreyas-l/DataSec.AI/blob/main/Documentation/logo_.png" alt="Markdownify" width="400">
</h1>

## Introduction

https://user-images.githubusercontent.com/58290353/137585333-99d3607e-4337-474f-8fd3-e903dc5d3ef5.mp4

## Description

<p> DataSec.AI aims to tackle data privacy issues of the 21st century by leveraging cutting-edge technologies integrated with state-of-the-art Artificial Intelligence Algorithms <p>

* DataSec.AI masks all the sensitive Personally Identifiable Information (PII) on the web
* The masking logic works real-time, connects to the company VPN & intercepts all the network traffic
* The masking logic can be configured by our clients, once their accounts are authorized by the admin
* Several types of masks are configured to ensure that DataSec covers all PII, especially pharma industry
* The software can be deployed as both Cloud and On-Premise setup 
* Containerized deployment on Google Kubernetes Engine helps speed up the anonymization, scaling, healing
* The CI/CD pipeline helps to push and deploy new code modifications with great ease
* Leveraged Service Mesh Architecture to deploy DataSec on Google Kubernetes Engine
* Squid Proxy acts as a Reverse Proxy capable of intercepting all the traffic on a given network
* Squid Proxy acts as a sidecar to the Python ICAP Server which Masks/Unmasks PII Data from intercepted traffic
* Redis used for in-memory caching of Masking logic, Request & Response Configurations, UserID Management
* Flask framework is used to develop the Configuration Software
* PostgreSQL Database is used for the purpose of RDBMS
* SpaCy's Presidio Analyzer Engine is leveraged to detect & anonymize PII from requests and responses
	
## Demo
	
![ezgif com-gif-maker](https://user-images.githubusercontent.com/58290353/137585762-4755f0c2-5b54-468b-8127-b377d3939f2c.gif)

## Tech Stack
	
## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com) and [Node.js](https://nodejs.org/en/download/) (which comes with [npm](http://npmjs.com)) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/amitmerchant1990/electron-markdownify

# Go into the repository
$ cd electron-markdownify

# Install dependencies
$ npm install

# Run the app
$ npm start
```

Note: If you're using Linux Bash for Windows, [see this guide](https://www.howtogeek.com/261575/how-to-run-graphical-linux-desktop-applications-from-windows-10s-bash-shell/) or use `node` from the command prompt.


## License

MIT

