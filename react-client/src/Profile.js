/**
 * The job of Profile is to show the image and username
 * of the person who is logged into the system.
 */

import React from 'react';

export default function Profile({user}) {
    if (!user) return '';
    return (
        <section className='profile'>
            <img src={user.image_url} alt={user.username + "'s profile picture"} />
            <h2>{user.username}</h2>
        </section>
    )
}