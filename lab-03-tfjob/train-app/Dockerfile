FROM tensorflow/tensorflow:2.4.0rc0
RUN pip install tensorflow_datasets
#RUN pip install -U fire cloudml-hypertune scikit-learn==0.20.4 pandas==0.24.2
WORKDIR /app
COPY main.py .
COPY mnist.py .

ENTRYPOINT ["python", "main.py"]