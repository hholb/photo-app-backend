import React from 'react';
import { useState, useEffect } from 'react';
import NavLinks from './NavLinks';
import Profile from './Profile';
import Suggestions from './Suggestions';
import Posts from './Posts';
import { getHeaders } from './utils';
import Stories from './Stories';
import Navbar from './Navbar';

export default function App ({token}) { 
    // console.log('access token:', token);
    
    const [profile, setProfile] = useState(null);

    useEffect(() => {
        async function fetchProfile() {
            const response = await fetch('/api/profile', {
                headers: getHeaders(token)
            });
            const data = await response.json();
            setProfile(data)
        }
        fetchProfile();
    }, []);

    if (!profile) return "";

    return (
        <div>
            
            {/* Navbar */}
           <Navbar user={profile} />
           
           {/* Right Panel */}
            <aside>
                <header>
                    <Profile 
                        user={profile}
                    />
                </header>
                <div className="suggestions">
                    <div>
                        <Suggestions token={token} />
                    </div>
                </div>
            </aside>

            <main>

                {/* Stories */}
                <header className="stories">
                    <Stories token={token} />
                </header>

                {/* Posts */}
                <div id="posts">
                    <Posts token={token} profile={profile}/>
                </div>

            </main>

        </div>
    );
    
}