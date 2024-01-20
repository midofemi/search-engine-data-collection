#This Sh script is just the command we want to run on our EC2 Machine to set it up. It very similar to what we did with terraform for the deep
#Authenticator project. So copy each command and paste on your EC2 machine.
## Docker install In ubuntu 22.04  lts
sudo apt-get update
sudo apt-get upgrade -y
##########################################################################################
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce -y
sudo systemctl status docker

sudo usermod -aG docker ubuntu
newgrp docker
##########################################################################################
## Aws cli installation
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install
#####################################################################################################
## Github Runner configuration. Please Go to your github and create the below script
# Create a folder
# Create a folder
mkdir actions-runner && cd actions-runner# Download the latest runner package
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz# Optional: Validate the hash
echo "29fc8cf2dab4c195bb147384e7e2c94cfd4d4022c793b346a6175435265aa278  actions-runner-linux-x64-2.311.0.tar.gz" | shasum -a 256 -c# Extract the installer
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz
############################################################################################################
## Important
# Create the runner and start the configuration experience
./config.sh --url https://github.com/midofemi/search-engine-data-collection --token AEVRYIGD4VU5E2ZAUVR3NQDFVKPS2
./run.sh
##################################################################################################
## Add Github runner as a service. What this does is, even if your EC2 stops running. The moment it comes back up, it will reconnect with
## your github action. You wont need to recreate a new runner
sudo ./svc.sh install
sudo ./svc.sh start
sudo ./svc.sh status

## To stop the service
sudo ./svc.sh stop
sudo ./svc.sh uninstall