import React from 'react';

export default function FollowButton({ func, followed }) {
    return (
        <button
            className="follow"
            onClick={func}
            aria-label={followed ? 'Follow user' : 'Unfollow user'}
            aria-checked={followed ? 'True' : 'False'}
        >
            {' '}
            {followed ? 'unfollow' : 'follow'}{' '}
        </button>
    );
}
