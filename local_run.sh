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
deactivate