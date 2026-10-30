import { File } from 'megajs';
const file = File.fromURL(process.argv[2]);
await file.loadAttributes();
console.log(JSON.stringify({ name: file.name, size: file.size, timestamp: file.timestamp }));
