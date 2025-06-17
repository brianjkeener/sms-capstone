import React, { useContext } from 'react';
import AuthContext from '../context/AuthContext';
import { Button, Container, Spinner } from 'react-bootstrap';
import AdminDashboard from '../components/AdminDashboard';
import TeacherDashboard from '../components/TeacherDashboard';
import StudentDashboard from '../components/StudentDashboard';

const Dashboard = () => {
  const { user, fullUserProfile, logout } = useContext(AuthContext);

  if (!user || !fullUserProfile) {
    // Show a loading spinner while wait for the /users/me API call
    return (
      <Container className="d-flex justify-content-center align-items-center" style={{ height: '100vh' }}>
        <Spinner animation="border" />
      </Container>
    );
  }

  const getFullName = () => {
    // If the full profile has loaded, show the first and last name
    if (fullUserProfile) {
      return `${fullUserProfile.first_name} ${fullUserProfile.last_name}`;
    }
    // Otherwise, fall back to the email from the token
    return user.sub;
  };

  const renderDashboard = () => {
    switch (user.role) {
      case 'admin':
        return <AdminDashboard />;
      case 'teacher':
        return <TeacherDashboard />;
      case 'student':
        return <StudentDashboard />;
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