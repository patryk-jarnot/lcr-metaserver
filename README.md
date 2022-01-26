# PlaToLoCo
## _Platform of tools for low complexity_

PlaToLoCo is a web server that allows you analyse low complexity regions in proteins.

Online version is available here: http://platoloco.aei.polsl.pl

## Features

- Run selected methods for low complexity regions identification
- Show protein sequence with information about its regions using feature-viewer [https://github.com/calipho-sib/feature-viewer]
- Compare the amino acids composition of the seqeunce (or its region) with commonly used databases
- Phobius, Pfam and PDB enrichment
- Download figures

## Docker

Build docker image

```
make build
```

Run the image

```
make run
```
Visit: http://localhost:8000

## Installation

### Ubuntu

The instruction below corresponds to fresh installation of Ubuntu 21.04:

Update your repository
```
sudo apt update
```

Install `npm` for a front-end server
```
sudo apt install npm
```

Install virtual environment for python 3
```
sudo apt install python3-venv
```
Create environment and activate it
```
python3 -m venv venv
source venv/bin/activate
```

Install flask dependencies
```
python3 -m pip install waitress flask flask_cors flask_restful
```
To .bashrc add (if you would like to use LCR identification program binaries for 64-bit linux):
```
export PATH="$HOME/lcr-metaserver/platolocorestapi/bin:$PATH"
```

## Configuration
Server IP configuration may be changed in the following file
```
platolocoui/app.module.js
```

Just set your server's ip address here
```js
]).constant('base_url', "http://127.0.0.1:5002");
```
## Run
To run Angular.js server, execute the following script
```
./run_angular.sh
```

To run waitress (flask) server, execute the following script
```
./run_flask.sh
```

Alternatively, you may run the server in separate screens by executing the following script
```
./start_server.sh
```



