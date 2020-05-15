import React from 'react';

class RobotFeed extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return <div className="robot-feed">
            <img src={window.videoFeed} alt="The robot feed. You really need to see it." />
        </div>;
    }
}

export default RobotFeed;