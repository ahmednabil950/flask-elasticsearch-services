echo "Creating Virtual Environment"
virtualenv .env

echo "Activating deveopment environment"
source bin ./.env/bin/source/activate

echo "Virtual environment activated"
echo "Installing dependencies"

sudo pip install -r requirements.txt

echo "Running Flask Server"
python app.py

echo "Running ElasticSearch Server"
./elasticsearch/elasticsearch/bin/elasticsearch

echo "Running Test sample for analyzing and indexing"
python main.py
