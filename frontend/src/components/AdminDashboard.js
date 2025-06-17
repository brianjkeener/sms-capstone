import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Table, Alert, Button } from 'react-bootstrap';
import UserForm from './UserForm'; // Import the new form component

const AdminDashboard = () => {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState('');
  
  // State for the modal form
  const [showModal, setShowModal] = useState(false);
  const [editingUser, setEditingUser] = useState(null);

  const fetchUsers = async () => {
    try {
      const response = await api.get('/users/');
      setUsers(response.data);
    } catch (err) {
      setError('Failed to fetch users.');
      console.error(err);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleShowCreateModal = () => {
    setEditingUser(null);
    setShowModal(true);
  };

  const handleShowEditModal = (user) => {
    setEditingUser(user);
    setShowModal(true);
  };

  const handleHideModal = () => {
    setShowModal(false);
    setEditingUser(null);
  };

  const handleSaveUser = async (userData) => {
    try {
      if (editingUser) {
        // Update existing user
        // Note: The backend PUT endpoint doesn't handle password changes, so we remove it.
        const { password, ...updateData } = userData;
        await api.put(`/users/${editingUser.user_id}`, updateData);
      } else {
        // Create new user
        await api.post('/users/', userData);
      }
      fetchUsers(); // Refresh the user list
      handleHideModal();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save user.');
      console.error(err);
    }
  };

  const handleDeleteUser = async (userId) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        await api.delete(`/users/${userId}`);
        fetchUsers(); // Refresh the user list
      } catch (err) {
        setError('Failed to delete user.');
        console.error(err);
      }
    }
  };

  return (
    <div>
      <h4>Admin Dashboard: User Management</h4>
      {error && <Alert variant="danger" onClose={() => setError('')} dismissible>{error}</Alert>}
      
      <Button variant="primary" onClick={handleShowCreateModal} className="mb-3">
        Create New User
      </Button>

      <UserForm
        show={showModal}
        onHide={handleHideModal}
        onSave={handleSaveUser}
        user={editingUser}
      />

      <h5>All Users</h5>
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>ID</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.user_id}>
              <td>{user.user_id}</td>
              <td>{user.first_name}</td>
              <td>{user.last_name}</td>
              <td>{user.email}</td>
              <td>{user.role}</td>
              <td>
                <Button variant="warning" size="sm" onClick={() => handleShowEditModal(user)} className="me-2">Edit</Button>
                <Button variant="danger" size="sm" onClick={() => handleDeleteUser(user.user_id)}>Delete</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default AdminDashboard;