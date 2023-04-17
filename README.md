# Introduction

*This framework is based on selenium-webdriver with python. It is used to test https://reqres.in/ application.

## Features

* Supports python-based automation for web applications.
* Tests can be run on popular browsers like chrome, chromium and firefox.
* Tests can be executed in headless mode.
* Browser type and headless mode are easily configurable via environment variables.
* Logger is implemented. It can be customized and used anywhere in framework.
* Extensive retry decorators are written with customizable timeout and polling interval.

## Main Components

* ‘Webdriver_factory’ for launching new webdriver instance.
* ‘browser’all browser related actions can be performed.
* ‘ext’ it contains methods for any action on web elements.

# Quick Start

## Prerequisites:

* Python 3 is installed.



## Setup Environment

* Execute setup_env.cmd.

## Browser Settings
* By default, chromium is supported in headless mode
* Change browser using set BROWSER_TYPE=chrome
* For headless mode: set HEADLESS_MODE=”True”

## Run Tests
* Run command "behave test_cases\features"

## Execute Tests And Generate Allure Reports
* behave test_cases\features -f allure_behave.formatter:AllureFormatter -o report\allure_report\
* allure serve .\report\allure_report\
# Pending Tasks
* Json_util is written but checking json response is still pending

