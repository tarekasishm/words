FROM python:3.10.3-slim

WORKDIR /usr/src/words

COPY ./requirements.txt /usr/src/words/ 

RUN apt update && apt install -y build-essential && \
    pip3.10 install -r requirements.txt
 
COPY src /usr/src/words/src/
 
EXPOSE 8080
 
ENTRYPOINT ["uvicorn", "src.main:app"]
 
CMD ["--host", "0.0.0.0", "--port", "8080"]