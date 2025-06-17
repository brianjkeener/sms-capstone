import React, { useContext } from 'react';
import AuthContext from '../context/AuthContext';
import { Button, Container } from 'react-bootstrap';
// We will create these components as templates
import AdminDashboard from '../components/AdminDashboard';
// import TeacherDashboard from '../components/TeacherDashboard';
// import StudentDashboard from '../components/StudentDashboard';

const Dashboard = () => {
  const { user, logout } = useContext(AuthContext);

  if (!user) {
    return <p>Loading...</p>;
  }

  // A simple function to get the full name
  const getFullName = () => {
    // This assumes your JWT payload from FastAPI looks like: {"sub": "email@email.com", "role": "admin", ...}
    // You might need to fetch the full user details from a /users/me endpoint for a better experience
    return user.sub; // For now, just show the email
  };

  const renderDashboard = () => {
    switch (user.role) {
      case 'admin':
        return <AdminDashboard />;
      case 'teacher':
        // return <TeacherDashboard />;
        return <p>Teacher Dashboard (To be built)</p>
      case 'student':
        // return <StudentDashboard />;
        return <p>Student Dashboard (To be built)</p>
      default:
        return <p>Unknown role.</p>;
    }
  };

  return (
    <Container className="mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Welcome, {getFullName()} ({user.role})</h2>
        <Button variant="danger" onClick={logout}>Logout</Button>
      </div>
      {renderDashboard()}
    </Container>
  );
};

export default Dashboard;