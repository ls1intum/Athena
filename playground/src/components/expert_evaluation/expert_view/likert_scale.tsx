import React, {useEffect, useState} from 'react';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCircleInfo} from "@fortawesome/free-solid-svg-icons/faCircleInfo";
import Popup from "@/components/expert_evaluation/expert_view/popup";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";

interface SingleChoiceLikertScaleProps {
    title: string;
    summary: string;
    description: string;
    passedValue: number | null;
    onLikertChange: (value: number) => void;
    resetState: boolean;
}

const SingleChoiceLikertScale: React.FC<SingleChoiceLikertScaleProps> = ({
                                                                             title,
                                                                             summary,
                                                                             description,
                                                                             passedValue,
                                                                             onLikertChange,
                                                                             resetState,
                                                                         }) => {
    const [selectedValue, setSelectedValue] = useState<number | null>(null);
    const [isPopupOpen, setIsPopupOpen] = useState(false);

    const handleInfoClick = () => {
        setIsPopupOpen(true);
    };

    useEffect(() => {
        console.log(passedValue)
        setSelectedValue(passedValue);
    }, [resetState]); //passedValue


    const handleChange = (value: number) => {
        setSelectedValue(value);
        onLikertChange(value);
    };

    const closePopup = () => {
        setIsPopupOpen(false);
    };

    // Define background colors matching the slider colors
    const scaleColors = [
        'bg-red-600',       // First section
        'bg-orange-500',    // Second section
        'bg-yellow-400',    // Third section
        'bg-green-400',     // Fourth section
        'bg-green-700',     // Fifth section
    ];

    useEffect(() => {
        //  setSelectedValue(null); // Reset the selection to unselect all options
    }, [resetState]); // Watch for changes to resetState

    return (
        <>
            {/* Title and Info Section */}
            <div className="flex items-center">
                <h3 className="text-xl font-semibold mr-2">{title}</h3>
                <span
                    onClick={handleInfoClick}
                    className="text-gray-500 cursor-pointer hover:text-gray-700"
                    role="img"
                    aria-label="info"
                >
          <FontAwesomeIcon icon={faCircleInfo}/>
        </span>
            </div>
            <Popup isOpen={isPopupOpen} onClose={closePopup} title="Information">
                <ReactMarkdown rehypePlugins={[rehypeRaw]} className="prose prose-sm max-w-none">
                    {description}
                </ReactMarkdown>
            </Popup>

            {/* Question Section */}
            <p className="text-gray-800">{summary}</p>

            {/* Single Choice Likert Scale */}
            <div className="flex items-center w-full">
                {[1, 2, 3, 4, 5].map((value, index) => (
                    <label
                        key={value}
                        className={`flex-1 flex items-center justify-center cursor-pointer py-0.5 ${scaleColors[index]} ${index === 0 ? 'rounded-l-full' : ''} ${index === 4 ? 'rounded-r-full' : ''}`}
                    >
                        <input
                            type="radio"
                            name="likert"
                            value={value}
                            checked={passedValue === value}
                            onChange={() => handleChange(value)}
                            className={`w-4 h-4  ${selectedValue === value ? 'border-white bg-black border-4' : 'border-gray-400 bg-transparent border-2'} rounded-full appearance-none`}
                        />
                    </label>
                ))}
            </div>
        </>
    );
};

export default SingleChoiceLikertScale;