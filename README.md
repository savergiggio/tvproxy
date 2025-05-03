# tvproxy

---

per adesso funziona solo su HuggingFace!

---

📜 M3U8 Proxy Dockerizzato

🚀 M3U8 Proxy è un server proxy basato su Flask e Requests che consente di:

Scaricare e modificare flussi M3U/M3U8.

Proxyare i segmenti .TS, mantenendo gli header personalizzati.

Superare restrizioni di accesso (es. Referer, User-Agent).

Dockerizzarlo per l'uso su qualsiasi macchina o server.

---

🔧 Installazione su Render

1️⃣ Andare su Projects -> Deploy a Web Service -> Piblic Git Repo

2️⃣ Metti il link github (https://github.com/nzo66/tvproxy) -> Connect

3️⃣ Mettere un nome a piacimento

4️⃣ Su "Instance Type" mettere Free -> Deploy Web Service (in basso)

---

🔧 Installazione su HuggingFace

1️⃣ Creare un nuovo Space

2️⃣ Metti un nome qualsiasi e seleziona docker

3️⃣ Lascialo Pubblico e crea il tuo Space

4️⃣ Andare in altro a destra, clicca sui tre puntini -> Files, carica qui tutti i file della repo -> FINITO

5️⃣ Adesso clicca sempre sui tre puntini -> Embed this Space, il Direct Url sarà il tuo Url da utilizzare

---

🔧 Installazione e Uso con Docker

1️⃣ Clonare il Repository

git clone https://github.com/nzo66/tvproxy.git
cd tvproxy

2️⃣ Costruire l'Immagine Docker

docker build -t tvproxy .

3️⃣ Avviare il Container

docker run -d -p 7860:7860 --name tvproxy tvproxy

4️⃣ Verificare che il Proxy sia Attivo

curl http://localhost:7860/

Dovresti ricevere una risposta tipo:

Not Found
The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.

---


📌 Gestione del Container Docker

🔹 Controllare i log del container

docker logs -f tvproxy

🔹 Fermare il container

docker stop tvproxy

🔹 Riavviare il container

docker start tvproxy

🔹 Rimuovere il container

docker rm -f tvproxy


---

📌 Deployment su un Server

Se vuoi eseguire il proxy su un server remoto (es. VPS con Ubuntu), segui questi passi:

1️⃣ Installa Docker su Ubuntu

sudo apt update && sudo apt install -y docker.io

2️⃣ Copia i file sul server

Se sei su Windows, usa WinSCP o scp:

scp -r tvproxy user@server-ip:/home/user/

3️⃣ Accedi al server e avvia il container

ssh user@server-ip
cd /home/user/tvproxy
docker build -t tvproxy .
docker run -d -p 7860:7860 --name tvproxy tvproxy

---

Ora il proxy sarà raggiungibile da qualsiasi dispositivo all’indirizzo:

(se utilizzi HuggingFace o Render non hai bisogno di mettere la Porta)

http://server-ip:7860/proxy/m3u?url=<URL_M3U8>

ricorda non proxare la lista completa ma dento la lista prima di ogni url m3u8 metti http://server-ip:7680/proxy/m3u?url=<URL_M3U8>

se hai headers diversi allora metti http://server-ip:7860/proxy/m3u?url=<URL_M3U8><HEADERS_PERSONALIZZATO>

esempio <HEADERS_PERSONALIZZATO>

&header_user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36&header_referer=https://ilovetoplay.xyz/&header_origin=https://ilovetoplay.xyz


---

🎉 Conclusione

✔ Supporta .m3u e .m3u8 automaticamente
✔ Mantiene e inoltra gli header HTTP per l'autenticazione
✔ Supera restrizioni basate su Referer, User-Agent, Origin
✔ Funziona su qualsiasi player IPTV
✔ Dockerizzato per un facile deployment

🚀 Ora puoi usare il tuo proxy per guardare flussi M3U8 senza restrizioni! 🚀




