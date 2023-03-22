# Vid2Coord

## File Structures

### Directories

- config
- data
- icon
- models
- qss

### Files

- camera_calibration.py
- camera.py
- color_signature.py
- config.py
- cv_face_detect.py
- cv_face_track.py
- gimbal_face_track.py
- gimbal_uart_protocol.py
- gui_camera.py
- gui_select_roi.py
- gui_slider.py
- gui_slider_btn.py

## Environment Setup

```bash
    pip install -r requirements.txt
```

## Functionalities

- Receive Camera's Signal
- Target Detecting
- Coordinates Processing
- Send through Serial

## Usage


## Weekly Plan

- [ ] 分离坐标发送和目标检测两部分的代码
- [ ] 将cv2.dnn模型更换为YoloV5模型
- [ ] 性能调查
- [ ] 更好的文件结构与说明文档

