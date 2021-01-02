import React from 'react';
import Notice from './Notice.js';

class Day extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			'visible': props.visible,
			isLoaded: false};
		
		this.clicked = this.clicked.bind(this);
		this.fetchData = this.fetchData.bind(this);

	}

	componentDidMount() {
	}

	componentWillUnmount() {
	}

	fetchData(){
		fetch("http://localhost:8080/"+this.props.year+"/"+this.props.month+"/"+this.props.day+"/")
		.then(res => res.json())
		.then(
			(result) => {
				console.log(result);
				var items = []
				for (var i=0; i<result.length; i++){
					items.push(
					<li key={this.props.year+"-"+this.props.month+"-"+this.props.day+"-"+i}>
						<Notice data={result[i].data} title={result[i].title} />	
					</li>
					);
				}
		
				this.setState({
					isLoaded: true,
					items: items
				});
			},
			(error) => {
				this.setState({
				isLoaded: true,
				error
				});
			}
		);
	}
	
	clicked(){
		if (!this.state.visible){
			this.fetchData();
		}
		
		this.setState({'visible': !this.state.visible});
	}

	render() {
		var items = [];
		if (this.state.visible){
			items = this.state.items;	
		}else{
			items = [];
		}

		return (<div>
		<div onClick={this.clicked}>{this.props.day+"."+this.props.month+"."+this.props.year}</div>
		<ul>{items}</ul>
		</div>);

	}
}

export default Day;
