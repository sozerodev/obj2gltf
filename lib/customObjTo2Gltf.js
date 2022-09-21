const obj2gltf = require("obj2gltf/lib/obj2gltf");
const path = require('path');
const fs = require('graceful-fs')
const fsExtra = require('fs-extra');
const { spawn } = require('child_process');
const jschardet = require('jschardet');
const iconv = require('iconv-lite');

module.exports = customObj2gltf;



function customObj2gltf(input, output, epsg){
    
    // custom options
    const convertingOptions = {
        binary: true,
        inputUpAxis: "Z",
        outputUpAxis: "Y"
    };



    const pythonModulePath = `${__dirname}${path.sep}..${path.sep}python_modules${path.sep}main.py`;
    const normPath = path.normalize(pythonModulePath);

    const result = spawn('python', [normPath, input, output, epsg]);

    result.stdout.on('data', function (data) {
        const charCode = jschardet.detect(data);
        const utf8Text = iconv.decode(data, charCode.encoding);
        console.log(utf8Text)
        
        if (utf8Text.indexOf("localized_obj_result:") !== -1) {
          const obj_path = utf8Text.toString().substring(21, utf8Text.indexOf("\r\n"));
          // const obj_path = 'F:/obj/jangsung/test/output/localized_obj'

          // output의 result폴더를 만든다.
          if (!fs.existsSync(output + "/glb")) fs.mkdirSync(output + "/glb")
          //  obj_path 의 파일들을 모두 읽어 obj2gltf()를 통해 비동기로 실행시킨다.
          console.log("----------------- obj파일을 glb로 변환 진행 -----------------\n");
          let file_list = getAllFiles(obj_path)


          for (let file of file_list){
              if (path.extname(file) == ".obj" || path.extname(file) ==".OBJ"){
                  
                  obj2gltf(file, convertingOptions).then(function (glb) {
                    const glbPath = output + path.sep + "glb" + path.sep + path.basename(file).split(".obj")[0] + ".glb"
                    fs.writeFileSync(glbPath, glb);
                    console.log(glbPath, " 작성 완료")
                  });

              }
          }
          
        }

      });
    
      result.stderr.on('data', function (data) {
        const charCode = jschardet.detect(data);
        const utf8Text = iconv.decode(data, charCode.encoding);
        console.log("error log : ", utf8Text);
      });
}


const getAllFiles = dir =>
    fs.readdirSync(dir).reduce((files, file) => {
        const name = path.join(dir, file);
        const isDirectory = fs.statSync(name).isDirectory();
    return isDirectory ? [...files, ...getAllFiles(name)] : [...files, name];
    }, []);