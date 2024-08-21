# Building CI/CD pipeline using github actions and azure devops to automatically deploy app to Azure AppService on commit pushed

## Project Plan

* Kanban dashboard: https://trello.com/b/SFadin4X/udacityazuredevopsproj2
* Project plan: https://docs.google.com/spreadsheets/d/1GPBI43P1IToysQQdEsCm09JOk34per7o/edit?usp=sharing&ouid=114898603581194088124&rtpof=true&sd=true

## Instructions
* An GitHub account: https://github.com
* An Azure account with a active subscription: https://portal.azure.com/

## Part 1: CI Pipeline with GitHub Actions

### Architecture diagram
* Architectural Diagram (Shows how key parts of the system work)>

### Instruction steps
* Visit Azure portal page with your Azure account and open Azure Cloud Shell

* Setup SSH key that used to pull/push code from your github repo
```sh
ssh-keygen
cat ~/.ssh/id_rsa.pub
```

![alt text](https://github.com/nhan4599a/nhanhnt1-udacity-ass3/blob/main/images/github_actions_diagram.jpg)

* This is project files meaning
| File name | Meaning |
| ------ | ------ |
| Makefile | Shortcuts to build, test, and deploy a project|
| requirements.txt| File that listed out all python dependencies that the app needed |
| hello.py | Basic python app |
| test_hello.py | Unittest for hello.py file|

* Create a python virtual environment and activate it so that App is not affected by global python version and installed python dependencies

```sh
python3.8 -m venv ~/.venv
source ~/.venv/bin/activate
```

* Run `make all` command manually to verify that the provided code is passed unit test and linting correctly
```sh
make all
```

* Add GitHub Actions to repository:
Just create a yml file with any name at the path: `.github/workflows/your_file_name.yml`
Here is sample file for you

```
name: Python application test with Github Actions

on: 
  push:
    branches:
      - '*'

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.8
      uses: actions/setup-python@v1
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        make install
    - name: Lint with pylint
      run: |
        make lint
    - name: Test with pytest
      run: |
        make test
```
and now, visit your actions page of your repo, you will see running pipeline here
![alt text](https://github.com/nhan4599a/nhanhnt1-udacity-ass3/blob/main/images/ci.png)
## Part 2: CD using Azure DevOps
### Architecture diagram
* Architecture Diagram
![alt text](https://github.com/nhan4599a/nhanhnt1-udacity-ass3/blob/main/images/azure_devops_pipeline_diagram.jpg)
### Instruction steps
* Go to Azure Devops page (https://dev.azure.com/)  and sign in it, create a new Project inside your organization

* In your new Project in Azure DevOps, go to Project Settings and create a new `Project settings --> Service Connection`
> Note 1: Service Connection must be created with type `Azure Resource Manager`
> Note 2: Use a link of as this `https://dev.azure.com/<your organization>/<your project>/_apis/serviceendpoint/endpoints?api-version=5.0-preview.2`

* Checkout branch azure_pipeline

```sh
git checkout azure_pipeline
```

* This is project files meaning
| File name | Meaning |
| ------ | ------ |
| app.py | Sample flask application that expose an home page and an endpoint to predict Boston's house price|
| requirements.txt| File that listed out all python dependencies that the app needed |
| *.joblib| File that contains prediction algorithm that can be used in app.py (currently, only `LinearRegression.joblib` is in used) |

* Create the webapp deploying the code from the local workspace to Azure app Service ( using Plan B1)

```sh
az webapp up -n <name of webapp> -g <name of resource_group> --sku B1 --runtime PYTHON:3.8
```
![deployed webapp](https://github.com/nhan4599a/nhanhnt1-udacity-ass3/blob/main/images/app.png)

> Note 1: `<name of webapp>` should be unique or the command will run into an error
> Note 2: This will took a while for Azure to create and deploy your app
> Note 3: Your deployed app should be visitable at url: `https://<name of webapp>.azurewebsites.net/`

* Create Azure VM and config that as Azure DevOps Agent
- Create a linux Azure VM
- Config VM as Azure DevOps Agent
+ Install docker
```sh
sudo snap install docker
```
+ Add user to docker user's group
```sh
sudo groupadd docker
sudo usermod -aG docker $USER
```
+ Restart the VM to ensure that above changes took affected
+ Install python 3.8 and zip package
```sh
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.8 python3.8-venv python3-pip python3.8-distutils zip
```
> Note: Command above will be varied based on what is runned by your pipeline, this is just an example

+ Generate an Azure DevOps access token (PAT)
1. Visit `https://dev.azure.com/<your organization>/_usersSettings/tokens`
2. Click `New token`
3. Choose `Full access` on Scopes
4. Click `Create`
5. Copy provided PAT and store it in a safe place because you cannot see it again

+ Create an Agent Pool: Agent Pool is a logical group that contains your Agents since Agent is a machine that will run your pipeline
1. Viset `https://dev.azure.com/<your organization>/<your project>/_settings/agentqueues`
2. Click `Add pool`
3. Choose `Self-hosted` on `Pool type`
4. Choose `Grant access permission to all pipelines`
5. Click `Create`

+ Install Azure DevOps Agent into VM
1. Down Agent files
```sh
curl -O https://vstsagentpackage.azureedge.net/agent/3.243.0/vsts-agent-linux-x64-3.243.0.tar.gz
mkdir myagent && cd myagent
tar zxvf ../vsts-agent-linux-x64-3.243.0.tar.gz
```
2. Config Agent
```sh
./config.sh
```
> Note 1: When asked Server URL, enter `https://dev.azure.com/<your organization>`
> Note 2: When asked agent pool, enter the name of agent pool which you created in above step
3. Run Agent as a linux service
```sh
sudo ./runsvc.sh install
sudo ./runsvc.sh start
```

* Create CD pipeline
- Enter https://dev.azure.com/<your organization>/<your project>/_build
- Click `New pipeline`
- Click `GitHub`
- Choose your repository that contains azure pipeline.yml file
- Choose `Existing Azure Pipelines YAML file`
- Choose `azure_pipeline` branch (because my azure pipeline yml file located in this branch)
- Choose `azure-pipeline.yml` (because my azure pipeline yml file is named `azure-pipeline.yml`)
- Click `Continue`
![alt text](https://github.com/nhan4599a/nhanhnt1-udacity-ass3/blob/main/images/create_pipeline.png)

* It's time to see result since a build/deploy should be trigger automatically after above steps

* Try to edit app.py and push it to branch `azure_pipeline`, and you will see your pipeline is automatic triggered again

* Check AppService log
```sh
az webapp log tail
```

![alt text](https://github.com/nhan4599a/nhanhnt1-udacity-ass3/blob/main/images/log.png)

## Enhancements
* Write more test cases
* Add performance testing to deployed application and modify CI pipeline to run it automatically on code pushed
## Demo 
https://drive.google.com/file/d/13hX61H0c2yxlwVmt4y_bdHUBuUhFYEve/view?usp=sharing
