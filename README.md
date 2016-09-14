# erudite-py

This is a python project containing scripts for web-scraping, data analysis and visualization in the **BigDataU Educational Resource Indexing** (`ERudIte`) project.

The majority of code for this system was built by [Florian Geigl](https://github.com/orgs/BMKEG/people/floriangeigl) 

Web Scraping
---
The system is run within a python script using the following method. First we write a scraper and register each scraper into the system (e.g., Coursera, EDX) and then run this on the system:

```
from scraper.field_definitions import Fields
from scraper.scraper import Scraper
from scraper.website.coursera import Coursera
from scraper.website.edx import EDX
from scraper.utils import *
import datetime

scraper = Scraper(fields_of_interest=[Fields.title, Fields.description, Fields.syllabus])
scraper.register_website(Coursera())
scraper.register_website(EDX())

urls = ['none',
        'https://www.edx.org/course/subject/computer-science']
        'https://www.coursera.org/browse/data-science']

df = scraper.scrape(urls)

df.to_csv('EDX' + format(datetime.datetime.now()) + '.tsv', sep='\t', encoding='utf-8')
```

### Coursera

This scraper goes to `https://www.coursera.org/browse/data-science?languages=en`, clicks on each Button marked 'See All', loads each one of the course pages from the resultant links and then scrapes them for details.

### EDX

This is scraper goes to `https://www.edx.org/course/subject/computer-science`, attempts to scroll down to force the loading of all the appropriate pages to load the URLS of each page. We then intend to scrape each page for details. 

> Currently, this process does not work. The dryscrape engine executes the scrolling function intermittently within the webkit-server engine and does not force a reload of more pages more than once or twice. We need a new solution to this issue. 

Docker
---
We also provide a docker image including all needed libraries to run the framework. We suggest the following procedure for using it on MacOs or any Linux distribution with the newest docker version installed (https://docs.docker.com/engine/installation/).
```
# Clone our github repositiory into erudite
git clone git@github.com:BMKEG/erudite-py.git erudite

# move into the erudite folder
cd erudite

# fix folder permissions
./init.sh

# run the docker image (first run takes some time, because it needs to download the whole image)
./start_docker.sh
``` 

Congratulations - You're now within the docker container at /tmp/erudite. This directory is your github repository mounted into docker, meaning that any changes you make (e.g., creation or modification of files) will be available after exiting docker in your local repository. You can exit the docker container by simply typing ```exit```. After this initialization you can always run the docker container by just typing ```./start_docker.sh```.

###Troubleshooting
If running start_docker.sh results in the following error 
``` Error starting userland proxy: listen tcp 0.0.0.0:8888: bind: address already in use.```
you might want to pass another local port to the start_docker.sh script ```./start_docker.sh PORT``` or directly modify and run the docker command
```docker run -i -t -v $PWD:/home/erudite/erudite -w=/home/erudite/erudite --rm -p PORT:8888 floriangeigl/erudite``` 
(see Jupyter Notebooks section for further information)

### Jupyter Notebooks
As soon as you start the image, you can access an ipython notebook server with your browser on port 8888 (if you want to change this port just pass your disired port to the ./start_docker.sh script ( ```./start_docker.sh PORT``` ) or modify the -p paramter to you're preferences (```-p PORT:8888```). Modifications of the notebooks are made in your local github repository, meaning that they are available after you shut down the docker image. If you're running docker on a server make use of port-forwarding to access the notebooks (```ssh -L 8888:127.0.0.1:8888``` where the first 8888 is your local desired port and the second refers to the port on the server - if you changed ```-p``` to another port please adjust the later 8888 in this cmd)

### I just want to run a python script
You can simply execute ```./python your_script.py your args``` to use the container's python installation.

### Installing Libraries
You can install any python libraries needed using conda or pip within the docker container. Be aware that they are gone as soon as you shut down the container. If the libraries are important for all users of erudite, please add them to our official docker image. Any changes you make to docker/Dockerfile will automatically trigger a rebuild of the image in the docker cloud. If the build succeeds (check at https://hub.docker.com/r/floriangeigl/erudite/) you can update your local docker image to the newest one (see Updating to latest docker image)

As an alternative you can remove the ```--rm``` paramter from the docker run cmd. This will prevent removing the container after exiting it. You can list all containers with ```docker ps -a```. Copy the CONTAINER ID and replace in the docker run cmd  ```floriangeigl/erudite``` with the CONTAINER ID for re-entering the container. This will keep any changes made to the image over shutdowns. 

### Updating to the latest docker image
After the inital run you can always update to the latest docker image using:
```
docker pull floriangeigl/erudite
```
This command can be exectued savely without losing any data since all your files should be in your local repository.
