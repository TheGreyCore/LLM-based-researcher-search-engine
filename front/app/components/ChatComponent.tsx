'use client'
import React, { useState, useRef, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { SendHorizonal } from 'lucide-react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'

type Message = {
  id: string
  text: string
  sender: 'user' | 'bot'
  timestamp: number
}

export default function ChatComponent() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputMessage, setInputMessage] = useState<string>('')
  const messagesEndRef = useRef<null | HTMLDivElement>(null)

  const generateId = () => {
    return Math.random().toString(36).substr(2, 9)
  }

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const generateBotResponse = async (userMessage: string): Promise<string> => {
    try {
      const response = await axios.get(`http://localhost:5000/prompt`, {
        params: {
          prompt: userMessage,
          key: 'forTesting'
        }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching bot response:', error)
      return 'Sorry, there was an error processing your request.'
    }
  }

  const handleSendMessage = async () => {
    if (inputMessage.trim() === '') return

    const userMessage: Message = {
      id: generateId(),
      text: inputMessage,
      sender: 'user',
      timestamp: Date.now()
    }
    setMessages(prevMessages => [...prevMessages, userMessage])
    setInputMessage('')

    try {
      const botResponseText = await generateBotResponse(inputMessage)
      const botMessage: Message = {
        id: generateId(),
        text: botResponseText,
        sender: 'bot',
        timestamp: Date.now()
      }

      setTimeout(() => {
        setMessages(prevMessages => [...prevMessages, botMessage])
      }, 500)
    } catch (error) {
      console.error('Error in handleSendMessage:', error)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-background p-4">
      <div className="w-[800px] h-[700px] flex flex-col border rounded-xl shadow-lg bg-card">
        {/* Chat Header */}
        <div className="p-4 border-b text-center font-semibold">
          Researcher Search Engine
        </div>
        {/* Chat Messages Container */}
        <div className="flex-grow overflow-auto p-4 space-y-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${
                msg.sender === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`max-w-[80%] p-3 rounded-2xl ${
                  msg.sender === 'user'
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-secondary text-secondary-foreground'
                }`}
              >
                {msg.sender === 'bot' ? (
                  <ReactMarkdown 
                    components={{
                      h2: ({node, ...props}) => (
                        <h2 className="text-lg font-bold mb-2" {...props} />
                      ),
                      strong: ({node, ...props}) => (
                        <strong className="font-bold" {...props} />
                      ),
                      em: ({node, ...props}) => (
                        <em className="italic" {...props} />
                      ),
                      li: ({node, ...props}) => (
                        <li className="ml-4 list-disc" {...props} />
                      )
                    }}
                  >
                    {msg.text}
                  </ReactMarkdown>
                ) : (
                  msg.text
                )}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        {/* Input Container */}
        <div className="p-4 border-t">
          <div className="relative">
            <Textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message..."
              className="pr-12 resize-none"
              rows={3}
            />
            <Button
              onClick={handleSendMessage}
              size="icon"
              variant="ghost"
              className="absolute bottom-2 right-2 h-8 w-8"
              disabled={inputMessage.trim() === ''}
            >
              <SendHorizonal className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}