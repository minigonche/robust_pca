#Python scrip for the robust PCA
#For division purpuses
from __future__ import division
#Imports Numpy for matrix manipulation
import numpy as np
#Imports the image handler
import image_interpreter as ii
#Imports OS for iteration inside the folder
import os

#Defines the shinkrage operator for matrixes
def shrinkage(X, tao):
	'''
	Parameters
	-----------------------------
	X : numpy.matrix 
		The matrix to be operated on	
	tao : float
		A number for the shrinkage value	
	-----------------------------
	Return
	shrink_matrix : np.matrix
		A numpy matrix where each coordenate has been shrinked	
	'''

	#Defines the function coordinate by coordinate
	def shrink(x, tao):
		return np.sign(x)*max(np.absolute(x) - tao, 0)

	v_shrink = np.vectorize(shrink)
	return v_shrink(X,tao)	

#Defines the singular value tresholding
def singular_value_tresholding(X, tao):
	'''
	Parameters
	-----------------------------
	X : numpy.matrix 
		The matrix to be operated on	
	tao : float
		A number for the shrinkage value	
	-----------------------------
	Return
	shrink_matrix : np.matrix
		A numpy matrix where operated over the singular
		value tresholding
	'''
	U, s, V = np.linalg.svd(X, full_matrices=False)
	s = np.diag(s)
	s = shrinkage(s, tao)

	response = np.dot(U,s)
	response = np.dot(response,V) 
	return(response)


def run_PCA(input_folder, output_folder, dimensions, eps, max_ite = 3000):
	'''
	input_folder : String	
		The folder name where the images will be imported
	output_folder : String
		The folder where the images will be saved	
	dimensions : (int, int)
		A 2 tuple containing the dimensions	of the output images (hight, width)
	eps : float
		epsylon for convergence		
	'''

	M = ii.folder_to_matrix(input_folder)
	
	mu = (M.shape[0]*M.shape[1])/(4*np.linalg.norm(M,1))
	mu_1 = 1/mu

	lamb = 1/np.sqrt(M.shape[0])

	L = np.matrix(np.zeros(M.shape))
	S = np.matrix(np.zeros(M.shape))
	Y = np.matrix(np.zeros(M.shape))

	counter = 0

	partial = 1
	

	tol = eps +1

	try:
		while( tol > eps):
			
			L = singular_value_tresholding( M - S + mu_1*Y, mu_1) 		
			S = shrinkage( M - L + mu_1*Y, lamb*mu_1)				
			Y = Y + mu*(M - L - S)

			tol = np.linalg.norm(M - (L + S), 'fro')/np.linalg.norm(M,'fro')

			counter = counter + 1

			print(str(S.max()) + ' ' + str(S.min()))
			print(tol)
			print(counter)

			if(counter > max_ite):
				
				out_temp = output_folder + '_' + 'partial_' + str(partial)

				if not os.path.exists(out_temp):
					os.makedirs(out_temp)

				m_out = out_temp + '/' + 'M'
				l_out = out_temp + '/' + 'L'
				s_out = out_temp + '/' + 'S'
				#Creates the output subfolderers
				if not os.path.exists(m_out):
					os.makedirs(m_out)
					
				if not os.path.exists(l_out):
					os.makedirs(l_out)

				if not os.path.exists(s_out):
					os.makedirs(s_out)

				print('Saving Partial Images...')
				ii.matrix_image_to_frames(np.absolute(M), dimensions, m_out , 'matrix_')
				ii.matrix_image_to_frames(np.absolute(L), dimensions, l_out , 'low_rank_')
				ii.matrix_image_to_frames(np.absolute(S), dimensions, s_out , 'sparse_')	
				print('ok')
				partial = partial + 1
				counter = 0

	finally:		

	
		#Creates the output folder
		if not os.path.exists(output_folder):
			os.makedirs(output_folder)

		m_out = output_folder + '/' + 'M'
		l_out = output_folder + '/' + 'L'
		s_out = output_folder + '/' + 'S'
		#Creates the output subfolderers
		if not os.path.exists(m_out):
			os.makedirs(m_out)
			
		if not os.path.exists(l_out):
			os.makedirs(l_out)

		if not os.path.exists(s_out):
			os.makedirs(s_out)

		print('Saving images...')
		ii.matrix_image_to_frames(np.absolute(M), dimensions, m_out , 'matrix_')
		ii.matrix_image_to_frames(np.absolute(L), dimensions, l_out , 'low_rank_')
		ii.matrix_image_to_frames(np.absolute(S), dimensions, s_out , 'sparse_')	
		print('ok')

if __name__ == "__main__":
	
	run_PCA('frames_all', 'frames_out', (90,160), 1/(10**9),1000)
	
    
    

