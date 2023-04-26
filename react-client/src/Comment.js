import React from 'react';

export default function Comment({ comment }) {
    return (
        <div className="comment">
            <hr></hr>
            <p>
                <span className="username">{comment.user.username}</span>
                {comment.text}
            </p>
            <p className="comment-date">{comment.display_time}</p>
        </div>
    );
}
