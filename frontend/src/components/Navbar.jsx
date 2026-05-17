import { useAuth } from '../context/AuthContext.jsx';
import { FiCheckSquare, FiLogOut } from 'react-icons/fi';

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <FiCheckSquare className="brand-icon" />
        <span>Taskflow</span>
      </div>
      <div className="navbar-user">
        <span className="navbar-username">Hello, {user?.username}</span>
        <button className="btn-logout" onClick={logout} id="logout-btn">
          <FiLogOut /> Logout
        </button>
      </div>
    </nav>
  );
}
