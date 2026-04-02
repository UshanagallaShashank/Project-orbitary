import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  timeout: 30000,
  retries: 1,
  use: {
    baseURL: 'http://localhost:5173',
    screenshot: 'on',
    video: 'retain-on-failure',
    headless: true,
  },
  outputDir: '../test-results/playwright/',
  reporter: [
    ['html', { outputFolder: '../test-results/playwright', open: 'never' }],
    ['json', { outputFile: '../test-results/playwright/results.json' }],
    ['list'],
  ],
  webServer: {
    command: 'npm run dev',
    port: 5173,
    reuseExistingServer: true,
    timeout: 30000,
  },
})
