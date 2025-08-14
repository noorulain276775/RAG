'use client'

import { useState } from 'react'
import { FileText, Trash2, Eye, Download, Calendar, File } from 'lucide-react'

interface Document {
  id: number
  name: string
  size: number
  type: string
  uploadedAt: string
  status: string
}

interface DocumentListProps {
  documents: Document[]
}

export default function DocumentList({ documents }: DocumentListProps) {
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(null)

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getFileIcon = (type: string) => {
    if (type.includes('pdf')) return '📄'
    if (type.includes('text') || type.includes('markdown')) return '📝'
    if (type.includes('word') || type.includes('document')) return '📄'
    if (type.includes('image')) return '🖼️'
    if (type.includes('code')) return '💻'
    return '📁'
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'processed':
        return 'bg-green-100 text-green-800'
      case 'processing':
        return 'bg-yellow-100 text-yellow-800'
      case 'error':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  if (documents.length === 0) {
    return (
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <FileText className="h-5 w-5 mr-2 text-primary-600" />
          Documents
        </h3>
        <div className="text-center py-8">
          <FileText className="h-12 w-12 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500 mb-2">No documents uploaded yet</p>
          <p className="text-sm text-gray-400">
            Upload some documents to get started with AI-powered Q&A
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="card max-w-full overflow-hidden">
      <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center justify-between">
        <div className="flex items-center">
          <FileText className="h-5 w-5 mr-2 text-primary-600" />
          Documents ({documents.length})
        </div>
      </h3>

      <div className="space-y-3 max-w-full">
        {documents.map((doc) => (
          <div
            key={doc.id}
            className="border border-gray-200 rounded-lg p-3 hover:bg-gray-50 transition-colors cursor-pointer w-full"
            onClick={() => setSelectedDocument(doc)}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-3 flex-1 min-w-0">
                <span className="text-lg flex-shrink-0">{getFileIcon(doc.type)}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 break-words leading-tight">
                    {doc.name}
                  </p>
                  <div className="flex flex-col sm:flex-row sm:items-center sm:space-x-4 text-xs text-gray-500 mt-1 space-y-1 sm:space-y-0">
                    <span className="flex items-center">
                      <File className="h-3 w-3 mr-1 flex-shrink-0" />
                      <span className="truncate">{formatFileSize(doc.size)}</span>
                    </span>
                    <span className="flex items-center">
                      <Calendar className="h-3 w-3 mr-1 flex-shrink-0" />
                      <span className="truncate">{formatDate(doc.uploadedAt)}</span>
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="flex items-center space-x-2 flex-shrink-0">
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(doc.status)}`}>
                  {doc.status}
                </span>
                <div className="flex space-x-1">
                  <button
                    className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                    title="View document"
                  >
                    <Eye className="h-4 w-4" />
                  </button>
                  <button
                    className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                    title="Download document"
                  >
                    <Download className="h-4 w-4" />
                  </button>
                  <button
                    className="p-1 text-red-400 hover:text-red-600 transition-colors"
                    title="Delete document"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Document Details Modal */}
      {selectedDocument && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Document Details</h3>
              <button
                onClick={() => setSelectedDocument(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>
            
            <div className="space-y-3">
              <div>
                <label className="text-sm font-medium text-gray-700">Name</label>
                <p className="text-sm text-gray-900">{selectedDocument.name}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700">Type</label>
                <p className="text-sm text-gray-900">{selectedDocument.type}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700">Size</label>
                <p className="text-sm text-gray-900">{formatFileSize(selectedDocument.size)}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700">Uploaded</label>
                <p className="text-sm text-gray-900">{formatDate(selectedDocument.uploadedAt)}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700">Status</label>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(selectedDocument.status)}`}>
                  {selectedDocument.status}
                </span>
              </div>
            </div>
            
            <div className="flex space-x-3 mt-6">
              <button className="btn-secondary flex-1">Download</button>
              <button className="btn-primary flex-1">View Content</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
