var redditApp = angular.module('redditApp', []);

redditApp.controller('RedditCtrl', function ($scope, $http, $location, $log) {

  	// $http.get('http://13.37.0.60:8888/data').success(function(data) {
  	// 	$scope.comments = data;
  	// 	preCompute();
  	// 	network();
  	// });

	var stopWords = ["'ll","a","a ","a's","able","about","about ","above","abst","accordance","according","accordingly","across","act","actually","added","adj","affected","affecting","affects","after","afterwards","again","against","ah","ain't","all","allow","allows","almost","alone","along","already","also","although","always","am","among","amongst","an","an ","and","announce","another","any","anybody","anyhow","anymore","anyone","anything","anyway","anyways","anywhere","apart","apparently","appear","appreciate","appropriate","approximately","are","are ","aren","aren't","arent","arise","around","as","as ","aside","ask","asking","associated","at","at ","auth","available","away","awfully","b","back","be","be ","became","because","become","becomes","becoming","been","before","beforehand","begin","beginning","beginnings","begins","behind","being","believe","below","beside","besides","best","better","between","beyond","biol","both","brief","briefly","but","by","by ","c","c'mon","c's","ca","came","can","can't","cannot","cant","cause","causes","certain","certainly","changes","clearly","co","com","com ","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't","couldnt","course","currently","d","date","definitely","described","despite","did","didn't","different","do","does","doesn't","doing","don't","done","down","downwards","due","during","e","each","ed","edu","effect","eg","eight","eighty","either","else","elsewhere","end","ending","enough","entirely","especially","et","et-al","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","f","far","few","ff","fifth","first","five","fix","followed","following","follows","for","for ","former","formerly","forth","found","four","from","further","furthermore","g","gave","get","gets","getting","give","given","gives","giving","go","goes","going","gone","got","gotten","greetings","h","had","hadn't","happens","hardly","has","hasn't","have","haven't","having","he","he'd","he'll","he's","hed","hello","help","hence","her","here","here's","hereafter","hereby","herein","heres","hereupon","hers","herself","hes","hi","hid","him","himself","his","hither","home","hopefully","how","how's","howbeit","however","hundred","i","I ","i'd","i'll","i'm","i've","id","ie","if","ignored","im","immediate","immediately","importance","important","in","in ","inasmuch","inc","indeed","index","indicate","indicated","indicates","information","inner","insofar","instead","into","invention","inward","is","is ","isn't","it","it ","it'd","it'll","it's","itd","its","itself","j","just","k","keep","keeps","kept","kg","km","know","known","knows","l","largely","last","lately","later","latter","latterly","least","less","lest","let","let's","lets","like","liked","likely","line","little","look","looking","looks","ltd","m","made","mainly","make","makes","many","may","maybe","me","mean","means","meantime","meanwhile","merely","mg","might","million","miss","ml","more","moreover","most","mostly","mr","mrs","much","mug","must","mustn't","my","myself","n","na","name","namely","nay","nd","near","nearly","necessarily","necessary","need","needs","neither","never","nevertheless","new","next","nine","ninety","no","nobody","non","none","nonetheless","noone","nor","normally","nos","not","noted","nothing","novel","now","nowhere","o","obtain","obtained","obviously","of","of ","off","often","oh","ok","okay","old","omitted","on","on ","once","one","ones","only","onto","or","or ","ord","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","owing","own","p","page","pages","part","particular","particularly","past","per","perhaps","placed","please","plus","poorly","possible","possibly","potentially","pp","predominantly","present","presumably","previously","primarily","probably","promptly","proud","provides","put","q","que","quickly","quite","qv","r","ran","rather","rd","re","readily","really","reasonably","recent","recently","ref","refs","regarding","regardless","regards","related","relatively","research","respectively","resulted","resulting","results","right","run","s","said","same","saw","say","saying","says","sec","second","secondly","section","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","shan't","she","she'd","she'll","she's","shed","shes","should","shouldn't","show","showed","shown","showns","shows","significant","significantly","similar","similarly","since","six","slightly","so","some","somebody","somehow","someone","somethan","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specifically","specified","specify","specifying","still","stop","strongly","sub","substantially","successfully","such","sufficiently","suggest","sup","sure","t's","take","taken","tell","tends","th","than","thank","thanks","thanx","that","that's","thats","the","the ","their","theirs","them","themselves","then","thence","there","there's","thereafter","thereby","therefore","therein","theres","thereupon","these","they","they'd","they'll","they're","they've","think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","to ","together","too","took","toward","towards","tried","tries","truly","try","trying","twice","two","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","value","various","very","via","viz","vs","want","wants","was","was ","wasn't","way","we","we'd","we'll","we're","we've","welcome","well","went","were","weren't","what","what ","what's","whatever","when","when's","whence","whenever","where","where's","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","who ","who's","whoever","whole","whom","whose","why","why's","will","will ","willing","wish","with","within","without","won't","wonder","would","wouldn't","www","yes","yet","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","zero"];

	var endpoint = $location.protocol() + "://" + $location.host() + ":" + $location.port() + '/';
	// endpoint = 'http://13.37.0.60:8888/';
	// $http.get( + '/words').success(function(data) {

	$scope.stats = {
		stopWords: 0,
		stopWordsOcc: 0,
		usedWords: 0,
		usedWordsOcc: 0
	};
	$http.get(endpoint + 'words').success(function(data) {

		tmp = [];
		var X = data.length;
		_.forIn(data, function(v,k) {
			if (!$.isNumeric(k) && !_.contains(stopWords, k)) {
				tmp.push({ text: k, weight: v });

				$scope.stats.usedWords++;
				$scope.stats.usedWordsOcc += v;
			} else {
				$scope.stats.stopWords++;
				$scope.stats.stopWordsOcc += v;
			}
		});
		window.words = $scope.words = tmp;
		wordCloud();
	});

	function wordCloud() {
		console.log(_.take($scope.words, 10));
		console.time("cloud")
		$('#wordCloud').jQCloud($scope.words);
		console.timeEnd("cloud")
	}

	$scope.try = {
		comment: '',
		external: 1,
		username: '',
		threadscore: 0
	};

	$scope.tries = [];

	$scope.tryYourself = function() {

		var data = angular.copy($scope.try);
		$http.post(endpoint + 'score', data).success(function(res) {
			$scope.tries.push({
				comment: data.comment,
				external: data.external,
				username: data.username,
				threadscore: data.threadscore,
				score: res.prediction.replace(/[\[\]]/g,'')
			});

		}).error(function(data) {
			alert("Something went wrong during the request. Check console for more info");
			console.warn(data);
		})

		$scope.try = {
			comment: '',
			external: 1,
			username: '',
			score: 0
		};
	}

	// $scope.network = {
	// 	options: {
	// 		sort: 'top',
	// 		limit: 100,
	// 		filter: 'global'
	// 	},
	// 	data: {

	// 	}
	// };

	// $scope.$watch('network.options', function() {
	// 	console.log($scope.network.options)
	// 	network();
	// }, true);

	// var preComputed = {};
	// function preCompute() {
	// 	console.log("Computing")
	// 	var authors = [];
	// 	var subs = [];
	// 	var edgeVals = [];
	// 	var edges = [];
	// 	var authorComments = [];
	// 	var subredditComments = [];

	// 	_.each($scope.comments, function(c) {
	// 		if (c.an == 'None' || c.s == 'None') {
	// 			return;
	// 		}
	// 		if (!_.find(authors, function(a) { return a.id == c.an; })) {
	// 			authors.push({id: c.an, label: c.an, group: 'users'});
	// 			authorComments[c.an] = 1;
	// 		} else {
	// 			authorComments[c.an] += 1;
	// 		}
	// 		if (!subs[c.s]) {
	// 			subs[c.s] = {id: c.s, label: c.s, group: 'usergroups'};
	// 		}
	// 		if (!edgeVals[c.an+','+c.s]) {
	// 			edgeVals[c.an+','+c.s] = 0;
	// 		}
	// 		edgeVals[c.an+','+c.s] = edgeVals[c.an+','+c.s] + 1;
	// 	});

	// 	_.forIn(edgeVals, function(v,k) {
	// 		tmp = k.split(',');
	// 		author = tmp[0];
	// 		subreddit = tmp[1];
	// 		edges.push({from: author, to: subreddit, value: v, label: v});

	// 		if (!subredditComments[subreddit]) {
	// 			subredditComments[subreddit] = [];
	// 		}
	// 		if (!subredditComments[subreddit][author]) {
	// 			subredditComments[subreddit][author] = 0;
	// 		}
	// 		subredditComments[subreddit][author] += 1;
	// 	});

	// 	preComputed = {
	// 		authors: authors,
	// 		subs: subs,
	// 		edges: edges,
	// 		authorComments: authorComments,
	// 		subredditComments: subredditComments
	// 	};
	// };

	// function network() {
	// 	console.log("Networking")
	// 	console.time("network");

	// 	var optionsFA = {
	// 	    height: '500px',
	// 	    clustering: true,
	// 	    groups: {
	// 	        usergroups: {
	// 	            shape: 'icon',
	// 	            iconFontFace: 'FontAwesome',
	// 	            icon: '\uf0ac',
	// 	            iconSize: 50,
	// 	            iconColor: '#AAA539'
	// 	        },
	// 	        users: {
	// 	            shape: 'icon',
	// 	            iconFontFace: 'FontAwesome',
	// 	            icon: '\uf007',
	// 	            iconSize: 50,
	// 	            iconColor: '#aa00ff'
	// 	        }
	// 	    }
	// 	};

 //        var tmp = [];
 //        _method = $scope.network.options.sort == 'top' ? _.take : _.takeRight;

 //        if ($scope.network.options.filter == 'global') {
 //        	authors = _.sortBy(preComputed.authors, function(a) {
	//     		// Dont ask me why, but this needs to be negative, so that _method also work when filter is by subreddit
	//         	return -preComputed.authorComments[a.label];
	//         })
 //        	_authors = _method(authors, $scope.network.options.limit);
 //        } else {
 //        	// By subreddit
 //        	_authors = [];
 //        	_.forIn(preComputed.subredditComments, function(sub) {
 //        		tmp = [];
 //        		tmp =_.sortBy(preComputed.authors, function(a) {
	// 	        	return sub[a.label];
	// 	        })
 //        		_authors = _.union(_authors, _method(tmp, $scope.network.options.limit));
 //        	});
	//         // Needed if filter is by sub reddit
	//         _authors = _.uniq(_authors);
 //        }
 //        tmp = [];

 //        _.forIn(_authors, function(a) {
 //        	tmp.push(a);
 //        });
 //        _.forIn(preComputed.subs, function(s) {
 //        	tmp.push(s);
 //        });

 //        var dataFA = {
 //        	nodes: tmp,
 //        	edges: preComputed.edges
 //        };

 //        console.time("draw");
 //        var containerFA = document.getElementById('mynetworkFA');
 //        var networkFA = new vis.Network(containerFA, dataFA, optionsFA);
 //        console.timeEnd("draw");
 //        console.timeEnd("network");
	// };

// setTimeout(function() {

	// $("#range_4").ionRangeSlider({
 //        type: "single",
 //        step: 5,
 //        postfix: " authors",
 //        from: 100,
 //        hideText: true,
 //        onFinish: function (data) {
	//         $scope.$apply(function() {
	//         	$scope.network.options.limit = data.fromNumber;
	//         })
	//     },
 //    });
// }, 10)
});
