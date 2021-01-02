import './App.css';
import Year from './Year.js';
import React from 'react';

class App extends React.Component {
	constructor(props) {
		super(props);
		this.state = {'items':[]}
	}
	
	componentDidMount(){
		fetch("http://localhost:8080/days/")
		.then(res => res.json())
		.then(
			(result) => {
				var dates = {}
				
				console.log(result);				
				for (var i=0; i<result.length; i++){
						var s = result[i].split("\.");
						var d = dates[s[0]];
						if (d === undefined){
							d = [];
						}
						d.push(s[1]+"-"+s[2]);
						dates[s[0]] = d;
				}
				var items = [];
				for (var k in dates){
					items.push(
						<Year year={k} dates={dates[k]}/>
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
	
	render(){
		return (
			<div className="App">
				<header className="App-header">
				{this.state.items}
				</header>
			</div>
		);
	}
}

export default App;
