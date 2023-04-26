import React, { useState, useEffect } from 'react';
import { getHeaders } from './utils';
import Post from './Post';

export default function Posts({ token, profile }) {
    const [posts, setPosts] = useState([]);
    const currentUserId = profile.id;

    useEffect(() => {
        async function fetchPosts() {
            const response = await fetch('/api/posts', {
                headers: getHeaders(token),
            });
            const data = await response.json();
            setPosts(data);
        }

        fetchPosts();
    }, [token]);

    if (posts.length === 0) return '';

    return (
        <>
            {posts.map((post) => {
                return (
                    <Post
                        postId={post.id}
                        post={post}
                        currentUserId={currentUserId}
                        token={token}
                    />
                );
            })}
        </>
    );
}
