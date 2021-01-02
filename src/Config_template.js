
class Config {
	constructor(){
		this.host = HOSTADDRESS;
		this.port = HOSTPORT;
		
		this.serverApi = "http://"+this.host+":"+this.port+"/api/";
		this.dayListAddress = this.serverApi+"days/";
	}
}

export default Config;
