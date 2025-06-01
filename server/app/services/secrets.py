from google.cloud import secretmanager


class GoogleSecretWrapper:
    _client = None

    @classmethod
    def get_secret(cls, secret_name: str):
        if cls._client is None:
            cls._client = secretmanager.SecretManagerServiceClient()

        secret_name = f"projects/1025610681903/secrets/{secret_name}/versions/latest"
        response = cls._client.access_secret_version(request={"name": secret_name})
        return response.payload.data.decode("UTF-8")
