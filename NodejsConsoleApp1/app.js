'use strict';

console.log('Hello world');

const { exec } = require('child_process');

exec('node Spellcasting1 - Copy.js', (error, stdout, stderr) => {
    if (error) {
        console.error(`Error executing file: ${error}`);
        return;
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
});
