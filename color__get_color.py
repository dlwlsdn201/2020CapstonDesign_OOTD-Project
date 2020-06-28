import numpy as np
import cv2
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from colormap import rgb2hex
import color__crop_image as crop_image
import color__similiar_decision

'''
K평균 클러스터링 기법을 이용하여 input 이미지에서 k 수 만큼의 색상을 팔레트 형식으로 출력하고, 
가장 많이 차지하고 있는 main 색상의 RGB 값, Hexcode 값을 도출하는 모듈 코드 구현.
'''

def centroid_histogram(clt):   #각 클러스터에 할당된 픽셀의 개수를 기반으로 각 색상의 영역에 대한 백분율 출력
    # grab the number of different clusters and create a histogram
    #  based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # 히스토그램 일반화 (normalize the histogram, such that it sums to one)
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist

def plot_colors(hist, centroids):
    # 각 색깔들의 상대적 주파수를 나타내는 bar chart 초기화
    # (initialize the bar chart representing the relative frequency of each of the colors)
    #각 색상 수
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0
    max_length = 0

    # loop over the percentage of each cluster and the color of
    # 각각의 클러스터의 백분율과 색상의 루프
    for (percent, color) in zip(hist, centroids):
        # 각 군집의 상대 백분율을 플로팅
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        color_bar_length = (endX - startX)
        if max_length < abs(color_bar_length):
            max_length = color_bar_length
            main_color, hex_color = get_main_color(color)  #가장 많은 비율 차지하는 색깔 추출
            # get_main_color_value(main_color, hex_color) #타겟의 메인 컬러값(RGB,hexcode) 리턴
        startX = endX
        # print("color:",color)  #각 클러스터 색상(RGB)값 출력

    # return the bar chart
    return bar,main_color,hex_color

def get_main_color(centroid_color):       # 가장 많은 비율 차지하는 색깔 추출
    main_color = centroid_color
    R = int(main_color[0])              #RGB 값을 정수로 변환
    G = int(main_color[1])
    B = int(main_color[2])
    main_color = [R,G,B]             #정수로 변환한 RGB값
    hex_color = rgb2hex(int(R),int(G),int(B))   #rgb2hex(R,G,B) : rgb 색상 ---> hex(16진수코드) 색상으로 변환해주는 colormap 라이브러리 함수.

    return main_color, hex_color

def image_color_cluster(image_path,category, k=5):
    # image = cv2.imread(image_path)  # 이미지 로드
    image = crop_image.crop_process_img(image_path, category)   #이미지 로드(crop_image 모듈을 이용하여 화면에 상품 비율이 더 커지도록함)
    # HSV_color = decision_color(image)
    #이미지 사이즈 전처리(옷부분만 집중적으로 나올 수 있게)
    cv2.imshow("cropped_image", image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  #BGR ---> RGB 변환/(*opencv로 이미지 로드 시 BGR로 리턴이 되기 떄문)
    image = image.reshape((image.shape[0] * image.shape[1], 3)) #원활한 수치적 계산을 위해 width&height 를 하나의 array로 통합.
    clt = KMeans(n_clusters=k)  #클러스터 개수 = k로 지정
    clt.fit(image) #fit : 실제 클러스터링 수행하는 메서드.
    hist = centroid_histogram(clt)
    product_color_values = plot_colors(hist, clt.cluster_centers_)[1:]  #옷의 rgb, hex_code return 값
    bar = plot_colors(hist, clt.cluster_centers_)[0]   #컬러 파레트 bar 리턴 값
    print(f"product_color_RGB :{product_color_values[0]}, Hex_code : {product_color_values[1]}")
    plt.figure(f'Color palette of k={k}')  # 이미지 출력
    plt.axis("off")
    plt.imshow(bar)  # 색깔 팔레트 출력 plt.imshow(bar)
    plt.show()


    return bar, product_color_values

def init(image_path, category, prefer_color):   #main 함수.     init(색상을 추출할 img 경로, 카테고리 명칭, 사용자 선택 색상)
    for image in image_path:
        imageObj = mpimg.imread(f"{image}")
        plt.figure('original Image')
        plt.imshow(imageObj)
        rgb, hexcode = image_color_cluster(image, category)[1]
        similiar_decision.init(prefer_color, hexcode)




