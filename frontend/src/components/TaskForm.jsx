import { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { FiPlus } from 'react-icons/fi';

export default function TaskForm({ onAdd }) {
  const [title, setTitle] = useState('');
  const [dueDate, setDueDate] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    onAdd(title.trim(), dueDate);
    setTitle('');
    setDueDate(null);
  };

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <div className="task-form-input-wrapper">
        <input
          id="task-input"
          className="task-form-input"
          type="text"
          placeholder="What needs to be done?"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
      </div>
      <div className="date-picker-wrapper">
        <DatePicker
          selected={dueDate}
          onChange={(date) => setDueDate(date)}
          placeholderText="Due date"
          dateFormat="MMM d, yyyy"
          minDate={new Date()}
          isClearable
        />
      </div>
      <button type="submit" className="btn-add-task" id="add-task-btn">
        <FiPlus /> Add Task
      </button>
    </form>
  );
}
