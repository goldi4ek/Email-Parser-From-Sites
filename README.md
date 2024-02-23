# Project Title

## Description

A script that allows you to load an Excel document that stores the addresses of web sites and get a modified document in which next to each site will be written the email address of the company.
If there is no email address on the site, the link to Facebook is checked and the email address is found there
If access to the site is limited (because the bot is working) we try to find a Facebook page with the same name as the site.

Also in case of unexpected errors log.txt is created where they are recorded.

## Add Excel file

Replace it in the root folder and add the name of the file in the main.py

## Add ChromeWebDriver

Replace it in the root folder and dowbload google chrome version 114

## Installation

Instructions on how to install and setup project.

```bash
git clone https://github.com/goldi4ek/Email-Parser-From-Sites.git

pip install -r requirements.txt

python main.py
```
