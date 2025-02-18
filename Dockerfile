FROM python:3-alpine

COPY .  /src/

RUN pip install --no-cache-dir -r  /src/requirements.txt

ENV ALIYUNPAN_CONF  "/data/aliyunpan.yaml"

RUN chmod 777 /src/aliyunpan.log

WORKDIR /data/

ENTRYPOINT ["python", "/src/main.py"]
