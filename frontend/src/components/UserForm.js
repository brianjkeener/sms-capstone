import React, { useState, useEffect } from 'react';
import { Form, Button, Modal } from 'react-bootstrap';

const UserForm = ({ show, onHide, onSave, user }) => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    role: 'student',
  });

  const isEditing = user !== null;

  useEffect(() => {
    if (isEditing) {
      setFormData({
        first_name: user.first_name,
        last_name: user.last_name,
        email: user.email,
        password: '', // Don't pre-fill password
        role: user.role,
      });
    } else {
      // Reset form for creating new user
      setFormData({
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        role: 'student',
      });
    }
  }, [user, show]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>{isEditing ? 'Edit User' : 'Create New User'}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>First Name</Form.Label>
            <Form.Control type="text" name="first_name" value={formData.first_name} onChange={handleChange} required />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Last Name</Form.Label>
            <Form.Control type="text" name="last_name" value={formData.last_name} onChange={handleChange} required />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Email</Form.Label>
            <Form.Control type="email" name="email" value={formData.email} onChange={handleChange} required />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" name="password" value={formData.password} onChange={handleChange} required={!isEditing} placeholder={isEditing ? 'Leave blank to keep current password' : ''} />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Role</Form.Label>
            <Form.Select name="role" value={formData.role} onChange={handleChange}>
              <option value="student">Student</option>
              <option value="teacher">Teacher</option>
              <option value="admin">Admin</option>
            </Form.Select>
          </Form.Group>
          <Button variant="secondary" onClick={onHide} className="me-2">Cancel</Button>
          <Button variant="primary" type="submit">Save</Button>
        </Form>
      </Modal.Body>
    </Modal>
  );
};

export default UserForm;