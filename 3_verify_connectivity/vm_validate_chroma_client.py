import os
import json
import cmlapi
import chromadb
from chromadb.config import Settings

try:
    #port=str(os.environ.get('CDSW_READONLY_PORT', 8100))
    CDSW_DOMAIN = os.environ.get("CDSW_DOMAIN",'undefined')
    CDSW_APIV2_KEY = os.environ.get("CDSW_APIV2_KEY",'undefined')
    CDSW_PROJECT_ID = os.environ.get("CDSW_PROJECT_ID",'undefined')
    WORKSPACE_DOMAIN = f"https://{CDSW_DOMAIN}"
    cml_client = cmlapi.default_client(WORKSPACE_DOMAIN, CDSW_APIV2_KEY)
    app_list = cml_client.list_applications(CDSW_PROJECT_ID, search_filter=json.dumps({"name": "ChromaDB Server"}))
    app_subdomain = app_list.applications[0].subdomain
    app_endpoint=f"https://{app_subdomain}.{CDSW_DOMAIN}"
    if os.environ.get('CHROMA_AUTH', 'false').lower() == 'true':
        user = os.environ.get('CHROMA_USER', 'admin')
        password = os.environ.get('CHROMA_PASSWORD', 'admin')
        print(f"u:{user}, p:{password}, h:{app_endpoint}, p:{port}")
        client = chromadb.HttpClient(host=app_endpoint, 
            settings=Settings(chroma_client_auth_provider="chromadb.auth.basic.BasicAuthClientProvider",chroma_client_auth_credentials=f"{user}:{password}"))
    else:
        client = chromadb.HttpClient(host=app_endpoint)
except Exception as e:
    print(f"Exception instantiating client: {str(e)}")

# Check public endpoints
print(f"Heartbeat check: {client.heartbeat()}")
print(f"Version: {client.get_version()}")

# Check private endpoints
print(f"Collections: {client.list_collections()}")

