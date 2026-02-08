'use client';

import React, { useState, useRef, useEffect } from 'react';
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  ConversationHeader,
  Conversation,
} from '@chatscope/chat-ui-kit-react';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import axios from 'axios';
import { getApiBase } from '@/lib/apiBase';

interface Message {
  id: number;
  role: string;
  content: string;
  timestamp: string;
  tool_calls?: any[];
  tool_responses?: any[];
}

interface ChatClientProps {
  userId: number | null;
}

const ChatClient: React.FC<ChatClientProps> = ({ userId }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      role: 'assistant',
      content: 'Hello! I\'m your AI assistant for managing your todo list. How can I help you today?',
      timestamp: new Date().toISOString(),
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messageEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (message: string) => {
    if (!message.trim()) return;

    // Safety check: ensure userId is available before sending
    if (!userId) {
      const errorMessage: Message = {
        id: messages.length + 1,
        role: 'assistant',
        content: 'Unable to send message. User authentication required.',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, errorMessage]);
      return;
    }

    // Add user message to the list
    const userMessage: Message = {
      id: messages.length + 1,
      role: 'user',
      content: message,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Use the canonical API base resolver
      const API_BASE = getApiBase();

      // Call the backend chat API
      const response = await axios.post(`${API_BASE}/api/${userId}/chat`, {
        message: message
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        }
      });

      const assistantMessage: Message = {
        id: messages.length + 2,
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date().toISOString(),
        tool_calls: response.data.messages.slice(-1)[0]?.tool_calls || [],
        tool_responses: response.data.messages.slice(-1)[0]?.tool_responses || [],
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage: Message = {
        id: messages.length + 2,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-full flex flex-col">
      <MainContainer>
        <ChatContainer>
          <ConversationHeader>
            <Conversation.Info avatar="🤖" name="AI Todo Assistant" />
          </ConversationHeader>

          <MessageList>
            {messages.map((msg) => (
              <Message
                key={msg.id}
                model={{
                  message: msg.content,
                  sender: msg.role,
                  direction: msg.role === 'user' ? 'outgoing' : 'incoming',
                }}
              >
                <Message.Footer sentTime={new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} />
              </Message>
            ))}

            {isLoading && (
              <Message
                model={{
                  message: "Thinking...",
                  sender: 'AI Assistant',
                  direction: 'incoming',
                }}
              >
                <Message.Footer sentTime={new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} />
              </Message>
            )}

            <div ref={messageEndRef} />
          </MessageList>

          <MessageInput
            placeholder="Type your message here..."
            onSend={handleSend}
            disabled={isLoading}
          />
        </ChatContainer>
      </MainContainer>
    </div>
  );
};

export default ChatClient;