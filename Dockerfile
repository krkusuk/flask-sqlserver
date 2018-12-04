FROM tiangolo/uwsgi-nginx-flask:python3.6
#FROM tianon/docker-brew-ubuntu-core:bionic

COPY requirements.txt /
COPY init.sh /

WORKDIR /

RUN pip install -r ./requirements.txt --no-cache-dir

COPY baselinewebapp/ /app/

#RUN apt-get update
#RUN apt-get install python-devel
#RUN apt-get install -y unixodbc-dev
#RUN ls /etc/apt/
#RUN ./installodbc.sh
#RUN pip install pyodbc
RUN  cat /etc/*-release
#RUN lsb_release -a
RUN pwd

RUN apt-get update
RUN apt-get install gcc g++ build-essential -y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
#RUN curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list | tee /etc/apt/sources.list.d/mssql-tools.list

RUN curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install msodbcsql17 -y && \
    ACCEPT_EULA=Y apt-get install mssql-tools  -y

RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
#RUN source ~/.bashrc
#RUN sqlcmd -S 'krishansqlserver.database.windows.net' -U 'krkusuk' -P 'College@2019' -d baseline -Q 'SELECT Name,grain_in_minutes FROM algorithm'
RUN find . -name 'odbcinst.ini' && \
    echo "Hello" >>/etc/odbcinst.ini && \
    cat /etc/odbcinst.ini && \
    odbcinst -j


RUN apt-get install unixodbc-dev -y
RUN pip install pyodbc Flask-SQLAlchemy

WORKDIR /app

# Make app folder writable for the sake of db.sqlite3, and make that file also writable.
#RUN chmod g+w /app
#RUN chmod g+w /app/db.sqlite3
ENV FLASK_DEBUG=1
ENV FLASK_APP=application.py
ENV DBHOST=krishansqlserver.database.windows.net
ENV DBPASS=College@2019
ENV DBUSER=krkusuk
ENV DBNAME=baseline
#flask run -h 0.0.0.0 -p 8000
RUN python  test.py
CMD flask run -h 0.0.0.0 -p 8000
