import { render, screen } from "@testing-library/react";
import { expect, test } from "vitest";
import { App } from "./App";

test("renders the placeholder heading", () => {
  render(<App />);

  expect(
    screen.getByRole("heading", { level: 1, name: "Agent Flow Builder" }),
  ).toBeDefined();
});

// Guards the cleanup between tests: without it the first test's heading is still on the page.
test("starts each test from an empty page", () => {
  render(<App />);

  expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
});
