'use client';

import { useState, useEffect } from 'react';
import { Task } from '../types';
import { apiClient } from '../lib/api';
import { getToken, removeToken } from '../lib/auth-utils';
import { useRouter } from 'next/navigation';
import GlassCard from '@/components/GlassCard';
import NeonButton from '@/components/NeonButton';
import NeonInput from '@/components/NeonInput';

export default function Dashboard() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState({ title: '', description: '' });
  const [editingTask, setEditingTask] = useState<{ id: number; title: string; description?: string } | null>(null);
  const [savingTask, setSavingTask] = useState<number | null>(null); // Track saving state for specific tasks
  const [saveError, setSaveError] = useState<string | null>(null);
  const [togglingTask, setTogglingTask] = useState<number | null>(null); // Track toggling state for specific tasks
  const [deletingTask, setDeletingTask] = useState<number | null>(null); // Track deleting state for specific tasks
  const [isRefreshing, setIsRefreshing] = useState(false); // Track global refresh state
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const router = useRouter();

  // Check if user is authenticated on component mount
  useEffect(() => {
    const token = getToken();
    if (!token) {
      // Redirect to login if no token
      router.push('/login');
      return;
    }

    // Load tasks on component mount
    loadTasks();
  }, [router]);

  const loadTasks = async () => {
    try {
      const data = await apiClient.get<Task[]>('/api/tasks');
      // Normalize task IDs to numbers to handle potential type mismatches
      const normalizedData = data.map(task => ({
        ...task,
        id: Number(task.id)
      }));
      setTasks(normalizedData);
    } catch (error) {
      console.error('Failed to load tasks:', error);
      // If unauthorized, redirect to login
      if ((error as any).toString().includes('401')) {
        removeToken();
        router.push('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const refreshTasks = async () => {
    setIsRefreshing(true);
    try {
      const data = await apiClient.get<Task[]>('/api/tasks');
      // Normalize task IDs to numbers to handle potential type mismatches
      const normalizedData = data.map(task => ({
        ...task,
        id: Number(task.id)
      }));
      setTasks(normalizedData);
    } catch (error) {
      console.error('Failed to refresh tasks:', error);
      // If unauthorized, redirect to login
      if ((error as any).toString().includes('401')) {
        removeToken();
        router.push('/login');
      }
    } finally {
      setIsRefreshing(false);
    }
  };

  const createTask = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await apiClient.post<any>('/api/tasks', newTask);

      // If response is null (unexpected for create), we can't add the task
      if (response === null) {
        console.error('Create task returned null response');
        return;
      }

      // Normalize the new task's ID to number
      const normalizedTask = {
        ...response,
        id: Number(response.id)
      };
      setTasks(prevTasks => [...prevTasks, normalizedTask]);
      setNewTask({ title: '', description: '' });
    } catch (error) {
      console.error('Failed to create task:', error);
      // If unauthorized, redirect to login
      if ((error as any).toString().includes('401')) {
        removeToken();
        router.push('/login');
      }
    }
  };

  const toggleTaskCompletion = async (taskId: number) => {
    setTogglingTask(taskId);

    try {
      const response = await apiClient.patch<any>(`/api/tasks/${taskId}/complete`);

      // If the response is null (e.g., 204 No Content), we can still consider it successful
      // and optimistically update the task's completed status
      if (response === null) {
        // Update the task in the local state by flipping the completed status
        setTasks(prevTasks => prevTasks.map(task =>
          Number(task.id) === Number(taskId) ? { ...task, completed: !task.completed } : task
        ));
      } else {
        // Update the task in the local state using the response from the server
        setTasks(prevTasks => prevTasks.map(task =>
          Number(task.id) === Number(taskId) ? response : task
        ));
      }
    } catch (error) {
      console.error('Failed to update task:', error);
      // If unauthorized, redirect to login
      if ((error as any).toString().includes('401')) {
        removeToken();
        router.push('/login');
      }
    } finally {
      setTogglingTask(null);
    }
  };

  const deleteTask = async (taskId: number) => {
    // Prevent double deletion by checking if already deleting
    if (deletingTask === taskId) return;

    setDeletingTask(taskId);

    try {
      // Treat successful delete (even with null response for 204) as success
      await apiClient.delete(`/api/tasks/${taskId}`);

      // Remove the task from the local state using numeric comparison to handle potential type mismatches
      setTasks(prevTasks => prevTasks.filter(task => Number(task.id) !== Number(taskId)));
    } catch (error) {
      console.error('Failed to delete task:', error);
      // If unauthorized, redirect to login
      if ((error as any).toString().includes('401')) {
        removeToken();
        router.push('/login');
      }
    } finally {
      setDeletingTask(null);
    }
  };

  const startEditing = (task: Task) => {
    setEditingTask({
      id: Number(task.id), // Normalize to number
      title: task.title,
      description: task.description
    });
  };

  const cancelEditing = () => {
    setEditingTask(null);
  };

  const saveEditedTask = async (taskId: number) => {
    if (!editingTask || Number(editingTask.id) !== Number(taskId)) return;

    setSavingTask(taskId);
    setSaveError(null);

    try {
      const response = await apiClient.put<any>(`/api/tasks/${taskId}`, {
        title: editingTask.title,
        description: editingTask.description,
        completed: tasks.find(t => Number(t.id) === Number(taskId))?.completed
      });

      // If response is null (e.g., 204 No Content), we'll use the edited values
      const updatedTask = response || {
        ...tasks.find(t => Number(t.id) === Number(taskId)),
        title: editingTask.title,
        description: editingTask.description,
        completed: tasks.find(t => Number(t.id) === Number(taskId))?.completed
      };

      // Update the task in the local state using numeric comparison to handle potential type mismatches
      setTasks(prevTasks => prevTasks.map(task =>
        Number(task.id) === Number(taskId) ? updatedTask : task
      ));

      setEditingTask(null);
    } catch (error) {
      console.error('Failed to update task:', error);
      setSaveError('Failed to update task. Please try again.');

      // If unauthorized, redirect to login
      if ((error as any).toString().includes('401')) {
        removeToken();
        router.push('/login');
      }
    } finally {
      setSavingTask(null);
    }
  };

  const handleLogout = () => {
    removeToken();
    router.push('/login');
  };

  // Filter tasks based on search term and selected filter
  const filteredTasks = tasks.filter(task => {
    const matchesSearch =
      task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (task.description && task.description.toLowerCase().includes(searchTerm.toLowerCase()));

    if (filter === 'active') {
      return !task.completed && matchesSearch;
    } else if (filter === 'completed') {
      return task.completed && matchesSearch;
    } else {
      return matchesSearch;
    }
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 flex items-center justify-center">
        <div className="text-white text-2xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 p-4 sm:p-6 md:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 mb-2">
            Neon Tasks
          </h1>
          <p className="text-purple-200 text-lg">Manage your tasks in style</p>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <GlassCard className="text-center">
            <div className="text-2xl font-bold text-cyan-400">{tasks.length}</div>
            <div className="text-sm text-gray-300">Total Tasks</div>
          </GlassCard>
          <GlassCard className="text-center">
            <div className="text-2xl font-bold text-yellow-400">{tasks.filter(t => !t.completed).length}</div>
            <div className="text-sm text-gray-300">Active</div>
          </GlassCard>
          <GlassCard className="text-center">
            <div className="text-2xl font-bold text-green-400">{tasks.filter(t => t.completed).length}</div>
            <div className="text-sm text-gray-300">Completed</div>
          </GlassCard>
        </div>

        {/* Action Bar */}
        <div className="flex flex-col lg:flex-row gap-4 mb-8">
          {/* Search Input */}
          <div className="flex-1">
            <NeonInput
              type="text"
              placeholder="Search tasks..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          {/* Filter Tabs */}
          <div className="flex space-x-2 bg-white/10 backdrop-blur-lg rounded-xl p-1 border border-white/20">
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2 rounded-lg transition-all duration-300 ${
                filter === 'all'
                  ? 'bg-cyan-500 text-white shadow-lg shadow-cyan-500/30'
                  : 'text-gray-300 hover:text-white hover:bg-white/10'
              }`}
            >
              All
            </button>
            <button
              onClick={() => setFilter('active')}
              className={`px-4 py-2 rounded-lg transition-all duration-300 ${
                filter === 'active'
                  ? 'bg-cyan-500 text-white shadow-lg shadow-cyan-500/30'
                  : 'text-gray-300 hover:text-white hover:bg-white/10'
              }`}
            >
              Active
            </button>
            <button
              onClick={() => setFilter('completed')}
              className={`px-4 py-2 rounded-lg transition-all duration-300 ${
                filter === 'completed'
                  ? 'bg-cyan-500 text-white shadow-lg shadow-cyan-500/30'
                  : 'text-gray-300 hover:text-white hover:bg-white/10'
              }`}
            >
              Completed
            </button>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-2">
            <NeonButton
              onClick={() => router.push('/chat')}
              variant="primary"
            >
              Chat with AI
            </NeonButton>
            <NeonButton
              onClick={refreshTasks}
              disabled={isRefreshing}
              variant="secondary"
              isLoading={isRefreshing}
            >
              {isRefreshing ? 'Refreshing...' : 'Refresh'}
            </NeonButton>
            <NeonButton
              onClick={handleLogout}
              variant="danger"
            >
              Logout
            </NeonButton>
          </div>
        </div>

        {/* Task Creation Form */}
        <GlassCard className="mb-8 p-6">
          <form onSubmit={createTask}>
            <div className="mb-4">
              <NeonInput
                type="text"
                placeholder="Task title"
                value={newTask.title}
                onChange={(e) => setNewTask({...newTask, title: e.target.value})}
                className="mb-3"
                required
              />
              <NeonInput
                as="textarea"
                placeholder="Task description"
                value={newTask.description}
                onChange={(e) => setNewTask({...newTask, description: e.target.value})}
                rows={2}
              />
            </div>
            <NeonButton type="submit" variant="gradient">
              Add Task
            </NeonButton>
          </form>
        </GlassCard>

        {/* Task List */}
        <div>
          {filteredTasks.length === 0 ? (
            <div className="text-center py-16">
              <div className="text-6xl mb-4">✨</div>
              <h3 className="text-xl text-gray-300 mb-2">No tasks found</h3>
              <p className="text-gray-400">
                {searchTerm || filter !== 'all'
                  ? 'Try adjusting your search or filter'
                  : 'Create your first task to get started'}
              </p>
            </div>
          ) : (
            <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {filteredTasks.map((task) => (
                <GlassCard
                  key={task.id}
                  className={`p-5 transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl hover:shadow-cyan-500/20 ${
                    task.completed
                      ? 'opacity-60 bg-gradient-to-br from-green-900/20 to-emerald-900/20 border-green-500/30'
                      : 'hover:border-cyan-400/50'
                  }`}
                >
                  {editingTask?.id === task.id ? (
                    // Edit mode
                    <div className="flex flex-col space-y-4">
                      <NeonInput
                        type="text"
                        value={editingTask.title}
                        onChange={(e) => setEditingTask({...editingTask, title: e.target.value})}
                        autoFocus
                      />
                      <NeonInput
                        as="textarea"
                        value={editingTask.description || ''}
                        onChange={(e) => setEditingTask({...editingTask, description: e.target.value})}
                        rows={2}
                      />
                      {saveError && (
                        <div className="text-red-400 text-sm">{saveError}</div>
                      )}
                      <div className="flex space-x-2">
                        <NeonButton
                          onClick={() => saveEditedTask(task.id)}
                          disabled={savingTask === task.id}
                          variant="secondary"
                          isLoading={savingTask === task.id}
                          size="sm"
                        >
                          {savingTask === task.id ? 'Saving...' : 'Save'}
                        </NeonButton>
                        <NeonButton
                          onClick={cancelEditing}
                          disabled={savingTask === task.id}
                          variant="primary"
                          size="sm"
                        >
                          Cancel
                        </NeonButton>
                      </div>
                    </div>
                  ) : (
                    // View mode
                    <div className="flex flex-col h-full">
                      <div className="flex items-start mb-3">
                        <input
                          type="checkbox"
                          checked={task.completed}
                          onChange={() => toggleTaskCompletion(task.id)}
                          disabled={togglingTask === task.id}
                          className={`mt-1 mr-3 h-5 w-5 rounded cursor-pointer ${
                            togglingTask === task.id
                              ? 'cursor-not-allowed opacity-50'
                              : 'accent-cyan-500'
                          }`}
                        />
                        <div className="flex-1">
                          <h3 className={`font-semibold text-lg ${
                            task.completed
                              ? 'line-through text-gray-400'
                              : 'text-white'
                          }`}>
                            {task.title}
                          </h3>
                          {task.description && (
                            <p className={`mt-2 text-sm ${
                              task.completed
                                ? 'line-through text-gray-500'
                                : 'text-gray-300'
                            }`}>
                              {task.description}
                            </p>
                          )}
                        </div>
                      </div>

                      <div className="flex items-center justify-between mt-auto pt-3 border-t border-white/10">
                        <div className="flex items-center space-x-2">
                          {task.completed && (
                            <span className="px-2 py-1 bg-green-500/20 text-green-300 text-xs rounded-full border border-green-500/30">
                              Completed
                            </span>
                          )}
                          <span className="text-xs text-gray-400">
                            {new Date(task.created_at).toLocaleDateString()}
                          </span>
                        </div>

                        <div className="flex space-x-2">
                          <NeonButton
                            type="button"
                            onClick={() => startEditing(task)}
                            variant="secondary"
                            size="sm"
                            className="p-2 min-w-0"
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                            </svg>
                          </NeonButton>
                          <NeonButton
                            type="button"
                            onClick={(e) => {
                              e.preventDefault();
                              e.stopPropagation();
                              deleteTask(task.id);
                            }}
                            disabled={deletingTask === task.id}
                            variant="danger"
                            size="sm"
                            className="p-2 min-w-0"
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                            </svg>
                          </NeonButton>
                        </div>
                      </div>

                      {togglingTask === task.id && (
                        <div className="mt-2 text-xs text-cyan-400">Updating...</div>
                      )}
                    </div>
                  )}
                </GlassCard>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}