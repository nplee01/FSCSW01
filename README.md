### Algorithmic Trading Backtesting App

Allows user to specify the input parameters to the Algorithmic Trading backend to discover the 
best strategies to make profits over a range of dates. 

#### Getting Started

Ensure you have git cli installed. Requires python >= 3.8.  
Then in a command prompt, 

    sudo apt install python3.8-venv
    cd any_working_directory
    python -m venv env_name
    source env_name/bin/activate
    git clone https://github.com/nplee01/FSCSW01.git
    cd FSCSW01
    install the Technical Analysis c library
        On Mac, on the command line, "brew install ta-lib"
        On Windows, download [ta-lib-0.4.0-msvc.zip](https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-msvc.zip) and extract to C:\ta-lib
        On Linux, download [ta-lib-0.4.0-src.tar.gz](https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz) and extract to a working directory.
            then cd to the working_directory and "./configure --prefix=/usr; make; sudo make install"
    pip install -r devreq.txt
    ./bin/gen_env.py backtest.env
    ./manage.py check
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py appdata
    ./manage.py stockdata
    ./manage.py runserver

Then in your Browser, http://localhost:8000/. This development version will
create a db.sqlite3 file as database. Ensure you have internet connection as we use CDN for bootstrap and jquery.
gen_env.py will generate a new .env file with secrets replaced in the same directory as the input file.

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

#### Deploying to production on bare metal

The default configuration will use gunicorn to serve django with a nginx front end 
that will proxy all requests to gunicorn, besides serving static files.

Please ensure you have installed the following on the server

    postgresql  # version 13
    python      # version 3.8
    nginx       # version 1.20
    you have cloned the repository to your working directory

Perform the following in your working directory

    ./manage.py collectstatic   # to copy all static files to prod/
    pip install -r prodreq.txt  # install gunicorn and postgresql db driver
    python bin/gen_env.py prod.env     # will override .env
    # Ensure postgresql up and running
    # use pgadmin4 to create user thecube and database thecube to be owned by thecube
    # Please use the password CUBE_DB_PASSWORD in .env
    # Please make sure thecube db user has login permission
    # Steps below will create the tables and load the fixtures data
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py appdata
    # Please link with absolute path
    edit config/gunicorn.service to change working directory to match yours
    ln -s ~/work/backtest/config/gunicorn.socket /etc/systemd/system
    ln -s ~/work/backtest/config/gunicorn.service /etc/systemd/system
    sudo systemctl enable gunicorn.socket
    sudo systemctl start gunicorn.socket
    # Now gunicorn will be listening on unix socket at /run/gunicorn.socket
    edit config/thecube.conf to change working directory
    ln -s ~/work/backtest/config/thecube.conf /etc/nginx/sites-enabled
    sudo systemctl restart nginx    # assumes nginx installed and running

Then access the system at http://localhost:8081 (or another port if you edited thecube.conf)

The above configuration will ensure that thecube app will auto restarted on system startup.

If you are running postgresql on another host, please edit .env CUBE_DB_HOST.

#### Deploying to production using docker-compose

Please ensure you have installed on your server

    docker
    docker-compose

Then from your working directory

    bin/gen_env.py prod.env # One time process
    docker-compose build    # One time process
    docker-compose up       # The next time, only this command is necessary

To shutdown
    ctrl-c  # to kill the containers
    docker-compose down

Then http://localhost:8080 to access the app.

docker-compose.yml defines 3 containers: 1) postgresql 2) django+gunicorn 3) nginx
It will read docker/ for the Dockerfile during the build. 

All data in the db will be lost on shutdown. Please read postgres docker image docs for information on using volumes
for PGDATA.

#### License
