# Simple Flask API

Author: Agustin Bassi - 2020

Project template to create super fast & simple REST API using Flask web framework in a single file. 

Due to the project nature of be as simple as possible Flask API, the code uses a file for storage data in JSON format instead of database.

In order to make the project portable, it can runs in a common Python virtual environment or as a Docker container.

In this README file there will be explained both methods to fit this project in your best requirements.

> **_NOTE:_**  For more complex project structure consider other projects looking at https://github.com/agustinBassi or in Github.


# Project structure

The project structure is shown in the next `tree` caption.

```sh
├── db
│   └── db.json
├── Dockerfile
└── src
    ├── app.py
    └── requirements.txt
```

* db/db.json: File to store application data in JSON format. By default it has mock data.
* Dockerfile: The file needed to build this project as a Docker image (can be used optionally).
* src/app.py: Main project file. It can be used as is, or a specific module can be added to this folder.
* src/requirements.txt: The Python packages dependencies.

# Software organization

The file src/app.py is splitted into sections to make it easy to read and grow.

* In the `Imports` section just put import sentencies (remember the order: First Standard packages, second third party packages and third project/personal packages).
* In the `Settings & Data` section put global configs, and things that strictly must be global.
* In the `Utils` section put the code that is useful to the application but it is not dependant of any other part of the code, for example conversions types, parsers, etc.
* In the `Application Views (endpoints)` section put the HTTP endpoints that application needs. In the provided endpoints are shown the current Flask configuration, and the endpoints to GET, POST, PUT and DELETE module specific settings/data. Note that every view has PREFIX, it is useful to support different versions of the API in the same application.
* In the `Specific module code` section is explained which kind of code you can put there. As is specified put code of your application, like access to some server, operate over a file, capture user input by interface or any other operation specific of your project.
* In the `Module main code` section is the code related to startup and run the application. This two actions are prefereably the only required in this section.

As you see, the code is organized in order to be easy to understand and maintain, try to follow the rules above to create an understandable application.

> **_NOTE:_**  If you think your specific module code is little big to be in the same `app.py` file, create a separate module and write your code there. In the import section just add a line `import your_module` and remove the example code in `Specific module code`. Then execute the calls to your_module from views.

# Installation & Run the project

The project can run in two ways, in a classic Python Virtual Environment or in a Docker container. In this section both methods are described.

## Virtual Environment

If you have Python3+ installed the tool for create it is bundled with Python. If not refer to [official documentation](https://python.org) to find installation procedure.

The first step is to create & activate the Python Virtual Environment with the commands below. By default this commands will create a venv in the `current_directory/.venv` (supposed to be in the project root folder), but you can change it for any path you want.

```sh
python3 -m venv "$PWD"/.venv
source "$PWD"/.venv/bin/activate
```

Once venv is activated execute the command below to install project dependencies.

```sh
pip install -r src/requirements.txt
```

To run the project, simply execute the next command.

```sh
python3 src/app.py
```

## Docker container

This option is prefereable in the majority of cases, because this application can be a part of a larger application. Besides, using Docker you garantee that project can be reproducible in any scenario with the same easy steps.

The first step is to build the Docker image which has all project dependencies bundled in it. Execute the next command.

```
docker build --tag local/flask-api:dev .
```

> **_NOTE:_**: You can build your image with `prod` tag putting your code into the image once you have your code finished. Read the Dockerfile to change from `dev` to `prod`.

The command above will create the image. You will see an output like the next.

```
Sending build context to Docker daemon  19.48MB
Step 1/9 : FROM python:3
 ---> 659f826fabf4
 ...
 ...
 ...
 ---> fed022191ead
Successfully built fed022191ead
Successfully tagged local/flask-api:dev
```

Finally run the project Docker image. In the project root folder run the next command.

```
docker run \
--rm \
--interactive \
--name flask-api \
--publish 5001:5000 \
--volume "$PWD"/db:/app/db \
--volume "$PWD"/src:/app/src \
local/flask-api:dev \
python app.py
```

In the command above you are running the Docker container with name `flask-api`, binding your host port 5001 into container port 5000, sharing the project db path (`"$PWD"/db`) into container db path (`/app/db`), sharing your source code folder (`"$PWD"/src`) into container source folder (`/app/db`), and running the `app.py` with python when container starts.

# Test the project

The easy and best way to test the project is using [Postman](https://www.postman.com/), a really intuitive and easy to use tool for execute HTTP methods.

If you decide to quicly test the project you can use `curl`. In the next snippets is shown how to test each project resource.

Get Flask configuration.

```
curl -i \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-X GET \
http://localhost:5001/api/v1/
```

Get module settings

```
curl -i \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-X GET \
http://localhost:5001/api/v1/module_settings/
```

Add or change a key in module settings.

```
curl -i \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-X POST \
--data '{ "username":"xyz" , "password":"xyz" }' \
http://localhost:5001/api/v1/module_settings/
```

Delete a key in module settings.

```
curl -i \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-X DELETE \
--data '{"keys_to_remove": [ "username", "password" ] }' \
http://localhost:5001/api/v1/module_settings/
```

# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

# Licence

MIT

You can do anything you want to this code. If you find it useful please helpme with follow to my Github user and a Star project, it will animate me to continue contribuiting with the great open source community.