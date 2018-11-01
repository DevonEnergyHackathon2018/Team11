# Award winning NOT a HOTDOG ripoff app for Oil and Gas Applications

Now better with Docker, Key Vault, and Azure Cointainer Services.
Prereqs:
- storage account with following blobs:
    - circles
    - photos
    - $web (enable the web portion of the blob account)
- azure key vault
- (optional) azure container registry
- (optional) azure kubernetes service

To create and run a docker container locally, fill out the secrets/env file with the correct values for the app and key vault

```bash
docker built -t drillbit .
docker run --env-file ./secrets/env drillbit
```
