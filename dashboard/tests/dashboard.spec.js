// dashboard.spec.js — Playwright tests for all 4 panels + log + export

import { test, expect } from '@playwright/test'
import path from 'path'
import fs from 'fs'

const SS = path.resolve('../test-results/playwright/screenshots')

test.beforeAll(() => {
  if (!fs.existsSync(SS)) fs.mkdirSync(SS, { recursive: true })
})

async function sendRequest(page, text) {
  await page.getByTestId('input-bar').fill(text)
  await page.getByTestId('input-bar').press('Enter')
  // Wait for React state to settle — mock applies synchronously so 500ms is plenty
  await page.waitForTimeout(500)
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

test('intent panel shows MENTOR after explain request', async ({ page }) => {
  await page.goto('/')

  await sendRequest(page, 'explain binary search')

  // classifyOffline maps "explain" → MENTOR — assert exact label
  await expect(page.getByTestId('intent-panel')).toContainText('MENTOR')

  await page.screenshot({ path: `${SS}/intent-after-request.png` })
})

test('intent panel shows TRACKER after streak request', async ({ page }) => {
  await page.goto('/')

  await sendRequest(page, 'show my leetcode streak')

  await expect(page.getByTestId('intent-panel')).toContainText('TRACKER')

  await page.screenshot({ path: `${SS}/intent-tracker.png` })
})

test('agent panel shows DONE status badge after request', async ({ page }) => {
  await page.goto('/')

  await sendRequest(page, 'explain recursion')

  await expect(page.getByTestId('agent-status')).toBeVisible()
  await expect(page.getByTestId('agent-status')).toHaveText('DONE')

  await page.screenshot({ path: `${SS}/agent-panel-done.png` })
})

test('memory panel shows Redis session key on load', async ({ page }) => {
  await page.goto('/')

  await expect(page.getByTestId('redis-key')).toBeVisible()
  await expect(page.getByTestId('redis-key')).toContainText('session')

  await page.screenshot({ path: `${SS}/memory-panel.png` })
})

test('voice panel shows transcript after request', async ({ page }) => {
  await page.goto('/')

  await sendRequest(page, 'what is a heap')

  await expect(page.getByTestId('voice-panel')).toContainText('what is a heap')
  await expect(page.getByTestId('voice-latency')).toContainText('ms')

  await page.screenshot({ path: `${SS}/voice-panel.png` })
})

test('request log adds a row after each request', async ({ page }) => {
  await page.goto('/')

  await sendRequest(page, 'read my emails')

  // Log row should appear with COMMS intent
  await expect(page.getByTestId('request-log')).toContainText('COMMS')

  await page.screenshot({ path: `${SS}/request-log.png`, fullPage: true })
})

test('export button is visible and labelled correctly', async ({ page }) => {
  await page.goto('/')

  const btn = page.getByTestId('export-button')
  await expect(btn).toBeVisible()
  await expect(btn).toContainText('export')

  await page.screenshot({ path: `${SS}/export-button.png` })
})
