import apriltag
import cv2
import os.path
import math



# def get_usb_camera_index():
#     # 获取USB摄像头的索引
#     camera_path = os.path.abspath('/dev/')
#     camera_list = list(camera_path.glob('video*'))
#     camera_list.sort()
#     index = 0
#     for i in range(len(camera_list)):
#         camera = camera_list[i]
#         name_file = camera.joinpath('name')
#         with open(name_file, 'r') as f:
#             info = f.readline()
#             if 'video' in info:
#                 index = i
#                 break
#     return index

frame = cv2.VideoCapture(-1)
at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11'))  # 创建一个apriltag检测器

taggle = 0
while (1) :
    ret,img = frame.read()
    img = img[100:]
    cv2.imshow("test",img)
    cv2.waitKey(1)
    # continue
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    tags = at_detector.detect(gray)  # 进行apriltag检测，得到检测到的apriltag的列表
    # print("%d apriltags have been detected."%len(tags))
    # if len(tags) == 0:
        # ser.write("4".encode("gb18030"))
    key_longest_side = [-1, -1, -1]
    print(taggle)
    if taggle == 0:
        taggle = 1 
    else:
        taggle = 0

    for tag in tags:
        x0, y0 = tuple(tag.corners[0].astype(int))
        x1, y1 = tuple(tag.corners[1].astype(int))
        x2, y2 = tuple(tag.corners[2].astype(int))
        x3, y3 = tuple(tag.corners[3].astype(int))

        d_up = math.sqrt(math.pow((x1 - x0), 2) + math.pow((y1 - y0), 2))
        d_down = math.sqrt(math.pow((x3 - x2), 2) + math.pow((y3 - y2), 2))
        d_left = math.sqrt(math.pow((x3 - x0), 2) + math.pow((y3 - y0), 2))
        d_right = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
        if (tag.tag_id) < 3 :
            if d_up >= d_down and d_up >= d_left and d_up >= d_right :  #get_longest_side
                key_longest_side[tag.tag_id] = d_up
            elif d_down >= d_up and d_down >= d_left and d_down >= d_right :
                key_longest_side[tag.tag_id] = d_down
            elif d_left >= d_up and d_left >= d_down and d_left >= d_right :
                key_longest_side[tag.tag_id] = d_left
            elif d_right >= d_up and d_right >= d_down and d_right >= d_left :
                key_longest_side[tag.tag_id] = d_right
        else :
            print("The id not in list!")

    key_index = -1 #save_longest_side_side
    if key_longest_side[0] >= key_longest_side[1] and key_longest_side[0] >= key_longest_side[2]:
        key_index = 0
    elif key_longest_side[1] >= key_longest_side[0] and key_longest_side[1] >= key_longest_side[2]:
        key_index = 1
    elif key_longest_side[2] >= key_longest_side[0] and key_longest_side[2] >= key_longest_side[1]:
        key_index = 2
    print(key_longest_side)
    # for tag in tags:
    #     if tag.tag_id == key_index:
    #         cv2.circle(img, tuple(tag.corners[0].astype(int)), 4, (255, 0, 0), 2)  # left-top
    #         cv2.circle(img, tuple(tag.corners[1].astype(int)), 4, (255, 0, 0), 2)  # right-top
    #         cv2.circle(img, tuple(tag.corners[2].astype(int)), 4, (255, 0, 0), 2)  # right-bottom
    #         cv2.circle(img, tuple(tag.corners[3].astype(int)), 4, (255, 0, 0), 2)  # left-bottom
    #         print(tag.tag_id)
    # cv2.imshow("test",img)
    # cv2.waitKey(1)