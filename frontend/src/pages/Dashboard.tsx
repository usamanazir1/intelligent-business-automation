import { useEffect, useState } from "react";
import {
  Card,
  Col,
  Row,
  Statistic,
  Spin,
  Alert,
  Typography,
} from "antd";
import {
  ApartmentOutlined,
  CheckCircleOutlined,
  ExperimentOutlined,
  RiseOutlined,
  ClockCircleOutlined,
} from "@ant-design/icons";

import { fetchDashboardSummary, type DashboardSummary } from "../api/client";

export function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboardSummary()
      .then(setSummary)
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : "Failed to load dashboard");
      });
  }, []);

  if (error) {
    return <Alert type="error" message="Unable to load dashboard" description={error} />;
  }

  if (!summary) {
    return <Spin size="large" />;
  }

  return (
    <div>
      <Typography.Title level={3}>Operational Overview</Typography.Title>
      <Row gutter={[16, 16]}>
        <Col xs={12} md={8} lg={4}>
          <Card>
            <Statistic
              title="Workflows"
              value={summary.total_workflows}
              prefix={<ApartmentOutlined />}
            />
          </Card>
        </Col>
        <Col xs={12} md={8} lg={4}>
          <Card>
            <Statistic
              title="Active Automations"
              value={summary.active_automations}
              prefix={<ExperimentOutlined />}
            />
          </Card>
        </Col>
        <Col xs={12} md={8} lg={4}>
          <Card>
            <Statistic
              title="Tasks Today"
              value={summary.tasks_completed_today}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
        <Col xs={12} md={8} lg={4}>
          <Card>
            <Statistic
              title="Success Rate"
              value={summary.success_rate_pct}
              precision={1}
              suffix="%"
              prefix={<RiseOutlined />}
            />
          </Card>
        </Col>
        <Col xs={12} md={8} lg={4}>
          <Card>
            <Statistic
              title="Pending Approvals"
              value={summary.pending_approvals}
              prefix={<ClockCircleOutlined />}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
}