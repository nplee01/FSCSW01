### Algorithmic Trading Backtesting App

Allows user to specify the input parameters to the Algorithmic Trading backend to discover the 
best strategies to make profits over a range of dates. 

#### Installation

Ensure you have git cli installed. Requires python >= 3.8.  
Then in a command prompt, 

    cd any_working_directory
    git clone https://github.com/nplee01/FSCSW01.git
    cd FSCSW01
    pip3 -r requirements.txt
    edit backtest.env to match your working_directory, mine is ~/work/backtest
    source backtest.env
    manage.py check
    manage.py makemigrations
    manage.py migrate
    manage.py createsuperuser
    load_fixtures.py
    manage.py runserver

Then in your Browser, http://localhost:8000/. This development version will
create a db.sqlite3 file as database. Ensure you have internet connection as we use CDN for bootstrap and jquery.

When you restart your computer, you will only need to

    cd working_directory/FSCSW01
    source backtest.env
    manage.py runserver

to restart the application.

#### Getting Started

#### License
