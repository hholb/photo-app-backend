import React, { useEffect, useRef, useState } from 'react';
import BookmarkButton from './BookmarkButton';
import LikeButton from './LikeButton';
import AllComments from './AllComments';
import Comment from './Comment';
import { getHeaders } from './utils';
import AddComment from './AddComment';

export default function Post({ postId, post, currentUserId, token }) {
    const [thisPost, setPost] = useState(post);
    const [numComments, setNumComments] = useState(thisPost.comments.length);
    const [like, setLike] = useState(thisPost.likes ? isLiked() : {});
    const [bookmarked, setBookmarked] = useState(
        thisPost.current_user_bookmark_id ? thisPost.current_user_bookmark_id : null
    );
    const [mostRecentComment, setMostRecentComment] = useState(
        numComments > 0 ? (
            <Comment comment={thisPost.comments[numComments - 1]} />
        ) : (
            ''
        )
    );

    const likeAPI = '/api/posts/likes/';
    console.log(thisPost);

    function isLiked() {
        const result = thisPost.likes.find(
            (like) => like.user_id === currentUserId
        );
        return result;
    }

    async function likePost() {
        console.log('liking...');
        const body = { post_id: thisPost.id };
        const response = await fetch(likeAPI, {
            method: 'POST',
            headers: getHeaders(token),
            body: JSON.stringify(body),
        });
        const data = await response.json();
        console.log(data);
        setLike(data);
        requeryPost();
    }

    async function unlikePost() {
        console.log('unliking...');
        const endpoint = likeAPI + like.id;
        console.log(endpoint);
        const response = await fetch(endpoint, {
            method: 'DELETE',
            headers: getHeaders(token),
        });
        const data = await response.json();
        console.log(data);
        setLike(undefined);
        requeryPost();
    }

    async function bookmarkPost() {
        console.log('bookmarking...');
        const endpoint = '/api/bookmarks';
        const postData = { post_id: thisPost.id };
        const request = await fetch(endpoint, {
            method: 'POST',
            headers: getHeaders(token),
            body: JSON.stringify(postData),
        });
        const data = await request.json();
        console.log(data);
        setBookmarked(data.id);
        requeryPost();
    }

    async function unbookmarkPost() {
        console.log('unbookamrking....');
        const endpoint = `api/bookmarks/${bookmarked}`;
        const request = await fetch(endpoint, {
            method: 'DELETE',
            headers: getHeaders(token),
        });
        const data = await request.json();
        console.log(data);
        setBookmarked(undefined);
        requeryPost();
    }

    async function postComment(event) {
        event.preventDefault();
        console.log('add comment');
        const endpoint = '/api/comments';
        const input = document.querySelector('#comment_' + thisPost.id);
        const text = input.value;
        const postData = {
            post_id: thisPost.id,
            text: text,
        };
        const request = await fetch(endpoint, {
            method: 'POST',
            headers: getHeaders(token),
            body: JSON.stringify(postData),
        });
        const data = await request.json();
        console.log(data);
        setMostRecentComment(<Comment comment={data}/>);
        setNumComments(numComments + 1);
        input.value = '';
        input.focus();
        requeryPost();
    }

    async function requeryPost() {
        const endpoint = '/api/posts/' + thisPost.id;
        const request = await fetch(endpoint, {
            method: "GET",
            headers: getHeaders(token)
        });
        const data = await request.json();
        setPost(data);
    }

    return (
        <section id={'post_' + thisPost.id} className="card" key={postId}>
            <h2>{thisPost.user.username}</h2>
            <img src={thisPost.image_url} alt="" />
            <section className="post-interactions">
                <LikeButton
                    isLiked={like}
                    func={like ? unlikePost : likePost}
                />
                <BookmarkButton
                    isBookmarked={bookmarked ? true : false}
                    func={bookmarked ? unbookmarkPost : bookmarkPost}
                />
            </section>
            <p className="caption">{thisPost.caption}</p>
            <section className="comment-section">
                {mostRecentComment}
                {numComments > 0 ? (
                    <button className="show-comments" aria-label='Show all comments'>
                        Show all {numComments} comments...
                    </button>
                ) : (
                    ''
                )}
            </section>
            <AddComment id={thisPost.id} func={postComment} />
        </section>
    );
}
