# Script for image interpreting

# For a frame by frame brakedown of any video, we used tool: VLC. For further details please check the 
# tutorial: https://www.isimonbrown.co.uk/vlc-export-frames/

#Imports teh division module
from __future__ import division
#Imports the image manipulator
from PIL import Image
#Imports OS for iteration inside the folder
import os
#Imports numpy for matrix habdeling
import numpy as np



def folder_to_matrix(folder_name):
	'''
	Parameters
	-----------------------------
	folder_name : String
		The name of the folder where the images are. This method
		will fail when the folder contains something other than images
	-----------------------------
	Return
	image_matrix : np.matrix
		A numpy matrix, where each column corresponds to a given frame, expressed
		as as sigle long vector. Each entry corresponds to a gray scale of the pixel	
	'''
	
	matrix = None


	for file in os.listdir(folder_name):
		if file.endswith('.png'):			
			im = Image.open(folder_name + '/'+ file)
			pix = im.load()
			#Creates the column vector
			temp_vector = np.zeros((im.size[0]*im.size[1],1))
			#Iterrates over the matrix to find each pixel horizontally
			for i in range(im.size[1]): #Rows
				for j in range(im.size[0]): #Columns
					temp_vector[i*im.size[0] + j] = np.mean(pix[j,i])/255

			if matrix is None:
				matrix = temp_vector
			else:
				#Puts each image as a columns vector of the image
				matrix = np.append(matrix, temp_vector, axis = 1)

			print('File: '+ file +' loaded')
			im.close()	

	return matrix



def matrix_image_to_frames(matrix, dimensions, folder = 'output', file_name = 'temp'):
	'''
	Parameters
	-----------------------------
	matrix : numpy.matrix
		A numpy matrix where each column represents a single image. Each entry is a (0,255) value respesenting
		a gray scale value
	dimensions : (int, int)
		A 2 tuple containing the dimensions	of the output images (hight, width)
	folder : String	
		The folder name where the images will be saved
	file_name : String
		A String with the standard	file names of the output images
		
	'''

	if not os.path.exists(folder):
		os.makedirs(folder)

	#Iterates over the columns of the matrix
	for i in range(matrix.shape[1]):
		array = np.matrix(matrix[:,i])
		array = array*255		
		array.resize(dimensions)
		im = Image.fromarray(array)
		im = im.convert('RGB')
		im.save(folder + '/' + file_name + str(i) + '.png')
		im.close()

		
    