<h1><u>TASK MANAGER:</u></h1>

### Hexlet tests and linter status:
[![Actions Status](https://github.com/Tragoedie/python-project-lvl4/workflows/hexlet-check/badge.svg)](https://github.com/Tragoedie/python-project-lvl4/actions)
[![test_and_linter_check](https://github.com/Tragoedie/python-project-lvl4/actions/workflows/linter_test_check.yml/badge.svg)](https://github.com/Tragoedie/python-project-lvl4/actions/workflows/linter_test_check.yml)
<a href="https://codeclimate.com/github/Tragoedie/python-project-lvl4/test_coverage"><img src="https://api.codeclimate.com/v1/badges/2a085ee6cdb9768e4436/test_coverage" /></a>

<h1>Description:</h1>

Task manager allows setting tasks, assigning performers and changing their statuses. Registration and authentication are required to work with the system.

<h2> App at Heroku:</h2>

Task manager is also deployed on Heroku, so feel free to register and make experiments with it:

https://task-manager-tragoedia.herokuapp.com/

All possible errors and bugs will be sent to Rollbar automatically and fixed as soon as possible.

<h2>Commands to start the application:</h2>

1) Clone repo:

```bash
$ pip install --user git+https://github.com/Tragoedie/python-project-lvl4.git
```
2) Create .env file
```bash
examples names of variables are placed in file: env.example
```
3) Install dependencies:
```bash
$ make install
```
4) Start migrations:
```bash
$ make migrate
```
5) Launch your server:
```bash
$ make run
```
