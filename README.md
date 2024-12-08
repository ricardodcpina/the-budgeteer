# The Budgeteer
#### Video demo: (Coming soon)<URL HERE>

The construction of this full-stack web application was motivated by the frequent necessity of managing my own financial transactions every single month. Also, it was an opportunity for me to work with different languages and tools, like Python, Flask and other technologies. 

I believe that financial education is imperative for every individual and unfortunately is not a widespread topic among Brazilian citizens. This tool could help you get on track with your expenses/incomes and make some future planning become possible if you discipline yourself enough. You can turn some of your lifelong dreams into reality - whether it is a house, a car or even traveling around the world.

Becoming financially successful is not about earning tons of money, but knowing how to manage your finances effectively, rather than throwing it all away on useless stuff and saving nothing at all.

I hope The Budgeteer comes in handy for you like it is for me!

#### Description

Budgeteer is a personal financial management web application that allows you to take over control of your finances instead of the other way around.

##### Technologies used

- HTML
- CSS
- Python
- Flask
- SQLite
- Bootstrap
- SQLAlchemy
- Plotly

##### Project structure

- Static directory: Budgeteer's logo, background image, favicon and CSS styles
- Templates directory: HTML files for user interface
- App.py: App configuration/initialization and all endpoints
- Helpers.py: Auxiliary functions that are used in app.py.
- Models.py: Database initialization and entity models
- Layout.html: Base HTML template for other html files
- Index.html: Intro page where user can login or register an account
- Financial_log.html: Dashboard with user's expenses/incomes and relevant data
- Accounts.html: Dashboard with user's accounts
- Reports.html: Dashboard with pie chart for providing monthly reports
- Auxiliary.html: Secondary dashboards containing account balance and categories

For better understanding of each file, the source code is properly commented with relevant information.

#### Getting started

1 - Check if Python and pip are installed beforehand. If yes, you should get the version of each running the commands below in the terminal. If not, you can download them [here](https://www.python.org/downloads/).
    
For Windows:

    python --version 
    pip --version

For Mac/Linux:

    python3 --version
    pip --version

2 - Clone repository
`git clone https://github.com/ricardodcpina/budgeteer`

3 - Access project folder
`cd budgeteer`

4 - Create and activate a virtual environment

Windows:

    python -m venv .venv
    .venv\Scripts\activate
    
Mac/Linux:

    python3 -m venv .venv
    source .venv/bin/activate

5 - Install dependencies

    pip install -r requirements.txt

6 - Run the application

    flask run

7 - Access application URL: http://localhost:5000/

#### Application usage

**Welcome Page**

First, you must register an account to be able to access the basic features.

The login and register buttons are located at the top right of the screen, and clicking on them will change the form and its contents depending if you want to login or register.

Once you have successfully registered or logged in, the user will be redirected to the financial log screen.

**Offcanvas Menu**

When credentials are validated and you have access to the dashboards, you can navigate between pages by clicking the toggle menu at the top-right of the screen.

An offcanvas menu is displayed and gives you navigation links to three main pages (My profile is under construction) and the logout button.

You may want to navigate to accounts page first to create an account so you can add transactions later.

**Financial Log Page**

This will be the page where all of your registered transactions, whether incomes or expenses, will be displayed. 

Before adding any transactions, you first need to create an account to associate the transaction with.

The add entry button will open a modal with the required data to register a transaction: 

- A transaction type defining if it is an expense or an income
- An account it will be associated with
- A value in US dollars
- Some text details for tracking it later if needed
- A category it will be associated with
- The date the transaction actually occurred

After submitting, the transaction should appear in your log with all the data you provided. If you click either on the close button, the x close window icon or outside the modal, it will close.

Filtering is also provided here. You can provide a year in YYYY format and a month in the inputs and then click the 'Apply filter' button to show transactions from different dates.

**Accounts Page**

This page displays all of your registered accounts. The first step before adding a transaction is creating an account first.

When you click the 'Add account' button a modal will be displayed and you have to fill in the type of the account, the bank it is associated with and a name for identification. After submitting it the account should be displayed in the accounts dashboard.

Notice that your newly created account is also displayed in a secondary dashboard Balance, along with the total balance. Each of the accounts will be listed in the balance dashboard in all pages except the welcome page.

Now for the second step for adding a transaction, you have to add a category that will help you to group transactions and later show them on the reports page.

Click the 'Add category' button in the Categories secondary dashboard (provided in all pages except the welcome page) and choose a name for your category. Once created, it will be displayed in the Categories dashboard.

Now you have all the requirements to add a transaction in the Financial Log page.

**Reports Page**

Reports are generated based on the transactions you registered. The pie chart will be displayed according to the current month and year, but you can change the date and filter by transaction type if needed. 

The chart is divided by categories and shows a percentage of the total spent/received in that month. You can opt in or out of any category clicking on each of them at the chart's legend. The chart shows tooltips on mouse hover.

#### This is CS50!

This should cover all the functionalities provided by Budgeteer at the present moment! I hope this application can help you improve your financial management, mitigating unnecessary costs and keeping track of where you spend the most. 