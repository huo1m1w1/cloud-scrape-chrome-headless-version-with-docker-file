A web scraper application collects opensea.io NFTs' ranking information and corresponding images. Save NFT information as a table in AWS RDS postgreSQL database, and send images to AWS S3

Instructions/prerequisit: 
Save your own AWS S3 access key, secret key and and RDS postgreSQL password in another file "security_keys.py" with format below:

access_key = "..."

secret_key = "..."

password = "..."

. AWS infrastructure setting: AWS RDS PostgreSQL database with name of "cloud-scraper" and S3 bucket with name of "cloud-scraper"

Create docker image use following command
 'sudo docker build .'

Run docker image by excute commend below:
' sudo docker run <image key/name>'


Note The solution relies on Google Chrome browser. 

Security See CONTRIBUTING for more information.

License This library is licensed under the MIT-0 License. See the LICENSE file.￼ ￼ ￼ ￼ ￼


￼



## Install and config prometheus and grafana
### if not required, just jup to CI/CD section

### connect to EC2
(base) h1m1w1 @ Michael:~$ ssh -i "web-scrape.pem" ubuntu@ec2-18-130-80-18.eu-west-2.compute.amazonaws.com

### upgrade packages

ubuntu@ip-172-31-29-136:~$ sudo apt update && sudo apt -y upgrade && sudo apt -y autoremove

### set as root user
ubuntu@ip-172-31-29-136:~$ sudo su -
root@ip-172-31-29-136:~# export RELEASE="2.2.1"

### install and config prometheus
root@ip-172-31-29-136:~# sudo useradd --no-create-home --shell /bin/false prometheus 
root@ip-172-31-29-136:~# sudo useradd --no-create-home --shell /bin/false node_exporter
root@ip-172-31-29-136:~# sudo mkdir /etc/prometheus
root@ip-172-31-29-136:~# sudo mkdir /var/lib/prometheus
root@ip-172-31-29-136:~# sudo chown prometheus:prometheus /etc/prometheus
root@ip-172-31-29-136:~# sudo chown prometheus:prometheus /var/lib/prometheus
root@ip-172-31-29-136:~# cd /opt/
root@ip-172-31-29-136:/opt# wget https://github.com/prometheus/prometheus/releases/download/v2.26.0/prometheus-2.26.0.linux-amd64.tar.gz


root@ip-172-31-29-136:/opt# sha256sum prometheus-2.26.0.linux-amd64.tar.gz
8dd6786c338dc62728e8891c13b62eda66c7f28a01398869f2b3712895b441b9  prometheus-2.26.0.linux-amd64.tar.gz
root@ip-172-31-29-136:/opt# tar -xvf prometheus-2.26.0.linux-amd64.tar.gz

root@ip-172-31-29-136:/opt# cd prometheus-2.26.0.linux-amd64
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# ls

root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo cp /opt/prometheus-2.26.0.linux-amd64/prometheus /usr/local/bin/
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo cp /opt/prometheus-2.26.0.linux-amd64/promtool /usr/local/bin/
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo cp -r /opt/prometheus-2.26.0.linux-amd64/consoles /etc/prometheus
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo cp -r /opt/prometheus-2.26.0.linux-amd64/console_libraries /etc/promethe
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo cp -r /opt/prometheus-2.26.0.linux-amd64/prometheus.yml /etc/prometheus
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo chown -R prometheus:prometheus /etc/prometheus/consoles
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo chown -R prometheus:prometheus /etc/prometheus/prometheus.yml

root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# cat /etc/prometheus/prometheus.yml

<!-- " # my global config
" global:
"  scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
"  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
"  # scrape_timeout is set to the global default (10s).

" # Alertmanager configuration
" alerting:
"   alertmanagers:
"  - static_configs:
    - targets:
      # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
    - targets: ['localhost:9090'] -->


root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo -u prometheus /usr/local/bin/prometheus \
>         --config.file /etc/prometheus/prometheus.yml \
>         --storage.tsdb.path /var/lib/prometheus/ \
>         --web.console.templates=/etc/prometheus/consoles \
>         --web.console.libraries=/etc/prometheus/console_libraries


root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# vi /etc/systemd/system/prometheus.service
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo systemctl daemon-reload
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo systemctl start prometheus
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo systemctl enable prometheus
Created symlink /etc/systemd/system/multi-user.target.wants/prometheus.service → /etc/systemd/system/prometheus.service.
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo systemctl status prometheus


root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo ufw allow 9090/tcp


## Install and config grafana
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo apt-get install -y software-properties-common wget
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
OK
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# echo "deb https://packages.grafana.com/enterprise/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
deb https://packages.grafana.com/enterprise/deb stable main
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo apt-get update

root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo apt-get install grafana

root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo systemctl start grafana-server
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo systemctl status grafana-server

root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo systemctl enable grafana-server.service


### Install note_explore
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz

root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo tar xvzf node_exporter-1.2.0.linux-amd64.tar.gz

root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# sudo tar xvzf node_exporter-1.3.1.linux-amd64.tar.gz

root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64# cd node_exporter-1.3.1.linux-amd64
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64/node_exporter-1.3.1.linux-amd64# sudo cp node_exporter /usr/local/bin
root@ip-172-31-29-136:/opt/prometheus-2.26.0.linux-amd64/node_exporter-1.3.1.linux-amd64# cd /lib/systemd/system
root@ip-172-31-29-136:/lib/systemd/system# sudo nano node_exporter.service
root@ip-172-31-29-136:/lib/systemd/system#  sudo systemctl daemon-reload
root@ip-172-31-29-136:/lib/systemd/system#  sudo systemctl enable node_exporter
Created symlink /etc/systemd/system/multi-user.target.wants/node_exporter.service → /lib/systemd/system/node_exporter.service.
root@ip-172-31-29-136:/lib/systemd/system#  sudo systemctl start node_exporter
root@ip-172-31-29-136:/lib/systemd/system# sudo systemctl status node_exporter

### config note_exporter
root@ip-172-31-29-136:/lib/systemd/system# cd /etc/prometheus
root@ip-172-31-29-136:/etc/prometheus# sudo nano prometheus.yml
root@ip-172-31-29-136:/etc/prometheus# sudo systemctl restart prometheus
root@ip-172-31-29-136:/etc/prometheus# cd /etc/prometheus
root@ip-172-31-29-136:/etc/prometheus# sudo nano prometheus.yml
copy following:
<!-- # my global config
global:
  scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself. -->

root@ip-172-31-29-136:/etc/prometheus# sudo systemctl restart prometheus
root@ip-172-31-29-136:/etc/prometheus# sudo nano prometheus.yml
root@ip-172-31-29-136:/etc/prometheus# sudo systemctl daemon-reload
root@ip-172-31-29-136:/etc/prometheus#  sudo systemctl enable node_exporter
root@ip-172-31-29-136:/etc/prometheus#  sudo systemctl start node_exporter
root@ip-172-31-29-136:/etc/prometheus# sudo systemctl status node_exporter

### if Note_exporter not available, cope following to /etc/systemd/system/node_exporter.service
 <!-- [Unit]
 Description=Prometheus Node Exporter
 After=network.target
 User=prometheus
 Group=prometheus

 [Service]
 Type=simple
 Restart=always
 ExecStart=/bin/sh -c '/usr/local/bin/node_exporter'

 [Install]
 WantedBy=multi-user.target -->
                           
root@ip-172-31-29-136:/etc/prometheus# sudo vim /etc/systemd/system/node_exporter.service
root@ip-172-31-29-136:/etc/prometheus# sudo systemctl daemon-reload
root@ip-172-31-29-136:/etc/prometheus# sudo systemctl status node_exporter

### Check http://18.130.80.18:3000/d/rYdddlPWkjbbnkn/linux-exporter-node?orgId=1&refresh=1m
    user:admin  password:admin


## CI/CD 


Contact
Michael Mingwang Huo - https://www.linkedin.com/in/mingwang-huo-5b7a3548/ - huomingwang@hotmail.com

Project Link: https://github.com/huo1m1w1/Cloud-scraper

Acknowledgments