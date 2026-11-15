import js from "@eslint/js";
import prettier from "eslint-config-prettier";
import { defineConfig } from "eslint/config";
import reactHooks from "eslint-plugin-react-hooks";
import tseslint from "typescript-eslint";

export default defineConfig(
  { ignores: ["dist"] },
  js.configs.recommended,
  // strictTypeChecked includes no-explicit-any and the no-unsafe-* rules that stop any from leaking in.
  tseslint.configs.strictTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
  // This file is plain JS outside tsconfig, so type-aware rules can't run on it.
  {
    files: ["eslint.config.js"],
    extends: [tseslint.configs.disableTypeChecked],
  },
  reactHooks.configs.flat.recommended,
  // Last, so it turns off any style rules that would fight Prettier.
  prettier,
);
