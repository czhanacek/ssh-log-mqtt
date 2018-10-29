FROM python:3.6
EXPOSE 80
COPY . .
RUN pip install pipenv
RUN pipenv install
CMD ["pipenv", "run", "python", "sender.py"]