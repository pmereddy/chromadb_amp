import os
import chromadb
from chromadb.config import Settings


try:
    port=str(os.environ.get('CDSW_APP_PORT', 8000))
    if os.environ.get('CHROMA_AUTH', 'false').lower() == 'true':
        user = os.environ.get('CHROMA_USER', 'admin')
        password = os.environ.get('CHROMA_PASSWORD', 'admin')
        client = chromadb.HttpClient(host="localhost", port=port, ssl=False,
            settings=Settings(chroma_client_auth_provider="chromadb.auth.basic.BasicAuthClientProvider",chroma_client_auth_credentials=f"{user}:{password}"))
    else:
        client = chromadb.HttpClient(host="localhost", port=port, ssl=False)
except Exception as e:
    print(f"Exception instantiating client: {str(e)}")
    exit(1)

# Check public endpoints
print(f"Heartbeat check: {client.heartbeat()}")
print(f"Version: {client.get_version()}")

# Check private endpoints
print(f"Collections: {client.list_collections()}")
