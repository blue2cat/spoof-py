# What is Spoofpy? 
Spoofpy is a containerized application that uses arp spoofing to collect network traffic from other devices on the same Wifi network. The application captures and stores data in a Postgres database. 

# Network-wide Arp Spoofing

This is a Dockerized Python app that captures network data and pipes it into an attached Postges data container. This data is then available for analysis via the pgAdmin container. This app runs cross-platform as all logic is abstracted from the OS via Docker. 


## Installation

1. Clone the repository
```bash
git clone https://github.com/blue2cat/spoof-py.git
```

2. Open the `.env` file and add a secure pgAdmin and PostgreSQL password.  
3. Install Docker if not already installed.
4. Run `docker compose up` from this directory. If you want the containers to run in the background add the `-d` flag to the command like so: `docker compose up -d`. 

## Usage
1. Navigate to [localhost:80](http://localhost:80) to view the pgAdmin interface. 
