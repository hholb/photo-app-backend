import React from 'react';

export default function NavLinks({user}) { 

    if (!user) {
        return '';
    }

    return (
        <ul>   
            <li>API Docs</li>
            <li className='username'><span>{user.username}</span></li>
            <li><button className='sign-out'><a href="logout">Sign out</a></button></li>
        </ul> 
    );
    
}
