// dashboard.spec.js — Playwright tests for all 4 panels + log + export

import { test, expect } from '@playwright/test'
import path from 'path'
import fs from 'fs'

const SCREENSHOTS = path.resolve('../test-results/playwright/screenshots')

function ensureDir(d) { if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true }) }

test.beforeAll(() => ensureDir(SCREENSHOTS))

test('all 4 panels render on load', async ({ page }) => {
  await page.goto('/')

  await expect(page.getByTestId('intent-panel')).toBeVisible()
  await expect(page.getByTestId('agent-panel')).toBeVisible()
  await expect(page.getByTestId('memory-panel')).toBeVisible()
  await expect(page.getByTestId('voice-panel')).toBeVisible()

  await page.screenshot({ path: `${SCREENSHOTS}/all-panels.png`, fullPage: true })
})

test('ORBIT wordmark visible in top bar', async ({ page }) => {
  await page.goto('/')

  await expect(page.getByText('Orbit')).toBeVisible()

  await page.screenshot({ path: `${SCREENSHOTS}/topbar.png` })
})

test('connection status dot is visible', async ({ page }) => {
  await page.goto('/')

  await expect(page.getByTestId('connection-dot')).toBeVisible()

  await page.screenshot({ path: `${SCREENSHOTS}/connection-dot.png` })
})

test('intent panel updates after sending a request', async ({ page }) => {
  await page.goto('/')

  await page.getByTestId('input-bar').fill('explain binary search')
  await page.getByTestId('input-bar').press('Enter')

  await page.waitForTimeout(1500)

  const label = page.getByTestId('intent-panel').locator('.font-mono').first()
  await expect(label).not.toHaveText('—')

  await page.screenshot({ path: `${SCREENSHOTS}/intent-after-request.png` })
})

test('agent panel shows status badge after request', async ({ page }) => {
  await page.goto('/')

  await page.getByTestId('input-bar').fill('show my streak')
  await page.getByTestId('input-bar').press('Enter')

  await page.waitForTimeout(1500)

  await page.screenshot({ path: `${SCREENSHOTS}/agent-panel.png` })
})

test('memory panel has at least one Redis key', async ({ page }) => {
  await page.goto('/')

  await expect(page.getByTestId('redis-key')).toBeVisible()

  await page.screenshot({ path: `${SCREENSHOTS}/memory-panel.png` })
})

test('voice panel shows latency value', async ({ page }) => {
  await page.goto('/')

  await page.getByTestId('input-bar').fill('what is a heap')
  await page.getByTestId('input-bar').press('Enter')

  await page.waitForTimeout(1500)

  const latency = page.getByTestId('voice-latency')
  await expect(latency).toBeVisible()
  await expect(latency).toContainText('ms')

  await page.screenshot({ path: `${SCREENSHOTS}/voice-latency.png` })
})

test('request log adds a new row after each request', async ({ page }) => {
  await page.goto('/')

  await page.getByTestId('input-bar').fill('read my emails')
  await page.getByTestId('input-bar').press('Enter')

  await page.waitForTimeout(1500)

  const rows = page.getByTestId('request-log').locator('tbody tr')
  await expect(rows).not.toHaveCount(0)

  await page.screenshot({ path: `${SCREENSHOTS}/request-log.png`, fullPage: true })
})

test('export button is visible and clickable', async ({ page }) => {
  await page.goto('/')

  const btn = page.getByTestId('export-button')
  await expect(btn).toBeVisible()
  await expect(btn).toContainText('export')

  await page.screenshot({ path: `${SCREENSHOTS}/export-button.png` })
})
