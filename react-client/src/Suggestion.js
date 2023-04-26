import React, { useState } from 'react';
import FollowButton from './FollowButton';
import { getHeaders } from './utils';

export default function Suggestion({ suggestion, token }) {
    console.log(suggestion);

    const [followed, setFollowed] = useState(false);
    const [followID, setFollowID] = useState(null);

    const followerID = suggestion.id;

    async function follow() {
        console.log('following...');
        const endpoint = '/api/following';
        const postData = { user_id: followerID };
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: getHeaders(token),
            body: JSON.stringify(postData),
        });

        const data = await response.json();
        console.log(data);
        setFollowID(data.id);
        setFollowed(true);
    }

    async function unfollow() {
        console.log('unfollowing...');
        const endpoint = `/api/following/${followID}`;
        const response = await fetch(endpoint, {
            method: 'DELETE',
            headers: getHeaders(token),
        });
        const data = await response.json();
        console.log(data);
        setFollowed(false);
    }

    return (
        <section className="suggestion-card">
            <img src={suggestion.image_url} alt="" />
            <div>
                <p className="suggestion-username username">{suggestion.username}</p>
                <p className="suggestion-text">suggested for you</p>
            </div>
            <FollowButton
                func={followed ? unfollow : follow}
                followed={followed}
            />
        </section>
    );
}
