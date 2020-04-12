// don't forget to run 'npx webpack' when changing this file
import React from 'react';
import axios from 'axios';

class RobotController extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            ids: [],
            identifyDisabled: false
        }
    }

    render() {
        var ids = this.state.ids.map((id, key) => <span className="id" key={key}>{id}</span>)
        return <div>
            <div className="row">
                <button className="square"/>
                <button className="square" onClick={() => this.move('forward')}>🔼</button>
                <button className="square"/>
            </div>
            <div className="row">
                <button className="square" onClick={() => this.move('left')}>◀️</button>
                <button className="square" onClick={() => this.identify()} disabled={this.state.identifyDisabled}>🔴</button>
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

    identify() {
        this.setState({identifyDisable:true})
        axios.get('/identify')
            .then(res => {
                console.log(res.data)
                // this.setState({ids: res.data.ids});
                this.setState({identifyDisable:false})
            })
    }
}

export default RobotController;
