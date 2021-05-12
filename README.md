## How to setup and run:

##### Install virtualenv
- `pip3 install virtualenv`

##### Setup virtualenv
```bash
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

##### Setup django app
`make init-app`

##### Run app
`make run`

##### Run tests
`make test`

##### Run lint
`make lint`