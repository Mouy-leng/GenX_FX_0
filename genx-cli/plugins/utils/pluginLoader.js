import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export async function loadPlugins() {
  const pluginDir = path.join(__dirname, '..');
  const pluginFiles = fs.readdirSync(pluginDir).filter(f => f.endsWith('.js'));

  const plugins = await Promise.all(pluginFiles.map(async (file) => {
    // Correctly construct the full path for import
    const pluginPath = path.join(pluginDir, file);
    // Use pathToFileURL to ensure correct module resolution
    const pluginModule = await import(pathToFileURL(pluginPath).href);
    return { ...pluginModule.default, name: path.basename(file, '.js') };
  }));

  return plugins;
}
