#! /bin/sh

echo "=========================================================="
echo "SETUP THE LOCAL VIRTUAL ENVIRONMENT."
echo "INSTALL ALL REQUIRED PYTHON LIBRARIES"
echo "----------------------------------------------------------"
if [ -d ".venv" ];
then
    echo ".venv folder exists"
else
    echo "creating .venv"
    python3.8 -m venv .venv
fi

# Activate virtual env
. .venv/bin/activate

# Upgrade the pip
pip install --upgrade pip
pip install -r requirements.txt

deactivate