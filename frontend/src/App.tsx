import { Layout, Menu, Typography } from "antd";
import {
  DashboardOutlined,
  ExperimentOutlined,
  ApartmentOutlined,
} from "@ant-design/icons";
import { Link, Navigate, Route, Routes } from "react-router-dom";
import { Dashboard } from "./pages/Dashboard";
import { Login } from "./pages/Login";

const { Header, Sider, Content } = Layout;

const menuItems = [
  { key: "dashboard", icon: <DashboardOutlined />, label: <Link to="/">Dashboard</Link> },
  { key: "workflows", icon: <ApartmentOutlined />, label: <Link to="/workflows">Workflows</Link> },
  { key: "automations", icon: <ExperimentOutlined />, label: <Link to="/automations">Automations</Link> },
];

export function App() {
  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider breakpoint="lg" collapsedWidth="0">
        <div className="logo">IBAM</div>
        <Menu theme="dark" mode="inline" defaultSelectedKeys={["dashboard"]} items={menuItems} />
      </Sider>
      <Layout>
        <Header
          style={{ background: "#fff", padding: "0 24px", display: "flex", alignItems: "center" }}
        >
          <Typography.Title level={4} style={{ margin: 0 }}>
            Intelligent Business Automation &amp; Management System
          </Typography.Title>
        </Header>
        <Content style={{ margin: 24 }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/workflows" element={<div>TODO: workflows page</div>} />
            <Route path="/automations" element={<div>TODO: automations page</div>} />
            <Route path="/login" element={<Login />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Content>
      </Layout>
    </Layout>
  );
}