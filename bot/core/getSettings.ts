import * as toml from 'smol-toml';
import * as fs from 'fs';

const _settingRawString = fs.readFileSync("config.toml", { encoding: 'utf8' });
export const settings = toml.parse(_settingRawString) as Record<string, any>;
