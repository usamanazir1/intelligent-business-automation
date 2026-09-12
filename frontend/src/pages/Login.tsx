import { useState } from "react";
import { Alert, Button, Card, Form, Input, Typography, message } from "antd";

import { login } from "../api/client";

interface LoginFormValues {
  username: string;
  password: string;
}

export function Login() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onFinish(values: LoginFormValues) {
    setLoading(true);
    setError(null);
    try {
      await login(values.username, values.password);
      message.success("Signed in successfully");
      window.location.assign("/");
    } catch {
      setError("Invalid credentials. Try admin / admin for the demo.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 380, margin: "64px auto" }}>
      <Card title="Sign in to IBAM">
        {error && <Alert type="error" message={error} style={{ marginBottom: 16 }} />}
        <Form<LoginFormValues> layout="vertical" onFinish={onFinish}>
          <Form.Item
            label="Username"
            name="username"
            rules={[{ required: true, message: "Username is required" }]}
          >
            <Input autoComplete="username" />
          </Form.Item>
          <Form.Item
            label="Password"
            name="password"
            rules={[{ required: true, message: "Password is required" }]}
          >
            <Input.Password autoComplete="current-password" />
          </Form.Item>
          <Button type="primary" htmlType="submit" block loading={loading}>
            Sign in
          </Button>
        </Form>
        <Typography.Paragraph type="secondary" style={{ marginTop: 16 }}>
          Demo credentials: username <code>admin</code> / password <code>admin</code>.
        </Typography.Paragraph>
      </Card>
    </div>
  );
}