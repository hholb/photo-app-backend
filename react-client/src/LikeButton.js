import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { solid, regular } from '@fortawesome/fontawesome-svg-core/import.macro';

export default function LikeButton({ isLiked, func }) {
    return (
        <button
            className="like-button"
            onClick={func}
            aria-label={isLiked ? 'Like post' : 'Unlike post'}
            aria-checked={isLiked ? 'True' : 'False'}
        >
            {isLiked ? (
                <FontAwesomeIcon icon={solid('heart')} />
            ) : (
                <FontAwesomeIcon icon={regular('heart')} />
            )}
        </button>
    );
}
