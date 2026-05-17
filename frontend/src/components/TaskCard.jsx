import { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { FiEdit2, FiTrash2, FiCheck, FiX, FiCalendar } from 'react-icons/fi';

export default function TaskCard({ task, onUpdate, onDelete, onToggle }) {
  const [editing, setEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDate, setEditDate] = useState(
    task.due_date ? new Date(task.due_date) : null
  );

  const handleSave = () => {
    if (!editTitle.trim()) return;
    onUpdate(task.id, {
      title: editTitle.trim(),
      due_date: editDate ? editDate.toISOString().split('T')[0] : null,
      completed: task.completed,
    });
    setEditing(false);
  };

  const handleCancel = () => {
    setEditTitle(task.title);
    setEditDate(task.due_date ? new Date(task.due_date) : null);
    setEditing(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSave();
    if (e.key === 'Escape') handleCancel();
  };

  // Format due date for display
  const formatDate = (dateStr) => {
    if (!dateStr) return null;
    const d = new Date(dateStr);
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  // Check if overdue
  const isOverdue = () => {
    if (!task.due_date || task.completed) return false;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return new Date(task.due_date) < today;
  };

  return (
    <div className={`task-card ${task.completed ? 'completed' : ''}`}>
      {/* Checkbox */}
      <label className="task-checkbox">
        <input
          type="checkbox"
          checked={!!task.completed}
          onChange={() => onToggle(task.id, task.completed)}
        />
        <span className="checkmark">
          {task.completed && <FiCheck />}
        </span>
      </label>

      {editing ? (
        /* Edit Mode */
        <div className="task-edit-form">
          <input
            className="task-edit-input"
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            onKeyDown={handleKeyDown}
            autoFocus
          />
          <div className="task-edit-date">
            <DatePicker
              selected={editDate}
              onChange={(date) => setEditDate(date)}
              placeholderText="Date"
              dateFormat="MMM d, yyyy"
              isClearable
            />
          </div>
          <button className="btn-save" onClick={handleSave} title="Save">
            <FiCheck />
          </button>
          <button className="btn-cancel" onClick={handleCancel} title="Cancel">
            <FiX />
          </button>
        </div>
      ) : (
        /* Display Mode */
        <>
          <div className="task-content">
            <div className="task-title">{task.title}</div>
            {task.due_date && (
              <div className={`task-date ${isOverdue() ? 'overdue' : ''}`}>
                <FiCalendar size={11} />
                {formatDate(task.due_date)}
              </div>
            )}
          </div>
          <div className="task-actions">
            {!task.completed && (
              <button
                className="btn-icon edit"
                onClick={() => setEditing(true)}
                title="Edit task"
              >
                <FiEdit2 />
              </button>
            )}
            <button
              className="btn-icon delete"
              onClick={() => onDelete(task.id)}
              title="Delete task"
            >
              <FiTrash2 />
            </button>
          </div>
        </>
      )}
    </div>
  );
}
