import React, { useState } from 'react'
import ChatBody from './ChatBody'

import Modal from 'react-bootstrap/Modal';

const Chat = () => {
    const [clear, setClear] = useState(false)
    const [option, setOption] = useState("Auto")
    const [darkmode, setDarkmode] = useState(false)
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);


    const handleClear = () => {
        setClear(true)
        setTimeout(() => {
            setClear(false)
        }, 1000)
    }

    return (
        <div>
            <Modal size='lgK' show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>About CodeSensei</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <section className="about-section">
                        <p className="about-text">
                            <strong>CodeSensei</strong> is an AI-powered coding assistant designed to simplify programming for developers of all levels. Whether you're writing your first "Hello World" or optimizing production-level code, CodeSensei is your reliable partner in code.
                        </p>

                        <p className="about-text">
                            Built using <strong>React</strong> and <strong>Vite</strong> for lightning-fast performance and a seamless developer experience, CodeSensei integrates with a powerful <strong>FastAPI</strong> backend. At its core is the intelligent <strong>LLaMA 3.2</strong> model, enabling natural and context-aware communication for coding tasks.
                        </p>

                        <h3 className="about-subtitle">✨ Key Features</h3>
                        <ul className="about-list">
                            <li><strong>Auto Mode:</strong> Provides instant smart suggestions and code completions.</li>
                            <li><strong>Explain Mode:</strong> Breaks down code into understandable pieces with simple explanations.</li>
                            <li><strong>Generate Mode:</strong> Creates tailored code snippets, functions, or algorithms on the fly.</li>
                            <li><strong>Ask Mode:</strong> Lets you ask coding or theoretical questions in natural language.</li>
                            <li><strong>Dark/Light Themes:</strong> Stylish interface that adapts to your preferred mode.</li>
                            <li><strong>Code Chat History:</strong> Track previous questions and interactions for reference.</li>
                            <li><strong>Clear UI:</strong> Minimalist and distraction-free layout for pure focus while coding.</li>
                        </ul>

                        <h3 className="about-subtitle">🚀 Our Mission</h3>
                        <p className="about-text">
                            CodeSensei aims to democratize access to intelligent code assistance. We're building a tool that helps coders learn faster, debug smarter, and code more efficiently — all in one sleek interface. Whether you're a student, freelancer, educator, or hobbyist, our goal is to empower you through AI.
                        </p>

                        <h3 className="about-subtitle">🧠 Powered by LLaMA 3.2</h3>
                        <p className="about-text">
                            With Meta's LLaMA 3.2 model at the heart of CodeSensei, the application understands nuanced prompts, generates clean code, and explains complex concepts like a pro tutor — making it feel like you're chatting with an expert developer.
                        </p>

                        <h3 className="about-subtitle">🛠️ Tech Stack</h3>
                        <ul className="about-list">
                            <li><strong>Frontend:</strong> React + Vite</li>
                            <li><strong>Backend:</strong> FastAPI (Python)</li>
                            <li><strong>LLM:</strong> LLaMA 3.2 (integrated via API)</li>
                            <li><strong>Styling:</strong> Custom CSS with theme support</li>
                        </ul>

                        <h3 className="about-subtitle">💬 Join the Conversation</h3>
                        <p className="about-text">
                            Have ideas, feedback, or cool feature requests? We’re building CodeSensei for the dev community — your input shapes the future of this app.
                        </p>

                        <p className="about-footer">
                            <em>Code smarter. Learn faster. Ask anything. That’s the power of CodeSensei.</em>
                        </p>
                    </section>
                </Modal.Body>
            </Modal>
            <div className={`navbar ${darkmode ? "navbar-darkmode" : ""}`}>
                <a href="/" className="logo">
                    CodeSensei
                </a>
                <div className="options">
                    <button className={`option ${option === "Auto" ? "active-option" : ""} ${darkmode && option !== "Auto" ? "option-darkmode" : ""}`} onClick={() => setOption("Auto")}>Auto</button>
                    <button className={`option ${option === "Explain" ? "active-option" : ""} ${darkmode && option !== "Explain" ? "option-darkmode" : ""}`} onClick={() => setOption("Explain")}>Explain</button>
                    <button className={`option ${option === "Generate" ? "active-option" : ""} ${darkmode && option !== "Generate" ? "option-darkmode" : ""}`} onClick={() => setOption("Generate")}>Generate</button>
                    <button className={`option ${option === "Ask" ? "active-option" : ""} ${darkmode && option !== "Ask" ? "option-darkmode" : ""}`} onClick={() => setOption("Ask")}>Ask</button>
                </div>
                <div className="utility">
                    <button className="utility-option" onClick={() => setDarkmode(!darkmode)}>🌙</button>
                    <button className="utility-option" onClick={handleClear}>Clear</button>
                    <button className="utility-option" onClick={handleShow}>?</button>
                </div>
            </div>
            <ChatBody clear={clear} option={option} darkmode={darkmode} />
        </div>
    )
}

export default Chat
