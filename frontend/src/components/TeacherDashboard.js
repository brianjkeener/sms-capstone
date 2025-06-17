import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Table, Alert, Button, Form, Spinner } from 'react-bootstrap';

const TeacherDashboard = () => {
  const [myClasses, setMyClasses] = useState([]);
  const [selectedClassId, setSelectedClassId] = useState('');
  const [students, setStudents] = useState([]);
  const [grades, setGrades] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch the teacher's classes when the component loads
  useEffect(() => {
    const fetchMyClasses = async () => {
      try {
        const response = await api.get('/classes/me');
        setMyClasses(response.data);
      } catch (err) {
        setError('Failed to fetch your classes.');
      }
    };
    fetchMyClasses();
  }, []);

  // Fetch students when a class is selected
  useEffect(() => {
    if (!selectedClassId) {
      setStudents([]);
      return;
    }

    const fetchStudents = async () => {
      setLoading(true);
      setError('');
      try {
        const response = await api.get(`/classes/${selectedClassId}/students`);
        setStudents(response.data);
        // Initialize the grades state with fetched grades
        const initialGrades = response.data.reduce((acc, student) => {
          acc[student.user_id] = {
            grade: student.grade || '',
            comments: student.comments || ''
          };
          return acc;
        }, {});
        setGrades(initialGrades);
      } catch (err) {
        setError('Failed to fetch students for this class.');
      } finally {
        setLoading(false);
      }
    };

    fetchStudents();
  }, [selectedClassId]);

  const handleGradeChange = (studentId, field, value) => {
    setGrades(prev => ({
      ...prev,
      [studentId]: { ...prev[studentId], [field]: value }
    }));
  };

  const handleSaveGrade = async (studentId) => {
    const gradeData = {
      student_id: studentId,
      class_id: selectedClassId,
      grade: grades[studentId].grade,
      comments: grades[studentId].comments
    };
    try {
      await api.post('/grades/', gradeData);
      alert('Grade saved successfully!');
    } catch (err) {
      alert('Failed to save grade.');
    }
  };

  return (
    <div>
      <h4>Teacher Dashboard</h4>
      {error && <Alert variant="danger">{error}</Alert>}

      <Form.Group className="mb-3">
        <Form.Label>Select a Class to Manage</Form.Label>
        <Form.Select onChange={(e) => setSelectedClassId(e.target.value)} value={selectedClassId}>
          <option value="">-- Please select a class --</option>
          {myClasses.map(c => (
            <option key={c.class_id} value={c.class_id}>
              {c.subject_name} (Room: {c.room_number})
            </option>
          ))}
        </Form.Select>
      </Form.Group>

      {loading && <Spinner animation="border" />}
      
      {!loading && students.length > 0 && (
        <>
          <h5>Student Roster</h5>
          <Table striped bordered hover responsive>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Grade</th>
                <th>Comments</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {students.map(student => (
                <tr key={student.user_id}>
                  <td>{student.user_id}</td>
                  <td>{student.first_name} {student.last_name}</td>
                  <td>
                    <Form.Control
                      type="number"
                      step="0.01"
                      value={grades[student.user_id]?.grade || ''}
                      onChange={(e) => handleGradeChange(student.user_id, 'grade', e.target.value)}
                    />
                  </td>
                  <td>
                    <Form.Control
                      type="text"
                      value={grades[student.user_id]?.comments || ''}
                      onChange={(e) => handleGradeChange(student.user_id, 'comments', e.target.value)}
                    />
                  </td>
                  <td>
                    <Button variant="success" size="sm" onClick={() => handleSaveGrade(student.user_id)}>Save</Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </>
      )}
    </div>
  );
};

export default TeacherDashboard;