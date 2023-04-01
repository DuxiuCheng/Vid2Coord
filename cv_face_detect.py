import time
import math
import cv2
import numpy as np
import torch

import sys
sys.path.insert(0, "models/yolov5")  # 将YoloV5模块路径添加到Path中
from models.common import DetectMultiBackend  # YoloV5网络模型
from utils.general import non_max_suppression  # 非极大值抑制函数

class FaceDetector:
	'''人脸检测器'''
	CONFIDENCE_THRESHOLD = 0.5 # 置信度阈值
	ROI_PADDING = 20 # ROI的边缘拓展像素
	FACE_SIZE_MIN = 50 # 尺寸阈值 最小
	FACE_SIZE_MAX = 400 # 尺寸阈值 最大
	def __init__(self):
		# 网络模型和预训练模型
		face_proto = "./models/face_detector/opencv_face_detector.pbtxt"
		face_model = "./models/face_detector/opencv_face_detector_uint8.pb"
		# 人脸检测的网络和模型
		# self.net = cv2.dnn.readNet(face_model, face_proto)
		# TODO: make this more flexible
		self.yolov5 = DetectMultiBackend(weights='models/weights/yolov5s6.pt', 
				   device='cpu', dnn=False, data='models/yolov5/data/coco128.yaml', fp16=False)
		self.names = self.yolov5.names
		self.resized_shape = (640, 384)  # resize due to yolov5 requirements

	def is_legal_face(self, face):
		'''判断人脸是否合法'''
		confidence = face[4]
		return confidence >= self.CONFIDENCE_THRESHOLD

	def adjust_xyxy(self, x1, y1, x2, y2, img_w, img_h):
		# 取出box框住的脸部进行检测,返回的是脸部图片
		padding = self.ROI_PADDING
		y1 = max(0, y1 - padding)
		y2 = min(y2 + padding, img_h-1)
		x1 = max(0, x1 - padding)
		x2 = min(x2 + padding, img_w - 1)
		return x1, y1, x2, y2
        
	def detect_face(self, img, confidence_threshold=None):
		'''检测人脸'''

		if confidence_threshold is None:
			confidence_threshold = self.CONFIDENCE_THRESHOLD
		# 拷贝
		canvas = img.copy()  # Why use hard copy?
		img_h, img_w, _  = canvas.shape

		# prepare im for yolov5 model
		resized_canvas = cv2.resize(canvas, self.resized_shape)
		# print(resized_canvas.shape, canvas.shape)
		im = torch.from_numpy(resized_canvas).to(self.yolov5.device)  # turn im into a tensor and moved to 'device'
		im = im.half() if self.yolov5.fp16 else im.float()  # uint8 to fp16/32
		im /= 255  # 0 - 255 to 0.0 - 1.0
		# transport im from WHC to CHW
		im = im.transpose(1, 2).transpose(0, 1)
		if len(im.shape) == 3:
			im = im[None]  # expand for batch dim
		pred = self.yolov5(im, augment=False, visualize=False)
		pred = non_max_suppression(pred,
			conf_thres=0.25, iou_thres=0.45, classes=None, agnostic=False, max_det=100)
		print("YOLOV5: Objects Number in Frame:", len(pred[0]))

		rect_list = []
		confidence_list = []

		for i, det in enumerate(pred):
			for *xyxy, conf, cls in det:
				# 忽略低于阈值的检测信息
				if conf < confidence_threshold:
					continue

				# rescale
				xyxy = [int(xyxy[0] * img_w / self.resized_shape[0]),
	    				int(xyxy[1] * img_h / self.resized_shape[1]),
						int(xyxy[2] * img_w / self.resized_shape[0]),
						int(xyxy[3] * img_h / self.resized_shape[1])]
				
				print(xyxy)
				confidence_list.append(conf)
				xywh = [xyxy[0], xyxy[1], xyxy[2] - xyxy[0], xyxy[3] - xyxy[1]]  # x1, y1, x2-x1, y2-y1
				rect_list.append(xywh)  # bounding box 的坐标
				# 绘制矩形框
				cv2.rectangle(canvas, (xyxy[:2]), (xyxy[2:]), (0, 255, 0), int(round(img_h / 150)),
							8)  # rectangle(img, pt1, pt2, color[, thickness[, lineType[, shift]]]) -> img
				cv2.putText(canvas, f'{self.names[int(cls)] if int(cls) in self.names.keys() else "Undefined"}, {conf}', 
							(xyxy[0], xyxy[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
		return rect_list, confidence_list, canvas


if __name__ == "__main__":
	from camera import Camera
	
	camera = Camera()
	capture = camera.get_video_capture()
	# 色块跟踪
	detector = FaceDetector()

	while True:
		t_start = time.time()
		ret,img_bgr = capture.read()
		if not ret:
			break
		rect_list, conf_list, canvas = detector.detect_face(img_bgr)
		
		t_end = time.time()
		t_pass = t_end - t_start
		fps = int(1/t_pass)

		# 绘制帧率
		cv2.putText(canvas, text=f"FPS:{fps}",\
			org=(20, 20), fontFace=cv2.FONT_HERSHEY_SIMPLEX, \
			fontScale=0.8, thickness=2, lineType=cv2.LINE_AA, color=(0, 0, 255))
		cv2.putText(canvas, text=f"Q:Quit",\
			org=(20, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, \
			fontScale=0.8, thickness=2, lineType=cv2.LINE_AA, color=(0, 0, 255))
		
		cv2.imshow("canvas", canvas)
		key = cv2.waitKey(1)
		if key == ord('q'):
			break
	cv2.destroyAllWindows()
	camera.capture.release()
 