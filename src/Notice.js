import React from 'react';

class Notice extends React.Component {
  constructor(props) {
    super(props);
    this.state = {'visible':false};
	
	this.clicked = this.clicked.bind(this);
  }

  componentDidMount() {
  }

  componentWillUnmount() {
  }
  
  clicked(){
		this.setState({'visible': !this.state.visible});
	}
	
  render() {
		var text;
	  
	  if (this.state.visible){
		  text = this.props.data;
	  }else{
		  text = this.props.title;
	  }
    return (
      <div onClick={this.clicked}>
	  {text}
      </div>
    );
  }
}

export default Notice;
