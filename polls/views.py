# from django.shortcuts import render

# # Create your views here.
# from django.http import HttpResponse


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")



from django.template.response import TemplateResponse
from polls.models import Reading

# def home(request):
#     data = Reading.objects.last()
#     return TemplateResponse(request, 'index.html', {'data': data})

###################################
###################################

###################################
###################################

###################################
###################################

###################################
###################################



from django.shortcuts import render
from django.core.files import File
from django.http import HttpResponse
from django.db import models
import tensorflow as tf,sys
import numpy as np
import random
import requests
from PIL import Image
import glob
import os
import re
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.contrib.staticfiles.storage import staticfiles_storage




class myApp:
	temp_list=[]
	temp_lista=[]
	temp_listb=[]

	def __init__(self,catID,num1,num2,imageData):  #,x,y,z,zz,method): # request):
		self.catID=catID
		self.num1=num1				#request.POST.get('catID') 
		self.num2=num2				#request.POST.get('num1')
		self.imageData=imageData				#request.POST.get('num2')

@csrf_exempt
def index(request):
	user=myApp(request.POST.get('catID'),request.POST.get('num1'),request.POST.get('num2'),request.POST.get("imageData"))
	temp_list=[]
	temp_lista=[]
	temp_listb=[]


	
	if request.method=="POST":
		catID=int(user.catID)
		num1=int(user.num1)
		num2=int(user.num2)
		img=str(user.imageData)

		# address=os.path.abspath(os.path.curdir)
		# address=address+"/webapp/static/webapp"
		address=staticfiles_storage.url('')	

		print(img)
		fh = open("./"+address+"images/cars.jpg", "wb")
		fh.write(base64.b64decode(img))
		fh.close()
		ans=num1+num2
		image_path="./"+address+'images/cars.jpg'
		#Read in the image_data
		image_data=tf.gfile.FastGFile(image_path,'rb').read()


		if(catID==1):
			#Loads label file ,strips pff carriage return
			label_lines=[line.rstrip() for line
						in tf.gfile.GFile("./"+address+"graph_files/basic_objects_retrained_labels.txt")]
						# in tf.gfile.GFile(os.path.join(os.pardir, "basic_objects_retrained_labels.txt"))]
						# in tf.gfile.GFile("/home/moeez/tdjango/ten2/webapp/static/webapp/basic_objects_retrained_labels.txt")]
				#Unpersists grapg from file 
			# with tf.gfile.FastGFile("/home/moeez/tdjango/ten2/webapp/static/webapp/basic_objects_retrained_graph.pb",'rb') as f:
			with tf.gfile.FastGFile(("./"+address+"graph_files/basic_objects_retrained_graph.pb"),'rb') as f:
				graph_def=tf.GraphDef()
				graph_def.ParseFromString(f.read())
				_ = tf.import_graph_def(graph_def,name='')
				#######################################################
			with tf.Session() as sess:
				#Feed the image_data as input to the graph and get first prediction
				softmax_tensor=sess.graph.get_tensor_by_name('final_result:0')
			
				predictions=sess.run(softmax_tensor, \
						{'DecodeJpeg/contents:0':image_data})
			
				#Sort to show labels of first predicton in order of confidence
				top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
				
				b=0
				a=any
				for node_id in top_k:
					human_string = label_lines[node_id]
					score=predictions[0][node_id]
					#true hai ye temp_list.append("%s(score=%.5f)"%(human_string, score))
					temp_lista.append("%s"%(human_string))
					temp_listb.append("%.4f"%(score))
				######################################################################
			print(temp_lista[0],temp_listb[0],ans)
			print(address)

			return JsonResponse(temp_lista[0],safe=False)
