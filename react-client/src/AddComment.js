import React from "react";

export default function AddComment({id, func}) {
    return (
        <form className="add-comment" onSubmit={func} >
            <input id={"comment_" + id} type="text" placeholder="Add comment..." autoFocus aria-label="Add a comment text input"></input>
            <button type="submit" placeholder="Add comment..." aria-label="Post Comment">Post</button>
        </form>
    )
}