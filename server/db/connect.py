import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client

from utils import *


@log_time
def connect_db(service_account, project_id):
    try:
        logger.info(
            f"connect firestore via service key certification - {service_account}"
        )
        # Use a service account
        cred = credentials.Certificate(service_account)
        firebase_admin.initialize_app(cred)
    except FileNotFoundError:
        logger.info(
            f"service key certification file not found. use project id - {project_id}"
        )
        # Use the application default credentials
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {"projectId": project_id, })
    finally:
        client: Client = firestore.client()
        logger.info("firestore connected")

    return client


client = connect_db(Config.SERVICE_ACCOUNT, Config.PROJECT_ID)
