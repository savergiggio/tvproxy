import asyncio
from aiohttp import ClientSession, ClientTimeout, TCPConnector
from flask import Flask, request, Response
from urllib.parse import urlparse, urljoin, quote, unquote
import re

app = Flask(__name__)

timeout = ClientTimeout(total=10)
connector = TCPConnector(limit_per_host=100)  # Più connessioni simultanee

# ClientSession globale per performance
session = ClientSession(connector=connector, timeout=timeout, headers={
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/33.0 Mobile/15E148 Safari/605.1.15",
    "Referer": "https://vavoo.to/",
    "Origin": "https://vavoo.to",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate"
})

def detect_m3u_type(content):
    if "#EXTM3U" in content and "#EXTINF" in content:
        return "m3u8"
    return "m3u"

def replace_key_uri(line, headers_query):
    match = re.search(r'URI="([^"]+)"', line)
    if match:
        key_url = match.group(1)
        proxied_key_url = f"/proxy/key?url={quote(key_url)}&{headers_query}"
        return line.replace(key_url, proxied_key_url)
    return line

async def fetch_content(url, headers=None, stream=False):
    async with session.get(url, headers=headers or {}, allow_redirects=True) as resp:
        if stream:
            while True:
                chunk = await resp.content.read(1024)
                if not chunk:
                    break
                yield chunk
        else:
            return await resp.text(), resp.url

@app.route('/proxy/m3u')
async def proxy_m3u():
    m3u_url = request.args.get('url', '').strip()
    if not m3u_url:
        return "Errore: Parametro 'url' mancante", 400

    custom_headers = {
        unquote(key[7:]).replace("_", "-"): unquote(value).strip()
        for key, value in request.args.items()
        if key.lower().startswith("header_")
    }

    try:
        m3u_content, final_url = await fetch_content(m3u_url, headers=custom_headers)

        file_type = detect_m3u_type(m3u_content)

        if file_type == "m3u":
            return Response(m3u_content, content_type="audio/x-mpegurl")

        parsed_url = urlparse(str(final_url))
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path.rsplit('/', 1)[0]}/"

        headers_query = "&".join([f"header_{quote(k)}={quote(v)}" for k, v in custom_headers.items()])

        modified_m3u8 = []
        for line in m3u_content.splitlines():
            line = line.strip()
            if line.startswith("#EXT-X-KEY") and 'URI="' in line:
                line = replace_key_uri(line, headers_query)
            elif line and not line.startswith("#"):
                segment_url = urljoin(base_url, line)
                line = f"/proxy/ts?url={quote(segment_url)}&{headers_query}"
            modified_m3u8.append(line)

        modified_m3u8_content = "\n".join(modified_m3u8)

        return Response(modified_m3u8_content, content_type="application/vnd.apple.mpegurl")

    except Exception as e:
        return f"Errore durante il download del file M3U/M3U8: {str(e)}", 500

@app.route('/proxy/ts')
async def proxy_ts():
    ts_url = request.args.get('url', '').strip()
    if not ts_url:
        return "Errore: Parametro 'url' mancante", 400

    custom_headers = {
        unquote(key[7:]).replace("_", "-"): unquote(value).strip()
        for key, value in request.args.items()
        if key.lower().startswith("header_")
    }

    async def generate():
        async for chunk in fetch_content(ts_url, headers=custom_headers, stream=True):
            yield chunk

    try:
        return Response(generate(), content_type="video/mp2t")

    except Exception as e:
        return f"Errore durante il download del segmento TS: {str(e)}", 500

@app.route('/proxy/key')
async def proxy_key():
    key_url = request.args.get('url', '').strip()
    if not key_url:
        return "Errore: Parametro 'url' mancante per la chiave", 400

    custom_headers = {
        unquote(key[7:]).replace("_", "-"): unquote(value).strip()
        for key, value in request.args.items()
        if key.lower().startswith("header_")
    }

    try:
        content, _ = await fetch_content(key_url, headers=custom_headers)
        return Response(content, content_type="application/octet-stream")

    except Exception as e:
        return f"Errore durante il download della chiave AES-128: {str(e)}", 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 7865))
    app.run(host="0.0.0.0", port=port, debug=False)
