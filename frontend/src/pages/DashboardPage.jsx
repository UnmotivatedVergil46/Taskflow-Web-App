import { useState, useEffect, useCallback } from 'react';
import api from '../api/axios.js';
import Navbar from '../components/Navbar.jsx';
import TaskForm from '../components/TaskForm.jsx';
import TaskList from '../components/TaskList.jsx';
import CompletedList from '../components/CompletedList.jsx';

export default function DashboardPage() {
  const [tasks, setTasks] = useState([]);

  const fetchTasks = useCallback(async () => {
    try {
      const res = await api.get('/tasks');
      setTasks(res.data);
    } catch (err) {
      console.error('Failed to fetch tasks:', err);
    }
  }, []);

  useEffect(() => { fetchTasks(); }, [fetchTasks]);

  const addTask = async (title, dueDate) => {
    try {
      const res = await api.post('/tasks', {
        title,
        due_date: dueDate ? dueDate.toISOString().split('T')[0] : null,
      });
      setTasks((prev) => [res.data, ...prev]);
    } catch (err) {
      console.error('Failed to add task:', err);
    }
  };

  const updateTask = async (id, updates) => {
    try {
      const res = await api.put(`/tasks/${id}`, updates);
      setTasks((prev) => prev.map((t) => (t.id === id ? res.data : t)));
    } catch (err) {
      console.error('Failed to update task:', err);
    }
  };

  const deleteTask = async (id) => {
    try {
      await api.delete(`/tasks/${id}`);
      setTasks((prev) => prev.filter((t) => t.id !== id));
    } catch (err) {
      console.error('Failed to delete task:', err);
    }
  };

  const toggleComplete = async (id, currentStatus) => {
    await updateTask(id, { completed: !currentStatus });
  };

  const activeTasks = tasks.filter((t) => !t.completed);
  const completedTasks = tasks.filter((t) => t.completed);

  return (
    <>
      <Navbar />
      <main className="dashboard">
        <div className="dashboard-header">
          <h2>My Tasks</h2>
          <p>Stay organized and get things done.</p>
        </div>
        <TaskForm onAdd={addTask} />
        <TaskList
          tasks={activeTasks}
          onUpdate={updateTask}
          onDelete={deleteTask}
          onToggle={toggleComplete}
        />
        <CompletedList
          tasks={completedTasks}
          onUpdate={updateTask}
          onDelete={deleteTask}
          onToggle={toggleComplete}
        />
      </main>
    </>
  );
}
