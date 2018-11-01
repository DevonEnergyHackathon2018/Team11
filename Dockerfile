FROM python:3.6
# setting up the pip environment
RUN pip install azure.storage azure.keyvault azure.common matplotlib numpy pandas opencv-python requests

# setting up the user and the logging folder
RUN groupadd -r drillbit && useradd -r -g drillbit drillbit
RUN mkdir /var/log/drillbit-logs && chown drillbit /var/log/drillbit-logs
RUN mkdir /opt/drillbit/ && chown drillbit /opt/drillbit/
RUN mkdir /opt/drillbit/cache && chown drillbit /opt/drillbit/cache

# getting gosu
RUN set -eux; \
        apt-get update; \
        apt-get install -y gosu; \
        rm -rf /var/lib/apt/lists/*; \
# verify that the binary works
        gosu drillbit true

# copying scripts over
COPY circle_predictor.py /opt/drillbit/
COPY circle_service.py /opt/drillbit/
COPY circles.py /opt/drillbit/
COPY teams_helper.py /opt/drillbit/
COPY secret_helper.py /opt/drillbit/
COPY status.json /opt/drillbit/
COPY bash/drillbit.sh /opt/drillbit/
RUN chown drillbit /opt/drillbit/status.json
RUN chmod +xxx /opt/drillbit/drillbit.sh

ENTRYPOINT ["/opt/drillbit/drillbit.sh"]

CMD [ "hotdog" ]