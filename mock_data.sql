-- To avoid errors if you run this script multiple times, this script will clear out existing data first.
-- The TRUNCATE command is fast but unstable
TRUNCATE TABLE grades, enrollments, classes, users, subjects, classrooms RESTART IDENTITY CASCADE;

-- ====================================================================================
-- Step 1: Insert Users (Admins, Teachers, Students)
-- ====================================================================================
-- For all users, the password is 'password123'
-- The hash is: '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G'

-- Admins (2)
INSERT INTO users (first_name, last_name, email, password_hash, role) VALUES
('Admin', 'User', 'admin@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'admin'),
('Brian', 'Root', 'brian.root@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'admin');

-- Teachers (4)
INSERT INTO users (first_name, last_name, email, password_hash, role) VALUES
('Eleanor', 'Vance', 'eleanor.vance@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'teacher'),
('Theodora', 'Crane', 'theodora.crane@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'teacher'),
('Luke', 'Sanderson', 'luke.sanderson@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'teacher'),
('Steven', 'Crain', 'steven.crain@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'teacher');

-- Students (15)
INSERT INTO users (first_name, last_name, email, password_hash, role) VALUES
('Olivia', 'Crain', 'olivia.crain@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'student'),
('Shirley', 'Jackson', 'shirley.jackson@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'student'),
('Hugh', 'Crain', 'hugh.crain@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'student'),
('Abigail', 'Dudley', 'abigail.dudley@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'student'),
('Arthur', 'Vance', 'arthur.vance@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'student'),
('Clara', 'Dudley', 'clara.dudley@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'student'),
('William', 'Hill', 'william.hill@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'student'),
('Poppy', 'Hill', 'poppy.hill@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'student'),
('Janet', 'Doe', 'janet.doe@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'student'),
('Mike', 'Flanagan', 'mike.flanagan@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'student'),
('Kate', 'Siegel', 'kate.siegel@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'student'),
('Henry', 'Thomas', 'henry.thomas@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'student'),
('Victoria', 'Pedretti', 'victoria.pedretti@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'student'),
('Carla', 'Gugino', 'carla.gugino@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'student'),
('Samantha', 'Sloyan', 'samantha.sloyan@school.com', '$2b$12$EixZa6S4E1nC4L5i5PpLteO95p6pGjHoL5zYwzKrv3sJ4iS3j8s9G', 'student');


-- ====================================================================================
-- Step 2: Insert Classrooms and Subjects
-- ====================================================================================
INSERT INTO classrooms (room_number, capacity) VALUES
('101', 30),
('102', 30),
('201-A', 25),
('201-B', 25),
('Lab A', 20),
('Library', 40);

INSERT INTO subjects (subject_name) VALUES
('Mathematics'),
('History'),
('Physics'),
('Literature'),
('Computer Science'),
('Art History');

-- ====================================================================================
-- Step 3: Create Classes (Assign Teachers to Subjects/Classrooms)
-- ====================================================================================
-- Note: User IDs 3, 4, 5, 6 are teachers.
INSERT INTO classes (subject_id, teacher_id, classroom_id) VALUES
(1, 3, 1), -- Eleanor Vance teaches Mathematics in Room 101
(2, 4, 2), -- Theodora Crane teaches History in Room 102
(3, 5, 5), -- Luke Sanderson teaches Physics in Lab A
(4, 3, 1), -- Eleanor Vance also teaches Literature in Room 101
(5, 6, 5); -- Steven Crain teaches Computer Science in Lab A


-- ====================================================================================
-- Step 4: Enroll Students in Classes
-- ====================================================================================
-- Note: User IDs 7 through 21 are students.
-- Enroll students in Mathematics (Class ID 1)
INSERT INTO enrollments (student_id, class_id) VALUES
(7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1);

-- Enroll students in History (Class ID 2)
INSERT INTO enrollments (student_id, class_id) VALUES
(13, 2), (14, 2), (15, 2), (16, 2), (17, 2), (18, 2);

-- Enroll students in Physics (Class ID 3)
INSERT INTO enrollments (student_id, class_id) VALUES
(19, 3), (20, 3), (21, 3), (7, 3), (8, 3);

-- Enroll students in Literature (Class ID 4)
INSERT INTO enrollments (student_id, class_id) VALUES
(9, 4), (10, 4), (11, 4), (12, 4);

-- Enroll students in Computer Science (Class ID 5)
INSERT INTO enrollments (student_id, class_id) VALUES
(13, 5), (14, 5), (15, 5), (16, 5), (17, 5), (18, 5), (19, 5), (20, 5), (21, 5);

-- ====================================================================================
-- Step 5: Add Some Grades for the Enrollments
-- ====================================================================================
-- Note: The enrollment_id corresponds to the order of insertion above.
-- Grades for Mathematics (Enrollment IDs 1-6)
INSERT INTO grades (enrollment_id, grade, comments) VALUES
(1, 95.50, 'Excellent grasp of calculus.'),
(2, 88.00, 'Good work, needs to show more steps.'),
(3, 76.50, 'Struggled with the final exam but passed.'),
(4, 99.00, 'Top of the class.');

-- Grades for History (Enrollment IDs 7-12)
INSERT INTO grades (enrollment_id, grade, comments) VALUES
(7, 82.00, 'Very good essay on the Roman Empire.'),
(8, 91.50, 'Insightful analysis and well-researched.'),
(9, 85.00, 'Solid performance throughout the semester.');

-- Grades for Physics (Enrollment IDs 13-17)
INSERT INTO grades (enrollment_id, grade, comments) VALUES
(13, 94.00, 'Exceptional lab work.'),
(14, 89.50, 'Strong understanding of quantum mechanics.');