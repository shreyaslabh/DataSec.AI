
<h1 align="center">
  <br>
  <img src="https://github.com/Shreyas-l/DataSec.AI/blob/main/Documentation/logo_.png" alt="Markdownify" width="400">
</h1>

## Demo

https://user-images.githubusercontent.com/58290353/137585333-99d3607e-4337-474f-8fd3-e903dc5d3ef5.mp4

## Description

<p> DataSec.AI aims to tackle data privacy issues of the 21st century by leveraging cutting-edge technologies integrated with state-of-the-art Artificial Intelligence Algorithms <p>

* DataSec.AI masks all the sensitive Personally Identifiable Information (PII) on the web
* The masking logic works in real-time and can connect to the company VPN and intercept all the traffic passing through the network 
* The masking logic can be configured by our clients, once their accounts are authorized by the admin
* Several types of masks are provided to ensure that DataSec covers all types of PII, especially in the pharmaceutical industry
* The software can be deployed as both Cloud and On-Premise setup 
* Containerized deployment on Google Kubernetes Engine helps speed up the anonymization process, auto-scaling, auto-healing in case of errors, regular health checks, and periodic report generation
* The CI/CD pipeline helps to push and deploy new code modifications with great ease
* Leveraged Service Mesh Architecture to deploy DataSec on Google Kubernetes Engine
* Squid Proxy acts as a Reverse Proxy capable of intercepting all the traffic on a given network
* Squid Proxy acts as a sidecar to the Python ICAP Server which Masks/Unmasks PII Data from the intercepted traffic
* Redis is used for the purpose of in-memory caching of Masking logic, Request Configurations, Response Configurations, and User ID Management
* Flask framework is used to develop the Configuration Software
* PostgreSQL Database is used for the purpose of RDBMS
* SpaCy's Presidio Analyzer Engine is leveraged to detect and anonymized the sensitive PII data from requests and responses. 

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


## Download

You can [download](https://github.com/amitmerchant1990/electron-markdownify/releases/tag/v1.2.0) the latest installable version of Markdownify for Windows, macOS and Linux.

## Emailware

Markdownify is an [emailware](https://en.wiktionary.org/wiki/emailware). Meaning, if you liked using this app or it has helped you in any way, I'd like you send me an email at <bullredeyes@gmail.com> about anything you'd want to say about this software. I'd really appreciate it!

## Credits

This software uses the following open source packages:

- [Electron](http://electron.atom.io/)
- [Node.js](https://nodejs.org/)
- [Marked - a markdown parser](https://github.com/chjj/marked)
- [showdown](http://showdownjs.github.io/showdown/)
- [CodeMirror](http://codemirror.net/)
- Emojis are taken from [here](https://github.com/arvida/emoji-cheat-sheet.com)
- [highlight.js](https://highlightjs.org/)

## Related

[markdownify-web](https://github.com/amitmerchant1990/markdownify-web) - Web version of Markdownify

## Support

<a href="https://www.buymeacoffee.com/5Zn8Xh3l9" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

<p>Or</p> 

<a href="https://www.patreon.com/amitmerchant">
	<img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="160">
</a>

## You may also like...

- [Pomolectron](https://github.com/amitmerchant1990/pomolectron) - A pomodoro app
- [Correo](https://github.com/amitmerchant1990/correo) - A menubar/taskbar Gmail App for Windows and macOS

## License

MIT

---

> [amitmerchant.com](https://www.amitmerchant.com) &nbsp;&middot;&nbsp;
> GitHub [@amitmerchant1990](https://github.com/amitmerchant1990) &nbsp;&middot;&nbsp;
> Twitter [@amit_merchant](https://twitter.com/amit_merchant)

