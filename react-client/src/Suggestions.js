/**
 * The job of Suggestions is to show suggestions
 */

import React from 'react';
import { useState, useEffect } from 'react';
import Suggestion from './Suggestion';
import { getHeaders } from './utils';

export default function Suggestions({ token }) {
    const [suggestions, setSuggestion] = useState([]);

    useEffect(() => {
        async function fetchSuggestions() {
            const response = await fetch('/api/suggestions', {
                headers: getHeaders(token),
            });
            const data = await response.json();
            setSuggestion(data);
        }

        fetchSuggestions();
    }, [token]);

    // console.log(suggestions);

    if (suggestions.length === 0) return '';

    return (
        <>
            {suggestions.map((suggestion) => {
                return (
                    <Suggestion
                        suggestion={suggestion}
                        token={token}
                    />
                );
            })}
        </>
    );
}
