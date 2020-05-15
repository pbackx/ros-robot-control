// don't forget to run 'npx webpack' when changing this file
import React from 'react';
import axios from 'axios';
import RobotFeed from "./RobotFeed";
import RobotId from "./RobotId";

class RobotController extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            ids: [],
            identifyDisabled: false,
            identifyText: "🔴",
            idToDraw: null
        }
        this.showId = this.showId.bind(this);
        this.clear = this.clear.bind(this);
    }

    render() {
        var ids = this.state.ids.map((id, key) =>
            <RobotId tag={id.id} key={key}
                     onMouseOver={() => this.showId(id)}
                     onMouseOut={this.clear}/>)
        return <div>
            <RobotFeed idToDraw={this.state.idToDraw}/>
            <div className="row">
                <button className="square"/>
                <button className="square" onClick={() => this.move('forward')}>🔼</button>
                <button className="square"/>
            </div>
            <div className="row">
                <button className="square" onClick={() => this.move('left')}>◀️</button>
                <button className="square" onClick={() => this.identify()} disabled={this.state.identifyDisabled}>
                    {this.state.identifyText}
                </button>
                <button className="square" onClick={() => this.move('right')}>▶️</button>
            </div>
            <div className="row">
                <button className="square"/>
                <button className="square" onClick={() => this.move('backward')}>🔽</button>
                <button className="square"/>
            </div>
            <div className="foundIds">
                {ids}
            </div>
        </div>;
    }

    move(direction) {
        axios.get(`/robot/${direction}`)
    }

    showId(id) {
        this.setState({
            idToDraw: id
        });
    }

    clear() {
        this.setState({
            idToDraw: null
        });
    }

    componentWillMount() {
        document.addEventListener("keydown", e => this.keyDown(e), false);
    }

    keyDown(key) {
        switch (key.keyCode) {
            case 37:
                this.move('left');
                break;
            case 38:
                this.move('forward');
                break;
            case 39:
                this.move('right');
                break;
            case 40:
                this.move('backward');
                break;
            case 32:
                if (!this.state.identifyDisabled) {
                    this.identify();
                }
                break;
        }
    }

    identify() {
        this.setState({
            identifyDisabled: true,
            identifyText: "⏳"
        })
        axios.get('/identify')
            .then(res => {
                console.log(res.data)
                this.setState({
                    identifyDisabled: false,
                    identifyText: "🔴",
                    ids: res.data
                });
            })
    }
}

export default RobotController;
