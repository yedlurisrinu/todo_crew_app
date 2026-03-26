"""
@Author: Srini Yedluri
@Date: 3/24/26
@Time: 3:59 PM
@File: secret_loader.py
"""
import os
import sys
import logging
from hvac import Client

logger = logging.getLogger(__name__)

def load_secrets():
    """
    Load secrets from Vault into environment variables.
    Works identically in Local, Docker, and GitHub Actions.
    Only requires:
      VAULT_ADDR  — where Vault is running
      VAULT_TOKEN — authentication token
    Both set externally per environment, never in code.
    """

    vault_address = os.getenv("VAULT_ADDR")
    vault_token = os.getenv("VAULT_TOKEN")
    secret_path = os.getenv("VAULT_SECRET_PATH","secret/AI")

    if not vault_address or not vault_token:
        logger.error(
            "VAULT_ADDR and VAULT_TOKEN must be set.\n"
            "  Local:   export VAULT_ADDR=... in your shell or set in user profile\n"
            "  Docker:  set in docker-compose.yml environment block\n"
            "  GitHub:  set in GitHub Secrets\n"
            "  These are the ONLY variables needed externally."
        )
        sys.exit(1)

    try:
        # Connect to vault
        client = Client(url=vault_address, token=vault_token)

        if not client.is_authenticated():
            logger.error("Vault authentication failed - check token information VAULT_TOKEN ")
            sys.exit(0)

        #Read all secrets from vault
        response = client.secrets.kv.v2.read_secret_version(
            path=secret_path.replace("secret", ""),
            mount_point="secret"
        )
        secrets = response['data']['data']
        # Inject into environment variables

        for key, value in secrets.items():
            os.environ[key] = str(value)

        logger.info(f" Secrets loaded from Vault: {list(secrets.keys())}")

    except Exception as e:
        logger.error(f"Exception while reading {e}", exc_info=True)
        sys.exit(1)
