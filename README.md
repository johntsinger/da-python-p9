# Python Application Developer - P9 - Develop a Web application using Django

## Description

Blog site using django.

#### Account :
  - ###### Not logged in :
    - Create new account
    - Login
  - ###### Logged in (by clicking on your name in the nav bar) :
    - On Profile :
      - Change email, password, profile image and username
      - Delete your account
    - Logout

#### Feed :
  - View all posts (tickets and reviews) from you and the users you follow
  - Create new tickets and reviews
  - Update and delete your own tickets and reviews
  - Write a review for your tickets and for the tickets of users you follow
  - Access other users posts by clicking on their username

#### Post :
  - ###### By clicking on Post in the nav bar:
      - View all posts (tickets and reviews) you have posted
      - If other users have replied to your tickets with a review, they are also displayed
      - Create new tickets and reviews
      - Update and delete your own tickets and reviews
      - Access other users posts by clicking on their username
      - Write a review for your tickets
  - ###### By clicking on the username of other users :
      - View all posts (ticket and reviews) from this user
      - If other users have replied to this user's tickets with a review, they are also displayed
      - If you don't follow him, a button allows you to follow him from here
      - Write a review for this user's tickets if you follow him
      - Create new tickets and reviews
   
#### Subscriptions :
  - Follow a new user by typing his username in the input bar and clicking on "Follow"
  - View all the users you follow and remove them by clicking on "Unsubscribe"
  - View all the users who follow you
  - Access other users posts by clicking on their username

## Installation guide

### Clone repository with Git :

    git clone https://github.com/johntsinger/da-python-p9.git
    
or

### Download the repository :

- On the [project page](https://github.com/johntsinger/da-python-p9)
- Click on green Code button
- Click on download ZIP
- Extract the file.

### Install Python :

If you don't have Python 3, please visit : https://www.python.org/downloads/ to download it !

### Virtual Environment :

#### Create a virtual environment in the project root :

    python -m venv env

#### Activate a virtual environment :

##### windows :

    env/Scripts/activate
    
##### linux/mac :

    source env/bin/activate
    
#### Install dependencies :

    pip install -r requirements.txt

## Run the program :

Go to the litrevu folder :

    cd litrevu

Run the server :

    python manage.py runserver

By default the port is 8000, but you can change it, e.g. to use port 8001 instead you can do :

    python manage.py runserver 8001 

⚠️ If you change the port, make sure you also change it in the url, replacing 8000 with the new port. 

Open a browser and go to :

http://127.0.0.1:8000/

Here we go !

## Django admin :

#### Superuser Admin :

| Username | Email | Password |
| --- | --- | --- |
| admin | admin<span>@</span>litrevu.com | litrevu |

#### Create new superuser :

You can create a new superuser :

    py manage.py createsuperuser

Then follow the instructions.

#### Access admin page :

http://127.0.0.1:8000/admin/

## Test :

You can use either admin or test users.

#### Registered users informations :

| Username | Email | Password |
| --- | --- | --- |
| usertest1 | user1<span>@</span>test.com | wxcv1234 |
| usertest2 | user2<span>@</span>test.com | wxcv1234 |

## Contact :
Jonathan Singer - john.t.singer@gmail.com\
Project link : https://github.com/johntsinger/da-python-p9
