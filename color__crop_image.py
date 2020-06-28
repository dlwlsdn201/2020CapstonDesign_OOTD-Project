import cv2

def crop_process_img(src_path, category):
    src = cv2.imread(src_path, cv2.IMREAD_COLOR)
    dst = src.copy()
    dict = {'outer':0,
            'top': 1,
            'pants':2,
            'skirt':3,
            'onepiece':4
            }


    if dict[category] <= 1 :
        dst = src[90:180, 60:160]  # 아우터, 상의 이미지를 위한 사이즈로 변경

    elif dict[category] <= 3:
        dst = src[40:140, 60:160]  # 바지, 치마 이미지를 (40~160 = 120 : 20~200 = 180) 사이즈로 변경
    else:
        dst = src[30:180, 80:140]   #원피스(전신) 이미지 옷만 나오는 적절 사이즈로 변경

    result = cv2.resize(dst, (220, 220))

    return result