import React from 'react';

class RobotId extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return <span className="id"
                     onMouseOver={this.props.onMouseOver}
                     onMouseOut={this.props.onMouseOut}>
                {this.props.tag}
            </span>;
    }
}

export default RobotId;