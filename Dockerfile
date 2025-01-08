FROM python:3

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY /au_b24 /app/au_b24
COPY /e5lib /app/e5lib
COPY /aulib /app/aulib

COPY /auapp_chatbot/bot.py /auapp_chatbot/_redis.py /auapp_chatbot/.env /auapp_chatbot/requirements.txt /app/

RUN pip install ./au_b24
RUN pip install ./e5lib
RUN pip install ./aulib
RUN pip install -r requirements.txt

RUN ln -fs /usr/share/zoneinfo/Asia/Yekaterinburg /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata

ENTRYPOINT ["python3", "bot.py"]