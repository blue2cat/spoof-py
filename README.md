# Arp Spoofing for Python

This is a Dockerized python app that captures network data and pipes it into an attached Postges data container. This data is then available for analysis via the pgAdmin container. This app runs cross-platform as all logic is abstracted from the OS via Docker. 


## Installation

1. Clone the repository
```bash
git clone https://github.com/blue2cat/spoof-py.git
```

2. Install Docker if not already installed.

3. Run `docker compose up` from this directory. If you want the containers to run in the background add the `-d` flag to the command like so: `docker compose up -d`. 

## Usage
1. Navigate to [localhost:80](http://localhost:80)
