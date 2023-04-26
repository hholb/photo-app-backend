import React, { useEffect } from 'react';
import NavLinks from './NavLinks';

export default function Navbar({ user }) {
     return (
        <nav className="main-nav">
            <h1>Photo App</h1>
            <NavLinks user={user} />
        </nav>
    );
}
