import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Table, Alert, Spinner } from 'react-bootstrap';

const StudentDashboard = () => {
  const [grades, setGrades] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchGrades = async () => {
      try {
        setLoading(true);
        // This API call gets the grades for the currently logged-in user
        const response = await api.get('/grades/me');
        setGrades(response.data);
      } catch (err) {
        setError('Failed to fetch your grades.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchGrades();
  }, []); // The empty array means this runs once when the component mounts

  if (loading) {
    return <Spinner animation="border" />;
  }

  if (error) {
    return <Alert variant="danger">{error}</Alert>;
  }

  return (
    <div>
      <h4>My Grades</h4>
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>Subject</th>
            <th>Teacher</th>
            <th>Grade</th>
            <th>Comments</th>
          </tr>
        </thead>
        <tbody>
          {grades.length > 0 ? (
            grades.map((gradeInfo, index) => (
              <tr key={index}>
                <td>{gradeInfo.subject_name}</td>
                <td>{gradeInfo.teacher_name}</td>
                <td>{gradeInfo.grade !== null ? gradeInfo.grade : 'Not Graded Yet'}</td>
                <td>{gradeInfo.comments}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4" className="text-center">You do not have any grades recorded.</td>
            </tr>
          )}
        </tbody>
      </Table>
    </div>
  );
};

export default StudentDashboard;