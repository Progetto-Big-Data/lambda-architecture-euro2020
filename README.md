# Euro2020 lambda architecture

Repository contenete il secondo progetto del corso di **Big Data** dell'università **Roma Tre**
L'obiettivo è la realizzazione di una lambda architecture al supporto delle analisi di **Euro 2020**.

## Installazione
L'esecuzione corretta è garantita su sistema operativo basato su Linux

- docker engine: https://docs.docker.com/engine/install/ 
- docker-compose: https://docs.docker.com/compose/install/

Si suggerisce di creare un virtual environment usando venv o conda, per poi installare i package Python richiesti:

    pip install -r requirements.txt

## Avvio

Si premette che ognuno di questi comandi va eseguito (in ordine) in una shell diversa (a parte docker-compose che libera il terminale).

Per avviare i vari servizi necessari alla soluzione è necessario inviare il seguente comando:

    docker-compose up -d

### [Dask](https://docs.dask.org/en/latest/) (Batch Job)

Attualemente non è supportato correttamente l'avvio di Dask su Docker, quindi conviene aprire in locale due terminali separati, uno per lo scheduler e l'altro per il nodo worker

    dask-scheduler
    dask-worker <scheduler-address>

dove nel parametro di *dask-worker* va inserito l'indirizzo che viene emesso dallo *scheduler* durante l'avvio

Se all'indirizzo indicato nello scheduler alla porta **8787** si apre una dashboard di Dask, allora l'avvio ha avuto successo.

A questo punto si può inviare un job a dask chiamando semplicemente lo script di python ***dalla cartella root del progetto***, ad esempio:

    python batch/total_goals/main.py

### [Faust](https://faust.readthedocs.io/en/latest/) (Streaming Job)

Per avviare un task faust avviare lo script dalla home del progetto:

    ./streaming/statistics/start-streaming-job.sh

**Attenzione**: è necessario attendere il messaggio "Worker Ready" prima di avviare i producer Kafka

### [Kafka](https://kafka.apache.org/intro) (Data Producers)

I vari Kafka producers sono presenti nella cartella *kafka*. Per avviarli eseguire lo script dalla home del progetto:

    ./kafka/start-all-producers.sh

### [MongoDB Shell](https://docs.mongodb.com/mongodb-shell/run-commands/)

Per entrare in MongoDB dalla shell, bisogna utilizzare l'utenza esposta nel docker-compose

    mongo -u root -p secret

Per avviare il comando è comunque necessario installare almeno la shell di mongo in locale (*mongosh* al posto di *mongo*). Per altre informazioni seguire [la documentazione ufficiale](https://docs.mongodb.com/mongodb-shell/install/#std-label-mdb-shell-install).

Alcuni comandi utili per visualizzare i dati presenti:

    show dbs
    use streaming_view
    
    show collections
    db.fixture_<id>.find()

Per cancellare i dati salvati durante un'esecuzione passata si consiglia di eseguire, dopo *use streaming_view*

    db.dropDatabase()

### MongoCharts

Durante l'utilizzo di charts è necessario impostare le Data Sources senza le quali non è possibile visualizzare dati. Aprire la pagina http://localhost:8080/mongodb-charts-evgoq/data-sources ed inserire in "New Data Source" l'URL:

    mongodb://root:secret@mongodb:27017

Selezionare a questo punto il db chiamato *streaming_view*, così da connettersi allo stesso db in esecuzione nel container *mongo* dove vengono inseriti i dati provenienti dai producer Kafka. A questo punto è possibile creare dei grafici per visualizzare i dati.  

La Dashboard risulterà vuota, è ancora necessario istanziarla nuovamente per ogni nuovo utente che usa il servizio.

## Arresto

Per terminare l'esecuzione dei vari servizi basta fare

    docker-compose down

## Problemi noti

- Utilizzando Faust insieme con Kafka, si può incorrerre in un errore nella gestione delle partizioni.
Per questo si consiglia di far creare i topic sempre a Faust, semplicemente avviandolo prima di qualsiasi producer Kafka.
In questa maniera Faust creerà le partizioni come più preferisce, evitando di andare in crash.
Per risolvere questo problema evidentemente bisognerà sincronizzare il numero di partizioni tra Kafka e Faust. Al momento però la soluzione non sembra così triviale.
- Non risulta facile esportare i grafici creati in MongoCharts, ed è quindi necessario istanziarli nuovamente per ogni utente che usa il servizio.