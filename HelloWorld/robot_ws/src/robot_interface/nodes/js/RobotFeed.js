import React from 'react';

class RobotFeed extends React.Component {
    constructor(props) {
        super(props);
        this.drawRectangle = this.drawRectangle.bind(this);
        this.clearCanvas = this.clearCanvas.bind(this);
    }

    drawRectangle(id) {
        const ctx = this.refs.canvas.getContext('2d');
        ctx.beginPath();
        ctx.strokeStyle = "red";
        ctx.rect(id.left, id.top, id.right-id.left, id.bottom-id.top);
        ctx.stroke();
    }

    clearCanvas() {
        const ctx = this.refs.canvas.getContext('2d');
        ctx.clearRect(0, 0, 400, 300);
    }

    componentDidUpdate() {
        if (this.props.idToDraw) {
            this.drawRectangle(this.props.idToDraw);
        } else {
            this.clearCanvas();
        }
    }

    render() {
        return <div className="robot-feed">
            <img id="videoFeedImg" src={window.videoFeed} alt="The robot feed. You really need to see it." />
            <canvas id="videoFeedCanvas" ref="canvas" width="400" height="300"/>
        </div>;
    }
}

export default RobotFeed;