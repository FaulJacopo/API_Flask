## MEME API FLASK

Con questo progetto è possibile gestire un API con la possibilità di generare dei MEME con immagini casuali inserendo due testi a discrezione dell'utente.
Tutti i MEME sono poi visualizzabili nella profilo dell'utente dove vi è anche la possibilità di visualizzare la propria API_KEY.

### CONFIGURAZIONE

La configurazione del progetto è molto semplice:
- Clonare il repository in una cartella.
- Entrare nel proprio environment python
- Installare tutti i pacchetti necessari
- Creare il file .env
- Impostare le variabili

#### PYTHON ENVIRONMENT

In caso non si avesse un python environment ci basterà crearlo con il comando: ``python -m venv .venv``
Successiavamente per attivarlo eseguire il comando: ``.venv\Scripts\activate``

#### INSTALLARE MODULI NECESSARI

Per scaricare tutti i moduli necessari al corretto funzionamento del nostro progetto ci basterà eseguire il comando: ``pip install -r requirements.txt``

#### FILE .ENV

Il file .env andrà creato nella root del nostro progetto "``/``".
Bisognerà popolarlo come segue:

```
SECRET_KEY="" <- Inserire una propria SECRET_KEY
SQLALCHEMY_DATABASE_URI="mysql+pymysql://utenteMYSQL:passMYSQL@ipDB/nomeDB"
@localhost/indrizzoVostraScelta"
```

Per finire il tutto eseguire il comando:

```
flask run
```