import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const apiBaseUrl = process.env.API_BASE_URL || "http://localhost:8000";

const rootDir = join(dirname(fileURLToPath(import.meta.url)), "..");
const content = `// URL base de la API REST. En local apunta a la API con docker-compose.\nwindow.API_BASE_URL = ${JSON.stringify(apiBaseUrl)};\n`;

writeFileSync(join(rootDir, "js/config.js"), content);
console.log(`Generated ${join(rootDir, "js/config.js")} with API_BASE_URL=${apiBaseUrl}`);