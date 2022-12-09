/**
 * OBJ파일을 GLB로 만들기 위한 CLI
 */
 const yargs = require('yargs');
 const path = require('path');
 const customObjTo2Gltf = require('../lib/customObjTo2Gltf');
 
 // obj bim 타일 만들기
 yargs.command({
   command: 'convert',
   describe: 'convert obj to glb',
   builder: {
     input: {
       alias: 'i',
       describe: 'Path to the obj file',
       type: 'string',
       normalize: true,
       demandOption: true
     },
     output: {
       alias: 'o',
       describe: 'Path of the converted result',
       type: 'string',
       normalize: true
     },
     epsg: {
       alias: 'e',
       describe: 'EPSG Code of target files',
       type: 'string',
       normalize: true
     },
     rotation: {
       alias: 'r',
       describe: 'Roatation value of obj',
       type: 'list',
       normalize: true
     }
   },
   handler: (argv) => {
     console.log('input:', argv.input);
     console.log('output:', argv.output);
     console.log('epsg:', argv.epsg);
     console.log('rotation:', argv.rotation);
     let out = argv.output;
     if (!out) {
       out = path.normalize(`${argv.input + path.sep}output`);
     }
     
     customObjTo2Gltf(argv.input, out, argv.epsg, argv.rotation);
   }
 }).help().argv;