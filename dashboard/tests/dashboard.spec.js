// dashboard.spec.js — Playwright tests for all 4 panels + log + export

import { test, expect } from '@playwright/test'
import path from 'path'
import fs from 'fs'

const SS = path.resolve('../test-results/playwright/screenshots')

test.beforeAll(() => {
  if (!fs.existsSync(SS)) fs.mkdirSync(SS, { recursive: true })
})

// Helper — send a request via the input bar and wait for state update
async function sendRequest(page, text) {
  await page.getByTestId('input-bar').fill(text)
  await page.getByTestId('input-bar').press('Enter')
  await page.waitForTimeout(800)
}

test('all 4 panels render on load', async ({ page }) => {
  await page.goto('/')

  await expect(page.getByTestId('intent-panel')).toBeVisible()
  await expect(page.getByTestId('agent-panel')).toBeVisible()
  await expect(page.getByTestId('memory-panel')).toBeVisible()
  await expect(page.getByTestId('voice-panel')).toBeVisible()

  await page.screenshot({ path: `${SS}/all-panels.png`, fullPage: true })
})

test('ORBIT wordmark is visible in top bar', async ({ page }) => {
  await page.goto('/')

  await expect(page.getByText('Orbit')).toBeVisible()

  await page.screenshot({ path: `${SS}/topbar.png` })
})

test('connection status dot renders', async ({ page }) => {
  await page.goto('/')

  await expect(page.getByTestId('connection-dot')).toBeVisible()

  await page.screenshot({ path: `${SS}/connection-dot.png` })
})

test('intent panel updates after sending a request', async ({ page }) => {
  await page.goto('/')

  await sendRequest(page, 'explain binary search')

  // Intent label must change from default dash
  const label = page.getByTestId('intent-panel').locator('p.font-mono').first()
  await expect(label).not.toHaveText('—')

  await page.screenshot({ path: `${SS}/intent-after-request.png` })
})

test('agent panel shows agent name and DONE status after request', async ({ page }) => {
  await page.goto('/')

  await sendRequest(page, 'show my leetcode streak')

  await expect(page.getByTestId('agent-panel')).toContainText('agent')
  await expect(page.getByTestId('agent-status')).toHaveText('DONE')

  await page.screenshot({ path: `${SS}/agent-panel-done.png` })
})

test('memory panel shows at least one Redis key', async ({ page }) => {
  await page.goto('/')

  await expect(page.getByTestId('redis-key')).toBeVisible()
  await expect(page.getByTestId('redis-key')).toContainText('session')

  await page.screenshot({ path: `${SS}/memory-panel.png` })
})

test('voice panel shows latency in ms after request', async ({ page }) => {
  await page.goto('/')

  await sendRequest(page, 'what is a heap')

  await expect(page.getByTestId('voice-latency')).toBeVisible()
  await expect(page.getByTestId('voice-latency')).toContainText('ms')

  await page.screenshot({ path: `${SS}/voice-latency.png` })
})

test('request log adds a new row after each request', async ({ page }) => {
  await page.goto('/')

  await sendRequest(page, 'read my emails')

  const rows = page.getByTestId('request-log').locator('tbody tr')
  await expect(rows.first()).not.toContainText('no requests yet')

  await page.screenshot({ path: `${SS}/request-log.png`, fullPage: true })
})

test('export button is visible and labelled correctly', async ({ page }) => {
  await page.goto('/')

  const btn = page.getByTestId('export-button')
  await expect(btn).toBeVisible()
  await expect(btn).toContainText('export')

  await page.screenshot({ path: `${SS}/export-button.png` })
})
