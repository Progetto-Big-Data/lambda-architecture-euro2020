# Euro2020 lambda architecture

Repository contenete il secondo progetto del corso di **Big Data** dell'università **Roma Tre**
L'obiettivo è la realizzazione di una lambda architecture al supporto delle analisi di **Euro 2020**

Il progetto è ancora in lavorazione e ogni elemento potrebbe essere modificato *anche profondamente*.

## Avvio

Per avviare i vari servizi necessari alla soluzione è necessario inviare il seguente comando:

    docker-compose up -d

### [Dask](https://docs.dask.org/en/latest/)

Attualemente non è supportato correttamente l'avvio di Dask su Docker, quindi conviene aprire in locale due terminali separati, uno per lo scheduler e l'altro per il nodo worker

    dask-scheduler
    dask-worker <scheduler-address>

dove nel parametro di *dask-worker* va inserito l'indirizzo che viene emesso dallo *scheduler* durante l'avvio

Se all'indirizzo indicato nello scheduler alla porta **8787** si apre una dashboard di Dask, allora l'avvio ha avuto successo.

A questo punto si può inviare un job a dask chiamando semplicemente lo script di python ***dalla cartella root del progetto***, ad esempio:

    python batch/total_goals/main.py

### [Faust](https://faust.readthedocs.io/en/latest/)

Per avviare un task faust conviene generare un file shell costruito in questa maniera

    faust -A <app-name> worker -l info

Dove *app-name* deve essere lo stesso nome dato all'interno del codice python al job Faust, ad esempio

    app = faust.App('app-name', ...)

A questo punto si può avviare il job dalla cartella contenente il file python relativo ad *\<app-name\>*.

### MongoDB

Per entrare in MongoDB dalla shell, bisogna aggiungere l'utenza esposta nel docker-compose

    mongo -u root -p secret

Per avviare il comando è comunque necessario installare almeno la shell di mongo in locale. Per altre informazioni seguire [la documentazione ufficiale](https://docs.mongodb.com/mongodb-shell/install/#std-label-mdb-shell-install)

### MongoCharts

Durante l'utilizzo di charts, quando viene chiesto l'indirizzo dove trovare le sorgenti da cui produrre i vari grafici, si può inserire

    mongodb://root:secret@mongodb:27017

Così da connettersi allo stesso db in esecuzione nel container *mongo*. Sarebbe da investigare il motivo per cui non avviene in automatico

### Kafka Producers

I vari kafka producers sono presenti nella cartella *kafka*. Per avviarli basta dalla cartella sorgente del progetto lanciare il comando

    python kafka/<producer-name>.py

## Arresto

Per terminare l'esecuzione dei vari servizi basta fare

    docker-compose down

## Problemi noti

- Utilizzando Faust insieme con Kafka, si può incorrerre in un errore nella gestione delle partizioni.
Per questo si consiglia di far creare i topic sempre a Faust, semplicemente avviandolo prima di qualsiasi producer Kafka.
In questa maniera Faust creerà le partizioni come più preferisce, evitando di andare in crash.
Per risolvere questo problema evidentemente bisognerà sincronizzare il numero di partizioni tra Kafka e Faust. Al momento però la soluzione non sembra così triviale.
- Il codice per la gestione del preprocessing è ancora fortemente in fase di sviluppo, per ora è sparso tra le cartelle *preprocessing* e *dataset/scripts*. Futuri sforzi saranno incentrati nel sistemare questa situazione.

## Da tenere a mente

- Kafka attualmente non salva i suoi dati in nessun volume, questo significa che ad ogni riavvio ripartirà con la coda vuota. Tale comportamento è voluto visto che non si vuole far persistere i dati streaming in Kafka ma bensì in MongoDB.
- La gestione delle password è praticamente inesistente, le varie password possono facilmente essere trovate nei file all'interno della cartella *docker*
