import React from 'react';
import {getHeaders} from './utils';
import { useState, useEffect } from "react";


export default function Posts({token}) { 

    // define the posts as a state variable that is initialized to null
    const [posts, setPosts] = useState(null); 

    // wrap all fetch function definitions and invocations
    // in a useEffect()
    useEffect(() => {
        async function fetchPosts() {
            const response = await fetch('/api/posts', {
                headers: getHeaders(token)
            });
            const data = await response.json();
            setPosts(data);
        }
        fetchPosts();
    }, [token]);

    

    if (!posts) {
        return '';
    }
    return (
        // iterate through each post and convert it to a div tag
        // you can make it more fancy later.
        posts.map(post => {
            return (
                <div className="card" key={post.id}>{post.caption}</div>
            )
        })
    );     
}