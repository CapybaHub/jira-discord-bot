#!/usr/bin/env bash

if [ "$1" == "-h" ]; then
	echo "This script will create an app inside the apps folder"
	echo "To use type the following line:"
	echo "bash start-app.sh app_name"
	echo "Replace app_name with the actual name for your app"
elif [ "$1" != "" ]; then
    if [ ! -d "apps" ]; then
        mkdir apps
        touch apps/__init__.py
    fi
    mkdir apps/$1
    if [ -f /.dockerenv ]; then
        python manage.py startapp $1 apps/$1 --template conf/app_template
    else
        docker-compose run --rm web python manage.py startapp $1 apps/$1 --template app_template
    fi
    echo "Success! The app $1 has been aded, don't forget to add INSTALLED_APPS += ['apps.$1'] in your project's settings.py"
else
	echo "Error! One parameter is expected: app_name"
fi
