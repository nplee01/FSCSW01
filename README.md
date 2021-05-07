### Algorithmic Trading Backtesting App

Allows user to specify the input parameters to the Algorithmic Trading backend to discover the 
best strategies to make profits over a range of dates. 

#### Getting Started

Ensure you have git cli installed. Requires python >= 3.8.  
Then in a command prompt, 

    cd any_working_directory
    git clone https://github.com/nplee01/FSCSW01.git
    cd FSCSW01
    pip3 install -r devreq.txt
    copy backtest.env to .env
    ./bin/gen_secret.py, copy the secret to use in edit .env
    edit .env to match your working_directory, mine is ~/work/backtest
    ./manage.py check
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py appdata
    ./manage.py runserver

Then in your Browser, http://localhost:8000/. This development version will
create a db.sqlite3 file as database. Ensure you have internet connection as we use CDN for bootstrap and jquery.

When you restart your computer, you will only need to

    cd working_directory/FSCSW01
    ./manage.py runserver

to restart the application.

To reset the application database
    rm db.sqlite3
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py appdata
    ./manage.py runserver

#### License
