
var React = require("react");
var ReactDOM = require('react-dom');
var Select = require('react-select');
var ReactCSSTransitionGroup = require('react-addons-css-transition-group');


var $ = require('jquery');


var SearchFilter = React.createClass({
    displayName: 'MultiSelect',
  
    getInitialState: function(){
        return {
            filters: []
        };
    },

    loadDataFromServer: function() {
        var self = this;
        $.getJSON("/assets/search.json", function(data) {
            data.sort(function(a, b) {
                if (a.label < b.label) return -1;
                else if (a.label > b.lavel) return 1;
                else return 0;

            });

           self.setState({filters: data});
        });
    },

    componentDidMount: function() {
        this.loadDataFromServer();
    },
    
    render: function(){
        var self = this;
        return (
            <div>
                    <Select
                        multi
                        simpleValue
                        className="nav-search select-value"
                        value={this.props.value}
                        name="search-filter"
                        placeholder="Enter query e.g. Pressure = 1200"
                        options={this.state.filters}
                        onChange={this.props.onFilterChange}
                    />

            </div>
        );
    },

});


var SearchResult = React.createClass({
    displayName: 'SearchResult',

    render: function() {
        var fileList = '';

        if (this.props.data.files)
        { 
            fileList = this.props.data.files.map(function(f) {
                 return (
                    <div className="row">
                        <span className="col-lg-1">
                            <i className="fa fa-file"></i>
                        </span>
                        <span className="col-lg-10">
                            {f.name} <span className="size">({f.size})</span>
                        </span>
                    </div>
                );
            });

        }

        var labels = [];
        var attrs = ['orientation', 'spray type', 'year data taken', 'filetype', 'injector', 'publication doi'];

        for (i = 0 ; i < attrs.length; i++) {
            if (this.props.data[attrs[i]])
            {
                labels.push(this.props.data[attrs[i]]);
            }
        }

        labelList = labels.map(function(f) {
            return (
                <span className="label label-default info-names"> {f}</span>
            );
        });


        return (
            <div className="row">
                <div className="col-md-10 newsfeed">
                    <div className="blog-posts">
                        <div className="post-info">
                            <article className="post post-medium post-article">
                                <div className="post-content">
                                    <h5 className="title-tag">
                                        <a href={this.props.data.zip_file ? this.props.upload + '/' + this.props.data.zip_file : '#'}>
                                            <i className="glyphicon glyphicon-folder-close">                                            {this.props.data.name}
 </i>  
                                        </a>
                                    </h5>
                                        <a href={this.props.data.zip_file ? this.props.upload + '/' + this.props.data.zip_file : '#'}><i className="fa fa-download"> .zip </i></a>  
                                        <a href={this.props.data.tar_file ? this.props.upload + '/' + this.props.data.tar_file : '#'}><i className="fa fa-download gap"> .tar.gz</i></a>

                                    <div className="newsfeed-info">
                                        {labelList}
                                    </div>
                                    <p className="feed-description">
                                        {this.props.data.description}
                                    </p>

                                   {fileList}

                                </div>
                            </article>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});

var SearchResultList = React.createClass({
    render: function() {
        var resultList = this.props.data.map(function(result){
            return (
                <div>
                    <SearchResult data={result} upload="/upload/"></SearchResult>
                    <hr className="small_right_margin small_left_margin"/>
                </div>

            );
        });
        return (
            <div>
                <ReactCSSTransitionGroup transitionName="example" transitionEnterTimeout={500} transitionLeaveTimeout={300}>
                    {resultList}
                </ReactCSSTransitionGroup>
            </div>
        );
    }
});


var SearchInfo = React.createClass({
    displayName: 'SearchInfo',

    render : function() {
        return (
            
            <span className="col-lg-10">
                <h4>Total datasets:  <span className="size">({this.props.data})</span></h4>
            </span>
        );
    }
})

var SearchComponent = React.createClass({
    displayName: 'SearchComponent',

    getInitialState: function() {
        return {
            resultList: [],
            filterValue: [],
            resultCount: 0,
        }
    },

    loadDataFromServer: function(query) {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            cache: false,
            method: 'post',
            data: {q:query},
            success: function(data) {
                this.setState({resultCount: data.length, resultList: data});
            }.bind(this),
            error:function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },

    handleSearchFilter: function(val) {
        this.setState({filterValue: val});
        this.loadDataFromServer(val);
    },

    componentDidMount: function() {
        this.loadDataFromServer({});
    },

    render: function() {
        return (
            <div>
                <div className="row fix-margin">
                    <div className="col-md-10">
                        <SearchFilter onFilterChange={this.handleSearchFilter} value={this.state.filterValue}/>
                    </div>
                </div>
                <div className="row fix-margin">
                   <SearchInfo data={this.state.resultCount}/>
                </div>
                <div className="row">
                    <SearchResultList data={this.state.resultList}/>
                </div>
            </div>
        );
    }
});

ReactDOM.render(
    <SearchComponent url="http://spraydataportal.xray.aps.anl.gov/api.php"/>,
    document.getElementById('searchcomponent')
);
