FROM python:3.7

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
#COPY test9.py /app
RUN pip install -r requirements.txt

COPY app.py /app
COPY noUI.py /app
COPY AssetList.csv /app
COPY static /app/static
COPY templates /app/templates
COPY TicketLog.csv /app

#RUN sed -i 's.'Etc/UTC'.'Europe/London'.g' /etc/timezone
#~RUN apt update
#RUN apt install firefox
CMD python app.py
