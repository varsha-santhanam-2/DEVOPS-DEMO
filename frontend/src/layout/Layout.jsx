import { Outlet } from "react-router-dom";
import Navbar from "../components/NavBar";

export default function Layout() {
  return (
    <div className="app">
      <Navbar />
      <div className="content">
        <Outlet />
      </div>
    </div>
  );
}