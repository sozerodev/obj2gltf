import os
import json
import shutil

from coordinate_transform import transform_world_to_local


def localize_world_obj(input_dir, output_dir, epsg="epsg:5186", rotation=[0,0,0]):
    """
    월드 좌표계의 obj파일을 로컬 좌표계로 변환시키는 함수
    input_dir 경로 안의 모든 월드 좌표 obj의 파일들을 읽어 로컬 모델로 변환시킨다.
    해당 함수를 거치며 작성되는 position.json은 파일의 이름을 key, 모델의 월드 중심점을 value로 하여금 작성한다.
    
    Args:
        input_dir: 좌표계 변환을 시킬 모델들이 위치한 경로
        output_dir: 로컬 좌표로 변환 모델을 저장할 경로
        epsg: 좌표계 입력
    

    """
    # TODO: 월드 좌표 모델을 로컬로 바꾸고,  
    # 로컬모델들이 있는 경로에 position.json을 작성하고 해당 경로를 allocate_obj_info의 input_dir에 넣어주기
    
    # 로컬모델이 저장될 경로 생성
    output_dir = os.path.join(output_dir, "localized_obj")
    
    try:
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
    except FileNotFoundError:
        print("output 디렉토리 생성 오류")
    
    
    center_result = {}
    file_list = {}
    for (root, directories, files) in os.walk(input_dir):
        file_list[root] = []
        for file in files:
            if file.endswith('.obj'):
                localized_path = os.path.join(output_dir, file.split('.obj')[0])

                try:
                    if not os.path.exists(localized_path):
                        os.mkdir(localized_path)
                except FileNotFoundError:
                    print("output 디렉토리 생성 오류")


                # option.json을 복사하는 과정도 필요
                # TODO: first_localized_obj에 각 파일명의 폴더를 만들고 거기에 option.json도 같이 복붙해주는 걸로(완료)
                try:
                    if os.path.exists(os.path.join(root, "option.json")):
                        try:
                            shutil.copy(os.path.join(root, "option.json"), localized_path)
                        except shutil.Error:
                            pass
                except:
                    pass


                center_point = transform_world_to_local(root, file, localized_path, epsg)

                # 
                center_result[file.split('.obj')[0]] = {
                        "position": list(center_point),
                        "roation": rotation # default
                }

                
    # position.json파일 작성
    position_path = os.path.join(output_dir, "position.json")
    with open(position_path, "w", encoding="utf-8") as make_file:
        json.dump(center_result, make_file, ensure_ascii=False, indent=4)


    return output_dir


# # test code
# if __name__ == '__main__':
#     localize_world_obj("F:/obj/hanmac/1구간_일부_테스트중", "F:/obj/hanmac/1구간_일부_테스트중/output", "epsg:5187")

