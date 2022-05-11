import React from "react";

const ChatBox = ({ msgList }) => {
    let allMessages;
    if (msgList) {
        allMessages = msgList.map((msg, index) => {
            return <p key={index}>{msg}</p>;
        })
    } else {
        allMessages = <p>You currently have no messages.</p>
    }

    return (
        <div>
            {allMessages}
        </div>
    )
}

export default ChatBox;