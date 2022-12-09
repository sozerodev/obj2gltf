
def rotate_obj(inputDir: str, fileName: str, rotation: List[int], up="Z": str):
    """obj에 회전값을 주는 함수 
    
    Args:
        inputDir (str): obj가 위치한 폴더 경로
        fileName (str): obj 파일 명
        rotation (list:int): roation값 ex) [0, 0, 0]
        up (str): 축 ("Y", "Z")
    """
    import bpy
    # 반환 값
    # result = None

    # splitFileName = fileName.split(".obj")
    # baseName = None
    # ext = None

    # baseName = splitFileName[0]
    # ext = "obj"
    # mtl 파일명
    # objFileName = baseName + "." + ext
    # 단일 obj 파일 절대 경로
    objFilePath = os.path.join(inputDir, fileName)
    
    # 씬에 객체가 있으면 삭제
    if len(bpy.data.objects) > 0:
        # 편집모드 변경
        bpy.ops.object.mode_set(mode='OBJECT')
        # 모든 객체 선택
        bpy.ops.object.select_all(action="SELECT")
        # 선택 객체 삭제
        bpy.ops.object.delete(use_global=False)
    # blender기본 제공 객체 전부 삭제.
    # bpy.ops.object.select_all(action="SELECT")
    # bpy.ops.object.delete(use_global=False)

    # blender에 파일 업로드
    try:
        bpy.ops.import_scene.obj(filepath=objFilePath)
    except RuntimeError:
        coordinate_logger.warning(objFilePath + " obj import 오류")

    # 현재 화면에 있는 객체 선택 취소(반복문시 우선순위 객체를 두지 않기 위해)
    bpy.ops.object.select_all(action="DESELECT")
    scene = bpy.context.scene

    for objs in scene.objects:
        bpy.context.view_layer.objects.active = objs
        # bpy.context.object.rotation_euler[0] = 0
        objs.select_set(state=True)

        # obj_list.append(objs.name + ".obj")
        # obj_list.append(objs.name + ".obj")
        # for v in obj_list:
        #     if v not in obfi_list:
        #         obfi_list.append(objs.name + ".obj")

        if objs.type == "MESH":
            bpy.ops.object.mode_set(mode='EDIT')
            if rotation:
                if up == "Z":
                    if rotation[0]:
                        objs.rotation_euler[0] = objs.rotation_euler[0] + math.radians(rotation[0])
                    if rotation[1]:
                        objs.rotation_euler[2] = objs.rotation_euler[1] + math.radians(rotation[1])
                    if rotation[2]:
                        objs.rotation_euler[1] = objs.rotation_euler[1] + math.radians(rotation[2])
                elif up == "Y":
                    if rotation[0]:
                        objs.rotation_euler[0] = objs.rotation_euler[0] + math.radians(rotation[0])
                    if rotation[1]:
                        objs.rotation_euler[1] = objs.rotation_euler[1] + math.radians(rotation[1])
                    if rotation[2]:
                        objs.rotation_euler[2] = objs.rotation_euler[2] + math.radians(rotation[2])
                

            # bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
            bpy.ops.mesh.split_normals()
            # bpy.ops.mesh.average_normals(average_type='CORNER_ANGLE')
            # objOutputPath = os.path.normpath(
            #     os.path.join(outputDir, baseName + "_" + str(ratio) + ".obj")
            # )
            objOutputPath = objFilePath
            # result = objOutputPath
            # if type(result) != tuple:
            #     result = [objOutputPath]
            # else:
            #     result.push(objOutputPath)

            try:
                bpy.ops.export_scene.obj(
                    filepath=str(objOutputPath), use_selection=True
                )

            except:
                coordinate_logger.warning(objOutputPath + " obj export 오류")
        objs.select_set(state=False)

