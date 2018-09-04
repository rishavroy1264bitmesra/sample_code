FROM 10.210.16.204:8083/document_hierarchy_identification_gi:1.0
RUN mkdir /document_hierarchy_identification
COPY . /document_hierarchy_identification
WORKDIR ./document_hierarchy_identification
RUN pip install -r requirements.txt
RUN rm -f Dockerfile
CMD ["python3", "app.py"]
EXPOSE 8885
