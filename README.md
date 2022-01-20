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
