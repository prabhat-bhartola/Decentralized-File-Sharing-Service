#! /bin/sh

echo "=========================================================="
echo "This will setup the local virtual env."
echo "----------------------------------------------------------"
if [ -d ".venv" ];
then
    echo "ENABLING VIRTUAL ENVIRONMENT"
else
    echo "ERROR - NO VIRTUAL ENVIRONMENT. RUN 'local_setup.sh' FIRST"
    exit N
fi

# Activate virtual env
. .venv/bin/activate
export ENV=development
python app.py

# gunicorn -b 192.168.29.83:8080 --workers 4 --threads 10 app:app
deactivate