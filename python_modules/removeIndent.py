import os
import shutil


# def removeIndent(input_dir, user_output_dir):
#     # mtl 시작에 tab이 들어간 것이 있을 때가 있다.
#     # 이거 에러나는데..빡친다... 만든다...탭 indent 없애는거.. 

#     output_dir = os.path.join(user_output_dir, "trimmed_obj")


    
#     # 폴더 통째로 복사
#     try:
#         shutil.copytree(input_dir, output_dir)
#     except:
#         print("폴더복사 에러")  
#     file_list = os.listdir(input_dir)

#     for file in file_list:
#         if os.path.splitext(file)[1].lower() == ".mtl":
#             with open(os.path.join(output_dir, file), "r", encoding="utf-8") as f:
#                 lines = f.readlines()
#             with open(os.path.join(output_dir, file), "w", encoding="utf-8") as f:
#                 for line in lines:
#                     if line.startswith("\t"):
#                         f.write(line.replace("\t", ""))


#                     else:
#                         f.write(line)

#                     print()

#     return output_dir



def removeIndent(input_dir, user_output_dir):
    # mtl 시작에 tab이 들어간 것이 있을 때가 있다.
    # 이거 에러나는데..빡친다... 만든다...탭 indent 없애는거.. 

    output_dir = os.path.join(user_output_dir, "trimmed_obj")
    
    # 폴더 통째로 복사
    try:
        shutil.copytree(input_dir, output_dir)
    except:
        print("폴더복사 에러")  
    file_list = os.listdir(input_dir)

    for file in file_list:
        has_error = False
        if os.path.splitext(file)[1].lower() == ".mtl":
            with open(os.path.join(output_dir, file), "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(os.path.join(output_dir, file), "w", encoding="utf-8") as f:
                for line in lines:
                    if line.startswith("\t"):
                        line = line.replace("\t", "")
                        if line.startswith("map_") and "?" in line.split(" ")[1]:
                            has_error = True

                            mapType, textureName = line.split(" ")[0], line.split("\\")[-1]
                            f.write(f"{mapType} {textureName}")
                        else:
                            f.write(line.replace("\t", ""))


                    else:
                        f.write(line)

        if (has_error):
            # 3ds로 obj를 만들었을 때 이러한 문제가 생기는 듯 함
            print("텍스쳐 참조 경로에 문제가 있는 파일명: ", file)

                            

    return output_dir

# removeIndent("F:/obj/jangsung/장성_담장obj")
# removeIndent("F:/obj/jangsung/장성군_최종_0927/glbList/trimmed_obj", "F:/obj/jangsung/장성군_최종_0927/glbList/test")
