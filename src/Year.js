import React from 'react';
import Month from './Month.js';

class Year extends React.Component {
	constructor(props) {
		super(props);
		this.state = {'visible': props.visible,
					'items':[]
					};
		
		this.clicked = this.clicked.bind(this);
		
		console.log(this.props.dates);
		var months = {};
		for (let i=0; i<this.props.dates.length; i++){
			var dates = this.props.dates[i].split("-");
			var d = months[dates[0]]
			if (d === undefined){
				d = [];
				months[dates[0]] = d;
			}
			d.push(dates[1]);
		}
		
		console.log(months);
		for (let i=1; i<13; i++){
			var x = months[i];
			if (x === undefined){
				continue;
			}
			this.state.items.push(<li key={this.props.year+"-"+i}><Month year={this.props.year} month={i} dates={months[i]}/>	</li>);
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
			items = this.state.items;	
		}else{
			items = [];
		}

		return (<div>
		<div onClick={this.clicked}>Year: {this.props.year}</div>
		<ul>{items}</ul>
		</div>);

	}
}

export default Year;
