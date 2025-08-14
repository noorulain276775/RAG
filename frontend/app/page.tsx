'use client'

import { useState, useRef } from 'react'
import { Upload, Send, FileText, Brain, MessageCircle, Settings } from 'lucide-react'
import DocumentUpload from '@/components/DocumentUpload'
import ChatInterface from '@/components/ChatInterface'
import DocumentList from '@/components/DocumentList'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'chat' | 'documents' | 'settings'>('chat')
  const [documents, setDocuments] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const handleDocumentUpload = async (files: File[]) => {
    setIsLoading(true)
    try {
      // Simulate API call for document upload
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      const newDocs = files.map((file, index) => ({
        id: Date.now() + index,
        name: file.name,
        size: file.size,
        type: file.type,
        uploadedAt: new Date().toISOString(),
        status: 'processed'
      }))
      
      setDocuments(prev => [...prev, ...newDocs])
    } catch (error) {
      console.error('Upload failed:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const tabs = [
    { id: 'chat', label: 'Chat', icon: MessageCircle },
    { id: 'documents', label: 'Documents', icon: FileText },
    { id: 'settings', label: 'Settings', icon: Settings }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="bg-primary-600 p-2 rounded-lg">
                <Brain className="h-6 w-6 text-white" />
              </div>
              <h1 className="text-xl font-bold text-gray-900">RAG System</h1>
            </div>
            <div className="text-sm text-gray-500">
              AI-Powered Document Q&A
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tab Navigation */}
        <div className="mb-8">
          <nav className="flex space-x-1 bg-white p-1 rounded-lg shadow-sm border border-gray-200">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                    activeTab === tab.id
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                </button>
              )
            })}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="animate-fade-in">
          {activeTab === 'chat' && (
            <div className="grid grid-cols-1 xl:grid-cols-4 gap-6">
              {/* Document Upload Sidebar */}
              <div className="xl:col-span-1 space-y-6">
                <DocumentUpload 
                  onUpload={handleDocumentUpload}
                  isLoading={isLoading}
                />
                <DocumentList documents={documents} />
              </div>
              
              {/* Chat Interface */}
              <div className="xl:col-span-3">
                <ChatInterface />
              </div>
            </div>
          )}

          {activeTab === 'documents' && (
            <div className="space-y-6">
              <div className="card">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Document Management</h2>
                <DocumentList documents={documents} />
              </div>
            </div>
          )}

          {activeTab === 'settings' && (
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">System Settings</h2>
              <div className="space-y-4">
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <h3 className="text-sm font-medium text-green-800">Free Local AI Active</h3>
                      <p className="text-sm text-green-700 mt-1">
                        Your system is using Ollama with local AI models. No API keys or costs required!
                      </p>
                    </div>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    AI Provider
                  </label>
                  <select className="input-field" disabled>
                    <option value="ollama">Ollama (Local - Free)</option>
                  </select>
                  <p className="text-sm text-gray-500 mt-1">
                    Currently using Ollama with llama2 model locally.
                  </p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Embedding Provider
                  </label>
                  <select className="input-field" disabled>
                    <option value="sentence-transformers">Sentence Transformers (Local - Free)</option>
                  </select>
                  <p className="text-sm text-gray-500 mt-1">
                    Using local sentence-transformers for document embeddings.
                  </p>
                </div>
                <div className="text-sm text-gray-600">
                  <p>✅ No API keys required</p>
                  <p>✅ Completely free to use</p>
                  <p>✅ Runs locally on your machine</p>
                  <p>✅ No internet dependency after setup</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
