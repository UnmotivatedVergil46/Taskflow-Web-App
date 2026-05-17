import TaskCard from './TaskCard.jsx';
import { FiList } from 'react-icons/fi';

export default function TaskList({ tasks, onUpdate, onDelete, onToggle }) {
  return (
    <section className="section-active">
      <div className="section-header">
        <FiList />
        <h3>Active Tasks</h3>
        <span className="task-count">{tasks.length}</span>
      </div>
      {tasks.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🎯</div>
          <p>No active tasks. Add one above to get started!</p>
        </div>
      ) : (
        tasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            onUpdate={onUpdate}
            onDelete={onDelete}
            onToggle={onToggle}
          />
        ))
      )}
    </section>
  );
}
