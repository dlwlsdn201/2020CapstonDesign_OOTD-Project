import color__get_color

category_list = ['outer', 'top', 'pants', 'skirt', 'onepiece']
color_list = ['red','pink','purple','orange','yellow','green','cyan','blue','navy','brown','white','black']


#이미지 경로 지정
image_URL = ["./images_sample/onepiece6.jpg"]

while True:   #출력받고자 하는 카테고리 입력
    print(f'아래 리스트 중에서 원하는 카테고리를 입력해주세요.')
    print("[outer/top/pants/skirt/onepiece]")
    category = input('입력 : ')
    if category in category_list :
        break
    print('옳지 않은 입력입니다. 다시 시도해주세요')
    print()

while True:
        print('아래 리스트 중에서 원하는 색상 계열을 입력해주세요.')
        print("[red/pink/purple/orange/yellow/green/cyan/blue/brown/white/gray/black]")
        prefer_color = input('입력 : ')
        if prefer_color in color_list:
            break
        print('옳지 않은 입력입니다. 다시 시도해주세요')
        print()    #출력받고자 하는 색상 입력


obj = get_color.init(image_URL, category, prefer_color)   #Total 실행 객체