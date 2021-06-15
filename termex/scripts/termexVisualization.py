#!/usr/bin/env python
import rospy
import numpy as np
import cv2 as cv
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Int8MultiArray



class VisualizationVectors:
	def __init__(self):
		self.raw_image = None
		self.vector_matrix = None
		self.treshold = 10
		self.scale = 5
		
		# get current image rescale and display vector on it 
		# TODO get image with the smame time stemp 
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/lepton_output", Image, self.callbackImage)
		
		self.vector_sub = rospy.Subscriber("/relocation_array", Int8MultiArray, self.callbackVector)
		
		self.image_pub = rospy.Publisher("/image_vector", Image, queue_size=10)
		
	def callbackImage(self, data):
		try:
			self.raw_image = self.bridge.imgmsg_to_cv2(data,"mono16")
		except CvBridgeError as e:
			print(e)
		
		
	def callbackVector(self, data):
		# when vector message come
		self.vector_matrix = data
		self.prepareVisualization()
		
		
	def prepareVisualization(self):
		#its only for help
	    recal_image = self.recalculate(self.raw_image)
	    resized_image = self.rescale_image(recal_image, self.scale)
	    resized_image = cv.cvtColor(resized_image, cv.COLOR_GRAY2BGR)
	    colored_image = cv.applyColorMap(resized_image, cv.COLORMAP_MAGMA)
	    
	    arrowed_image = self.add_arrows(colored_image, self.scale)
        
	    aaa = self.bridge.cv2_to_imgmsg(arrowed_image,"bgr8")
	    aaa.header.stamp = rospy.Time.now()
	    self.image_pub.publish(aaa)
		
	def recalculate(self, data):
		"""
		:param data: numpy array
		:return:Array with values from 0-255 (8bits)
		"""
		minimum = np.min(data)
		maximum = np.max(data)
		difference = maximum - minimum

		data = (((data - minimum) / difference) * 255).astype('uint8')

		return data
		
		
	def rescale_image(self, image, scale):
		height, width = image.shape[:2]
		resize_image = cv.resize(image,(scale * width, scale * height),interpolation=cv.INTER_CUBIC)
		return resize_image
		
	
	def add_arrows(self, image, scale):
		size_array = self.vector_matrix.layout.dim[0].size
		n = self.vector_matrix.layout.dim[1].size;
		b_size = self.vector_matrix.layout.dim[1].stride//2

		for i in range(size_array):
		    corr = self.vector_matrix.data[i*n+4]
		    if corr < self.treshold: 
		        break
		    
		    
		    start_point = ((self.vector_matrix.data[i*n+1] + b_size)*scale, (self.vector_matrix.data[i*n] + b_size)*scale)
		    end_point = ((self.vector_matrix.data[i*n+3] + b_size)*scale, (self.vector_matrix.data[i*n+2] + b_size)*scale)
		    
		    
		    cv.arrowedLine(image, start_point, end_point, (0,4*corr,0), 2)
		return image
		
		
def main():
    vis = VisualizationVectors()
    rospy.init_node("Visualization", anonymous=True)
    rospy.spin()


if __name__ == '__main__':
    main()

