FROM python:3.10-slim-buster

WORKDIR /usr/src/app

COPY . .
RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["streamlit_app/app.py"]
