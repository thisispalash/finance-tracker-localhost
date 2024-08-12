# setup data directory for uploads
mkdir data
cd data
mkdir receipts
mkdir statements
cd ..

# download tesseract
brew install tesseract

# install tailwindcss
yarn

# install other dependencies
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

# run the app
npx tailwindcss -i ./static/css/tailwind.css -o ./static/css/base.css
python3 app.py