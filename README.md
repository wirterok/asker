# Project setup
Run postgres with docker-compose

`docker-compose up db`

Run migrations

`alembic upgrade head`

Run main app:

`docker-compose up asker-app`

# Project usage
Your project is avalibale by link `0.0.0.0:8000`. You will see a windown with form for sending a questions

When sending new questions endpoint `api/message/ask` will be trigerred.

# Avaliable endpoints
`api/document` - `GET` - return list of uploaded documents

`api/document` - `POST` - save and create new document record in database

`api/document/{document_id}` - `GET` - retrieve document record by id

`api/document/{document_id}` - `DELETE` - delete document record both from db and filesystem

`api/message/ask` - `POST` - endpoint for asking question to system and retrieving answer based on uploaded documents

`api/message` - `GET` - retrieve list of asked questions and answers from system

More detailed api documentation is avaliable on `0.0.0.0:8000/docs`

# Selected model
For retrieving relevant information was used `Basic TF-IDF vectorization + cosine similarity` model avalible as `TfidfVectorizer` from scikit-learn library.

First of all text from updated documents are retrieved from database and combined to one text. Than text is being splitted to sentences using `nltk` python library. After that system find most similar sentence using vectorized and saves it to db as answer.