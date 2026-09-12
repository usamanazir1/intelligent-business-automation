import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

import { App } from "./App";

vi.mock("./api/client", () => ({
  fetchDashboardSummary: vi.fn().mockResolvedValue({
    total_workflows: 12,
    active_automations: 7,
    tasks_completed_today: 143,
    success_rate_pct: 98.2,
    pending_approvals: 3,
  }),
}));

describe("App", () => {
  it("renders the application shell", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <App />
      </MemoryRouter>,
    );
    expect(
      screen.getByText(/Intelligent Business Automation/i),
    ).toBeInTheDocument();
  });
});