# do-not-procrastinate

## Objective

> Create a personal scoreboard which inlfuence people to implement positive habits with consistency and to become more disciplined.

### Video Demo: TODO

<URL HERE>

---

## Description

### Why did we decided to create this?

It is no overstatement to say that all people, even in different levels, have difficulties with the creation of positive habits and discipline. Although the ambition for big dreams and having the knowledge that the persistence is one necessary key for success, it is still common the feeling of frustration at the end of the day for spending more time than it should in the socials networks and less time than necessary with books, physical exercise and other important matters.

In the studies about work execution [[Covey, S. (2015). 4 disciplines of execution. Simon & Schuster.]] it is show that keeping a compelling scoreboard is one of the pilars of execution, keeping people more engaged, motivated and focused on their goals.

This project was born from this ideia. The first version was deployed on papers and pencils, in some months became a online spreadsheet and for the final project of CS50 course we developed an application with the same principals.

### What do we want to achieve?

The main ideia of this application is to be the compelling scoreboard for your the daily tasks of the user, and with some small time give the user the vision if he is heading to a positive outcome and towards he's goal or if he is moving to a different path.

From this application there are several ideias of improvement, more features and better user experience, but for this version we focused on the main value, letting the user define a main goal, the rules that are derived from this goal and the feature to create the registry of user's actions to monitor the progress.

### How the program work?

1. Create user to get started and login in the application

    > The 'user' will be used in the login page, while the 'name' will be used only to personalize the user's home page

2. Create a Goal description

    > Another pilar of execution from the book [[Covey, S. (2015). 4 disciplines of execution. Simon & Schuster.]] is to focus on the wildly important. By this you should create a goal description that extremely valuable and concise.

3. Create the rules based on the actions that bring you closer to and further from your main goal

    > The ideia here is to understand what are the actions that you want to implement in your routine, and what are the negative habits that you want to stop. Combine with that you should weight the points for each one of the rules and identify if is a negative or a positive action.

4. With all set now is time to add your tasks and monitor your progress

## Stack used

-   Front: CSS + HTML + Javascript
-   Back: python + flask + SQL

### Files

#### app.py

-   [ ] @COXA

#### models.py

-   [ ] @COXA

#### utils.py

-   [ ] @COXA

#### templates

In this folder it is located all the html templates that are rendered for the user.

-   layout.html

    > It's the basic html of every page in the application, defining the DOCTYPE and head tag, leaving the block body and block script to be filled by the others templates

-   login.html

    > Login page and form for the user

-   login_failed.html

    > Habdle erros in the login step

-   register.html

    > Register page and form for the user

-   register_failed.html

    > Habdle erros in the register step

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
