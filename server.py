from flask import Flask,request
import os
import datetime
from Files import Files
import random
import pandas as pd
from dataset import Dataset


ExampleFiles=Files(root_path='sample_folder',extension='.txt')
if not os.path.exists('sample_folder'):
    os.mkdir('sample_folder')

app = Flask(__name__)


datasets={'id':Dataset}

@app.get('/')
def default():
    print('something')
    return "Welcome to the server to send command related to file management use the endpoint  /file_handler/<filename>"



@app.route('/file_handler/simple_example/<string:filename>',methods=['GET','POST','PUT','DELETE'])
def simple_example(filename):
    """it creates, edits, delete and delivery files"""

    if request.method=="GET":
        data=ExampleFiles.load_file(filename=filename)
        return data  
          
    elif request.method=="POST":
        return ExampleFiles.add_file(filename=filename)

    elif request.method=="PUT":
        return ExampleFiles.edit(filename)

    elif request.method=="DELETE":
        return ExampleFiles.remove_file(filename=filename)
    

def error():
    pass
    
def dataset_request_manager(dataset_info)-> dict:

    if dataset_info.get('schema'):
        schema=dataset_info.get('schema')
        if schema.get('columns'):
            columns=schema.get('columns')
        else:
            error()
        
        if schema.get('max_rows'):
            max_rows=schema.get('max_rows')

    if dataset_info.get('extension'):
        extension=dataset_info.get('extension')

    if dataset_info.get('datasetName'):
        dataset_name=dataset_info.get('datasetName')
    else:
        dataset_name='Unkown_'+str(random.randint(1,1000))+str(random.randint(1,1000))
    
    dtypes={item['name']:item['type'] for item in columns}
    
    return {'name':dataset_name,'columns':[column['name'] for column in columns],'dtypes':dtypes,'max_rows':max_rows,'extension':extension}


    




@app.route('/file_handler/dataset/<string:datasetId>/config',methods=['GET','POST'])
def dataset(datasetId):
    if request.is_json:
        body=request.json
        print(body)
  

    if request.method=="GET":
        
        return {'dataset_info':str(datasets[datasetId]),'dataset':datasets[datasetId].df}
    
    
    elif request.method=="POST":
        ##handling bad requests
        kwargs=dataset_request_manager(body)        
        datasets[datasetId]=Dataset(**kwargs)

        return {'created':'yes','dataset_info':str(datasets[datasetId])}




@app.route('/file_handler/dataset/<string:extension>')
def dataset_edit(extension):

    if request.method=="GET":
        pass

    elif request.method=="POST":
        pass

    elif request.method=="PUT":
        pass

    elif request.method=="DELETE":
        pass


if __name__== '__main__':
    app.run(host='0.0.0.0', port=5000)