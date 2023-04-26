import React from 'react';
import Comment from './Comment';

export default function AllComments({ comments }) {
    return (
        <>
            {
                comments.map(comment => {
                    return(
                        <Comment comment={comment}/>
                    )
                })
            }
        </>
    )
}
