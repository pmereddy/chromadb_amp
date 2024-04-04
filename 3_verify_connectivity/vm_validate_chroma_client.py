import os
import chromadb
from chromadb.config import Settings

try:
    port=str(os.environ.get('CDSW_READONLY_PORT', 8100))
    if os.environ.get('CHROMA_AUTH', 'false').lower() == 'true':
        user = os.environ.get('CHROMA_USER', 'admin')
        password = os.environ.get('CHROMA_PASSWORD', 'admin')
        host=os.environ.get('CDSW_PROJECT_URL','')
        print(f"u:{user}, p:{password}, h:{host}, p:{port}")
        client = chromadb.HttpClient(host=host, port=port, 
            settings=Settings(chroma_client_auth_provider="chromadb.auth.basic.BasicAuthClientProvider",chroma_client_auth_credentials=f"{user}:{password}"))
    else:
        client = chromadb.HttpClient(host=host, port=port)
except Exception as e:
    print(f"Exception instantiating client: {str(e)}")

# Check public endpoints
print(f"Heartbeat check: {client.heartbeat()}")
print(f"Version: {client.get_version()}")

# Check private endpoints
print(f"Collections: {client.list_collections()}")
