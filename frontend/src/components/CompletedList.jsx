import TaskCard from './TaskCard.jsx';
import { FiCheckCircle } from 'react-icons/fi';

export default function CompletedList({ tasks, onUpdate, onDelete, onToggle }) {
  if (tasks.length === 0) return null;

  return (
    <section className="section-completed">
      <div className="section-header">
        <FiCheckCircle />
        <h3>Completed</h3>
        <span className="task-count">{tasks.length}</span>
      </div>
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onUpdate={onUpdate}
          onDelete={onDelete}
          onToggle={onToggle}
        />
      ))}
    </section>
  );
}
