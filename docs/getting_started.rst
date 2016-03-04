.. _getting-started:

Getting Started
===============

There are a number of ways you can deploy apostello:

* On your server using the :ref:`ansible playbook <deploy-ansible>` included in the repo
* One click :ref:`Heroku <deploy-heroku>` deploy
* Manually on your own server, you will need to setup a message broker, a database, a web server and the django app and celery background worker. If you have deployed a Django app before, then you should be able to do this

Prerequisites
-------------

* *Required*: A domain name and a server (or you can use Heroku instead)
* *Required*: A `Twilio <https://www.twilio.com/>`_ account with a purchased number
* *Required*: An SMTP server or `Mailgun <https://www.mailgun.com/>`_, `Mandrill <https://mandrillapp.com/>`_, etc account for sending email notifications
* *Optional*: A web app registered for authentication with a Google account
* *Optional*: An `Elvanto <https://www.elvanto.com/r_Y7HXKNE6>`_ API Key for importing Elvanto groups
* *Optional*: An `opbeat <https://opbeat.com/>`_ account for error logging. You can setup opbeat logging on the front and back ends in separate opbeat apps: one for the django app and one for the js front end.

First Run
---------

After you have successfully installed apostello there are a few more steps to finish setup.

* Open your instance of apostello, you will be redirected to the login page
* Click the sign up button at the bottom to create a user account
* You should receive a confirmation email (if this does not work, there may be something wrong with your email settings)
* Once you have confirmed your email address, log in to your site. As the first user you will have been given admin privileges
* Open the `Tools` menu where you can edit the site configuration and some canned responses
* If you want to let users sign in with Google, then you need to follow the steps `here <https://django-allauth.readthedocs.org/en/stable/providers.html#google>`_
* If you need to approve new users, you will need to visit `/admin/auth/user/` in the admin panel
* Now you need to :ref:`setup Twilio <setup-twilio>`
* You may want to send yourself a test message to verify your setup
* You can now continue to set up apostello: import contacts, start sending messages, publicise your number, etc
* Any future users will be able to use the sign up page. If you do not whitelist any domains, you will need to approve new users before they can do anything


.. _setup-twilio:

Twilio Setup
============

Once you have apostello setup we need to tell Twilio what url to talk to when it receives an SMS:

* Open https://www.twilio.com/user/account/messaging/phone-numbers
* Click the number you are using in apostello and a popup should appear
* Click the "Messaging" tab if it is not already selected
* Select "Configure with URL"
* Ensure the HTTP method is set to `POST`
* In the "Request URL field" add the url to your server, followed by "/sms/". If you are using Heroku it may look like `https://apostello-demo.herokuapp.com/sms/` or if your site is hosted at `https://sms.example.com`, your URL would be `https://sms.example.com/sms`.
* Click save

Now you should be able to test your setup - send a message to your number and you should receive an automated reply. If not, raise an `issue <https://github.com/monty5811/apostello/issues/new?title=[Setup%20Help]>`_ or get in touch on `slack <http://chat.church.io>`_.
