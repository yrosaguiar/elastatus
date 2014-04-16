Elastatus
=========

A Flask application using Boto and Bootstrap to display read-only information from multiple Amazon Web Services accounts in one place.


WHY?
----

Amazon Web Services are great... awesome in fact. However, there is one tiny thing that is annoying and has been for some time. Once you have multiple AWS accounts there is no means by which you can view infrastructure and services from all accounts in one single browser session - and at Mind Candy we have separate accounts for different environments.

The other problem when you have multiple accounts is user access management. AWS has Identity and Access Management (IAM) which are great, and we use them extensively. However, as a growing start-up we have a quite a large number of people - qa, developers, engineers - who all require some sort of access to AWS information and managing many IAM users over multiple accounts, either using Roles or just individual access per account, can be quite the administrative overhead.

More often than not the access required by those outside NetOps is only read-only anyway. This is so developers can quickly and easily find out where their EC2 instances are, what the endpoint for an Elasticache or RDS instance might be, or what a specific CloudFormation templates actually looks like. So we wrote this to provide quick read-only access to the most common information that people want across all our AWS accounts.


CURRENT RELEASE TAG
-------------------

  * 1.0.2


REQUIREMENTS
------------

    PyYAML==3.10
    Flask==0.10.1
    boto==2.25.0


INSTALL
-------

To run elastatus locally for testing you can do it in virtualenv

    me@localhost:~$ virtualenv myenv
    me@localhost:~$ cd myenv/
    me@localhost:~/myenv$ source bin/activate
    (myenv)me@localhost:~/myenv$ git clone git@github.com:mindcandy/elastatus.git
    (myenv)me@localhost:~/myenv$ cd elastatus
    (myenv)me@localhost:~/myenv/elastatus$ pip install -r requirements.txt
    (myenv)me@localhost:~/myenv/elastatus$ cp app/config.yaml.sample app/config.yaml


### config.yaml settings

##### accounts 

  * This is fairly straight forward and obvious. Put your AWS accounts in here. At the minimum you need one, but you can add as many as you like. The name you give these in this file will be used as the name in the menus within elastatus, so it would wise to give them a sensible name e.g. production. elastatus will capitalize these in the menus. If you use underscores it does not, as yet, replace them for spaces.

  * _IMPORTANT:_ It is not advisable or sensible to use your account access keys and secrets here. You should go into the AWS console for each account and create an IAM user and give that user Read-Only access to all services. If you choose to use your primary account details then it is on your own head.

        accounts:
            account1:
                aws_access_key_id: 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
                aws_secret_access_key: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
            account2:
                aws_access_key_id: 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
                aws_secret_access_key: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
            account3:
                aws_access_key_id: 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
                aws_secret_access_key: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'


##### regions 

  * This is a Python list (or an array if that's what you want to call it) of strings denoting the various AWS regions. You need at least one region in here. These will also be displayed in the menu in the app and are also used to connect to the regions when querying the API i.e. they're important. 

        regions: ['eu-west-1','us-east-1']

##### aws:$service

  * The app's menu layout is in line with the separation of services in the AWS Console. i.e. compute, database, deployments, services. You are free to remove elements from the lists depending on what you actually use in Amazon. 
  * _Do not remove any of the elements completely_ though or things will break due to some currently hard-coded things in the template. 
  * The currently supported AWS services are the ones in the sample file.


        aws: 
            compute: ['ec2', 'ebs', 'snapshots', 'elb', 'autoscale']
            database: ['rds','dynamodb', 'elasticache', 'redshift']
            deployments: ['cloudformation']
            services: ['route53', 'sqs', 'sns']

##### default_*

  * There are three "default_*" settings for account, region and service. 
  * These are used by the app to determine the landing page when you browse to the root of the site or click the elastatus (home) link in the menu. 
  * _Required settings_

        default_account: 'account1'
        default_region: 'eu-west-1'
        default_service: 'ec2'

##### route53

  * Strictly speaking Route53 does not use regions, although you can connect to a region to use the service. As such the way in which in the app connect to Amazon for Route53 is slightly different. 
  * If you want to use Route53 you need to specify which account from your account settings is to be used, the domain name you want to see and its Route53 Zone ID. 
  * If you don't want to use this, or don't use Route53 simple remove "route53" from the services list in the aws settings above and leave this setting as it is.

        route53:
            account: 'account1'
            domain: 'mydomain'
            zone_id: 'myzoneid'


RUNNING THE APP
---------------

  * Once you've set up you're configuration you can run the app with the built-in Flask development web server like this:

        (myenv)me@localhost:~/myenv/elastatus$ python runserver.py
         * Running on http://127.0.0.1:5000/
         * Restarting with reloader

  * Now go to http://127.0.0.1:5000/ in your browser of choice and you should see information about your "default_account"
  * _NOTE:_ Debug mode is set to True in runserver.py


RUNNING IN NON-DEVELOPMENT ENVIRONMENT
--------------------------------------

  * Setting the app up in a non-development with something like uWSGI and nginx is beyond the scope of this README.
  * The following Flask document page can help you out with this: http://flask.pocoo.org/docs/deploying/uwsgi/


SCREENSHOTS
-----------

#### EC2 View

![EC2_View](screenshots/ec2.png?raw=true)

#### Autoscaling Groups

![Autoscaling_Groups](screenshots/asg.png?raw=true)

#### CloudFormation

![CloudFormation](screenshots/cf.png?raw=true)


KNOWN ISSUES
------------

  * As mentioned above, the navigation menu content is largely driven by the config file, but there is also some hard-coding in layout.html. This needs to be fixed at some point.
  * Exception handling may be missing in some circumstances.
  * Depending on the amount of AWS assets it may be a little slow. This is especially the case for CloudFormation as it actually makes more than one call to the API in order to provide a download link for the JSON template.
  * The project uses [Twitter Bootsrap 2.3.2](http://getbootstrap.com/2.3.2/) which is no longer officially supported. The reason for this is that the JavaScript used to generate the dynamic search tables is not compatible with Bootrap 3.


ROADMAP
-------

This app is under active development and new services will be added including but not limited too:

  1. Drill down into a detailed EC2 Instance view.
  2. CloudWatch Alarm statuses and history.
  3. S3 browsing of specific named buckets in config.yaml
  4. Authenticated views allowing certain actions, e.g. update CloudFormation, start/stop instances.
  5. Detailed Billing view with support for Consolidated billing.
  6. Background queue processing so views are displayed from cached content to limit and manage the number of API calls.
  7. Front-End improvements.
  8. Dashboard views giving headline figures such as number of instances, types, status etcetra.


CONTRIBUTIONS AND BUG REPORTS
-----------------------------

  * Anyone is free to contribute and make it better (and it can be much better). Just fork it, create a branch and submit a pull request.
  * The installation and set up instructions in this README have been tested. Please open an issue if you find any bugs or have problems.


EXTERNAL CREDITS
----------------

  * [boto](https://github.com/boto/boto) aws library - backend talking to Amazon
  * [Twitter Bootsrap](http://getbootstrap.com/2.3.2/) - web layout
  * [Datatables](http://datatables.net/) - JQuery plugin library that does the table pagination and responsive search.
  * [Amazon Simple Icons](http://aws.amazon.com/architecture/icons/)


LICENSE
-------

  * elastatus MIT License (elastatus.LICENSE)
  * Twitter Bootstrap MIT License (boostrap.LICENSE)
  * Datatables BSD License (datatables.LICENSE)
  * AWS Simple Icons License Free/Creative Commons [AWS Blog](http://aws.typepad.com/aws/2011/12/introducing-aws-simple-icons-for-your-architecture-diagrams.html)
