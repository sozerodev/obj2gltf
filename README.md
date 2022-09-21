# obj2gltf
## TODO
- 월드 좌표의 obj를 로컬 모델로 변환시킨 후 glb와 해당 모델의 월드 중심점을 json으로 export
(Change obj of world coordinates into obj of local coordinates obj, glb and it's world center point by json)


- Used [Cesium obj2gltf](https://github.com/CesiumGS/obj2gltf)
- Change obj's coordinates system by using python module
    


## how to use

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
- input 경로 내 여러 obj모델들을 일괄적으로 변환할 수 있습니다.
(it can convert multiple obj models in the input path)


#### example
```
node ${workspaceFolder}\\bin\\customObj2gltf.js convert --i='F:/obj/input' --o='F:/obj/output' --e='epsg:5186'
```

