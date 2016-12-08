#Backgroung extraction of video using photoshop's scheme
#For division purpuses
from __future__ import division
#Imports Numpy for matrix manipulation
import numpy as np
#IMport scipy for mode detection
from scipy import stats
#Imports the image handler
import image_interpreter as ii
#Imports OS for iteration inside the folder
import os



def run_photoshop(input_folder, output_folder, dimensions, merge_option):
    '''
    input_folder : String	
        The folder name where the images will be imported
    output_folder : String
        The folder where the images will be saved	
    dimensions : (int, int)
        A 2 tuple containing the dimensions	of the output images (hight, width)
    '''
    
    M = ii.folder_to_matrix(input_folder)
    if(merge_option.upper() == 'MEAN'):
        print('Mean')
        mode = np.matrix(np.apply_along_axis(lambda x: np.mean(x.T), 1, M)).T
    else:    
        print('Mode')
        mode = np.matrix(np.apply_along_axis(lambda x: stats.mode(x.T)[0], 1, M))

    L = mode
    for i in range(M.shape[1]-1):
        L = np.hstack((L,mode))
    
    S = np.absolute(M - L)
    
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
    
    print('saving images...')
    ii.matrix_image_to_frames(np.absolute(M), dimensions, m_out , 'matrix_')
    ii.matrix_image_to_frames(np.absolute(L), dimensions, l_out , 'low_rank_')
    ii.matrix_image_to_frames(np.absolute(S), dimensions, s_out , 'sparse_')	
    print('ok')

#Method that runs mean or median after the images have been processed by robust PCA
def run_photoshop_after(input_folder_pca, input_folder_original, output_folder, dimensions, merge_option):

	M_1 = ii.folder_to_matrix(input_folder_pca)

	if(merge_option.upper() == 'MEAN'):
		print('Mean')
		mode = np.matrix(np.apply_along_axis(lambda x: np.mean(x.T), 1, M_1)).T
	else:    
		print('Mode')
		mode = np.matrix(np.apply_along_axis(lambda x: stats.mode(x.T)[0], 1, M_1))

	L = mode
	for i in range(M_1.shape[1]-1):
		L = np.hstack((L,mode))

	M = ii.folder_to_matrix(input_folder_original) 
	S = np.absolute(M - L)

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

	print('saving images...')
	ii.matrix_image_to_frames(np.absolute(M), dimensions, m_out , 'matrix_')
	ii.matrix_image_to_frames(np.absolute(L), dimensions, l_out , 'low_rank_')
	ii.matrix_image_to_frames(np.absolute(S), dimensions, s_out , 'sparse_')	
	print('ok')    

    
    
if __name__ == "__main__":
	
	run_photoshop_after('background','frames_all', 'frames_final', (90,160), 'Mean')    
        
    
    