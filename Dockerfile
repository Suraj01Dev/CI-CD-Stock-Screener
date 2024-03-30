FROM python:3.9-slim 
WORKDIR /app
RUN pip install --no-cache-dir  streamlit==1.28.0
COPY stock_screener  .
ENTRYPOINT ["streamlit","run","stock_screener.py"]
