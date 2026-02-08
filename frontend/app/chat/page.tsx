'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getToken } from '@/lib/auth-utils';
import axios from 'axios';
import { getApiBase } from '@/lib/apiBase';
import ChatClient from './ChatClient';

const ChatPage = () => {
  const [userId, setUserId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const fetchUserId = async () => {
      // Check if user is authenticated using existing token system
      // First try the standard getToken function, then fallback to direct localStorage access
      let token = getToken();
      if (!token && typeof window !== 'undefined') {
        token = localStorage.getItem('token');
      }

      if (!token) {
        // If no token exists, redirect to login
        router.push('/login');
        return;
      }

      try {
        // Use the canonical API base resolver
        const API_BASE = getApiBase();

        // Call the backend /auth/me API to get user ID
        const response = await axios.get(`${API_BASE}/auth/me`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        });

        const userIdFromResponse = response.data.user_id;
        if (userIdFromResponse) {
          setUserId(Number(userIdFromResponse));
          setLoading(false);
        } else {
          // If no user ID found in response, redirect to login
          router.push('/login');
        }
      } catch (error) {
        console.error('Error fetching user info from /auth/me:', error);
        // If the /auth/me call fails (e.g., 401), redirect to login
        if (axios.isAxiosError(error) && error.response?.status === 401) {
          // Remove the invalid token
          if (typeof window !== 'undefined') {
            localStorage.removeItem('token');
          }
        }
        router.push('/login');
      }
    };

    fetchUserId();
  }, [router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl">Loading chat...</div>
      </div>
    );
  }

  if (!userId) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl">User not authenticated</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      <div className="container mx-auto px-4 py-8 flex-grow">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold text-white text-center mb-2">AI Todo Assistant</h1>
          <p className="text-center text-blue-200 mb-8">Chat with your AI assistant to manage your tasks</p>

          <div className="bg-white rounded-2xl shadow-2xl overflow-hidden" style={{ height: '70vh' }}>
            <ChatClient userId={userId} />
          </div>

          <div className="mt-6 text-center text-sm text-blue-200">
            <p>Examples: "Add a task to buy groceries", "Show me my tasks", "Mark task 1 as complete"</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;