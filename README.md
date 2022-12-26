# do-not-procrastinate

## Objective

> Create a personal scoreboard which influence people to implement positive habits with consistency and to become more disciplined.

### Video Demo: TODO

<URL HERE>

---

## Description

### Why did we decided to create this?

It is no overstatement to say that all people, even in different levels, have difficulties with the creation of positive habits and discipline. Although the ambition for big dreams and having the knowledge that the persistence is one necessary key for success, it is still common the feeling of frustration at the end of the day for spending more time than it should in the socials networks and less time than necessary with books, physical exercise and other important matters.

In the studies about work execution [[Covey, S. (2015). 4 disciplines of execution. Simon & Schuster.]] it is shown that keeping a compelling scoreboard is one of the pillars of execution, keeping people more engaged, motivated and focused on their goals.

This project was born from this idea. The first version was deployed on papers and pencils, in some months became a online spreadsheet and for the final project of CS50 course we developed an application with the same principals.

### What do we want to achieve?

The main idea of this application is to be the compelling scoreboard for the daily tasks of the user.
Also, it gives a quick access of the user vision, an overview if he is heading to a positive outcome 
towards his goal or if the user is just procrastinating.

The main focus of the application are: 
- let the user define a main goal 
- let the user define the rules that are derived from the main goal 
- let the user to registry his actions, monitoring his progress

### How does the program work?

1. Create a user to get started and login in the application

    > The 'username' will be used in the login page, while the 'name' will be used only to personalize the user's home page

2. Create a Goal description

    > Another pilar of execution from the book [[Covey, S. (2015). 4 disciplines of execution. Simon & Schuster.]] is to focus on the wildly important. Therefore, you should create the goal's description which is extremely valuable and concise.

3. Create the rules based on the actions that bring you closer to and further from your main goal

    > The idea here is to understand what are the actions that you want to implement in your routine, and what are the negative habits that you want to stop. Also, you should weight the points for each one of the rules while and identify them as positive or negative action.

4. With all set now is time to add your tasks and monitor your progress

## Stack used

### Frontend 

CSS + HTML + Javascript

### Backend

Python + Flask + SQLAlchemy

### Files

#### app.py

- It is the main file of the application. Here, all the requests are handled
and the proper html page will be rendered. Also, the database will be created once
the app is started, using the `models.py` file.

#### models.py

- All models for the database are defined here. The database is composed by
the tables: `User`, `Tasks` and `Rules`. `Rules` is used to store the set of
rules in which the user will daily do to accomplish his goal. `Tasks` is used
to store the user "rules" when they do them. The `User` table stores all
relevant information for the user.

#### utils.py

- This script contains only helper functions for the app.

#### /templates

In this folder it is located all the html templates that are rendered for the user.

-   layout.html

    > It's the basic html of every page in the application, defining the DOCTYPE and head tag, leaving the block body and block script to be filled by the others templates

-   login.html

    > Login page and form for the user

-   login_failed.html

    > Handle erros in the login step

-   register.html

    > Register page and form for the user

-   register_failed.html

    > Handle erros in the register step

-   home.html

    > This template contains the scoreboard combined with the registry of actions added by the user and the options to manage goal, rules and add more tasks.

-   rule.html
    > This page contains the table with the rules added by the user and the option to add and remove the rules.

#### static

In this folder is located the cascading style sheets file and the images that are used in the site;

-   app.css
    > cascading style sheets responsible to personalize the site layout

---

# How to run

The following examples are for Linux machines. However, the commands are similar for Windows.

1. Create a python virtual environment with `venv`. Inside the folder /do-not-procrastinate:

`python3 -m venv .venv`

2. Activate the virtual environment:

`source .venv/bin/activate`

3. Install the requirements using **pip** and the **requirements.txt** file:

`pip install -r requirements.txt`

4. Run the `app.py` application with `Flask`:

`flask run`

---

# Improvements and next steps

From this application there are several ideas of improvement, more features and better user experience.
Some of them are:

- Add the possibility to show other user tasks and points for comparison and competition
- Add graphs displaying the points over time

