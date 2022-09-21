import os
import shutil
import sys
from localize_world_obj import localize_world_obj
from removeIndent import removeIndent


if __name__ == "__main__":
    # input_dir = "F:/obj/jangsung/test/input"
    # output_dir = "F:/obj/jangsung/test/output"
    # epsg = "epsg:5186"
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    epsg = sys.argv[3]

    # removeIndent먼저
    trimmed_path = removeIndent(input_dir, output_dir)

    # 로컬로 당기기
    localized_path = localize_world_obj(trimmed_path, output_dir, epsg)
    
    # 경위도고도 좌표 남기기
    position_json_path = os.path.join(localized_path, "position.json") # 경위도고도값 정보 담긴 json파일
    


    # glb만들어질 폴더 생성
    glb_path = os.path.join(output_dir, "glb")
    try:
        if not os.path.exists(glb_path):
            os.mkdir(glb_path)
    except FileNotFoundError:
        print("glb 디렉토리 생성 오류")

    try:
        shutil.move(position_json_path, os.path.join(glb_path, "position.json"))
    except:
        print("파일이동 에러")



    # 결과물 폴더 노드로 옮기기
    print(f"localized_obj_result:{localized_path}")
    
