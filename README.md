# Visualizzatore dipendenze tra moduli Odoo

Il programma `collect-dep.py` consente una visualizzazione della mappa delle dipendenze tra moduli Odoo.

Odoo è un software gestionale per Aziende Open Source, scritto in Python e JavaScript. La versione community (Community Edition, CE) è gratuita, mentre la versione per Aziende (Enterprise Edition, EE) richiede un abbonamento da [Odoo SA](https://www.odoo.com/it_IT/page/editions).

Molto spesso ai moduli standard disponibili in CE e EE si aggiungono altri moduli, sia ottenuti da [OCA](https://odoo-community.org/) (un'associazione internazionale di utenti e sviluppatori Odoo), sia da altre terze parti [Apps](https://apps.odoo.com/apps/modules), sia creati localmente come personalizzazioni.

Odoo si può distribuire ed installare in vari modi, ma ci sarà sempre un processo di selezione di quali moduli rendere disponibili in una distribuzione (che sia pensata come generica o per singola installazione).

Sulla stessa installazione è possibile appoggiare instanze multiple di Odoo, ciascuna con il suo (potenzialmente diverso) sottoinsieme di moduli attivati (ovvero "installati" secondo la nomenclatura Odoo). Il sistema ovviamente verifica la presenza di tutte le dipendenze di modulo prima di attivarlo, tuttavia tale controllo viene effettuaato  dal processo di installazione stesso, in pratica si scopre la mancanza di un modulo solo quando si cerca di installarne uno che dipende da esso.

Data una collezione di moduli resi disponibili a livello di distribuzione, l'unico modo per verificare se sono tutti installabili (non mancano dipendenze) è provare ad installarli tutti: si tratta di un'operazione on-line, "a caldo", per la quale serve un'instanza attiva (database compreso).

`collect-dep.py` consente di effettuare un controllo sulle dipendenze off-line, "a freddo", senza attivare un'istanza Odoo, basandosi solo sui file presenti nella distribuzione.


## Installazione

Per il seguente paragrafo si assume un minimo di conoscenza su come viene installato Odoo.

Per l'installazione è richiesta una installazione potenzialmente funzionante di Odoo (a livello python, non serve un database). Si può semplicamente copiare il file allo stesso livello dell'eseguibile principale di Odoo `odoo-bin`, e lanciarlo nello stesso modo, con le stesse opzioni, compresa la specifica di un file di configurazione. In questo modo si garantisce che l'elenco delle directory da esaminare (`addon-dir`) sia lo stesso di Odoo. È ovviamente possibile modificare tale elenco con le stesse opzioni che si userebbero con Odoo.

### Dipendenze

Oltre ad Odoo, è richiesta l'installazione di pygraphviz e PIL. Il programma è stato sviluppato e testato in un'installazione di Odoo dotata di virtualenv dedicato, si consiglia di installare le librerie nello stesso environment. È richiesta la versione 3 di Python.

## Utilizzo

Il programma richiede solo tkInter come interfaccia grafica minimalistica, che fa parte della distribuzione standard di Python. Si limita ad aprire una finestra scrollabile, all'interno della quale viene visualizzato il grafico delle dipendenze. In rosso sono segnati gli eventuali problemi riscontrati. Non sono previste altre interazioni se non lo scroll.

Il programma è stato testato esclusivamente su Fedora Linux 34.

### Esempio

`odoo/collect-dep.py --addons-path OCA/l10n-italy,OCA/account-financial-tools,OCA/account-financial-reporting,OCA/bank-statement-import,OCA/partner-contact,OCA/reporting-engine,OCA/server-ux,OCA/web,odoo/odoo/addons`

### Copyright

Copyright (c) 2021 PHI srl

Distribuito sotto licenza AGPL-3.

Vd. file LICENSE incluso nella distribuzione.
