

import os
import shutil


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
        if os.path.splitext(file)[1].lower() == ".mtl":
            with open(os.path.join(output_dir, file), "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(os.path.join(output_dir, file), "w", encoding="utf-8") as f:
                for line in lines:
                    if line.startswith("\t"):
                        f.write(line.replace("\t", ""))
                    else:
                        f.write(line)


    return output_dir



# removeIndent("F:/obj/jangsung/장성_담장obj")
# removeIndent("F:/obj/jangsung/test")
