import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { solid, regular } from '@fortawesome/fontawesome-svg-core/import.macro';

export default function BookmarkButton({ isBookmarked, func }) {
    return (
        <button
            className="bookmark"
            onClick={func}
            aria-label={isBookmarked ? 'Bookmark post' : 'Unbookmark post'}
            aria-checked={isBookmarked ? 'True' : 'False'}
        >
            {isBookmarked ? (
                <FontAwesomeIcon icon={solid('bookmark')} />
            ) : (
                <FontAwesomeIcon icon={regular('bookmark')} />
            )}
        </button>
    );
}
