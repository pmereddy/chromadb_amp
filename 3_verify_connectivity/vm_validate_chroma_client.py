import os
import time
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
    app_id = app_list.applications[0].id
    cml_client.update_application({"bypass_authentication": True}, CDSW_PROJECT_ID, app_id)
    #cml_client.restart_application({"bypass_authentication": True}, CDSW_PROJECT_ID, app_id)
    time.sleep(30)
    app_endpoint=f"https://{app_subdomain}.{CDSW_DOMAIN}"
    if os.environ.get('CHROMA_AUTH', 'false').lower() == 'true':
        user = os.environ.get('CHROMA_USER', 'admin')
        password = os.environ.get('CHROMA_PASSWORD', 'admin')
        print(f"u:{user}, p:{password}, h:{app_endpoint}")
        client = chromadb.HttpClient(host=app_endpoint, 
            settings=Settings(chroma_client_auth_provider="chromadb.auth.basic.BasicAuthClientProvider",chroma_client_auth_credentials=f"{user}:{password}"))
    else:
        client = chromadb.HttpClient(host=app_endpoint)
except Exception as e:
    print(f"Exception instantiating client: {str(e)}")

try:
    hb = client.heartbeat()
    print(f"Heartbeat: {hb}")
    gv = client.get_version()
    print(f"Version: {gv}")
    lc = client.list_collections()
    print(f"Collections: {lc}")
except Exception as e:
    print(f"Connectivity error: {str(e)}")
