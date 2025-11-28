# File Converter

This App convert two special file according to recip.
App creates two catalogs, Source and Target.
Put your files to Source, press the button Convert.
Script convert it and save in Target catalog.

## How to install in system

Go to desire catalog and clone repositiory, it will come with File_Converter directory.
Create and activate venv inside directory.
Install dependencies.
Run the App.

### Create venv:

Inside catalog run:

`
sudo apt update
sudo apt upgrade -y
sudo apt install python3-venv -y
`

Create and activate venv:

`
python3 -m venv venv
source venv/bin/activate
`

### Install dependencies

Inside venv run:

`
pip install -r requirements.txt
`

### Disable keyring if necesairly

`
pip uninstall keyring
echo 'export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring' >> ~/.bashrc
`

### Run the App

Inside venv run:

`
streamlit run my_project\MainApp.py\
`

it will create webserver you can reach locally or via network

### GUI

Local URL: http://localhost:8501 or simmilar Network URL: http://10.141.152.181:8501

### How to run auto-reload

Add and edit my_app.service file in RPi environment:

/etc/systemd/system/my_app.service

Content:

[Unit]
Description=My application
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/File_Converter
ExecStart=/home/pi/File_Converter/venv/bin/python MainApp.py
Restart=always

[Install]
WantedBy=multi-user.target

### Run in console:

sudo systemctl daemon-reload
sudo systemctl enable my_app
sudo systemctl start my_app

