'use client'

import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, FileText, Copy, Check } from 'lucide-react'

interface Message {
  id: string
  type: 'user' | 'assistant'
  content: string
  timestamp: Date
  sources?: Array<{
    title: string
    content: string
    score: number
  }>
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'assistant',
      content: 'Hello! I\'m your AI assistant. Upload some documents and I\'ll be able to answer questions about them with full context awareness.',
      timestamp: new Date()
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [copiedId, setCopiedId] = useState<string | null>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputValue.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      // Call the actual RAG system API with timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 120000); // 2 minutes timeout
      
      try {
        const response = await fetch('http://localhost:8000/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            question: inputValue,
            k: 3
          }),
          signal: controller.signal
        });
        
        clearTimeout(timeoutId);
      
        if (!response.ok) {
          throw new Error(`Chat failed: ${response.statusText}`)
        }
        
        const ragResponse = await response.json()
        
        // Create response message from actual RAG system
        const assistantResponse: Message = {
          id: (Date.now() + 1).toString(),
          type: 'assistant',
          content: ragResponse.answer,
          timestamp: new Date(),
          sources: ragResponse.sources.map((source: any) => ({
            title: source.metadata?.source || 'Document',
            content: source.page_content || source.content || '',
            score: source.score || 0.95
          }))
        }

        setMessages(prev => [...prev, assistantResponse])
      } catch (error: any) {
        let errorContent = 'Sorry, I encountered an error while processing your question. Please try again or check your configuration.';
        
        if (error.name === 'AbortError') {
          errorContent = 'The request timed out. This might be because Ollama is taking too long to respond. Please try asking a simpler question or check if Ollama is running properly.';
        } else if (error.message) {
          errorContent = `Error: ${error.message}`;
        }
        
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          type: 'assistant',
          content: errorContent,
          timestamp: new Date()
        }
        setMessages(prev => [...prev, errorMessage])
      }
    } finally {
      setIsLoading(false)
    }
  }

  const copyToClipboard = async (text: string, messageId: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedId(messageId)
      setTimeout(() => setCopiedId(null), 2000)
    } catch (err) {
      console.error('Failed to copy text: ', err)
    }
  }

  const formatTimestamp = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <div className="card h-[600px] flex flex-col">
      <div className="flex items-center space-x-2 mb-4">
        <Bot className="h-5 w-5 text-primary-600" />
        <h3 className="text-lg font-semibold text-gray-900">AI Chat Assistant</h3>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`flex items-start space-x-3 max-w-[80%] ${message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
              <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                message.type === 'user' 
                  ? 'bg-primary-600 text-white' 
                  : 'bg-gray-200 text-gray-700'
              }`}>
                {message.type === 'user' ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
              </div>
              
              <div className={`rounded-lg p-3 ${
                message.type === 'user'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs opacity-75">
                    {message.type === 'user' ? 'You' : 'AI Assistant'}
                  </span>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs opacity-75">
                      {formatTimestamp(message.timestamp)}
                    </span>
                    <button
                      onClick={() => copyToClipboard(message.content, message.id)}
                      className="opacity-60 hover:opacity-100 transition-opacity"
                    >
                      {copiedId === message.id ? (
                        <Check className="h-3 w-3" />
                      ) : (
                        <Copy className="h-3 w-3" />
                      )}
                    </button>
                  </div>
                </div>
                
                <div className="whitespace-pre-wrap text-sm">
                  {message.content}
                </div>

                {/* Sources */}
                {message.sources && message.sources.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <p className="text-xs font-medium mb-2 text-gray-600">Sources:</p>
                    <div className="space-y-2">
                      {message.sources.map((source, index) => (
                        <div key={index} className="bg-white bg-opacity-50 rounded p-2">
                          <div className="flex items-center space-x-2 mb-1">
                            <FileText className="h-3 w-3 text-gray-500" />
                            <span className="text-xs font-medium text-gray-700">
                              {source.title}
                            </span>
                            <span className="text-xs text-gray-500">
                              (Score: {source.score.toFixed(2)})
                            </span>
                          </div>
                          <p className="text-xs text-gray-600 line-clamp-2">
                            {source.content}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}

        {/* Loading indicator */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
                <Bot className="h-4 w-4 text-gray-700" />
              </div>
              <div className="bg-gray-100 rounded-lg p-3">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="flex space-x-3">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question about your documents..."
          className="flex-1 input-field"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={!inputValue.trim() || isLoading}
          className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Send className="h-4 w-4" />
        </button>
      </form>

      {/* Chat Tips */}
      <div className="mt-4 p-3 bg-blue-50 rounded-lg">
        <p className="text-xs text-blue-700">
          💡 <strong>Tip:</strong> Ask specific questions about your uploaded documents. 
          The AI will search through your content and provide contextual answers.
        </p>
      </div>
    </div>
  )
}
