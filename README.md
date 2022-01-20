# COAMiner Anleitung
Vor der Verwendung der folgenden Anleitung muss erwähnt werden, dass alle Tests auf einer Ubuntu 20.04 LTS Distribution ausgeführt wurden. Eine Garantie für die Ausführung des Codes auf anderen Distributionen kann nicht gegeben werden. Zudem wurde für die Entwicklung der Anwendung die Python-Version 3.7.12 verwendet. Es fand kein Test mit einer anderen Python-Version statt.

## Herunterladen und Installation
Für das Herunterladen des Quellcodes und die Installation der Requirements bitte die
folgenden Befehle ausführen.

```shell
# Repository downloaden
git clone https://github.com/jmscoding/COAMiner.git
cd COAMiner

# Virtuelle Python Umgebung kreiieren
python −m venv venv

# Installiere Requirements
pip install -r requirements.txt
```
Zusätzlich muss für die Datenanbindung eine lokale MongoDB-Datenbank auf dem Rechner unter dem Port 27015 zur Laufzeit des Programms aktiv sein.

```shell
# Installiere mongodb Datenbank unter Ubuntu
wget −qO − https://www. mongodb.org/static/pgp/server-5.0.asc | sudo apt −key add −
echo " deb [ arch=amd64, arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb−org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb−org−5.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# Starte mongodb
sudo systemctl start mongod
sudo systemctl enable mongod

# Wichtige Datenbanken hinzufügen
mongorestore Database/knowledgebase/
mongorestore Database/testdb/
mongorestore Database/coaminer/
```

Die Anwendung umfasst einige Teilfunktionen, die jeweils alle einzeln getestet werden können. Voraussetzung für die Ausführung ist die Installation, der im vorherigen Abschnitt beschriebenen Komponenten. Produktive Tests der Gesamtanwendung waren nur auf einerphysischen Maschine erfolgreich. Einzelne Funktionen können auch in einer virtuellen Maschine erfolgreich ausgeführt werden. Als erste Funktion kann der Scraper ausgeführt werden. Da die verwendete Library Selenium sehr viele Hardwareressourcen benögigt, kann es in einer virtuellen Umgebung zum Absturz kommen.

```Python
# Teste den Scraper
python scraper.py
```

Des Weiteren kann der Classificator ausgeführt werden. Hierbei wird ein Testdatensatz verwendet, der im Repository unter src/test_ds.json zu finden ist. Nach der Klassifikation wird über die Kommandozeile eine Liste an Tupeln ausgegeben, die jeweils an der ersten Stelle, das Ergebnis der Funktion anzeigt und an der zweiten Stelle das Label des Datensatzes präsentiert.

```Python
# Teste den Classificator
python classificator.py
```

Außerdem existiert eine Testfunktion des Extractor-Moduls. Hierbei wird der gleiche Datensatz wie beim Classificator-Modul verwendet. Nach Beendigung der Funktion wird im Ordner res ein JSON-Dokument mit den Informationen der extrahierten Course of Action hinterlegt.

```Python
# Teste den Extractor
python extractor.py
```

Um einen Test der Gesamtanwendung zu initialisieren, muss der folgende Befehl ausgeführt werden. Hierbei muss beachtet werden, dass für den Test das Argument **test** an den Befehl angehängt werden muss.

```Python
# Starte Test der kompletten Anwendung
python main.py test
```
