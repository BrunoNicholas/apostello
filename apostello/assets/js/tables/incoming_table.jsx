var ReprocessButton = React.createClass({
    render: function () {
        if (this.props.sms.loading){
        return(<div/>);
        } else {
        return(<a className='btn btn-secondary btn-sm' onClick={this.props.reprocessSms}>Reprocess</a>)
        }
    }
});
var SenderCell = React.createClass({
    render: function () {
        return (
            <td>
                <a href={this.props.sms.sender_url} style={{"color": "#212121"}}>{this.props.sms.sender_name}</a>
            </td>
        )
    }
});
var KeywordCell = React.createClass({
    render: function () {
        if (this.props.sms.matched_link === '#') {
            return (<td><b>{this.props.sms.matched_keyword}</b></td>)
        }
        else {
            return (<td><b><a href={this.props.sms.matched_link} style={{"color": "#212121"}}>{this.props.sms.matched_keyword}</a></b></td>)

        }
    }
});
var SmsInRow = React.createClass({
    render: function () {
        return (
            <tr style={{'backgroundColor': this.props.sms.matched_colour}}>
                <SenderCell sms={this.props.sms}></SenderCell>
                <KeywordCell sms={this.props.sms}></KeywordCell>
                <td>{this.props.sms.content}</td>
                <td>{this.props.sms.time_received}</td>
                <td><ReprocessButton sms={this.props.sms} reprocessSms={this.props.reprocessSms}/></td>
            </tr>
        )
    }
});
var InTable = React.createClass({
    reprocessSms: function (sms) {
        var that = this;
        $.ajax({
            url : '/api/v1/sms/in/'+sms.pk,
            type : "POST",
            data : { 'reingest': true },
            success : function(json) {
              that.loadResponsesFromServer()
            },
            error : function(xhr,errmsg,err) {
                window.alert("uh, oh. That didn't work.")
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    },
    loadResponsesFromServer: function () {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            success: function (data) {
                this.setState({data: data});
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    getInitialState: function () {
        return {data: [{"sender_name": "Loading...", "loading": true}]};
    },
    componentDidMount: function () {
        this.loadResponsesFromServer();
        setInterval(this.loadResponsesFromServer, this.props.pollInterval);
    },
    render: function () {
        var that = this;
        var rows = this.state.data.map(function (sms, index) {
                return (<SmsInRow sms={sms} key={index} reprocessSms={that.reprocessSms.bind(null, sms)}/>)
        });
        return (
            <div className="table-responsive">
            <table className="table table-sm table-striped" style={{'tableLayout':'fixed', 'wordWrap':'break-word'}}>
            <thead>
            <tr>
            <th>From</th>
            <th>Keyword</th>
            <th>Message</th>
            <th>Time</th>
            <th></th>
            </tr>
            </thead>
            <tbody className="searchable">
            {rows}
            </tbody>
            </table>
            </div>
        );
    }
});
