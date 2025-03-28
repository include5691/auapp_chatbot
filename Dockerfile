FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY /au_b24 /app/au_b24
COPY /e5lib /app/e5lib
COPY /e5nlp /app/e5nlp
COPY /aulib /app/aulib
COPY /au_sheets /app/au_sheets

COPY /auapp_chatbot/bot /app/bot
COPY /auapp_chatbot/models /app/models
COPY /auapp_chatbot/app.py /auapp_chatbot/_bot.py /auapp_chatbot/_redis.py /auapp_chatbot/_orm.py /auapp_chatbot/.env /auapp_chatbot/requirements.txt /app/

RUN pip install ./au_b24
RUN pip install ./e5lib
RUN pip install ./e5nlp
RUN pip install ./aulib
RUN pip install -e ./au_sheets
RUN pip install -r requirements.txt

RUN ln -fs /usr/share/zoneinfo/Asia/Yekaterinburg /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata

ENTRYPOINT ["python3", "app.py"]