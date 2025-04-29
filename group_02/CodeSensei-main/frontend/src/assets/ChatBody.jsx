import React, { useState, useEffect } from 'react'
import axios from 'axios'

import ChatRenderer from './ChatRenderer';

const ChatBody = (props) => {

    const [value, setValue] = useState("")
    const [chats, setChats] = useState([])
    const [loading, setLoading] = useState(false)
    const [placeholder, setPlaceholder] = useState("Type code or ask away...")

    useEffect(() => {
        if (props.option === "Explain") {
            setPlaceholder("Explain this code...")
        } else if (props.option === "Generate") {
            setPlaceholder("Generate code for me...")
        } else if (props.option === "Ask") {
            setPlaceholder("Ask me anything...")
        } else {
            setPlaceholder("Type code or ask away...")
        }
    }, [props.option])

    useEffect(() => {
        if (props.clear) {
            setChats([])
            setValue("")
        }
    }, [props.clear])

    const handleChange = (e) => {
        setValue(e.target.value)
    }

    const handleSubmit = async () => {
        if (value.trim() === "") return

        const newChat = {
            sender: "user",
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            chat: value
        }

        setChats((prevChats) => [...prevChats, newChat])
        setValue("")

        setLoading(true)
        const response = axios.post("http://localhost:8000/chat", { user: "user", message: value, prev: chats, option: props.option });
        response.then((res) => {
            console.log(res);
            setLoading(false)
            const newChat = {
                sender: "ai",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                chat: res.data
            }
            setChats((prevChats) => [...prevChats, newChat])
        }).catch((err) => {
            console.log(err)
        })

    }

    return (
        <div className='chat-body'>
            <div className={`chat-container ${props.darkmode ? "darkmode-chat-container" : ""}`}>
                <div>
                    {
                        chats.map((chat, index) => {
                            if (chat.sender === "user") {
                                return (
                                    <div key={index} className={`message message-${chat.sender}`}>
                                        <p>{chat.chat}</p>
                                        <span className="timestamp">{chat.timestamp}</span>
                                    </div>
                                )
                            } else {
                                return (
                                    <div key={index} className={`message message-${chat.sender} ${props.darkmode ? "darkmode-message" : ""}`}>
                                        <ChatRenderer chat={chat.chat} />
                                        <span className="timestamp">{chat.timestamp}</span>
                                    </div>
                                )
                            }
                        })

                    }
                    
                    {
                        loading && (<div className={`loader ${props.darkmode ? "darkmode-loader" : ""}`}></div>)
                    }
                </div>
            </div>
            <div className={`input-container ${props.darkmode ? "darkmode-input-container" : ""}`}>
                <textarea value={value} onChange={handleChange} id="input" placeholder={placeholder} rows="1"></textarea>
                <button className="send-btn" onClick={handleSubmit}>➤</button>
            </div>
        </div>
    )
}

export default ChatBody
