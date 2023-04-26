/**
 * The job of stories is to display stoies in the stoires panel
 */

import React from 'react';
import { useState, useEffect } from 'react';
import { getHeaders } from './utils';

export default function Stories({ token }) {
    const [stories, setStories] = useState([]);

    useEffect(() => {
        async function fetchPosts() {
            const response = await fetch('/api/stories', {
                headers: getHeaders(token),
            });
            const data = await response.json();
            setStories(data);
        }

        fetchPosts();
    }, [token]);

    console.log(stories);

    if (stories.length === 0) return '';

    return (
        <>
            {stories.map((story) => {
                return (
                    <section className='story-card'>
                        <img src={story.user.image_url} alt="" />
                        <p className='username'>{story.user.username}</p>
                    </section>
                );
            })}
        </>
    );
}
