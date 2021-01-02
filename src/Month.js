import React from 'react';
import Day from './Day.js';

class Month extends React.Component {
	constructor(props) {
		super(props);
		this.state = {'visible': props.visible};
		
		this.clicked = this.clicked.bind(this);
		
		this.items = []
		console.log(this.props.dates);
		for (var i=0; i<this.props.dates.length; i++){
			this.items.push(<li key={this.props.year+"-"+this.props.month+"-"+i}><Day year={this.props.year} month={this.props.month} day={this.props.dates[i]} />	</li>);
		}
	}

	componentDidMount() {
	}

	componentWillUnmount() {
	}

	clicked(){
		this.setState({'visible': !this.state.visible});
	}

	render() {
		var items = []

		if (this.state.visible){
			items = this.items;	
		}else{
			items = [];
		}

		return (<div>
		<div onClick={this.clicked}>Month: {this.props.month}</div>
		<ul>{items}</ul>
		</div>);

	}
}

export default Month;
