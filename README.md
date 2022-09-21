# obj2gltf (English)
## TODO
- Change obj of world coordinates into obj of local coordinates obj, glb and it's world center point by json


- Used [Cesium obj2gltf](https://github.com/CesiumGS/obj2gltf)
- Change obj's coordinates system by using python module
    - this module's trasforming coords system completes quite fast even though it use's `geodesic` which is quite slow in performing speed because of using python's multiprocessing. 
    - this performs fast especially when transforming big size of obj. It is more faster when converting small amount of models with big size more than transforming lots of models with small size. 

## how to use
You must prepare python environment, and then run node.
### python
- python version >= 3.8
```
pip install -r requirements.txt
```


### node 
```
npm i 
node ${workspaceFolder}\\bin\\customObj2gltf.js convert --i=${input path} --o=${output path} --e=${coordinates}
```
- it can convert multiple obj models in the input path


#### example
```
node ${workspaceFolder}\\bin\\customObj2gltf.js convert --i='F:/obj/input' --o='F:/obj/output' --e='epsg:5186'
```

---
</br></br></br>

# obj2gltf (Korea)
## TODO
- 월드 좌표의 obj를 로컬 모델로 변환시킨 후 glb와 해당 모델의 월드 중심점을 json 파일로 export 함


- Used [Cesium obj2gltf](https://github.com/CesiumGS/obj2gltf)
- 해당 파이썬 모듈 내 좌표계를 변환하는 함수는 작은 용량의 obj 여러개를 변환하는 것 보다 적은 수여도 큰 모델의 obj를 변환할 때 빠른 좌표 변환 속도를 냄. 이는 파이썬의 multiprocessing 을 통해 속도 개선. (작은 용량의 많은 obj를 한번에 변환하는 좌표계 변환함수는 추후 여유로울 때 개발 예정)

## how to use
You must prepare python environment, and then run node.
### python
- python version >= 3.8
```
pip install -r requirements.txt
```


### node 
```
npm i 
node ${workspaceFolder}\\bin\\customObj2gltf.js convert --i=${input path} --o=${output path} --e=${coordinates}
```
- input 경로 내 여러 obj모델들을 일괄적으로 변환할 수 있음


#### example
```
node ${workspaceFolder}\\bin\\customObj2gltf.js convert --i='F:/obj/input' --o='F:/obj/output' --e='epsg:5186'
```

