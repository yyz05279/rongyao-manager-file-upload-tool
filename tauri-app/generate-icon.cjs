const fs = require('fs');
const path = require('path');

// 简单创建一个基本的 ICO 文件头
// ICO 格式：图标头(6字节) + 图标目录项(16字节) + PNG数据
function generateIco() {
  const pngPath = path.join(__dirname, 'src-tauri/icons/icon.png');
  const icoPath = path.join(__dirname, 'src-tauri/icons/icon.ico');
  
  const pngData = fs.readFileSync(pngPath);
  
  // ICO 文件头 (6 bytes)
  const header = Buffer.alloc(6);
  header.writeUInt16LE(0, 0);  // Reserved (0)
  header.writeUInt16LE(1, 2);  // Type (1 = ICO)
  header.writeUInt16LE(1, 4);  // Count (1 image)
  
  // 图标目录项 (16 bytes)
  const dirEntry = Buffer.alloc(16);
  dirEntry.writeUInt8(128, 0);   // Width (128)
  dirEntry.writeUInt8(128, 1);   // Height (128)
  dirEntry.writeUInt8(0, 2);     // Color palette
  dirEntry.writeUInt8(0, 3);     // Reserved
  dirEntry.writeUInt16LE(1, 4);  // Color planes
  dirEntry.writeUInt16LE(32, 6); // Bits per pixel
  dirEntry.writeUInt32LE(pngData.length, 8);  // Size of image data
  dirEntry.writeUInt32LE(22, 12); // Offset to image data (6 + 16 = 22)
  
  // 组合所有数据
  const icoData = Buffer.concat([header, dirEntry, pngData]);
  
  fs.writeFileSync(icoPath, icoData);
  console.log('✅ icon.ico 已生成:', icoPath);
}

try {
  generateIco();
} catch (error) {
  console.error('❌ 生成失败:', error.message);
  process.exit(1);
}

