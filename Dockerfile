FROM python:3.8.8-slim



RUN python -m pip install rasa

WORKDIR /app

COPY . .

RUN rasa train nlu
RUN rasa train core 

#set the user to run, don't run as root
USER 1001

ENTRYPOINT [ "rasa" ]

CMD [ "run", "--enable-api", "--port", "8080" ]