# agent-flow-web

The React frontend for agent-flow-builder. It will hold the canvas where you wire nodes together and watch them run. For now it renders one placeholder heading.

## Layout

| File               | What it does                                                                                               |
| ------------------ | ---------------------------------------------------------------------------------------------------------- |
| `index.html`       | The page Vite serves. It loads `src/main.tsx`.                                                             |
| `src/main.tsx`     | Mounts `<App />` into `#root`, inside React's `StrictMode`.                                                |
| `src/App.tsx`      | The root component. Renders the placeholder heading.                                                       |
| `src/App.test.tsx` | Checks the heading renders, using Vitest and Testing Library.                                              |
| `vite.config.ts`   | Vite build config, plus the Vitest config (`test`), which runs tests in jsdom.                             |
| `tsconfig.json`    | TypeScript in `strict` mode. Only type checks, because Vite does the compiling.                            |
| `eslint.config.js` | ESLint with typescript-eslint's `strictTypeChecked` rules, which forbid `any`, plus the React hooks rules. |

## Commands

Run these from `apps/web`. You need Node.js 22.22+, 24.15+ or 26+ (jsdom's minimum, the strictest of the dependencies) and [pnpm](https://pnpm.io/). Run `pnpm install` first.

| Command          | What it does                                           |
| ---------------- | ------------------------------------------------------ |
| `pnpm dev`       | Serve the app with hot reload at http://localhost:5173 |
| `pnpm lint`      | ESLint, then Prettier in check mode                    |
| `pnpm format`    | Format every file with Prettier                        |
| `pnpm typecheck` | Type check with `tsc`                                  |
| `pnpm test`      | Run the tests once                                     |
| `pnpm build`     | Type check, then build into `dist/`                    |
