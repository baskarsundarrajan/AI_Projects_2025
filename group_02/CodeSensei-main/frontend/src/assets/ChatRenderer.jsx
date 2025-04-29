import React, { useEffect, useState } from 'react'

import { CopyBlock, dracula } from 'react-code-blocks';
import parse from 'html-react-parser';

const ChatRenderer = ({ chat }) => {
    const { response, code } = chat;

    const [chatParts, setChatParts] = useState([])

    useEffect(() => {
        const parts = response.split(/(__CODEBLOCK_\d+__)/g)

        const newParts = parts.map((part, index) => {
            const isCodeBlock = part.match(/__CODEBLOCK_\d+__/g)
            if (isCodeBlock) {
                const codeBlockIndex = parseInt(part.match(/\d+/)[0], 10)
                const [c, language] = code[codeBlockIndex]

                return (
                    <div>
                        <CopyBlock
                            key={index}
                            text={c.trim()}
                            language={language}
                            showLineNumbers={true}
                            theme={dracula}
                        />
                    </div>
                )
            }
            return parse(part.trim())
        })


        setChatParts(newParts)

    }, [chat, setChatParts])

    return (
        <div>
            {
                chatParts.map((part, index) => {
                    if (typeof part === 'string') {
                        return <p key={index}>{part}</p>
                    } else {
                        return part
                    }
                })
            }
        </div>
    )
}

export default ChatRenderer
