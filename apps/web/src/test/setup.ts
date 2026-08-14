import { beforeEach } from "vitest"
import "@testing-library/jest-dom/vitest"

const localStorageMock = (() => {
  let store: Record<string, string> = {}

  return {
    get length() {
      return Object.keys(store).length
    },
    key(index: number) {
      return Object.keys(store)[index] ?? null
    },
    getItem(key: string) {
      return store[key] ?? null
    },
    setItem(key: string, value: string) {
      store[key] = value
    },
    removeItem(key: string) {
      delete store[key]
    },
    clear() {
      store = {}
    },
  }
})()

Object.defineProperty(globalThis, "localStorage", {
  value: localStorageMock,
  writable: true,
})

beforeEach(() => {
  localStorageMock.clear()
})
