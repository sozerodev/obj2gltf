from audioop import reverse
from pyproj import Transformer
import shutil

# import geopy.distance
from geopy.distance import geodesic
import os

import sys
import multiprocessing
import time


ORIG_SYS_PATH = list(sys.path)


def create_jpg(inputDir, outputDir, fileName):
    """
    텍스쳐파일인 jpg를 복사하는 함수

    inputDir : 복사해야할 jpg가 있는 경로
    outputDir : 복사한 jpg를 붙여넣을 경로
    fileName : 해당 jpg의 이름
    """
    try:
        shutil.copy(os.path.join(inputDir, fileName), outputDir)
    except FileNotFoundError:
        print(fileName + " 복사 오류")
        pass

    return outputDir


def get_center_point(v_list):
    """
    wgs로 변환된 리스트를 받아 center point를 구하는 함수
    """
    min_coordinate = [None, None, None]
    max_coordinate = [None, None, None]

    # for line in v_list:
    for i in range(len(v_list)):
        line = v_list[i]
        if line.startswith("v "):
            split_line = line.split(" ")
            x = float(split_line[1])
            y = float(split_line[2])
            z = float(split_line[3])

            # if x > 200 or y > 200:
            #     print(x)
            #     print(y)

            if min_coordinate[0] is None:
                min_coordinate[0] = x
            if min_coordinate[1] is None:
                min_coordinate[1] = y
            if min_coordinate[2] is None:
                min_coordinate[2] = z


            if max_coordinate[0] is None:
                max_coordinate[0] = x
            if max_coordinate[1] is None:
                max_coordinate[1] = y

            if max_coordinate[2] is None:
                max_coordinate[2] = z

            if min_coordinate[0] > x:
                min_coordinate[0] = x
            if min_coordinate[1] > y:
                min_coordinate[1] = y
            if min_coordinate[2] > z:
                min_coordinate[2] = z

            if max_coordinate[0] < x:
                max_coordinate[0] = x
            if max_coordinate[1] < y:
                max_coordinate[1] = y
            if max_coordinate[2] < z:
                max_coordinate[2] = z

    # 4326 월드 중심점
    center = (
        (min_coordinate[0] + max_coordinate[0]) / 2,
        (min_coordinate[1] + max_coordinate[1]) / 2,
        (min_coordinate[2] + max_coordinate[2]) / 2,

    )
    return center


def convert_to_local_with_pool(center_point, wgs_list):
# def convert_to_local_old(center_point, wgs_list):
    """
    center point와 wgs로 변환된 좌표 리스트를 통해
    로컬 좌표계로 변환하는 함수
    """
    # 축별 최대 최소값
    box = {"min": [None, None, None], "max": [None, None, None]}
    length = {
        "x": None,
        "y": None
        # "z" : None
    }

    reverse_center = (center_point[1], center_point[0])

    args = ((line, center_point, reverse_center) for line in wgs_list)
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    pool_result = p.map_async(compute_distance, args)
    
    p.close()
    p.join()
    # print(pool_result)






    return {
        "local": pool_result.get()
    }


def compute_distance(args):
    """
    
    """
    line, center_point, reverse_center = args
    destination_x = (center_point[1], float(line.split(" ")[1]))
    destination_y = (float(line.split(" ")[2]), center_point[0])

    distance_x = None
    distance_y = None
    # distance_z = line.split(" ")[3]  # 줄바꿈돼야하니까 strip()하지 않는다.

    # 높이까지 원점으로 당기기
    distance_z = float(line.split(" ")[3].strip()) - center_point[2]

    # geopy를 사용해서 distance 구하기 
    # geodesic이 시간이 많이 걸린다...
    if center_point[0] > float(line.split(" ")[1]):
        distance_x = float((geodesic(reverse_center, destination_x).meters) * (-1))
    else:
        distance_x = float(geodesic(reverse_center, destination_x).meters)

    if center_point[1] > float(line.split(" ")[2]):
        distance_y = float((geodesic(reverse_center, destination_y).meters) * (-1))
    else:
        distance_y = float(geodesic(reverse_center, destination_y).meters)


    return (f"v {distance_x} {distance_y} {distance_z}\n")


def transform_world_to_local(
    dir_name, file_name, output_dir, epsg="epsg:5186"
):
    """
    world좌표계를 local좌표계로 변환하는 파일단위 함수
    타일 볼륨, 월드 중심점
    해당 함수가 사용되는 중임
    """
    # start_time = timeit.default_timer()

    # print("로컬좌표계로 변환 시작..")
    # 인풋 경로 넣지 않았을 때 오류
    try:
        if dir_name is None:
            raise ValueError
    except ValueError:
        print(dir_name + " 의 파일 경로 없음")

    obj_path = os.path.join(dir_name, file_name)

    wgs_v_list = []
    reading_obj = []

    transformer = Transformer.from_crs(epsg, "epsg:4326")

    # 병렬처리 필요
    with open(obj_path, "r", encoding="utf-8") as original_obj:
        reading_obj = original_obj.readlines()
        for line in reading_obj:
            if line.startswith("v "):
                # v 뒤에 공백이 두개인 경우가 있어서
                # split(" ")시 빈 데이터는 삭제한다.
                line_list = list(filter(None, line.split(" ")))
                x_coordinate = line_list[1]
                y_coordinate = line_list[2]
                z_coordinate = line_list[3]  # 줄바꿈해야하니까 strip()하지 않는다.
                # x y 순서가 아님 위경도 순으로 입력
                wgs84_coordinates = transformer.transform(y_coordinate, x_coordinate)
                # xyz 순서로 다시 변경
                wgs_v_list.append(f"v {str(wgs84_coordinates[1])} {str(wgs84_coordinates[0])} {z_coordinate}")


    # center point 구하기
    center_point = get_center_point(wgs_v_list)


    # 로컬좌표계 변환
    local_result = convert_to_local_with_pool(center_point, wgs_v_list)

    local_coordinate_list = local_result.get("local")
    tile_volume = local_result.get("volume")

    output_path = os.path.join(output_dir, file_name)
    v_cnt = 0

    # 새로 파일 작성
    with open(output_path, "w", encoding="utf-8") as new_file:
        for new_line in reading_obj:
            if new_line.startswith("v "):
                if local_coordinate_list[v_cnt]:
                    new_file.write(local_coordinate_list[v_cnt])
                    v_cnt += 1
            else:
                new_file.write(new_line)

    # mtl파일 복사
    mtl_path = os.path.join(dir_name, file_name.split(".obj")[0] + ".mtl")
    try:
        shutil.copy(mtl_path, output_dir)
    except FileNotFoundError:
        print("mtl 파일 찾을 수 없습니다. 무시 후 진행합니다.")
        print(mtl_path + " mtl 파일이 존재하지 않음")
        pass

    try:
        with open(mtl_path, "r", encoding="utf-8") as f:
            file_list = f.readlines()
            for line in file_list:
                if (
                    line.startswith("map_Kd")
                    or line.startswith("map_Ka")
                    or line.startswith("map_Ks")
                ):
                    # jpg파일 복사
                    create_jpg(dir_name, output_dir, line.split(" ")[1].strip())
    except FileNotFoundError:
        print(mtl_path + " mtl파일이 존재하지 않음")



    # print("로컬좌표로 변환 완료")
    # termintate_time = timeit.default_timer()
    # print(termintate_time - start_time)
    # 폴더를 리턴하려면 output_dir
    # 파일의 경로까지 리턴하려면 output_path
    # return {"path": output_path, "tileVolume": tile_volume, "worldPoint": center_point}
    return center_point


def handle_local_obj(
    dir_name, file_name, world_point, output_dir=None, epsg="epsg:5186", up="Z", unit="m"
):
    """
    local좌표계의 obj에 대한 처리를 하는 함수
    
    todo) 타일 볼륨만 구하기. 월드중심점은 있는거 활용.
    """
    # start_time = timeit.default_timer()

    # print("로컬좌표계로 변환 시작..")
    # 인풋 경로 넣지 않았을 때 오류
    try:
        if dir_name is None:
            raise ValueError
    except ValueError:
        print(dir_name + " 의 파일 경로 없음")
        # print("파일 경로 없음")
        # return None
    
    # output 디렉토리 없으면 인풋경로에 생성
    if output_dir is None:
        output_dir = os.path.join(dir_name, "localized_obj")
    else:
        output_dir = os.path.join(output_dir, "localized_obj")
    try:
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
    except FileNotFoundError:
        print(output_dir + " output 경로 생성 오류")
        # print("output 디렉토리 생성 과정 중 문제 발생")


    obj_path = os.path.join(dir_name, file_name)
    
    wgs_v_list = []
    reading_obj = []

    # transformer = Transformer.from_crs(epsg, "epsg:4326")
    origin_local_result = []
    with open(obj_path, "r", encoding = "utf-8") as original_obj:
        reading_obj = original_obj.readlines()
        for line in reading_obj:
            if line.startswith("v "):
                # v 뒤에 공백이 두개인 경우가 있어서 
                # split(" ")시 빈 데이터는 삭제한다.
                line_list = list(filter(None, line.split(" ")))
                x_coordinate = line_list[1]
                y_coordinate = None
                z_coordinate = None
                if up == "Y":
                    y_coordinate = float(line_list[3]) * -1
                    z_coordinate = float(line_list[2]) # 줄바꿈해야하니까 strip()하지 않는다.
                else:
                    y_coordinate = float(line_list[2])
                    z_coordinate = float(line_list[3])

                # # x y 순서가 아님 위경도 순으로 입력
                # wgs84_coordinates = transformer.transform(y_coordinate, x_coordinate)
                # # xyz 순서로 다시 변경
                # wgs_v_list = wgs_v_list + [f'v {str(wgs84_coordinates[1])} {str(wgs84_coordinates[0])} {z_coordinate}']
                origin_local_result.append(f'v {x_coordinate} {str(y_coordinate)} {str(z_coordinate)}')

    # center point 구하기
    # center_point = get_center_point(wgs_v_list)
    center_point = tuple(world_point)

    # 로컬좌표계 변환 
    # local_result = convert_to_local(center_point, origin_local_result)
    
    # 로컬좌표계의 tile_volume구하기


    local_coordinate_list = origin_local_result
    local_result = get_local_tile_volume(center_point, local_coordinate_list, up, unit)
    tile_volume = local_result.get("volume")
    convert_local_list = local_result.get("local")

    output_path = os.path.join(output_dir, file_name)

    # 새로 파일 작성
    with open(output_path, "w", encoding = "utf-8") as new_file:
        v_cnt = 0
        for new_line in reading_obj:
            if new_line.startswith("v "):
                if convert_local_list[v_cnt]:
                    new_file.write(convert_local_list[v_cnt])
                    v_cnt += 1
            else:
                new_file.write(new_line)

    # obj, mtl파일 복사
    obj_path = os.path.join(dir_name, file_name.split(".obj")[0] + ".obj")
    mtl_path = os.path.join(dir_name, file_name.split(".obj")[0] + ".mtl")
    # try: 
    #     shutil.copy(obj_path, output_dir)
    # except FileNotFoundError:
    #     print("obj 파일 찾을 수 없습니다. 무시 후 진행합니다.")
    #     print(obj_path + " obj 파일이 존재하지 않음")
    #     pass

    try: 
        shutil.copy(mtl_path, output_dir)
    except FileNotFoundError:
        # print("mtl 파일 찾을 수 없습니다. 무시 후 진행합니다.")
        print(mtl_path + " mtl 파일이 존재하지 않음")
        pass

    try:
        with open(mtl_path, "r", encoding="utf-8") as f:
            file_list = f.readlines()
            for line in file_list:
                if line.startswith("map_Kd") or line.startswith("map_Ka") or line.startswith("map_Ks"):
                    # jpg파일 복사
                    create_jpg(dir_name, output_dir, line.split(" ")[1].strip())
    except FileNotFoundError:
        print(mtl_path + " mtl파일이 존재하지 않음")
                

    # print("로컬좌표로 변환 완료")
    # termintate_time = timeit.default_timer()
    # print(termintate_time - start_time)
    # 폴더를 리턴하려면 output_dir
    # 파일의 경로까지 리턴하려면 output_path
    return {
        "path" : output_path,
        "tileVolume" : tile_volume,
        "worldPoint" : center_point
    }


def find_world_point(parent_point, local_list):
    """
    부모의 월드 중심점과 자식의 로컬 버텍스를 통한 자식 로컬 메쉬의 타일 볼륨과 월드 중심점을 찾는다
    """

    # 축별 최대 최소값
    box = {"min": [None, None, None], "max": [None, None, None]}
    length = {
        "x": None,
        "y": None
        # "z" : None
    }

    offset_box = {"min": [None, None, None], "max": [None, None, None]}
    offset_length = {
        "x": None,
        "y": None
        # "z" : None
    }

    # 부모 중심점 기준 로컬 버텍스의 BBOX를 구함
    for line in local_list:
        if line.startswith("v "):
            trim_line = " ".join(line.split())
            split_line = trim_line.split(" ")
            x = float(split_line[1])
            y = float(split_line[2])
            z = float(split_line[3])

            if box["min"][0] is None or box["min"][0] > x:
                box["min"][0] = x
            if box["min"][1] is None or box["min"][1] > y:
                box["min"][1] = y
            if box["min"][2] is None or box["min"][2] > z:
                box["min"][2] = z

            if box["max"][0] is None or box["max"][0] < x:
                box["max"][0] = x
            if box["max"][1] is None or box["max"][1] < y:
                box["max"][1] = y
            if box["max"][2] is None or box["max"][2] < z:
                box["max"][2] = z

    # bbox의 로컬 중점을 구한다
    x_center = box["max"][0] - ((box["max"][0] - box["min"][0]) / 2)
    y_center = box["max"][1] - ((box["max"][1] - box["min"][1]) / 2)

    # x_center = (box["max"][0] + box["min"][0]) / 2
    # y_center = (box["max"][1] + box["min"][1]) / 2

    offset_local_list = []
    # 로컬 버텍스를 bbox 로컬 중점과 모델의 로컬 중점(원점)과 계산하여 offset 시킨다
    for line in local_list:
        if line.startswith("v "):
            trim_line = " ".join(line.split())
            split_line = trim_line.split(" ")
            x = float(split_line[1])
            y = float(split_line[2])
            z = float(split_line[3])
            offset_x = x - x_center
            offset_y = y - y_center
            offset_line = (
                "v " + str(offset_x) + " " + str(offset_y) + " " + str(z) + "\n"
            )
            offset_local_list.append(offset_line)
        else:
            offset_local_list.append(line)

    # 월드 중점에서 bbox 로컬 중점만큼 이동한 로컬 메쉬의 월드 중점을 구한다
    # 이동 방향각
    bearing_x = 90 if x_center > 0 else -90
    bearing_y = 0 if y_center > 0 else 180

    reverse_parent = (parent_point[1], parent_point[0])
    destination_x = geodesic(meters=abs(x_center)).destination(
        reverse_parent, bearing=bearing_x
    )
    destination = geodesic(meters=abs(y_center)).destination(
        destination_x, bearing=bearing_y
    )
    # offset 된 버텍스의 타일 볼륨을 구한다

    for line in offset_local_list:
        if line.startswith("v "):
            trim_line = " ".join(line.split())
            split_line = trim_line.split(" ")
            x = float(split_line[1])
            y = float(split_line[2])
            z = float(split_line[3])

            if offset_box["min"][0] is None or offset_box["min"][0] > x:
                offset_box["min"][0] = x
            if offset_box["min"][1] is None or offset_box["min"][1] > y:
                offset_box["min"][1] = y
            if offset_box["min"][2] is None or offset_box["min"][2] > z:
                offset_box["min"][2] = z

            if offset_box["max"][0] is None or offset_box["max"][0] < x:
                offset_box["max"][0] = x
            if offset_box["max"][1] is None or offset_box["max"][1] < y:
                offset_box["max"][1] = y
            if offset_box["max"][2] is None or offset_box["max"][2] < z:
                offset_box["max"][2] = z

    offset_length["x"] = abs(offset_box["max"][0] - offset_box["min"][0])
    offset_length["y"] = abs(offset_box["max"][1] - offset_box["min"][1])

    height = None
    if offset_box["max"][2] > 0:
        if offset_box["min"][2] > 0 or offset_box["min"][2] == 0:
            height = offset_box["max"][2] - offset_box["min"][2]
        elif offset_box["min"][2] < 0:
            height = offset_box["max"][2] + abs(offset_box["min"][2])
    elif offset_box["max"][2] == 0:
        if offset_box["min"][2] == 0:
            height = 0
        elif offset_box["min"][2] < 0:
            height = abs(offset_box["min"][2])
    elif offset_box["max"][2] < 0:
        if offset_box["min"][2] < 0:
            height = abs(offset_box["max"][2]) + abs(offset_box["min"][2])

    try:
        if height is None:
            raise ValueError
    except ValueError:
        print("타일 높이값 없음")

    return {
        "local": offset_local_list,
        "tileVolume": {
            "minHeight": offset_box["min"][2],
            "maxHeight": offset_box["max"][2],
            "tileWidth": offset_length["x"],
            "tileHeight": offset_length["y"],
            "height": height,
        },
        "worldPoint": (destination[1], destination[0]),
    }
