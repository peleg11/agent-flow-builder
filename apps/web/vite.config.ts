import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    // Testing Library only unmounts between tests when afterEach is global.
    globals: true,
  },
});
