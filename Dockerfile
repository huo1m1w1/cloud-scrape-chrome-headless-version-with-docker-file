# build python environment
FROM python:3.9-buster

# Adding trusting keys to apt for repositories,
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# get Google Chrome
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# update apt-get
RUN apt-get -y update

# install google-chrome-stable
RUN apt-get install -y google-chrome-stable

# get chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

# get unzip package
RUN apt-get install -yqq unzip

# unzip chromedriver
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# copy requiremnts/packages needed, and get installed
COPY requirements.txt requirements.txt 
RUN pip install -r ./requirements.txt 

# copy all files
COPY . . 

# run the application
CMD [ "python", "main.py" ]
