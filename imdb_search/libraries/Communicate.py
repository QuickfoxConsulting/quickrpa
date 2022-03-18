"""
ASYNC CRYPTOGRAPHY LIBRARY FOR ROBOT
1.generates pub,priv pem keys
2.sends pub keys to server
3.receives encrypted data
4.decrypts encrypted data using priv key
"""

import base64
import json
import logging
from typing import Dict

import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from robot.libraries.BuiltIn import BuiltIn


IDENTIFIER = BuiltIn().get_variable_value("${identifier}")
# BASE_URL = "http://127.0.0.1:8000/api/v1"
BASE_URL = "http://13.58.117.7:8000/api/v1"


class CustomVault(object):
    def __init__(
        self,
        vault_name=None,
        identifier=IDENTIFIER,
        URL=None
    ) -> None:
        self.identifier = identifier
        self.vault_name = vault_name
        if URL:
            self.URL = f"{URL}/vaultdata-request/{identifier}/"
        else:
            self.URL = f"{BASE_URL}/vaultdata-request/{identifier}/"

    @staticmethod
    def robot_generate_pub_priv_keys() -> bytes:
        """GENEWRATES PEM FORMAT PUBLIC,PRIVATE KEY"""

        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )
        public_key = private_key.public_key()

        # serializing keys
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        private_key = serialization.load_pem_private_key(
            private_pem, password=None, backend=default_backend()
        )
        return public_pem, private_key

    @staticmethod
    def robot_decrypt_encrypted(private_key, encrypted_b64_decode) -> bytes:
        """decrypts b64 decoded bytes"""

        for_robot_decrypted_data = private_key.decrypt(
            encrypted_b64_decode,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return for_robot_decrypted_data

    def set_dict(self, data_list) -> Dict:
        for decrypted_data in data_list:
            data_dict = {}
            for datum in decrypted_data:
                key = datum.get("key", None)
                value = datum.get("value", None)
                data_dict[key] = value
            return data_dict

    def get_vault(self, vault_name):
        try:
            logger = logging.getLogger(__name__)
            self.vault_name = vault_name

            """RETURN RESPONSE FROM API CALL"""
            # get pem bytes
            public_pem, private_key = self.robot_generate_pub_priv_keys()

            # send request

            data_to_send = {
                "public_pem": base64.b64encode(public_pem).decode("UTF-8"),
                "vault_name": self.vault_name,
            }
            headers = {"content-type": "application/json",
                       "Accept": "application/json"}
            resp = requests.get(self.URL, json=data_to_send, headers=headers)
            if resp.status_code == 200:
                received = resp.json()
                final_dict = {}
                for datum in received.get("encrypted"):
                    data_level1 = base64.b64decode(datum)
                    decrypted_data_bytes = self.robot_decrypt_encrypted(
                        private_key, data_level1
                    )
                    data_level2 = decrypted_data_bytes.decode("UTF-8")
                    data_level3 = json.loads(data_level2)
                    key = data_level3["key"]
                    value = data_level3["value"]
                    final_dict[key] = value
                return final_dict
            else:
                logger.info(resp.text)
                raise Exception(f"Received status code of {resp.status_code}")
        except Exception as e:
            logger.info(str(e))
            raise Exception(e)


class RunItem(object):
    def __init__(self, identifier=IDENTIFIER, URL=None) -> None:
        self.identifier = identifier
        if URL:
            self.URL = f"{URL}/runitems-request/{identifier}/"
        else:
            self.URL = f"{BASE_URL}/runitems-request/{identifier}/"

    def create_run_items(self, run_items=None):
        try:
            logger = logging.getLogger(__name__)
            data = run_items

            resp = requests.post(url=self.URL, json=data)
            if resp.status_code == 200:
                return True
            else:
                logger.info(resp.text)
                raise Exception(f"Received status code of {resp.status_code}")
        except Exception as e:
            logger.info(e)
            raise Exception(str(e))
