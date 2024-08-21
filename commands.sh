ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub

mkdir -p .github/workflows && nano .github/workflows/pipeline.yml

sudo snap install docker
sudo groupadd docker
sudo usermod -aG docker $USER
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.8 python3.8-venv python3-pip python3.8-distutils zip

az webapp up --name nhanhnt1-udacity-ass2 --sku B1 -g udacity-ass2

curl -O https://vstsagentpackage.azureedge.net/agent/3.243.0/vsts-agent-linux-x64-3.243.0.tar.gz
cd agent
tar zxvf ../vsts-agent-linux-x64-3.243.0.tar.gz
./config.sh
sudo ./svc.sh install
sudo ./svc.sh start
